from typing import Any

import psycopg2
from psycopg2 import sql

from src.models import Aeroplane, Country


def create_database(
    database_name: str,
    params: dict[str, Any],
) -> None:
    """Создает базу данных, если она еще не существует."""
    connection = psycopg2.connect(dbname="postgres", **params)
    connection.autocommit = True

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT 1 FROM pg_database WHERE datname = %s",
                (database_name,),
            )

            if cursor.fetchone() is None:
                query = sql.SQL("CREATE DATABASE {}").format(
                    sql.Identifier(database_name)
                )
                cursor.execute(query)
    finally:
        connection.close()


def create_tables(
    database_name: str,
    params: dict[str, Any],
) -> None:
    """Создает таблицы стран и самолетов."""
    connection = psycopg2.connect(
        dbname=database_name,
        **params,
    )

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS countries (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) UNIQUE NOT NULL,
                    south_latitude DOUBLE PRECISION NOT NULL,
                    north_latitude DOUBLE PRECISION NOT NULL,
                    west_longitude DOUBLE PRECISION NOT NULL,
                    east_longitude DOUBLE PRECISION NOT NULL
                )
                """
            )

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS aeroplanes (
                    id SERIAL PRIMARY KEY,
                    icao24 VARCHAR(20) NOT NULL,
                    callsign VARCHAR(50),
                    origin_country VARCHAR(100),
                    longitude DOUBLE PRECISION,
                    latitude DOUBLE PRECISION,
                    baro_altitude DOUBLE PRECISION,
                    on_ground BOOLEAN NOT NULL DEFAULT FALSE,
                    velocity DOUBLE PRECISION,
                    country_id INTEGER NOT NULL,
                    CONSTRAINT fk_aeroplanes_country
                        FOREIGN KEY (country_id)
                        REFERENCES countries(id)
                        ON DELETE CASCADE,
                    CONSTRAINT uq_aeroplane_country
                        UNIQUE (icao24, country_id)
                )
                """
            )

        connection.commit()
    finally:
        connection.close()


def save_data_to_database(
    data: list[tuple[Country, list[Aeroplane]]],
    database_name: str,
    params: dict[str, Any],
) -> None:
    """Перезаписывает актуальные страны и самолеты в таблицах."""
    connection = psycopg2.connect(
        dbname=database_name,
        **params,
    )

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                TRUNCATE TABLE aeroplanes, countries
                RESTART IDENTITY CASCADE
                """
            )

            for country, aeroplanes in data:
                cursor.execute(
                    """
                    INSERT INTO countries (
                        name,
                        south_latitude,
                        north_latitude,
                        west_longitude,
                        east_longitude
                    )
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id
                    """,
                    (
                        country.name,
                        country.south_latitude,
                        country.north_latitude,
                        country.west_longitude,
                        country.east_longitude,
                    ),
                )

                row = cursor.fetchone()

                if row is None:
                    raise RuntimeError(
                        "Не удалось получить id созданной страны"
                    )

                country_id = row[0]

                for aeroplane in aeroplanes:
                    cursor.execute(
                        """
                        INSERT INTO aeroplanes (
                            icao24,
                            callsign,
                            origin_country,
                            longitude,
                            latitude,
                            baro_altitude,
                            on_ground,
                            velocity,
                            country_id
                        )
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """,
                        (
                            aeroplane.icao24,
                            aeroplane.callsign,
                            aeroplane.origin_country,
                            aeroplane.longitude,
                            aeroplane.latitude,
                            aeroplane.baro_altitude,
                            aeroplane.on_ground,
                            aeroplane.velocity,
                            country_id,
                        ),
                    )

        connection.commit()
    finally:
        connection.close()
