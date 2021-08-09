from src.config import is_prod
import os

CLOUD_SQL_USERNAME = 'recai-demo'  # put cloud mysql username
CLOUD_SQL_PASSWORD = 'demopass'  # put cloud mysql password
CLOUD_SQL_DATABASE_NAME = 'Retail'  # put cloud mysql database name
CLOUD_SQL_HOST = os.environ.get('CLOUD_SQL_IP') if 'CLOUD_SQL_IP' in os.environ and is_prod else '127.0.0.1'  # cloud mysql private ip or localhost if using cloud_sql_proxy
