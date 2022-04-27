from typing import Optional, Union

from pymysql import Connection
from pymysql.cursors import Cursor

from src.exception import AppException
from src.todo.models import TodoItem


class TodoStore:
    TABLE = "todos"

    def __init__(self, sql_conn: Connection) -> None:
        self.sql_conn = sql_conn

    def fetch(self, uid: int, id: int = None) -> Union[list[TodoItem], Optional[TodoItem]]:
        cursor: Cursor
        with self.sql_conn.cursor() as cursor:
            if id:
                cursor.execute(
                    f"SELECT * FROM `{self.TABLE}` WHERE `id` = %s AND (`user_id` = %s OR `assignee` = %s)",
                    (id, uid, uid),
                )
                result = cursor.fetchone()
                if result:
                    return TodoItem(**result)
            else:
                cursor.execute(f"SELECT * FROM `{self.TABLE}`")
                result = cursor.fetchall()
                return [TodoItem(**todo) for todo in result]

    def add(self, uid: int, desc: str) -> TodoItem:
        cursor: Cursor
        with self.sql_conn.cursor() as cursor:
            cursor.execute(
                f"INSERT INTO `{self.TABLE}` (`user_id`, `desc`, `assignee`) VALUES (%s, %s, %s)",
                (uid, desc, uid),
            )
            new_id = cursor.lastrowid

        self.sql_conn.commit()
        new_todo = TodoItem(id=new_id, desc=desc)
        return new_todo

    def toggle_completed(self, uid: int, id: int) -> TodoItem:
        cursor: Cursor
        with self.sql_conn.cursor() as cursor:
            todo = self.fetch(uid, id)
            if not todo:
                msg = f"No todo with {id=}"
                raise AppException(msg)
            cursor.execute(
                f"UPDATE `{self.TABLE}` SET `is_completed` = %s WHERE `id` = %s AND (`user_id` = %s OR `assignee` = %s)",
                (not todo.is_completed, id, uid, uid),
            )

        self.sql_conn.commit()
        todo.is_completed = not todo.is_completed
        return todo

    def change_desc(self, uid: int, id: int, desc: str) -> TodoItem:
        cursor: Cursor
        with self.sql_conn.cursor() as cursor:
            todo = self.fetch(uid, id)
            cursor.execute(
                f"UPDATE `{self.TABLE}` SET `desc` = %s WHERE `id` = %s AND `user_id` = %s",
                (desc, id, uid),
            )
            if not cursor.rowcount:
                msg = f"No todo with {id=}"
                raise AppException(msg)

        self.sql_conn.commit()
        todo.desc = desc
        return todo

    def delete(self, uid: int, id: int) -> None:
        cursor: Cursor
        with self.sql_conn.cursor() as cursor:
            cursor.execute(
                f"DELETE FROM {self.TABLE} WHERE `id` = %s AND `user_id` = %s",
                (id, uid),
            )
            if not cursor.rowcount:
                msg = f"No todo with {id=}"
                print(f"[STORE] [ERROR]: {msg}")
                raise AppException(msg)
        self.sql_conn.commit()
