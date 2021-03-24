import os

is_prod = True if 'GAE_DEPLOYMENT_ID' in os.environ else False