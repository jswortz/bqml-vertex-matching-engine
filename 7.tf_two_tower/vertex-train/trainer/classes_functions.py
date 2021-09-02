import tensorflow as tf


def parse_tfrecord_fn(example):
    feature_description = {
         #query features
        "query": tf.io.FixedLenFeature([1], tf.string),
        "last_viewed": tf.io.FixedLenFeature([1], tf.string),

        #candidate features
        "IVM_s": tf.io.FixedLenFeature([1], tf.string),
        "description": tf.io.FixedLenFeature([1], tf.string),
        "price_td": tf.io.FixedLenFeature([1], tf.float32),
        "PriceRange_s": tf.io.FixedLenFeature([1],  tf.string),
        "productTypeCombo_ss": tf.io.FixedLenFeature([1], tf.string),
        "visual": tf.io.FixedLenFeature([2048,], tf.float32),
        "month": tf.io.FixedLenFeature([1], tf.string),
        "hour": tf.io.FixedLenFeature([1], tf.string)
    }
    example = tf.io.parse_single_example(example, feature_description)
    return example


def parse_tfrecord_catalog(example):
    feature_description = {
        #candidate features
        "IVM_s": tf.io.FixedLenFeature([1], tf.string),
        "description": tf.io.FixedLenFeature([1], tf.string),
        "price_td": tf.io.FixedLenFeature([1], tf.float32),
        "PriceRange_s": tf.io.FixedLenFeature([1],  tf.string),
        "productTypeCombo_ss": tf.io.FixedLenFeature([1], tf.string),
         "visual": tf.io.FixedLenFeature([2048,], tf.float32)
    }
    example = tf.io.parse_single_example(example, feature_description)
    return example

