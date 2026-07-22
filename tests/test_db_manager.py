from typing import Any

from src.db_manager import DBManager


class FakeCursor:
    """Возвращает готовые строки вместо PostgreSQL."""

    def __init__(self, rows: list[tuple[Any, ...]]) -> None:
        self.rows = rows
        self.query = ""
        self.values: tuple[Any, ...] | None = None

    def execute(
        self,
        query: str,
        values: tuple[Any, ...] | None = None,
    ) -> None:
        self.query = query
        self.values = values

    def fetchall(self) -> list[tuple[Any, ...]]:
        return self.rows

    def __enter__(self) -> "FakeCursor":
        return self

    def __exit__(self, *args: Any) -> None:
        return None


class FakeConnection:
    """Имитирует соединение с PostgreSQL."""

    def __init__(self, cursor: FakeCursor) -> None:
        self.test_cursor = cursor
        self.closed = False

    def cursor(self) -> FakeCursor:
        return self.test_cursor

    def close(self) -> None:
        self.closed = True


def test_execute_query(monkeypatch) -> None:
    cursor = FakeCursor([("Germany", 2)])
    connection = FakeConnection(cursor)
    monkeypatch.setattr(
        "src.db_manager.psycopg2.connect",
        lambda **kwargs: connection,
    )
    manager = DBManager("aircraft_tracker", {"host": "localhost"})

    result = manager._execute_query("SELECT test", ("value",))

    assert result == [("Germany", 2)]
    assert cursor.query == "SELECT test"
    assert cursor.values == ("value",)
    assert connection.closed is True


def test_get_countries_and_aeroplanes_count(monkeypatch) -> None:
    manager = DBManager("aircraft_tracker", {})
    saved_query = []

    def fake_execute(query, values=None):
        saved_query.append(query)
        return [("Germany", 2)]

    monkeypatch.setattr(manager, "_execute_query", fake_execute)

    result = manager.get_countries_and_aeroplanes_count()

    assert result == [("Germany", 2)]
    assert "LEFT JOIN" in saved_query[0]
    assert "COUNT" in saved_query[0]


def test_get_all_aeroplanes(monkeypatch) -> None:
    manager = DBManager("aircraft_tracker", {})
    rows = [("3c6444", "DLH123", "Germany", 13.4)]
    saved_query = []

    def fake_execute(query, values=None):
        saved_query.append(query)
        return rows

    monkeypatch.setattr(manager, "_execute_query", fake_execute)

    assert manager.get_all_aeroplanes() == rows
    assert "INNER JOIN" in saved_query[0]


def test_get_avg_speed(monkeypatch) -> None:
    manager = DBManager("aircraft_tracker", {})
    monkeypatch.setattr(
        manager,
        "_execute_query",
        lambda query, values=None: [(250.126,)],
    )

    assert manager.get_avg_speed() == 250.13


def test_get_avg_speed_without_data(monkeypatch) -> None:
    manager = DBManager("aircraft_tracker", {})
    monkeypatch.setattr(
        manager,
        "_execute_query",
        lambda query, values=None: [(None,)],
    )

    assert manager.get_avg_speed() == 0.0


def test_get_aeroplanes_with_higher_speed(monkeypatch) -> None:
    manager = DBManager("aircraft_tracker", {})
    saved_query = []

    def fake_execute(query, values=None):
        saved_query.append(query)
        return [("3c6444", "DLH123", "Germany", 250.0)]

    monkeypatch.setattr(manager, "_execute_query", fake_execute)

    result = manager.get_aeroplanes_with_higher_speed()

    assert result[0][1] == "DLH123"
    assert "SELECT AVG(velocity)" in saved_query[0]


def test_get_aeroplanes_with_keyword(monkeypatch) -> None:
    manager = DBManager("aircraft_tracker", {})
    saved_values = []

    def fake_execute(query, values=None):
        saved_values.append(values)
        assert "ILIKE %s" in query
        return [("3c6444", "DLH123", "Germany", 250.0)]

    monkeypatch.setattr(manager, "_execute_query", fake_execute)

    result = manager.get_aeroplanes_with_keyword("DLH")

    assert result[0][1] == "DLH123"
    assert saved_values[0] == ("%DLH%",)
