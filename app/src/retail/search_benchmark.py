from src.config import ELASTICSEARCH_CLOUD_ID
from src.config import ELASTICSEARCH_INDEX
from src.config import ELASTICSEARCH_USER
from src.config import ELASTICSEARCH_PASSWORD

from datetime import datetime, timedelta
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
import math 

_client = Elasticsearch(
    cloud_id = ELASTICSEARCH_CLOUD_ID,
    http_auth = (ELASTICSEARCH_USER, ELASTICSEARCH_PASSWORD))

_MAX_PAGE_SIZE = 120
_SEARCH_FIELD = 'NAME'
_FIELD_NAMES = [
    'AVAILABILITY',
    'BRAND',
    'CATEGORY',
    'COLOR',
    'COMPANY',
    'ESTIMATED_DELIVERY_DAY',
    'ID',
    'image_link',
    'NAME',
    'RETAIL_PRICE',
    'REVIEW',
    'SIZE',
    'SUB_CATEGORY'
]
_FIELD_RENAME_MAP = {
    'image_link': 'IMAGE LINK',
    'RETAIL_PRICE': 'PRICE'
}

def _autocorrect(user_query):
    
    results = (
        Search(using=_client, index=ELASTICSEARCH_INDEX)
        .suggest('autocorrection', user_query, term={'field': _SEARCH_FIELD})
        .execute())

    suggestions = results.suggest.autocorrection
    
    search_args = []
    for word in suggestions:
        if word.options:
            search_args.append(word.options[0].text)
        else:
            search_args.append(word.text)
    
    return ' '.join(search_args)

def _format_hit(row_dict):

    row = {k:v for k, v in row_dict.items() if k in _FIELD_NAMES}

    for old_key, new_key in _FIELD_RENAME_MAP.items():
        row[new_key] = row.pop(old_key)

    days = row.pop('ESTIMATED_DELIVERY_DAY')

    dt = datetime.utcnow() + timedelta(days=days)
    dt = dt.replace(hour=0, minute=0, second=0, microsecond=0)

    row['ESTIMATE_DELIVERY_AT'] = math.floor(dt.timestamp() * 1000)

    return row


def search_benchmark(
    query='',
    autocorrect=True,
    page=1,
    pageSize=50,
    **kwargs):

    page = max(page, 1)
    page_size = min(pageSize, _MAX_PAGE_SIZE)
    corrected_query = _autocorrect(query) if autocorrect else query

    raw_results = (
        Search(using=_client, index=ELASTICSEARCH_INDEX)
        .query('match', **{_SEARCH_FIELD: corrected_query})
        [(page - 1) * page_size : page * page_size]
        .execute())

    response = {
        'numPages': math.ceil(raw_results.hits.total.value / page_size),
        'results': [_format_hit(hit.to_dict()) for hit in raw_results]
    }

    if corrected_query != query:
        response['correctedQuery'] = corrected_query
    
    return response
