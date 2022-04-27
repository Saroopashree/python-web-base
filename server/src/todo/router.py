from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel

from src.containers import ApplicationContainer
from src.todo.models import TodoItem

app_container = ApplicationContainer()

store = app_container.todo_store()


class DescPayload(BaseModel):
    desc: str


router = APIRouter(prefix="/todo")


@router.get("/{uid}", response_model=list[TodoItem])
async def fetch_all_todos(uid: int) -> list[TodoItem]:
    return store.fetch(uid)


@router.get("/{uid}/{tid}", response_model=Optional[TodoItem])
async def fetch_todo_by_id(uid: int, tid: int) -> Optional[TodoItem]:
    return store.fetch(uid, tid)


@router.post("/{uid}", response_model=TodoItem)
async def add_todo(uid: int, payload: DescPayload) -> TodoItem:
    return store.add(uid, payload.desc)


@router.put("/{uid}/toggle-complete/{tid}", response_model=TodoItem)
async def toggle_completed(uid: int, tid: int) -> TodoItem:
    return store.toggle_completed(uid, tid)


@router.put("/{uid}/change-desc/{tid}", response_model=TodoItem)
async def change_description(uid: int, tid: int, payload: DescPayload) -> TodoItem:
    return store.change_desc(uid, tid, payload.desc)


@router.delete("/{uid}/{tid}", response_model=None)
async def delete(uid: int, tid: int) -> None:
    store.delete(uid, tid)
