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


@router.get("/", response_model=list[TodoItem])
async def fetch_all_todos() -> list[TodoItem]:
    return store.fetch()


@router.get("/{tid}", response_model=Optional[TodoItem])
async def fetch_todo_by_id(tid: int) -> Optional[TodoItem]:
    return store.fetch(tid)


@router.post("/", response_model=TodoItem)
async def add_todo(payload: DescPayload) -> TodoItem:
    return store.add(payload.desc)


@router.put("/toggle-complete/{tid}", response_model=TodoItem)
async def toggle_completed(tid: int) -> TodoItem:
    return store.toggle_completed(tid)


@router.put("/change-desc/{tid}", response_model=TodoItem)
async def change_description(tid: int, payload: DescPayload) -> TodoItem:
    return store.change_desc(tid, payload.desc)


@router.delete("/{tid}", response_model=None)
async def delete(tid: int) -> None:
    store.delete(tid)
