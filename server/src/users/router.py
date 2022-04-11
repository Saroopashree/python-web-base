from fastapi import APIRouter

from server.src.users.models import UserAuthRequest, UserAuthResponse


router = APIRouter("/users")


@router.post("/login")
async def login(payload: UserAuthRequest) -> UserAuthResponse:
    ...


@router.post("register")
async def register(payload: UserAuthRequest) -> UserAuthResponse:
    ...


@router.get("/list")
async def list_all_users() -> List[User]:
    ...
