import logging

from fastapi import FastAPI
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from src.db.db_migration import DBMigration
from src.db.utils import get_db

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

@app.on_event("startup")
def perform_db_migration():
    db_migation = DBMigration(get_db())
    db_migation.migrate("sql")


app.include_router(todo_router)
