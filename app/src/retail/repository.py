"""Exposes raw, business-logic free Retail API methods"""

from src.config import PROJECT_NUMBER
#TODO: migrate to google.cloud.retail official client after retail search release
from google_auth_httplib2 import AuthorizedHttp
import google.auth
import json
from string import Template
from urllib.parse import urlencode

_creds, _ = google.auth.default(scopes=['https://www.googleapis.com/auth/cloud-platform'])

BASE_URL = 'https://retail.googleapis.com/v2alpha'
DEFAULT_LOCATION = 'global'
DEFAULT_CATALOG = 'default_catalog'
DEFAULT_BRANCH = 'default_branch'
DEFAULT_SEARCH_PLACEMENT = 'default_search'

CATALOG_PATH_TMPL = Template('projects/$project_number/locations/$location/catalogs/$catalog')
BRANCH_PATH_TMPL = Template('projects/$project_number/locations/$location/catalogs/$catalog/branches/$branch')
PRODUCT_PATH_TMPL = Template('projects/$project_number/locations/$location/catalogs/$catalog/branches/$branch/products/$product')
PLACEMENT_PATH_TMPL = Template('projects/$project_number/locations/$location/catalogs/$catalog/placements/$placement')

PRODUCT_URL_TMPL = Template(f'{BASE_URL}/$product_path')
BRANCH_URL_TMPL = Template(f'{BASE_URL}/$branch/products')
SEARCH_URL_TMPL = Template(f'{BASE_URL}/$placement:search')
COMPLETEQUERY_URL_TMPL = Template(f'{BASE_URL}/$catalog:completeQuery')
RECOMMEND_URL_TMPL = Template(f'{BASE_URL}/$placement:predict')

class RetailRequestError(Exception):
    pass

def _request(credentials=_creds, *args, **kwargs):
    """Makes a service account authenticated http call passing args and kwargs 
    directly to a wrapped httplib2.Http().request instance.
    
    Args:
        credentials (google.auth.credentials.Credentials)
    Returns:
        data (dict): parsed json response
    Raises:
        RetailRequestError: if client or server errors are reported
    """

    http = AuthorizedHttp(credentials)
    response, content = http.request(*args, **kwargs)

    data = json.loads(content)

    if int(response.status) >= 400:
        raise RetailRequestError(data)
    
    return data

def get_product(
    product_id,
    project_number=PROJECT_NUMBER,
    location=DEFAULT_LOCATION,
    catalog=DEFAULT_CATALOG,
    branch=DEFAULT_BRANCH):
    """Retrieves a Retail API Product instance given it's id.
    
    Args:
        product_id (str | int)
        project_number (str | int): Google Cloud Platform project number
        location (str): Resource location
        catalog (str): Catalog id
        branch (str): Branch id 
    Returns:
        Product (dict): https://cloud.google.com/retail/search/docs/reference/rest/v2alpha/projects.locations.catalogs.branches.products
    """
    
    client = AuthorizedHttp(_creds)

    resource = PRODUCT_PATH_TMPL.substitute(
        project_number=project_number,
        location=location,
        catalog=catalog,
        branch=branch,
        product=product_id
    )
    
    url = PRODUCT_URL_TMPL.substitute(product_path=resource)

    return _request(uri=url, method='GET')

def list_products():
    raise NotImplementedError

def search_products(
    query,
    visitorId,
    project_number=PROJECT_NUMBER,
    location=DEFAULT_LOCATION,
    catalog=DEFAULT_CATALOG,
    placement=DEFAULT_SEARCH_PLACEMENT,
    branch=DEFAULT_BRANCH,
    **kwargs):
    """Searches for products.
    
    Args:
        query (str): User query
        visitorId (str): Unique user identifier
        project_number (str | int): Google Cloud Platform project number
        location (str): Resource location
        catalog (str): Catalog id
        placement (str): Search placement id
        branch (str): Branch id
        **kwargs: Extra keyword arguments passed directly to 
            SearchRequest body (https://cloud.google.com/retail/search/docs/reference/rest/v2alpha/projects.locations.catalogs.placements/search#request-body)
            excluding 'branch', 'query' and 'visitorId'.
    Returns:
        SearchResponse (dict): https://cloud.google.com/retail/search/docs/reference/rest/v2alpha/projects.locations.catalogs.placements/search#response-body
    """

    client = AuthorizedHttp(_creds)

    placement_path = PLACEMENT_PATH_TMPL.substitute(
        project_number=project_number,
        location=location,
        catalog=catalog,
        placement=placement)

    branch_path = BRANCH_PATH_TMPL.substitute(
        project_number=project_number,
        location=location,
        catalog=catalog,
        branch=branch)

    url = SEARCH_URL_TMPL.substitute(placement=placement_path)

    body = json.dumps({
        'query': query,
        'visitorId': visitorId,
        'branch': branch_path,
        **kwargs
    })

    return _request(uri=url, method='POST', body=body)

def complete_query(
    query,
    project_number=PROJECT_NUMBER,
    location=DEFAULT_LOCATION,
    catalog=DEFAULT_CATALOG,
    **kwargs):

    client = AuthorizedHttp(_creds)

    resource = CATALOG_PATH_TMPL.substitute(
        project_number=project_number,
        location=location,
        catalog=catalog
    )

    params = urlencode({'query': query, **kwargs})
    url = f'{COMPLETEQUERY_URL_TMPL.substitute(catalog=resource)}?{params}'

    return _request(uri=url, method='GET')

def recommend(
    placement_id,
    userEvent,
    project_number=PROJECT_NUMBER,
    location=DEFAULT_LOCATION,
    catalog=DEFAULT_CATALOG,
    **kwargs):

    client = AuthorizedHttp(_creds)

    resource = PLACEMENT_PATH_TMPL.substitute(
        project_number=project_number,
        location=location,
        catalog=catalog,
        placement=placement_id)

    url = RECOMMEND_URL_TMPL.substitute(placement=resource)

    body = json.dumps({
        'userEvent': userEvent,
        'validateOnly': True,
        **kwargs
    })

    return _request(uri=url, method='POST', body=body)
