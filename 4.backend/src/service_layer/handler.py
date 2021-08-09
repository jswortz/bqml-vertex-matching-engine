from src.models import models
from src.data_layer import default_params
import json
import os

FBT_PLACEMENT = os.environ.get('FBT_PLACEMENT') if 'FBT_PLACEMENT' in os.environ else 'copurchased'  # frequently bought together placement id
OYML_PLACEMENT = os.environ.get('OYML_PLACEMENT') if 'OYML_PLACEMENT' in os.environ else 'pdp'  # others you may like placement id

def getproduct(pro_id):
    final_output = {}
    try:
        default_parameters = default_params.PARAMS
        default_parameters['params']['userEvent']['productEventDetail']['productDetails'][0]['id'] = pro_id
        default_parameters['placement_name'] = FBT_PLACEMENT
        model_obj = models.Models(pro_id, default_parameters)
        default_parameters['placement_name'] = OYML_PLACEMENT
        similar_obj = models.Models(pro_id, default_parameters)
        final_output = json.loads(model_obj.get_product_recommendation_custom())
        similar_output = json.loads(similar_obj.get_product_recommendation_custom())
        model_obj = models.Models(final_output)
        similar_obj = models.Models(similar_output)
        final_output = json.loads(json.loads(json.dumps(model_obj.fetch_top_product_demo(pro_id))))
        similar_output = json.loads(json.loads(json.dumps(similar_obj.fetch_top_product_demo(pro_id))))
        model_obj = models.Models(pro_id)
        similar_obj = models.Models(pro_id)
        product_output = json.loads(json.loads(json.dumps(model_obj.fetch_product_id())))
        product_output[0]['RECOMMENDATIONS'] = final_output
        product_output[0]['SIMILAR'] = similar_output
        final_output = product_output

    except Exception as e:
        print(e)

    return json.dumps(final_output)


def gettopproduct(pro_id):
    final_output = {}
    try:
        model_obj = models.Models(pro_id)
        product_output = json.loads(json.loads(json.dumps(model_obj.fetch_product_id())))
        final_output = json.loads(model_obj.get_product_recommendation())
        model_obj = models.Models(final_output)
        final_output = json.loads(json.loads(json.dumps(model_obj.fetch_top_product())))
        product_output[0]['RECOMMENDATIONS'] = final_output
        final_output = product_output
    except Exception as e:
        print(e)

    return json.dumps(final_output)


def getbrand():
    final_output = {}
    try:
        model_obj = models.Models()
        final_output = model_obj.fetch_brand()
    except Exception as e:
        print(e)

    return final_output


def getcategory():
    final_output = {}
    try:
        model_obj = models.Models()
        final_output = model_obj.fetch_category()
    except Exception as e:
        print(e)

    return final_output


def getsales():
    final_output = {}
    try:
        model_obj = models.Models()
        final_output = model_obj.fetch_sales()
    except Exception as e:
        print(e)

    return final_output


def get_product_by_filter(request_data):
    final_output = {}
    try:
        models_obj = models.Models()
        final_output = models_obj.fetch_filter_data(request_data)
    except Exception as e:
        print(e)
    return final_output


def gettopproductdemo(request_data):
    final_output = {}
    try:
        model_obj = models.Models(request_data.get('product_id'), request_data)
        final_output = json.loads(model_obj.get_product_recommendation_custom())
        model_obj = models.Models(final_output)
        final_output = json.loads(json.loads(json.dumps(model_obj.fetch_top_product_demo(request_data))))
        model_obj = models.Models(request_data.get('product_id'))
        product_output = json.loads(json.loads(json.dumps(model_obj.fetch_product_id())))
        product_output[0]['RECOMMENDATIONS'] = final_output
        final_output = product_output
    except Exception as e:
        print(e)

    return json.dumps(final_output)


def get_user_detail():
    final_output = {}
    try:
        models_obj = models.Models()
        final_output = models_obj.fetch_user_details()
    except Exception as e:
        print(e)
    return final_output

def get_chatbot_response(session_id, query_string):
    final_output = {}
    try:
        model_obj = models.Models()
        final_output = model_obj.fetch_chatbot_response(session_id, query_string)
    except Exception as e:
        print(e)

    return final_output
