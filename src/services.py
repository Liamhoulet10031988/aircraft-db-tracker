from src.base_api import BaseAeroplaneAPI, BaseCountryAPI
from src.models import Aeroplane, Country


class AircraftDataCollector:
    """Собирает страны и самолеты через переданные API-клиенты."""

    def __init__(
        self,
        country_api: BaseCountryAPI,
        aeroplane_api: BaseAeroplaneAPI,
    ) -> None:
        self.country_api = country_api
        self.aeroplane_api = aeroplane_api

    def collect(
        self,
        country_names: list[str],
    ) -> list[tuple[Country, list[Aeroplane]]]:
        """Возвращает страны вместе с найденными самолетами."""
        result = []

        for country_name in country_names:
            country = self.country_api.get_country(country_name)
            aeroplanes = self.aeroplane_api.get_aeroplanes(country)
            result.append((country, aeroplanes))

        return result
