from typing import Any

from src.db_manager import DBManager
from src.user_interaction import print_rows, user_interaction


class FakeManager(DBManager):
    """Возвращает готовые результаты для проверки меню."""

    def __init__(self) -> None:
        """Не создает настоящее подключение к PostgreSQL."""

    def get_countries_and_aeroplanes_count(
        self,
    ) -> list[tuple[Any, ...]]:
        """Возвращает количество самолетов."""
        return [("Germany", 2)]

    def get_all_aeroplanes(self) -> list[tuple[Any, ...]]:
        """Возвращает пустой список для проверки сообщения."""
        return []

    def get_avg_speed(self) -> float:
        """Возвращает тестовую среднюю скорость."""
        return 250.0

    def get_aeroplanes_with_higher_speed(
        self,
    ) -> list[tuple[Any, ...]]:
        """Возвращает один быстрый самолет."""
        return [("3c6444", "DLH123", "Germany", 300.0)]

    def get_aeroplanes_with_keyword(
        self,
        keyword: str,
    ) -> list[tuple[Any, ...]]:
        """Возвращает самолет с подходящим позывным."""
        return [("3c6444", keyword, "Germany", 250.0)]


def test_print_rows(capsys) -> None:
    print_rows([("Germany", 2)])

    output = capsys.readouterr().out

    assert "Germany | 2" in output


def test_user_interaction_all_commands(monkeypatch, capsys) -> None:
    answers = iter(["1", "2", "3", "4", "5", "DLH", "9", "0"])
    monkeypatch.setattr("builtins.input", lambda text: next(answers))

    user_interaction(FakeManager())

    output = capsys.readouterr().out

    assert "Germany | 2" in output
    assert "Данные не найдены" in output
    assert "Средняя скорость: 250.0 м/с" in output
    assert "DLH" in output
    assert "Неизвестная команда" in output
    assert "Работа программы завершена" in output
