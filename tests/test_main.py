import src.main as main_module


def test_main_connects_all_parts(monkeypatch) -> None:
    calls = []

    class FakeCollector:
        """Возвращает готовый результат сбора."""

        def __init__(self, country_api, aeroplane_api) -> None:
            calls.append("collector created")

        def collect(self, country_names):
            calls.append(len(country_names))
            return []

    monkeypatch.setattr(main_module, "config", lambda: {"host": "test"})
    monkeypatch.setattr(
        main_module,
        "create_database",
        lambda name, params: calls.append("database"),
    )
    monkeypatch.setattr(
        main_module,
        "create_tables",
        lambda name, params: calls.append("tables"),
    )
    monkeypatch.setattr(main_module, "NominatimAPI", lambda: object())
    monkeypatch.setattr(main_module, "OpenSkyAPI", lambda: object())
    monkeypatch.setattr(main_module, "AircraftDataCollector", FakeCollector)
    monkeypatch.setattr(
        main_module,
        "save_data_to_database",
        lambda data, name, params: calls.append("saved"),
    )
    monkeypatch.setattr(
        main_module,
        "DBManager",
        lambda name, params: "manager",
    )
    monkeypatch.setattr(
        main_module,
        "user_interaction",
        lambda manager: calls.append(manager),
    )

    main_module.main()

    assert calls == [
        "database",
        "tables",
        "collector created",
        10,
        "saved",
        "manager",
    ]


def test_main_prints_expected_error(monkeypatch, capsys) -> None:
    def broken_config():
        raise FileNotFoundError("database.ini")

    monkeypatch.setattr(main_module, "config", broken_config)

    main_module.main()

    output = capsys.readouterr().out

    assert "Не удалось выполнить программу" in output
    assert "database.ini" in output
