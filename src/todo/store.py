import logging
from typing import Final, Optional
from src.todo.models import TodoItem
import itertools

LOG = logging.getLogger(__name__)


class TodoStore:
    id_iter = itertools.count()
    rows: dict[int, TodoItem] = {}

    def fetch(self, id: int = None) -> list[TodoItem] | Optional[TodoItem]:
        if id:
            return self.rows.get(id)
        else:
            todos = list(self.rows.values())
            print(todos)
            return todos

    def add(self, todo: TodoItem) -> TodoItem:
        new_id = next(self.id_iter)
        todo.id = new_id
        self.rows[new_id] = todo
        return todo

    def toggle_completed(self, id: int) -> TodoItem:
        try:
            todo = self.rows[id]
            todo.is_completed = not todo.is_completed
            return todo
        except KeyError:
            msg = f"No todo with {id=}"
            LOG.error(msg)
            raise msg

    def delete(self, id: int) -> None:
        try:
            del self.rows[id]
        except KeyError:
            msg = f"No todo with {id=}"
            LOG.error(msg)
            raise msg

    def change_desc(self, id: int, desc: str) -> TodoItem:
        try:
            todo = self.rows[id]
            todo.desc = desc
            return todo
        except KeyError:
            msg = f"No todo with {id=}"
            LOG.error(msg)
            raise msg
