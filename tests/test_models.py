import pytest

from src.models import Aeroplane, Country


def test_country_init(country: Country) -> None:
    assert country.name == "Germany"
    assert country.south_latitude == 47.27
    assert country.north_latitude == 55.09
    assert country.west_longitude == 5.86
    assert country.east_longitude == 15.04


def test_country_from_nominatim() -> None:
    country = Country.from_nominatim(
        "Germany",
        {
            "boundingbox": [
                "47.2701114",
                "55.099161",
                "5.8663153",
                "15.0419309",
            ]
        },
    )

    assert country.name == "Germany"
    assert country.south_latitude == 47.2701114
    assert country.east_longitude == 15.0419309


def test_country_without_boundingbox() -> None:
    with pytest.raises(ValueError, match="нет boundingbox"):
        Country.from_nominatim("Germany", {})


def test_aeroplane_init() -> None:
    aeroplane = Aeroplane(
        "3c6444",
        "DLH123  ",
        "Germany",
        13.405,
        52.52,
        10000.0,
        False,
        250.0,
    )

    assert aeroplane.icao24 == "3c6444"
    assert aeroplane.callsign == "DLH123"
    assert aeroplane.origin_country == "Germany"
    assert aeroplane.longitude == 13.405
    assert aeroplane.latitude == 52.52
    assert aeroplane.baro_altitude == 10000.0
    assert aeroplane.on_ground is False
    assert aeroplane.velocity == 250.0


def test_aeroplane_without_callsign() -> None:
    aeroplane = Aeroplane(
        "3c6444",
        None,
        "Germany",
        None,
        None,
        None,
        True,
        None,
    )

    assert aeroplane.callsign is None


def test_aeroplane_from_opensky_state(
    opensky_state: list[object],
) -> None:
    aeroplane = Aeroplane.from_opensky_state(opensky_state)

    assert aeroplane.icao24 == "3c6444"
    assert aeroplane.callsign == "DLH123"
    assert aeroplane.velocity == 250.0


def test_aeroplane_rejects_short_state() -> None:
    with pytest.raises(ValueError, match="недостаточно данных"):
        Aeroplane.from_opensky_state(["3c6444"])


def test_aeroplane_rejects_empty_icao24() -> None:
    with pytest.raises(ValueError, match="не может быть пустым"):
        Aeroplane("", None, "Germany", None, None, None, False, None)
