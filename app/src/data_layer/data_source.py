from src.config import is_prod

CLOUD_SQL_USERNAME= 'root'                                  #put cloud mysql username
CLOUD_SQL_PASSWORD= 'root'                                  #put cloud mysql password
CLOUD_SQL_DATABASE_NAME= 'Retail'                           #put cloud mysql database name
CLOUD_SQL_HOST = '10.246.0.3' if is_prod else '127.0.0.1'   #cloud mysql private ip or localhost if using cloud_sql_proxy