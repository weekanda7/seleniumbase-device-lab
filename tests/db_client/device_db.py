import psycopg
from psycopg.rows import dict_row

from config import Config


class DeviceDb:
    """Read-only checks straight against Postgres.

    Tests never write to the DB directly: data goes in through the API (like a real user),
    the DB is only used to verify what the API actually persisted.
    """

    COLUMNS = "id, name, type, status, location, created_at"

    @staticmethod
    def find_by_id(device_id: int) -> dict | None:
        with psycopg.connect(Config.DB_DSN, row_factory=dict_row) as conn:
            return conn.execute(
                f"SELECT {DeviceDb.COLUMNS} FROM devices WHERE id = %s", (device_id,)
            ).fetchone()

    @staticmethod
    def count_by_name(name: str) -> int:
        with psycopg.connect(Config.DB_DSN) as conn:
            return conn.execute(
                "SELECT count(*) FROM devices WHERE name = %s", (name,)
            ).fetchone()[0]
