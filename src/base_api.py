from abc import ABC, abstractmethod

from src.models import Aeroplane, Country


class BaseCountryAPI(ABC):
    """Интерфейс API для получения данных о стране."""

    @abstractmethod
    def get_country(self, country_name: str) -> Country:
        """Возвращает страну с географическими границами."""
        raise NotImplementedError


class BaseAeroplaneAPI(ABC):
    """Интерфейс API для получения самолетов."""

    @abstractmethod
    def get_aeroplanes(self, country: Country) -> list[Aeroplane]:
        """Возвращает самолеты в границах страны."""
        raise NotImplementedError
