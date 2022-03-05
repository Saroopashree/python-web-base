from fastapi import FastAPI
from pymysql.cursors import Cursor
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

from src.containers import ApplicationContainer
from src.exception import AppException, router_exception_handler
from src.todo.router import router as todo_router

app_container = ApplicationContainer()


def perform_db_migration():
    print("[ASGI]: Starting initial DB setup")
    sql_conn = app_container.sql_conn_provider().get_conn()

    cursor: Cursor
    with sql_conn.cursor() as cursor:
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS `db_migration` (
        `version` VARCHAR(16) NOT NULL,
        `name` VARCHAR(256) NOT NULL,
        PRIMARY KEY (`version`)
        )ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;"""
        )
    db_migation = app_container.db_migration_orchestrator()
    db_migation.migrate("sql")


def dispose_connection():
    print("[ASGI]: App shutting down...")
    app_container.sql_conn_provider().close_conn()


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
    on_startup=[perform_db_migration],
    on_shutdown=[dispose_connection],
    exception_handlers={AppException: router_exception_handler},
)


app.include_router(todo_router)
