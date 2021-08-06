from src.config import ELASTICSEARCH_CLOUD_ID
from src.config import ELASTICSEARCH_INDEX
from src.config import ELASTICSEARCH_USER
from src.config import ELASTICSEARCH_PASSWORD
from src.retail.config import MAX_PAGE_SIZE
from src.types.retail import SearchResponse
from src.types.retail import SearchProduct

from datetime import datetime, timedelta
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
import math 

_client = Elasticsearch(
    cloud_id = ELASTICSEARCH_CLOUD_ID,
    http_auth = (ELASTICSEARCH_USER, ELASTICSEARCH_PASSWORD))

_SEARCH_FIELD = 'NAME'

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


def search_benchmark(
    query='',
    autocorrect=True,
    page=1,
    pageSize=50,
    **kwargs):

    page = max(page, 1)
    page_size = min(pageSize, MAX_PAGE_SIZE)
    corrected_query = _autocorrect(query) if autocorrect else query

    raw_results = (
        Search(using=_client, index=ELASTICSEARCH_INDEX)
        .query('match', **{_SEARCH_FIELD: corrected_query})
        [(page - 1) * page_size : page * page_size]
        .execute())

    was_autocorrected = corrected_query != query
    
    num_pages = math.ceil(raw_results.hits.total.value / page_size)
    
    results = [SearchProduct.from_elastic(hit.to_dict()) for hit in raw_results]
    
    return SearchResponse(
        results,
        num_pages,
        corrected_query,
        was_autocorrected)
