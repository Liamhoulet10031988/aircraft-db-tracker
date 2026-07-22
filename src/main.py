import psycopg2
import requests

from src.api import NominatimAPI, OpenSkyAPI
from src.config import config
from src.database import (
    create_database,
    create_tables,
    save_data_to_database,
)
from src.db_manager import DBManager
from src.exceptions import CountryNotFoundError, EmptyAPIResponseError
from src.services import AircraftDataCollector
from src.user_interaction import user_interaction

DATABASE_NAME = "aircraft_tracker"

COUNTRY_NAMES = [
    "Germany",
    "France",
    "Spain",
    "Italy",
    "Poland",
    "Netherlands",
    "Belgium",
    "Austria",
    "Switzerland",
    "Czechia",
]


def main() -> None:
    """Собирает данные, сохраняет их в БД и запускает меню."""
    try:
        params = config()
        create_database(DATABASE_NAME, params)
        create_tables(DATABASE_NAME, params)

        collector = AircraftDataCollector(
            NominatimAPI(),
            OpenSkyAPI(),
        )
        data = collector.collect(COUNTRY_NAMES)

        save_data_to_database(
            data,
            DATABASE_NAME,
            params,
        )

        manager = DBManager(DATABASE_NAME, params)
        user_interaction(manager)
    except (
        CountryNotFoundError,
        EmptyAPIResponseError,
        requests.RequestException,
        psycopg2.Error,
        FileNotFoundError,
        KeyError,
        RuntimeError,
        ValueError,
    ) as error:
        print(f"Не удалось выполнить программу: {error}")


if __name__ == "__main__":
    main()
