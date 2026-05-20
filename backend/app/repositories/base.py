from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path
from typing import Iterator, Protocol

import sqlite3


class Repository(Protocol):
    @contextmanager
    def connect(self) -> Iterator[sqlite3.Connection]:
        ...

    @contextmanager
    def transaction(self) -> Iterator[sqlite3.Connection]:
        ...


def normalize_sqlite_path(database_path: str | Path) -> Path:
    return Path(database_path)
