import pandas as pd


def generate_category_response(response_data):
    output_response = []
    for each_object in response_data:
        each_output_object = {'category': {
            "name": each_object['CATEGORY'],
            "subcategories": generate_subcategory_list(each_object["SUB_CATEGORY"])
        }}
        output_response.append(each_output_object)
    return output_response


def generate_subcategory_list(sub_category):
    list_of_subcat = sub_category.split(',')
    final_list_of_subcat = []
    for each_subcat in list_of_subcat:
        final_list_of_subcat.append({"name": each_subcat})

    return final_list_of_subcat


def convet_result_to_dataframe(query_result, columns, orient_value):
    df = pd.DataFrame(query_result, columns=columns)
    return df.to_json(orient=orient_value)


def create_where_condition(request_data):
    where_condition_str = []
    if request_data.get('filters') is None:
        return where_condition_str
    if request_data['filters'].get('name') is not None and request_data['filters'].get('name').strip() is not '':
        where_condition_str.append("NAME LIKE '%" + request_data['filters'].get('name') + "%' ")
    if request_data['filters'].get('company') is not None and request_data['filters'].get('company').strip() is not '':
        where_condition_str.append("BRAND = '" + request_data['filters'].get('company') + "' ")
    if request_data['filters'].get('sizes') is not None and request_data['filters'].get('sizes').strip() is not '':
        where_condition_str.append("SIZE = '" + request_data['filters'].get('sizes') + "' ")
    if request_data['filters'].get('colors') is not None and request_data['filters'].get('colors').strip() is not '':
        where_condition_str.append("COLOR = '" + request_data['filters'].get('colors') + "' ")
    if request_data['filters'].get('category') is not None and len(request_data['filters'].get('category')) > 0:
        where_condition_str.append("CATEGORY in (" + ','.join(map(put_single_quotes, request_data['filters'].get('category'))) + ") ")
    if request_data['filters'].get('subcategory') is not None and len(request_data['filters'].get('subcategory')) > 0:
        where_condition_str.append("SUB_CATEGORY in (" + ','.join(map(put_single_quotes, request_data['filters'].get('subcategory'))) + ") ")

    if len(where_condition_str) > 0:
        where_condition_str = 'AND '.join(where_condition_str)
    return where_condition_str


def put_single_quotes(word):
    return "'"+word+"'"


def get_ids_instr(json_data):
    results=json_data["results"]
    output_list = []
    for each_id in results:
        output_list.append(each_id['id'])
    return '('+",".join(output_list)+')'

