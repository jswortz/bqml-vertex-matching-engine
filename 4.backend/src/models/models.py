from src.utils import db_connection
from src.data_layer import query_source, column_information as ci
from src.utils import utils
from google.cloud import dialogflow
import requests
import json
import os

PROJECT_ID = os.environ.get('RECAI_PROJECT') if 'RECAI_PROJECT' in os.environ else 'babrams-recai-demo'
PREDICT_KEY = os.environ.get('PREDICT_KEY') if 'PREDICT_KEY' in os.environ else 'AIzaSyAptd6M3SUokdQKMgCAssv-adCOP7fO8s8'

class Models():
    def __init__(self, prod_id="", request_data=''):
        self.product_id = prod_id
        self.requested_data = request_data
        self.connection_object = db_connection.Db_connection()
        self.client = self.connection_object.get_client_ref()

    def fetch_product_id(self):
        query = query_source.GET_PRODUCT_QUERY.format(self.product_id)
        columns = ci.GET_PRODUCT_QUERY_COLUMNS
        with self.client.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
        self.client.close()
        return utils.convet_result_to_dataframe(result,columns, "records")

    def fetch_brand(self):
        query = query_source.GET_BRAND_QUERY
        columns = ci.GET_BRAND_QUERY_COLUMNS
        with self.client.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
        self.client.close()
        return utils.convet_result_to_dataframe(result,columns, "records")

    def fetch_category(self):
        query = query_source.GET_CATAGORY_QUERY
        columns = ci.GET_CATAGORY_QUERY_COLUMNS
        with self.client.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
        self.client.close()
        response = json.loads(json.loads(json.dumps(utils.convet_result_to_dataframe(result, columns, "records"))))
        return json.dumps(utils.generate_category_response(response))

    def fetch_sales(self):
        query = query_source.GET_SALES_QUERY
        columns = ci.GET_SALES_QUERY_COLUMNS
        with self.client.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
        self.client.close()
        return utils.convet_result_to_dataframe(result,columns, "records")

    def fetch_filter_data(self, requested_data):
        where_condition = utils.create_where_condition(requested_data)
        query = query_source.GET_FILTER_QUERY.format(where_condition)
        columns = ci.GET_FILTER_QUERY_COLUMNS
        with self.client.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
        self.client.close()
        return utils.convet_result_to_dataframe(result,columns, "records")

    def fetch_user_details(self):
        query = query_source.GET_USER_EVENT
        columns = ci.GET_USER_DETAIL_COLUMNS
        with self.client.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
        self.client.close()
        return utils.convet_result_to_dataframe(result,columns, "records")

    def get_product_recommendation_custom(self):
        if self.requested_data.get('eventType') is not None or self.requested_data.get('eventType') is not '':
            placementName = self.requested_data.get('placement_name')
            payload = json.dumps(self.requested_data.get('params'))
        else:
            placementName = ""
            payload = ""
        url = "https://recommendationengine.googleapis.com/v1beta1/projects/"+PROJECT_ID+"/locations" \
              "/global/catalogs/default_catalog/eventStores/default_event_store/placements/"+placementName+":predict?key" \
              "="+PREDICT_KEY

        payload = payload
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        return json.loads(json.dumps(response.text))

    def fetch_top_product(self):
        json_output = self.product_id
        all_ids_str = utils.get_ids_instr(json_output)
        columns = ci.GET_TOP_PRODUCT_QUERY
        query = query_source.GET_TOP_PRODUCT_QUERY.format(all_ids_str)
        with self.client.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
        self.client.close()
        return utils.convet_result_to_dataframe(result,columns, "records")

    def fetch_top_product_demo(self, request_data):
        json_output = self.product_id
        all_ids_str = utils.get_ids_instr(json_output)
        columns = ci.GET_TOP_PRODUCT_QUERY
        query = query_source.GET_TOP_PRODUCT_QUERY.format(all_ids_str)
        with self.client.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
        self.client.close()
        return utils.convet_result_to_dataframe(result,columns, "records")

    def fetch_chatbot_response(self, session_id, query_string):
        session_client = dialogflow.SessionsClient()
        session = session_client.session_path(PROJECT_ID, session_id)

        text_input = dialogflow.TextInput(text=query_string, language_code="en-US")
        query_input = dialogflow.QueryInput(text=text_input)

        response = session_client.detect_intent(
            request={"session": session, "query_input": query_input}
        )

        return response.query_result.fulfillment_text

