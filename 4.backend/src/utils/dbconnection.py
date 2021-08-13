from src.data_layer import data_source
import os
import pymysql


class DbConnection:
    def __init__(self):
        self.db_user = data_source.CLOUD_SQL_USERNAME
        self.db_password = data_source.CLOUD_SQL_PASSWORD
        self.db_name = data_source.CLOUD_SQL_DATABASE_NAME
        self.db_host = data_source.CLOUD_SQL_HOST

    def get_client_ref(self):
        client = pymysql.connect(
            user=self.db_user,
            password=self.db_password,
            host=self.db_host,
            db=self.db_name
        )
        return client
