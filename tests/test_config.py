from pathlib import Path

import pytest

from src.config import config


def test_config_reads_postgresql_section(tmp_path: Path) -> None:
    file_path = tmp_path / "database.ini"
    file_path.write_text(
        "[postgresql]\n"
        "host=localhost\n"
        "user=postgres\n"
        "password=test\n"
        "port=5432\n",
        encoding="utf-8",
    )

    params = config(str(file_path))

    assert params["host"] == "localhost"
    assert params["user"] == "postgres"
    assert params["port"] == "5432"


def test_config_without_file(tmp_path: Path) -> None:
    file_path = tmp_path / "missing.ini"

    with pytest.raises(FileNotFoundError, match="не найден"):
        config(str(file_path))


def test_config_without_section(tmp_path: Path) -> None:
    file_path = tmp_path / "database.ini"
    file_path.write_text("[other]\nvalue=1\n", encoding="utf-8")

    with pytest.raises(KeyError, match="postgresql"):
        config(str(file_path))
