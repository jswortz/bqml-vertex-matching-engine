
import json
import os
from classes_functions import QueryModel, TheTwoTowers, ProductModel, parse_tfrecord_fn, parse_tfrecord_catalog
from absl import app
from absl import flags
from absl import logging
import tensorflow as tf
import tensorflow_recommenders as tfrs
from google.cloud import storage


FLAGS = flags.FLAGS

def _get_model_dir(model_dir):
    """Defines utility functions for model saving.

    In a multi-worker scenario, the chief worker will save to the
    desired model directory, while the other workers will save the model to
    temporary directories. It’s important that these temporary directories
    are unique in order to prevent multiple workers from writing to the same
    location. Saving can contain collective ops, so all workers must save and
    not just the chief.
    """

    def _is_chief(task_type, task_id):
        return ((task_type == 'chief' and task_id == 0) or task_type is None)

    tf_config = os.getenv('TF_CONFIG')
    if tf_config:
        tf_config = json.loads(tf_config)

    if not _is_chief(tf_config['task']['type'], tf_config['task']['index']):
        model_dir = os.path.join(model_dir,
                                 'worker-{}').format(tf_config['task']['index'])

    logging.info('Setting model_dir to: %s', model_dir)

    return model_dir

def main(_):
    
    ## set params TODO - make params work with `absl`
    
    EMBEDDING_DIM = 32
    MAX_TOKENS = 50_000 #1265634
    N_PRODUCTS = 10_000 #212_862 212861
    N_HEIR = 10_000 #54724 
    BATCH_SIZE = 2048
    ARCH = [256, 128, 64]
    NUM_EPOCHS = 30
    TF_RECORDS_DIR = 'gs://tfrs-central-a'
    TF_RECORDS_CAT = 'gs://prod-catalog-central'
    NUM_RECORDS = 4_293_302

    
    ## get product, query data files
    client = storage.Client()
    files = []
    for blob in client.list_blobs('tfrs-tf-records'):
        files.append(blob.public_url.replace("https://storage.googleapis.com/", "gs://"))

    
    files_cat = []
    for blob in client.list_blobs('prod-catalog-central'):
        files_cat.append(blob.public_url.replace("https://storage.googleapis.com/", "gs://"))

    print(files_cat[:2])client = storage.Client()
    files = []
    for blob in client.list_blobs('tfrs-tf-records'):
        files.append(blob.public_url.replace("https://storage.googleapis.com/", "gs://"))


    files_cat = []
    for blob in client.list_blobs('prod-catalog-central'):
        files_cat.append(blob.public_url.replace("https://storage.googleapis.com/", "gs://"))

    ## establish the pipelines
    # Set dev dataset CHANGE THIS LATER TO THE WHOLE DIR
    raw_dataset = tf.data.TFRecordDataset(files) #local machine training wheels - using smaller data set for starters
    cat_dataset = tf.data.TFRecordDataset(files_cat)


    #See `pipeline-opts.ipynb` for more info on tuning options
    parsed_dataset = raw_dataset.map(
            parse_tfrecord_fn,
            num_parallel_calls=tf.data.AUTOTUNE
        ).prefetch(  # Overlap producer and consumer works
            tf.data.AUTOTUNE
        )


    # Doing another pipeline for the adapts to get startup to run much faster

    parsed_dataset_adapt = raw_dataset.map(
        parse_tfrecord_fn,
        num_parallel_calls=tf.data.AUTOTUNE
        ).prefetch(  # Overlap producer and consumer works
            tf.data.AUTOTUNE
        )

    parsed_dataset_adapt = parsed_dataset_adapt.batch(BATCH_SIZE)

    # parsed_dataset_adapt = parsed_dataset_adapt.batch(BATCH_SIZE)
    # loading de-duplicated product catalog

    parsed_dataset_candidates = cat_dataset.map(
            parse_tfrecord_catalog,
            num_parallel_calls=tf.data.AUTOTUNE
        ).prefetch(  # Overlap producer and consumer works
            tf.data.AUTOTUNE
        )

    parsed_dataset_candidates = parsed_dataset_candidates.cache()
    tf.random.set_seed(42)

    shuffled = parsed_dataset.shuffle(200_000, seed=42, reshuffle_each_iteration=False)
    # shuffled = shuffled.cache()

    test_pct = 0.05
    n_test = int(NUM_RECORDS * test_pct)

    # train_records
    test = shuffled.take(n_test)
    train = shuffled.skip(n_test)

    cached_train = train.batch(BATCH_SIZE)
    cached_test = test.batch(BATCH_SIZE * 2).cache()
    
    model = TheTwoTowers(ARCH)

    model.compile(optimizer=tf.keras.optimizers.Adagrad(0.1))
    
    layer_history = model.fit(
        cached_train,
        validation_data=cached_test,
        validation_freq=5,
        epochs=NUM_EPOCHS,
        verbose=0)

    accuracy = layer_history.history["factorized_top_k/top_100_categorical_accuracy"][-1]
    print(f"Top-100 accuracy: {accuracy:.2f}.")
