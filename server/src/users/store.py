import hashlib
import os
from typing import List, Tuple
from pymysql import Connection
from pymysql.cursors import Cursor
from server.src.users.models import UserAuthResponse

from src.users.models import UserView


class UserStore:
    TABLE = "users"

    def __init__(self, sql_conn: Connection) -> None:
        self.sql_conn = sql_conn

    def list_all(self) -> List[UserView]:
        cursor: Cursor
        with self.sql_conn.cursor as cursor:
            cursor.execute(f"SELECT * FROM `{self.TABLE}`")
            result = cursor.fetchall()
            return [UserView(**user) for user in result]

    def __hash_password(self, password: str, salt: str = None) -> Tuple[str, str]:
        salt = salt or os.urandom(16)
        key = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100000)
        return key, salt

    def create_user(self, username: str, password: str) -> UserAuthResponse:
        key, salt = self.__hash_password(password)

        cursor: Cursor
        with self.sql_conn.cursor as cursor:
            cursor.execute(
                f"INSERT INTO `{self.TABLE}` (`username`, `password`, `salt`) VALUES (%s, %s, %s)",
                (username, key, salt),
            )
            new_id = cursor.lastrowid

        self.sql_conn.commit()
        return UserAuthResponse(id=new_id, message=f"User {username} created")

    def authenticate(self, username: str, password: str) -> UserAuthResponse:
        cursor: Cursor
        with self.sql_conn.cursor as cursor:
            cursor.execute(
                f"SELECT * FROM `{self.TABLE}` WHERE `username` = %s",
                (username),
            )
            result = cursor.fetchone()
            if not result:
                return UserAuthResponse(message=f"User {username} not found")

            key, _ = self.__hash_password(password, result["salt"])
            if result["password"] != key:
                return UserAuthResponse(message=f"Wrong password for {username}")

            return UserAuthResponse(id=result["id"], message="Successfully authenticated")
