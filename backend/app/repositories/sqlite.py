from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

import sqlite3

from app.repositories.base import normalize_sqlite_path


class SQLiteRepository:
    def __init__(self, database_path: str | Path) -> None:
        self.database_path = normalize_sqlite_path(database_path)

    @contextmanager
    def connect(self) -> Iterator[sqlite3.Connection]:
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        try:
            yield connection
            connection.commit()
        finally:
            connection.close()

    @contextmanager
    def transaction(self) -> Iterator[sqlite3.Connection]:
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        try:
            yield connection
        except Exception:
            connection.rollback()
            raise
        else:
            connection.commit()
        finally:
            connection.close()
