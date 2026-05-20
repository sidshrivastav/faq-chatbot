from __future__ import annotations

import sqlite3

import pytest

from app.repositories.sqlite import SQLiteRepository


def test_sqlite_repository_opens_connection_with_row_factory(tmp_path) -> None:
    repo = SQLiteRepository(tmp_path / "local.sqlite3")

    with repo.connect() as connection:
        connection.execute("CREATE TABLE sample (name TEXT NOT NULL)")
        connection.execute("INSERT INTO sample (name) VALUES (?)", ("HR",))
        row = connection.execute("SELECT name FROM sample").fetchone()

    assert isinstance(row, sqlite3.Row)
    assert row["name"] == "HR"


def test_transaction_commits_on_success(tmp_path) -> None:
    repo = SQLiteRepository(tmp_path / "local.sqlite3")

    with repo.transaction() as connection:
        connection.execute("CREATE TABLE sample (name TEXT NOT NULL)")
        connection.execute("INSERT INTO sample (name) VALUES (?)", ("IT",))

    with repo.connect() as connection:
        count = connection.execute("SELECT COUNT(*) AS count FROM sample").fetchone()["count"]

    assert count == 1


def test_transaction_rolls_back_on_error(tmp_path) -> None:
    repo = SQLiteRepository(tmp_path / "local.sqlite3")

    with repo.connect() as connection:
        connection.execute("CREATE TABLE sample (name TEXT NOT NULL)")

    with pytest.raises(RuntimeError):
        with repo.transaction() as connection:
            connection.execute("INSERT INTO sample (name) VALUES (?)", ("Admissions",))
            raise RuntimeError("force rollback")

    with repo.connect() as connection:
        count = connection.execute("SELECT COUNT(*) AS count FROM sample").fetchone()["count"]

    assert count == 0
