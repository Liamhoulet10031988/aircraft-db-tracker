from configparser import ConfigParser
from pathlib import Path
from typing import Any


def config(
    filename: str = "database.ini",
    section: str = "postgresql",
) -> dict[str, Any]:
    """Читает параметры PostgreSQL из локального INI-файла."""
    file_path = Path(filename)

    if not file_path.exists():
        raise FileNotFoundError(f"Файл настроек {filename} не найден")

    parser = ConfigParser()
    parser.read(file_path, encoding="utf-8")

    if not parser.has_section(section):
        raise KeyError(f"В файле нет раздела {section}")

    return dict(parser.items(section))
