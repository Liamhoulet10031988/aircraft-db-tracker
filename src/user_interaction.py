from typing import Any

from src.db_manager import DBManager


def print_rows(rows: list[tuple[Any, ...]]) -> None:
    """Печатает строки результата SQL в консоль."""
    if not rows:
        print("Данные не найдены")
        return

    for row in rows:
        values = [str(value) for value in row]
        print(" | ".join(values))


def user_interaction(manager: DBManager) -> None:
    """Запускает меню для работы с запросами DBManager."""
    while True:
        print("\nВыберите действие:")
        print("1 - страны и количество самолетов")
        print("2 - все самолеты")
        print("3 - средняя скорость")
        print("4 - самолеты со скоростью выше средней")
        print("5 - поиск по позывному")
        print("0 - завершить программу")

        choice = input("Введите номер: ").strip()

        if choice == "1":
            rows = manager.get_countries_and_aeroplanes_count()
            print_rows(rows)
        elif choice == "2":
            rows = manager.get_all_aeroplanes()
            print_rows(rows)
        elif choice == "3":
            average_speed = manager.get_avg_speed()
            print(f"Средняя скорость: {average_speed} м/с")
        elif choice == "4":
            rows = manager.get_aeroplanes_with_higher_speed()
            print_rows(rows)
        elif choice == "5":
            keyword = input("Введите часть позывного: ").strip()
            rows = manager.get_aeroplanes_with_keyword(keyword)
            print_rows(rows)
        elif choice == "0":
            print("Работа программы завершена")
            break
        else:
            print("Неизвестная команда")
