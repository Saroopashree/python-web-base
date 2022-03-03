import itertools
import logging
from typing import Final, Optional, Union

from pymysql import Connection

from src.todo.models import TodoItem

LOG = logging.getLogger(__name__)


class TodoStore:
    id_iter = itertools.count()
    rows: dict[int, TodoItem] = {}

    TABLE = "todos"

    def __init__(self, sql_conn: Connection) -> None:
        self.sql_conn = sql_conn

    def fetch(self, id: int = None) -> Union[list[TodoItem], Optional[TodoItem]]:
        with self.sql_conn.cursor() as cursor:
            if id:
                cursor.exec(f"SELECT * FROM `{self.TABLE}` WHERE `id` = %s", (id))
                result = cursor.fetchone()
                if result:
                    return TodoItem(**result)
            else:
                cursor.exec(f"SELECT * FROM `{self.TABLE}`")
                result = cursor.fetchall()
                return [TodoItem(**todo) for todo in result]

    def add(self, todo: TodoItem) -> TodoItem:
        with self.sql_conn.cursor() as cursor:
            cursor.execte(
                f"INSERT INTO `{self.TABLE}` (`desc`, `is_completed`) VALUES (%s, %s)",
                todo.desc,
                todo.is_completed,
            )
            new_id = cursor.lastrowid

        self.sql_conn.commit()
        todo.id = new_id
        return todo

    def toggle_completed(self, id: int) -> TodoItem:
        with self.sql_conn.cursor() as cursor:
            todo = self.fetch(id)
            if not todo:
                msg = f"No todo with {id=}"
                raise msg
            cursor.execute(
                f"UPDATE `{self.TABLE}` SET `is_completed` = %s WHERE `id` = %s",
                (id, not todo.is_completed),
            )

        self.sql_conn.commit()
        todo.is_completed = not todo.is_completed

    def delete(self, id: int) -> None:
        with self.sql_conn.cursor() as cursor:
            cursor.execute(f"DELETE FROM {self.TABLE} WHERE `id` = %s", (id))
            if not cursor.rowcount:
                msg = f"No todo with {id=}"
                LOG.error(msg)
                raise msg
        self.sql_conn.commit()

    def change_desc(self, id: int, desc: str) -> TodoItem:
        with self.sql_conn.cursor() as cursor:
            todo = self.fetch(id)
            cursor.execute(
                f"UPDATE `{self.TABLE}` SET `desc` = %s WHERE `id` = %s", (id, desc)
            )
            if not cursor.rowcount:
                msg = f"No todo with {id=}"
                raise msg

        self.sql_conn.commit()
        todo.desc = not todo.desc
        return todo
