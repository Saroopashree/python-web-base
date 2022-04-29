from fastapi import Request
from fastapi.responses import JSONResponse


class AppException(Exception):
    def __init__(self, msg: str) -> None:
        super().__init__(msg)
        self.msg = msg


def router_exception_handler(request: Request, exc: AppException):
    return JSONResponse(status_code=400, content={"detail": exc.msg})
