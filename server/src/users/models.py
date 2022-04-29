from pydantic import BaseModel

from typing import Optional


class UserAuthRequest(BaseModel):
    username: str
    password: str


class UserAuthResponse(BaseModel):
    id: Optional[int] = None
    message: Optional[str] = None


class UserView(BaseModel):
    id: int
    username: str


class User(UserView):
    password: str
    salt: str
