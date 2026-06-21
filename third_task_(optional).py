import sys


def parse_log_line(line: str) -> dict:
    """
    Парсить один рядок логу та повертає словник з полями:
    date, time, level, message.

    Очікуваний формат рядка:
    2024-01-22 08:30:01 INFO User logged in successfully.
    """
    parts = line.strip().split(maxsplit=3)

    if len(parts) < 4:
        # Рядок не відповідає очікуваному формату - пропускаємо
        return {}

    date, time, level, message = parts

    return {
        "date": date,
        "time": time,
        "level": level.upper(),
        "message": message,
    }


def load_logs(file_path: str) -> list:
    """
    Завантажує лог-файл, парсить кожен рядок та повертає список
    словників з розібраними записами логу.
    """
    logs = []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                if not line.strip():
                    continue  # пропускаємо порожні рядки

                parsed_line = parse_log_line(line)
                if parsed_line:  # додаємо лише коректно розпарсені рядки
                    logs.append(parsed_line)

    except FileNotFoundError:
        print(f"Помилка: файл '{file_path}' не знайдено.")
        sys.exit(1)
    except OSError as e:
        print(f"Помилка при читанні файлу '{file_path}': {e}")
        sys.exit(1)

    return logs


def filter_logs_by_level(logs: list, level: str) -> list:
    """
    Повертає список записів логу, що відповідають вказаному рівню логування.
    Використовує функцію filter() - елемент функціонального програмування.
    """
    level = level.upper()
    return list(filter(lambda log: log.get("level") == level, logs))


def count_logs_by_level(logs: list) -> dict:
    """
    Підраховує кількість записів логу для кожного рівня логування.
    Повертає словник виду {"INFO": 4, "ERROR": 2, ...}.
    """
    counts = {}

    for log in logs:
        level = log.get("level")
        counts[level] = counts.get(level, 0) + 1

    return counts


def display_log_counts(counts: dict) -> None:
    """
    Форматує та виводить результати підрахунку записів за рівнем логування
    у вигляді таблиці.
    """
    print(f"{'Рівень логування':<17} | {'Кількість'}")
    print(f"{'-' * 17}|{'-' * 10}")

    # Сортуємо рівні за спаданням кількості записів
    for level, count in sorted(counts.items(), key=lambda item: -item[1]):
        print(f"{level:<17} | {count}")


def display_log_details(logs: list, level: str) -> None:
    """
    Виводить детальну інформацію про всі записи вказаного рівня логування.
    """
    filtered_logs = filter_logs_by_level(logs, level)

    print(f"\nДеталі логів для рівня '{level.upper()}':")
    for log in filtered_logs:
        print(f"{log['date']} {log['time']} - {log['message']}")


def main():
    # Перевірка наявності обов'язкового аргументу - шляху до файлу логів
    if len(sys.argv) < 2:
        print("Використання: python main.py <шлях_до_файлу_логів> [рівень]")
        sys.exit(1)

    file_path = sys.argv[1]
    level_filter = sys.argv[2] if len(sys.argv) > 2 else None

    logs = load_logs(file_path)

    if not logs:
        print("Не знайдено жодного коректного запису логу у файлі.")
        sys.exit(1)

    counts = count_logs_by_level(logs)
    display_log_counts(counts)

    if level_filter:
        display_log_details(logs, level_filter)


if __name__ == "__main__":
    main()
