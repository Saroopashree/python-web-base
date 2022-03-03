import os
from typing import Generator

import pymysql
from pymysql import Connection
from pymysql.cursors import DictCursor


# Dependency
def get_db() -> Generator[Connection, None, None]:
    database = os.getenv("MYSQL_DATABASE")
    username = os.getenv("MYSQL_USER")
    password = os.getenv("MYSQL_PASSWORD")
    localhost = "127.0.0.1"
    conn = pymysql.connect(
        host=localhost,
        user=username,
        password=password,
        database=database,
        cursorclass=DictCursor,
        init_command="""
    CREATE TABLE IF NOT EXISTS `db_migration` (
        `version` VARCHAR(16) NOT NULL,
        `name` VARCHAR(256) NOT NULL,
        PRIMARY KEY (`version`)
    );""",
    )

    try:
        yield conn
    finally:
        conn.close()
