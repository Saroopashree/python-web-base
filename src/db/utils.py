import os

import pymysql
from pymysql import Connection
from pymysql.cursors import DictCursor


class SqlConnProvider:
    def __init__(self) -> None:
        self._cached_conn: Connection = None
        self.create_conn()

    def create_conn(self) -> Connection:
        self.close_conn()

        database = os.getenv("MYSQL_DATABASE")
        username = os.getenv("MYSQL_USER")
        password = os.getenv("MYSQL_PASSWORD")
        host = "mysqldb"

        print("[SQL_CONN_PROVIDER]: Creating new MySQL connection...")

        self._cached_conn = pymysql.connect(
            host=host,
            port=3306,
            user=username,
            password=password,
            database=database,
            cursorclass=DictCursor,
        )
        return self._cached_conn

    def get_conn(self):
        return self._cached_conn or self.create_conn()

    def close_conn(self):
        if self._cached_conn:
            print("[SQL_CONN_PROVIDER]: Closing existing MySQL connection...")
            self._cached_conn.close()
            self._cached_conn = None
