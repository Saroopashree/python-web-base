from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Singleton
from src.users.store import UserStore

from src.db.db_migration import DBMigrationOrchestrator
from src.db.sql import SqlConnProvider
from src.todo.store import TodoStore


class ApplicationContainer(DeclarativeContainer):
    sql_conn_provider: Singleton[SqlConnProvider] = Singleton(SqlConnProvider)
    db_migration_orchestrator: Singleton[DBMigrationOrchestrator] = Singleton(
        DBMigrationOrchestrator, sql_conn=sql_conn_provider.provided.get_conn.call()
    )

    todo_store: Singleton[TodoStore] = Singleton(TodoStore, sql_conn=sql_conn_provider.provided.get_conn.call())
    user_store: Singleton[UserStore] = Singleton(UserStore, sql_conn=sql_conn_provider.provided.get_conn.call())
