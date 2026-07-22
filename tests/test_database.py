from typing import Any

import pytest

from src.database import (
    create_database,
    create_tables,
    save_data_to_database,
)
from src.models import Aeroplane, Country


class FakeCursor:
    """Запоминает SQL без обращения к PostgreSQL."""

    def __init__(self, row: tuple[int] | None = None) -> None:
        self.row = row
        self.queries: list[tuple[Any, Any]] = []

    def execute(self, query: Any, values: Any = None) -> None:
        self.queries.append((query, values))

    def fetchone(self) -> tuple[int] | None:
        return self.row

    def __enter__(self) -> "FakeCursor":
        return self

    def __exit__(self, *args: Any) -> None:
        return None


class FakeConnection:
    """Имитирует соединение psycopg2."""

    def __init__(self, cursor: FakeCursor) -> None:
        self.test_cursor = cursor
        self.autocommit = False
        self.committed = False
        self.closed = False

    def cursor(self) -> FakeCursor:
        return self.test_cursor

    def commit(self) -> None:
        self.committed = True

    def close(self) -> None:
        self.closed = True


def test_create_database(monkeypatch) -> None:
    cursor = FakeCursor(row=None)
    connection = FakeConnection(cursor)
    monkeypatch.setattr(
        "src.database.psycopg2.connect",
        lambda **kwargs: connection,
    )

    create_database("aircraft_tracker", {"host": "localhost"})

    assert connection.autocommit is True
    assert connection.closed is True
    assert len(cursor.queries) == 2


def test_create_database_when_it_exists(monkeypatch) -> None:
    cursor = FakeCursor(row=(1,))
    connection = FakeConnection(cursor)
    monkeypatch.setattr(
        "src.database.psycopg2.connect",
        lambda **kwargs: connection,
    )

    create_database("aircraft_tracker", {"host": "localhost"})

    assert len(cursor.queries) == 1
    assert connection.closed is True


def test_create_tables(monkeypatch) -> None:
    cursor = FakeCursor()
    connection = FakeConnection(cursor)
    monkeypatch.setattr(
        "src.database.psycopg2.connect",
        lambda **kwargs: connection,
    )

    create_tables("aircraft_tracker", {"host": "localhost"})

    assert connection.committed is True
    assert connection.closed is True
    assert len(cursor.queries) == 2


def test_save_data_to_database(monkeypatch) -> None:
    cursor = FakeCursor(row=(1,))
    connection = FakeConnection(cursor)
    monkeypatch.setattr(
        "src.database.psycopg2.connect",
        lambda **kwargs: connection,
    )
    country = Country("Germany", 47.27, 55.09, 5.86, 15.04)
    aeroplane = Aeroplane(
        "3c6444",
        "DLH123",
        "Germany",
        13.40,
        52.52,
        10000.0,
        False,
        250.0,
    )

    save_data_to_database(
        [(country, [aeroplane])],
        "aircraft_tracker",
        {"host": "localhost"},
    )

    assert connection.committed is True
    assert connection.closed is True
    assert len(cursor.queries) == 3


def test_save_data_without_country_id(monkeypatch) -> None:
    cursor = FakeCursor(row=None)
    connection = FakeConnection(cursor)
    monkeypatch.setattr(
        "src.database.psycopg2.connect",
        lambda **kwargs: connection,
    )
    country = Country("Germany", 47.27, 55.09, 5.86, 15.04)

    with pytest.raises(RuntimeError, match="получить id"):
        save_data_to_database(
            [(country, [])],
            "aircraft_tracker",
            {"host": "localhost"},
        )

    assert connection.closed is True
    assert connection.committed is False
