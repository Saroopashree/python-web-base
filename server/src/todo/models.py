from typing import Optional

from pydantic import BaseModel


class TodoItem(BaseModel):
    id: int
    desc: str
    is_completed: bool = False
