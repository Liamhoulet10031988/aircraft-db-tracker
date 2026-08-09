from typing import Any

import pytest

from src.api import NominatimAPI, OpenSkyAPI
from src.exceptions import CountryNotFoundError, EmptyAPIResponseError
from src.models import Country


class FakeResponse:
    """Имитирует небольшой ответ requests."""

    def __init__(self, data: Any) -> None:
        self.data = data
        self.status_checked = False

    def raise_for_status(self) -> None:
        self.status_checked = True

    def json(self) -> Any:
        return self.data


def test_nominatim_get_country(monkeypatch) -> None:
    response = FakeResponse(
        [
            {
                "boundingbox": [
                    "47.27",
                    "55.09",
                    "5.86",
                    "15.04",
                ]
            }
        ]
    )
    request_data = {}

    def fake_get(url, params, headers, timeout):
        request_data["url"] = url
        request_data["params"] = params
        request_data["headers"] = headers
        request_data["timeout"] = timeout
        return response

    monkeypatch.setattr("src.api.requests.get", fake_get)
    monkeypatch.setattr("src.api.time.sleep", lambda seconds: None)

    country = NominatimAPI().get_country("Germany")

    assert country.name == "Germany"
    assert country.north_latitude == 55.09
    assert response.status_checked is True
    assert request_data["params"]["country"] == "Germany"
    assert "aircraft-db-tracker" in request_data["headers"]["User-Agent"]


def test_nominatim_country_not_found(monkeypatch) -> None:
    monkeypatch.setattr(
        "src.api.requests.get",
        lambda *args, **kwargs: FakeResponse([]),
    )
    monkeypatch.setattr("src.api.time.sleep", lambda seconds: None)

    with pytest.raises(CountryNotFoundError, match="не найдена"):
        NominatimAPI().get_country("Unknown")


def test_opensky_get_aeroplanes(
    monkeypatch,
    country: Country,
    opensky_state: list[object],
) -> None:
    response = FakeResponse(
        {
            "time": 1710000000,
            "states": [
                opensky_state,
                ["short"],
                "wrong state",
            ],
        }
    )
    monkeypatch.setattr(
        "src.api.requests.get",
        lambda *args, **kwargs: response,
    )

    aeroplanes = OpenSkyAPI().get_aeroplanes(country)

    assert len(aeroplanes) == 1
    assert aeroplanes[0].callsign == "DLH123"
    assert response.status_checked is True


def test_opensky_without_states(monkeypatch, country: Country) -> None:
    monkeypatch.setattr(
        "src.api.requests.get",
        lambda *args, **kwargs: FakeResponse({"states": None}),
    )

    assert OpenSkyAPI().get_aeroplanes(country) == []


def test_opensky_empty_response(monkeypatch, country: Country) -> None:
    monkeypatch.setattr(
        "src.api.requests.get",
        lambda *args, **kwargs: FakeResponse({}),
    )

    with pytest.raises(EmptyAPIResponseError, match="пустой ответ"):
        OpenSkyAPI().get_aeroplanes(country)
