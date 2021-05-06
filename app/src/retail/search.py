from src.config import PROJECT_NUMBER
from src.retail.config import MAX_PAGE_SIZE
from src.retail.repository import search_products
from src.types.retail import SearchProduct
from src.types.retail import SearchResponse

import json


def search(
    query='',
    visitorId='',
    page=1,
    pageSize=50,
    **kwargs):

    offset = max((page - 1) * pageSize, 0)
    page_size = min(pageSize, MAX_PAGE_SIZE)

    # response = search_products(query, visitorId, pageSize=pageSize, offset=offset)

    return SearchResponse 