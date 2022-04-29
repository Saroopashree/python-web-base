import os
from pathlib import Path

from pymysql import Connection
from pymysql.cursors import Cursor

ROOT_DIR = os.getcwd()


class DBMigrationOrchestrator:
    def __init__(self, sql_conn: Connection) -> None:
        self.sql_conn = sql_conn

    def migrate(self, migration_sql_dir: str = None) -> None:
        """
        :param migration_sql_dir: The path has to be relative to the project root.
        Defaults to location `"sql"` relative to the project root.
        """
        print("[DB_MIGRATION]: Starting database migration...")
        migration_sql_dir = migration_sql_dir or "sql"
        absolute_uri = os.path.join(ROOT_DIR, migration_sql_dir)

        for file in sorted(Path(absolute_uri).glob("*.sql")):
            self.unit_migration(file.name, migration_sql_dir)

        print("[DB_MIGRATION]: Database migration finished.")

    def unit_migration(self, file_name: str, migration_sql_dir: str) -> None:
        version, migration_script_name = file_name.split("__")
        migration_name = migration_script_name.split(".")[0]

        cursor: Cursor
        with self.sql_conn.cursor() as cursor:
            cursor.execute(f"SELECT * FROM db_migration WHERE version = %s", (version))
            result = cursor.fetchone()
            if result:
                return

            with open(os.path.join(ROOT_DIR, migration_sql_dir, file_name), "r") as reader:
                content = reader.read()

            print(f"[DB_MIGRATION]: Performing migration for {version=} with {migration_name=}")
            cursor.execute(content)
            cursor.execute(
                f"INSERT INTO `db_migration` (`version`, `name`) VALUES (%s, %s)",
                (version, migration_name),
            )
        self.sql_conn.commit()
