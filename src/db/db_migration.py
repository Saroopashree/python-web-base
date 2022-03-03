import os
from pathlib import Path

from pymysql import Connection

ROOT_DIR = Path(__file__)


class DBMigration:
    def __init__(self, sql_conn: Connection) -> None:
        self.sql_conn = sql_conn

    def migrate(self, migration_sql_dir: str = None) -> None:
        """
        :param migration_sql_dir: The path has to be relative to the project root
        """
        absolute_uri = os.path.join(ROOT_DIR, migration_sql_dir or "sql")

        for file in Path(absolute_uri).glob("*"):
            self.unit_migration(file.name)

    def unit_migration(self, file_name: str) -> None:
        version, migration_name = file_name.split("__")
        with self.sql_conn.cursor() as cursor:
            cursor.execute(f"SELECT * FROM db_migration WHERE version = %s", (version))
            result = cursor.fetchone()
            if result:
                return

            with open(os.path.join(ROOT_DIR, file_name), "r") as reader:
                content = reader.read()

            cursor.execute(content)
            cursor.execute(
                f"INSERT INTO `db_migration` (`version`, `name`) VALUES (%s, %s)",
                (version, migration_name),
            )
        self.sql_conn.commit()
