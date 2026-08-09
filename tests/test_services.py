from src.base_api import BaseAeroplaneAPI, BaseCountryAPI
from src.models import Aeroplane, Country
from src.services import AircraftDataCollector


class FakeCountryAPI(BaseCountryAPI):
    """Возвращает готовую страну без HTTP-запроса."""

    def get_country(self, country_name: str) -> Country:
        """Создает страну с тестовыми границами."""
        return Country(country_name, 47.0, 55.0, 5.0, 15.0)


class FakeAeroplaneAPI(BaseAeroplaneAPI):
    """Возвращает готовый самолет без HTTP-запроса."""

    def get_aeroplanes(self, country: Country) -> list[Aeroplane]:
        """Создает один тестовый самолет."""
        return [
            Aeroplane(
                "3c6444",
                "DLH123",
                country.name,
                13.4,
                52.5,
                10000.0,
                False,
                250.0,
            )
        ]


def test_collect_data() -> None:
    collector = AircraftDataCollector(
        FakeCountryAPI(),
        FakeAeroplaneAPI(),
    )

    result = collector.collect(["Germany", "France"])

    assert len(result) == 2
    assert result[0][0].name == "Germany"
    assert result[0][1][0].callsign == "DLH123"
    assert result[1][0].name == "France"
