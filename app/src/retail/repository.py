from src.config import PROJECT_NUMBER
#TODO: migrate to google.cloud.retail official client after retail search release
from google_auth_httplib2 import AuthorizedHttp
import google.auth
import json
from string import Template

_creds, _ = google.auth.default(scopes=['https://www.googleapis.com/auth/cloud-platform'])

BASE_URL = 'https://retail.googleapis.com/v2alpha'
DEFAULT_LOCATION = 'global'
DEFAULT_CATALOG = 'default_catalog'
DEFAULT_BRANCH = 'default_branch'
DEFAULT_SEARCH_PLACEMENT = 'default_search'

CATALOG_PATH_TMPL = Template('projects/$project_number/locations/$location/catalogs/$catalog')
BRANCH_PATH_TMPL = Template('projects/$project_number/locations/$location/catalogs/$catalog/branches/$branch')
PRODUCT_PATH_TMPL = Template('projects/$project_number/locations/$location/catalogs/$catalog/branches/$branch/products/$product_id')
PLACEMENT_PATH_TMPL = Template('projects/$project_number/locations/$location/catalogs/$catalog/placements/$placement')

PRODUCT_URL_TMPL = Template(f'{BASE_URL}/$product_path')
BRANCH_URL_TMPL = Template(f'{BASE_URL}/$branch/products')
SEARCH_URL_TMPL = Template(f'{BASE_URL}/$placement:search')


def get_product(
    product_id,
    project_number=PROJECT_NUMBER,
    location=DEFAULT_LOCATION,
    catalog=DEFAULT_CATALOG,
    branch=DEFAULT_BRANCH):
    
    client = AuthorizedHttp(_creds)

    resource = PRODUCT_PATH_TMPL.substitute(
        project_number=project_number,
        location=location,
        catalog=catalog,
        branch=branch,
        product_id=product_id
    )
    
    url = PRODUCT_URL_TMPL.substitute(product_path=resource)
    
    _, response = client.request(url, method='GET')
    return json.loads(response)

def list_products():
    raise NotImplementedError

def search_products(search_request):
    raise NotImplementedError

def complete_query(query):
    raise NotImplementedError

def recommend(placement_id):
    raise NotImplementedError

