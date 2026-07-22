class CountryNotFoundError(Exception):
    """Страна не найдена в ответе Nominatim."""


class EmptyAPIResponseError(Exception):
    """Внешний API вернул ответ без ожидаемых данных."""
