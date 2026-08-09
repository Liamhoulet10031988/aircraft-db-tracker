import time
from typing import Any

import requests

from src.base_api import BaseAeroplaneAPI, BaseCountryAPI
from src.exceptions import CountryNotFoundError, EmptyAPIResponseError
from src.models import Aeroplane, Country


class NominatimAPI(BaseCountryAPI):
    """Получает географические границы стран через Nominatim."""

    def __init__(self) -> None:
        self.url = "https://nominatim.openstreetmap.org/search"
        self.headers = {
            "User-Agent": (
                "aircraft-db-tracker/1.0 "
                "(github.com/Liamhoulet10031988/aircraft-db-tracker)"
            )
        }

    def get_country(self, country_name: str) -> Country:
        """Возвращает объект страны с географическими границами."""
        params = {
            "country": country_name,
            "format": "json",
            "limit": "1",
        }

        response = requests.get(
            self.url,
            params=params,
            headers=self.headers,
            timeout=10,
        )
        time.sleep(1)
        response.raise_for_status()
        data: list[dict[str, Any]] = response.json()

        if not data:
            raise CountryNotFoundError(
                f"Страна {country_name} не найдена"
            )

        return Country.from_nominatim(country_name, data[0])


class OpenSkyAPI(BaseAeroplaneAPI):
    """Получает самолеты в географических границах страны."""

    def __init__(self) -> None:
        self.url = "https://opensky-network.org/api/states/all"

    def get_aeroplanes(self, country: Country) -> list[Aeroplane]:
        """Возвращает объекты самолетов в границах страны."""
        params = {
            "lamin": country.south_latitude,
            "lamax": country.north_latitude,
            "lomin": country.west_longitude,
            "lomax": country.east_longitude,
        }

        response = requests.get(
            self.url,
            params=params,
            timeout=20,
        )
        response.raise_for_status()
        data: dict[str, Any] = response.json()

        if not data:
            raise EmptyAPIResponseError(
                f"OpenSky вернул пустой ответ для {country.name}"
            )

        states = data.get("states") or []
        aeroplanes = []

        for state in states:
            if not isinstance(state, list):
                continue

            try:
                aeroplane = Aeroplane.from_opensky_state(state)
            except ValueError:
                continue

            aeroplanes.append(aeroplane)

        return aeroplanes
