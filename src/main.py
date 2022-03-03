import logging

from fastapi import FastAPI
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

from src.todo.router import router as todo_router

LOG = logging.getLogger(__name__)

app = FastAPI(
    title="Todo Backend",
    middleware=[
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_methods=["*"],
            allow_headers=["*"],
        )
    ],
    on_startup=[lambda: LOG.debug("App starting up...")],
    on_shutdown=[lambda: LOG.debug("App shutting down...")],
)


app.include_router(todo_router)
