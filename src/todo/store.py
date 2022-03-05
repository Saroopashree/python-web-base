import itertools
from typing import Final, Optional, Union

from pymysql import Connection
from pymysql.cursors import Cursor

from src.exception import AppException
from src.todo.models import TodoItem


class TodoStore:
    id_iter = itertools.count()
    rows: dict[int, TodoItem] = {}

    TABLE = "todos"

    def __init__(self, sql_conn: Connection) -> None:
        self.sql_conn = sql_conn

    def fetch(self, id: int = None) -> Union[list[TodoItem], Optional[TodoItem]]:
        cursor: Cursor
        with self.sql_conn.cursor() as cursor:
            if id:
                cursor.execute(f"SELECT * FROM `{self.TABLE}` WHERE `id` = %s", (id))
                result = cursor.fetchone()
                if result:
                    return TodoItem(**result)
            else:
                cursor.execute(f"SELECT * FROM `{self.TABLE}`")
                result = cursor.fetchall()
                return [TodoItem(**todo) for todo in result]

    def add(self, desc: str) -> TodoItem:
        cursor: Cursor
        with self.sql_conn.cursor() as cursor:
            cursor.execute(
                f"INSERT INTO `{self.TABLE}` (`desc`) VALUES (%s)",
                (desc),
            )
            new_id = cursor.lastrowid

        self.sql_conn.commit()
        new_todo = TodoItem(id=new_id, desc=desc)
        return new_todo

    def toggle_completed(self, id: int) -> TodoItem:
        cursor: Cursor
        with self.sql_conn.cursor() as cursor:
            todo = self.fetch(id)
            if not todo:
                msg = f"No todo with {id=}"
                raise AppException(msg)
            cursor.execute(
                f"UPDATE `{self.TABLE}` SET `is_completed` = %s WHERE `id` = %s",
                (not todo.is_completed, id),
            )

        self.sql_conn.commit()
        todo.is_completed = not todo.is_completed
        return todo

    def change_desc(self, id: int, desc: str) -> TodoItem:
        cursor: Cursor
        with self.sql_conn.cursor() as cursor:
            todo = self.fetch(id)
            cursor.execute(
                f"UPDATE `{self.TABLE}` SET `desc` = %s WHERE `id` = %s", (desc, id)
            )
            if not cursor.rowcount:
                msg = f"No todo with {id=}"
                raise AppException(msg)

        self.sql_conn.commit()
        todo.desc = desc
        return todo

    def delete(self, id: int) -> None:
        cursor: Cursor
        with self.sql_conn.cursor() as cursor:
            cursor.execute(f"DELETE FROM {self.TABLE} WHERE `id` = %s", (id))
            if not cursor.rowcount:
                msg = f"No todo with {id=}"
                print(f"[STORE] [ERROR]: {msg}")
                raise AppException(msg)
        self.sql_conn.commit()
