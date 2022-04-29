from typing import List
from fastapi import APIRouter
from src.containers import ApplicationContainer

from src.users.models import UserAuthRequest, UserAuthResponse, UserView

app_container = ApplicationContainer()

store = app_container.user_store()

router = APIRouter(prefix="/users")


@router.post("/login")
async def login(payload: UserAuthRequest) -> UserAuthResponse:
    return store.authenticate(payload.username, payload.password)


@router.post("/register")
async def register(payload: UserAuthRequest) -> UserAuthResponse:
    return store.create_user(payload.username, payload.password)


@router.get("/list")
async def list_all_users() -> List[UserView]:
    return store.list_all()
