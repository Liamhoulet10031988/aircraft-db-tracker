from typing import Any

import psycopg2


class DBManager:
    """Выполняет запросы к данным о странах и самолетах."""

    def __init__(
        self,
        database_name: str,
        params: dict[str, Any],
    ) -> None:
        self.database_name = database_name
        self.params = params

    def _execute_query(
        self,
        query: str,
        values: tuple[Any, ...] | None = None,
    ) -> list[tuple[Any, ...]]:
        """Выполняет SELECT-запрос и возвращает все строки."""
        connection = psycopg2.connect(
            dbname=self.database_name,
            **self.params,
        )

        try:
            with connection.cursor() as cursor:
                cursor.execute(query, values)
                return cursor.fetchall()
        finally:
            connection.close()

    def get_countries_and_aeroplanes_count(
        self,
    ) -> list[tuple[Any, ...]]:
        """Возвращает страны и количество самолетов в каждой из них."""
        query = """
            SELECT countries.name, COUNT(aeroplanes.id)
            FROM countries
            LEFT JOIN aeroplanes
                ON countries.id = aeroplanes.country_id
            GROUP BY countries.id, countries.name
            ORDER BY countries.name
        """
        return self._execute_query(query)

    def get_all_aeroplanes(self) -> list[tuple[Any, ...]]:
        """Возвращает полную информацию обо всех самолетах."""
        query = """
            SELECT
                aeroplanes.icao24,
                aeroplanes.callsign,
                aeroplanes.origin_country,
                aeroplanes.longitude,
                aeroplanes.latitude,
                aeroplanes.baro_altitude,
                aeroplanes.on_ground,
                aeroplanes.velocity,
                countries.name AS tracked_country
            FROM aeroplanes
            INNER JOIN countries
                ON aeroplanes.country_id = countries.id
            ORDER BY aeroplanes.callsign NULLS LAST
        """
        return self._execute_query(query)

    def get_avg_speed(self) -> float:
        """Возвращает среднюю скорость самолетов в метрах в секунду."""
        query = """
            SELECT AVG(velocity)
            FROM aeroplanes
            WHERE velocity IS NOT NULL
        """
        result = self._execute_query(query)
        average_speed = result[0][0]

        if average_speed is None:
            return 0.0

        return round(float(average_speed), 2)

    def get_aeroplanes_with_higher_speed(
        self,
    ) -> list[tuple[Any, ...]]:
        """Возвращает самолеты со скоростью выше средней."""
        query = """
            SELECT
                icao24,
                callsign,
                origin_country,
                velocity
            FROM aeroplanes
            WHERE velocity > (
                SELECT AVG(velocity)
                FROM aeroplanes
                WHERE velocity IS NOT NULL
            )
            ORDER BY velocity DESC
        """
        return self._execute_query(query)

    def get_aeroplanes_with_keyword(
        self,
        keyword: str,
    ) -> list[tuple[Any, ...]]:
        """Ищет самолеты по части позывного без учета регистра."""
        query = """
            SELECT
                icao24,
                callsign,
                origin_country,
                velocity
            FROM aeroplanes
            WHERE callsign ILIKE %s
            ORDER BY callsign
        """
        return self._execute_query(query, (f"%{keyword}%",))
