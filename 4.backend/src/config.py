import os

is_prod = True if 'GAE_DEPLOYMENT_ID' in os.environ else False

PROJECT_NUMBER = os.environ.get('PROJECT_NUMBER', '569181271116')
ELASTICSEARCH_INDEX = 'products'

# TODO: move secrets to SecretManager
ELASTICSEARCH_CLOUD_ID = 'RetailStore:dXMtY2VudHJhbDEuZ2NwLmNsb3VkLmVzLmlvJDkwZmZhNWM2NjI0YjRhYTQ5YzNiZjRkOGZlNWVlMzFiJDU4Y2M0MmI2OTExYTRhOTY4NGJlM2FjZTgxOTk3M2Fk'
ELASTICSEARCH_USER = 'elastic'
ELASTICSEARCH_PASSWORD = 'lOhWUMPhC03lg1CfGtQsph6c'

DIALOGFLOW_AUTH_USER = '0c7020f8-c34d-4133-8c92-ddcd95509e16'
DIALOGFLOW_AUTH_PASSWORD = r'e4M55Wxp!F]YY)qc4,yk=KL!CY94sT9Q)Cj6GEk@E&5Lp-~u;Agzq&!t=~-U'
