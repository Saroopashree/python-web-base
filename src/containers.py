from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Provider, Singleton
from pymysql import Connection

from src.db.db_migration import DBMigrationOrchestrator
from src.db.utils import SqlConnProvider
from src.todo.store import TodoStore


class ApplicationContainer(DeclarativeContainer):
    sql_conn_provider: Provider[SqlConnProvider] = Singleton(SqlConnProvider)
    db_migration_orchestrator: Provider[DBMigrationOrchestrator] = Singleton(
        DBMigrationOrchestrator, sql_conn=sql_conn_provider.provided.get_conn.call()
    )

    todo_store: Provider[TodoStore] = Singleton(
        TodoStore, sql_conn=sql_conn_provider.provided.get_conn.call()
    )
