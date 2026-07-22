# Aircraft Database Tracker

Консольное приложение получает сведения о самолетах через открытые API,
сохраняет их в PostgreSQL и выполняет аналитические SQL-запросы.

Проект подготовлен в рамках курсовой работы Skypro после блока
«Работа с базами данных».

## Возможности

- получение географических границ десяти стран через Nominatim;
- получение самолетов в границах стран через OpenSky;
- сохранение стран и самолетов в связанные таблицы PostgreSQL;
- вывод количества самолетов по каждой стране;
- вывод полной информации обо всех самолетах;
- расчет средней скорости;
- поиск самолетов со скоростью выше средней;
- поиск самолетов по части позывного.

## Технологии

- Python 3.12;
- PostgreSQL;
- `psycopg2`;
- `requests`;
- Poetry;
- pytest и pytest-cov.

## Структура базы данных

Таблица `countries` хранит названия стран и их географические границы.

Таблица `aeroplanes` хранит данные самолетов. Поле `country_id` является
внешним ключом и связывает самолет с отслеживаемой страной.

```text
countries (1) -> (много) aeroplanes
```

## Основные модули

```text
src/api.py               получение данных из Nominatim и OpenSky
src/models.py            классы Country и Aeroplane
src/services.py          последовательный сбор данных
src/database.py          создание и заполнение таблиц
src/db_manager.py        аналитические SQL-запросы
src/user_interaction.py  консольное меню
src/main.py              точка запуска приложения
```

## Установка

```powershell
poetry install
```

## Настройка PostgreSQL

Создайте локальный файл `database.ini` по примеру
`database.ini.example`:

```ini
[postgresql]
host=localhost
user=postgres
password=ваш_пароль
port=5432
```

Настоящий `database.ini` добавлен в `.gitignore`, поэтому пароль не попадет
в репозиторий.

## Запуск

```powershell
poetry run python -m src.main
```

При первом запуске программа создает базу `aircraft_tracker`, создает таблицы,
получает актуальный снимок данных и открывает консольное меню.

## Тесты

```powershell
poetry run pytest
```

## Покрытие тестами

```powershell
poetry run pytest --cov=src --cov-report=term-missing --cov-report=html:coverage_html
```

HTML-отчет хранится в папке `coverage_html` и добавляется в репозиторий по
требованию наставника.

## Проверка качества кода

```powershell
poetry run isort .
poetry run flake8
poetry run mypy .
```

## Источники данных

- Nominatim: `https://nominatim.openstreetmap.org`;
- OpenSky Network: `https://opensky-network.org`;
- географические данные: OpenStreetMap contributors.

Публичный Nominatim допускает не более одного запроса в секунду. Приложение
делает запросы последовательно с обязательной паузой. Не запускайте массовый
сбор данных многократно подряд.