class QueryModel(tf.keras.Model):
    
    def __init__(self, layer_sizes):
        super().__init__()
        
        month_vocab = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
        hour_vocab = month_vocab + ["13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "00"]

        self.month_embedding = tf.keras.Sequential([
            tf.keras.layers.experimental.preprocessing.StringLookup(
                vocabulary=month_vocab, mask_token=None, name="month_lookup"),
            tf.keras.layers.Embedding(
                len(month_vocab)+1, EMBEDDING_DIM, mask_zero=True, name="month_emb"),
            tf.keras.layers.GlobalAveragePooling1D()
        ])
        
        self.hour_embedding = tf.keras.Sequential([
            tf.keras.layers.experimental.preprocessing.StringLookup(
                vocabulary=hour_vocab, mask_token=None, name="hour_lookup"),
            tf.keras.layers.Embedding(len(hour_vocab)+1, EMBEDDING_DIM, mask_zero=True, name="hour_emb"),
            tf.keras.layers.GlobalAveragePooling1D()
        ])
    
        self.query_vectorizor = tf.keras.layers.experimental.preprocessing.TextVectorization(
            max_tokens=MAX_TOKENS, name="query_tv")
        
        self.last_viewed_vectorizor = tf.keras.layers.experimental.preprocessing.TextVectorization(
            max_tokens=MAX_TOKENS, name="last_viewed_tv")
        
        self.query_embedding = tf.keras.Sequential([
            self.query_vectorizor,
            tf.keras.layers.Embedding(MAX_TOKENS, EMBEDDING_DIM , mask_zero=True, name="query_emb"),
            tf.keras.layers.GlobalAveragePooling1D()
        ])
        
        self.last_viewed_embedding = tf.keras.Sequential([
            self.last_viewed_vectorizor,
            tf.keras.layers.Embedding(MAX_TOKENS, EMBEDDING_DIM , mask_zero=True, name="last_v_emb"),
            tf.keras.layers.GlobalAveragePooling1D()
        ])
        
        ### adapt stuff
        self.query_vectorizor.adapt(parsed_dataset_adapt.map(lambda x: x['query']))
        self.last_viewed_vectorizor.adapt(parsed_dataset_adapt.map(lambda x: x['last_viewed'])) 
        
        # Then construct the layers.
        self.dense_layers = tf.keras.Sequential()

        # Use the ReLU activation for all but the last layer.
        for layer_size in layer_sizes[:-1]:
            self.dense_layers.add(tf.keras.layers.Dense(layer_size, activation="relu"))
        # No activation for the last layer
        for layer_size in layer_sizes[-1:]:
            self.dense_layers.add(tf.keras.layers.Dense(layer_size, kernel_regularizer='l2')) #l2 reg was in research - helps performance


    def call(self, data):    
        all_embs = tf.concat(
                [
                    self.month_embedding(data['month']),
                    self.hour_embedding(data['hour']),
                    self.query_embedding(data['query']),
                    self.last_viewed_embedding(data['last_viewed'])
                ], axis=1)
        return self.dense_layers(all_embs)
    
class ProductModel(tf.keras.Model):
    def __init__(self, layer_sizes):
        super().__init__()
        
        #continuous example - allowing batch norms via layer below for standardization of inputs
        self.price_normalizer = tf.keras.layers.experimental.preprocessing.Normalization(name="price_norm")

        #categorical with vocabs
        pr_vocab = ['002_$100 - $299', '000_$0 - $49', '001_$50 - $99', 
                    '003_$300 - $599', '005_$1000 - $3999', '004_$600 - $999', 
                    '006_$4000+', '']

        self.price_range_embedding = tf.keras.Sequential([
            tf.keras.layers.experimental.preprocessing.StringLookup(
                  vocabulary=pr_vocab, mask_token=None, name="price_range_lu"),
            tf.keras.layers.Embedding(
                len(pr_vocab)+1, EMBEDDING_DIM, mask_zero=True, name="price_range_emb"),
            tf.keras.layers.GlobalAveragePooling1D(name="price_range_flatten")
        ])
        
        # categorical: description - below are all embeddings with unk vocabs - will be adapted 
        self.description_vectorizor = tf.keras.layers.experimental.preprocessing.TextVectorization(
            max_tokens=N_PRODUCTS, name = "description_vectorizor")

        self.description_embedding = tf.keras.Sequential([
            self.description_vectorizor,
            tf.keras.layers.Embedding(N_PRODUCTS+1, EMBEDDING_DIM, mask_zero=True, name = "desc_emb"),
            tf.keras.layers.GlobalAveragePooling1D(name="desc_flatten")
        ])
        
        #categorical: sku
        self.sku_vectorizor = tf.keras.layers.experimental.preprocessing.TextVectorization(
            max_tokens=N_PRODUCTS, name = "sku_vectorizor")

        self.sku_embedding = tf.keras.Sequential([
            self.sku_vectorizor,
            tf.keras.layers.Embedding(N_PRODUCTS+1, EMBEDDING_DIM, mask_zero=True, name = "sku_emb"),
            tf.keras.layers.GlobalAveragePooling1D(name="sku_flat")
        ])
        
        ## product ragged stuff - 

        ## prod heirarcy
        def split_fn(string):
            return tf.strings.split(string, sep="|")

        self.prod_heir_vectorizor = tf.keras.layers.experimental.preprocessing.TextVectorization(
            max_tokens=N_HEIR, split=split_fn, name = "heir_vectorizor")
        #54724 - count unique
        self.heir_embedding = tf.keras.Sequential([
            self.prod_heir_vectorizor,
            tf.keras.layers.Embedding(N_HEIR+1, EMBEDDING_DIM, mask_zero=True, name = "heir_emb"),
            tf.keras.layers.GlobalAveragePooling1D(name="heir_flat")
        ])
        
        # Then construct the layers.
        self.dense_layers = tf.keras.Sequential()

        # Use the ReLU activation for all but the last layer.
        for layer_size in layer_sizes[:-1]:
            self.dense_layers.add(tf.keras.layers.Dense(layer_size, activation="relu"))
            # No activation for the last layer
        for layer_size in layer_sizes[-1:]:
            self.dense_layers.add(tf.keras.layers.Dense(layer_size, kernel_regularizer='l2')) #l2 reg was in research - helps performance
        
        #adapt stuff
        self.description_vectorizor.adapt(parsed_dataset_candidates.map(lambda x: x['description']))
        self.sku_vectorizor.adapt(parsed_dataset_candidates.map(lambda x: x['IVM_s']))
        self.prod_heir_vectorizor.adapt(parsed_dataset_candidates.map(lambda x: x['productTypeCombo_ss']))
        
        #continous adapts - look ahead batching - grab up to batch_size
        self.price_normalizer.adapt(parsed_dataset_candidates.map(lambda x: x['price_td']))        


    def call(self, data):
        all_embs = tf.concat(
            [
                self.price_normalizer(data['price_td']),
                self.price_range_embedding(data['PriceRange_s']),
                self.description_embedding(data['description']),
                self.sku_embedding(data['IVM_s']),
                self.heir_embedding(data['productTypeCombo_ss']),
                data['visual']
            ], axis=1)
#         return self.dense_layers(all_embs)  #last plus for number continuous + 1 if you add other(s)
        return self.dense_layers(all_embs)  #last plus for number continuous + 1 if you add other(s) 2048 for visual

#now combine them and assign retreival tasks, etc..

class TheTwoTowers(tfrs.models.Model):

    def __init__(self, layer_sizes):
        super().__init__()
        self.query_model = QueryModel(layer_sizes)
        self.candidate_model = ProductModel(layer_sizes)
        self.task = tfrs.tasks.Retrieval(
            metrics=tfrs.metrics.FactorizedTopK(
                candidates=parsed_dataset_candidates.batch(128).map(self.candidate_model),
            ),
        )

    def compute_loss(self, data, training=False):
        query_embeddings = self.query_model(data)
        product_embeddings = self.candidate_model(data)

        return self.task(
            query_embeddings, product_embeddings)#, compute_metrics=not training)#### turn off metrics to save time on training