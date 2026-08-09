from typing import Any


class Country:
    """Страна и ее географические границы."""

    def __init__(
        self,
        name: str,
        south_latitude: float,
        north_latitude: float,
        west_longitude: float,
        east_longitude: float,
    ) -> None:
        self.name = name
        self.south_latitude = south_latitude
        self.north_latitude = north_latitude
        self.west_longitude = west_longitude
        self.east_longitude = east_longitude

    @classmethod
    def from_nominatim(
        cls,
        name: str,
        data: dict[str, Any],
    ) -> "Country":
        """Создает страну из одного результата Nominatim."""
        boundingbox = data.get("boundingbox")

        if not boundingbox or len(boundingbox) != 4:
            raise ValueError("В ответе Nominatim нет boundingbox")

        return cls(
            name=name,
            south_latitude=float(boundingbox[0]),
            north_latitude=float(boundingbox[1]),
            west_longitude=float(boundingbox[2]),
            east_longitude=float(boundingbox[3]),
        )


class Aeroplane:
    """Самолет, полученный из ответа OpenSky."""

    def __init__(
        self,
        icao24: str,
        callsign: str | None,
        origin_country: str,
        longitude: float | None,
        latitude: float | None,
        baro_altitude: float | None,
        on_ground: bool,
        velocity: float | None,
    ) -> None:
        if not icao24:
            raise ValueError("ICAO24 не может быть пустым")

        self.icao24 = icao24
        self.callsign = callsign.strip() if callsign else None
        self.origin_country = origin_country
        self.longitude = longitude
        self.latitude = latitude
        self.baro_altitude = baro_altitude
        self.on_ground = on_ground
        self.velocity = velocity

    @classmethod
    def from_opensky_state(cls, state: list[Any]) -> "Aeroplane":
        """Создает самолет из одной строки states OpenSky."""
        if len(state) < 10:
            raise ValueError("В строке OpenSky недостаточно данных")

        return cls(
            icao24=state[0],
            callsign=state[1],
            origin_country=state[2],
            longitude=state[5],
            latitude=state[6],
            baro_altitude=state[7],
            on_ground=state[8],
            velocity=state[9],
        )
