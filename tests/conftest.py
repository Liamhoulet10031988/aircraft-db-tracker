import pytest

from src.models import Country


@pytest.fixture
def country() -> Country:
    """Возвращает страну для тестов API и моделей."""
    return Country(
        "Germany",
        47.27,
        55.09,
        5.86,
        15.04,
    )


@pytest.fixture
def opensky_state() -> list[object]:
    """Возвращает одну строку states из ответа OpenSky."""
    return [
        "3c6444",
        "DLH123  ",
        "Germany",
        1710000000,
        1710000000,
        13.405,
        52.52,
        10000.0,
        False,
        250.0,
    ]
