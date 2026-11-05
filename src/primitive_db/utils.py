import json
import os

from .constants import DATA_DIR


def load_metadata(filepath):
    """Загружает структуру таблиц или возвращает пустой словарь."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            metadata = json.load(f)
    except FileNotFoundError:
        metadata = {}
    return metadata


def save_metadata(filepath, data):
    """Сохраняет структуру таблиц в JSON-файл."""
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def load_table_data(table_name):
    """Загружает записи таблицы или возвращает пустой список."""
    filepath = os.path.join(DATA_DIR, f"{table_name}.json")
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            table_data = json.load(f)
    except FileNotFoundError:
        table_data = []
    return table_data


def save_table_data(table_name, data):
    """Сохраняет записи таблицы в JSON-файл."""
    os.makedirs(DATA_DIR, exist_ok=True)
    filepath = os.path.join(DATA_DIR, f"{table_name}.json")
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def create_cacher():
    """Создаёт функцию с кэшем результатов по ключу."""
    cache = {}

    def cache_result(key, value_func):
        """Возвращает результат из кэша или вычисляет и сохраняет его."""
        if key in cache:
            return cache[key]
        else:
            cache[key] = value_func()
            return cache[key]

    return cache_result


def delete_table_data(table_name):
    """Удаляет файл записей таблицы, если он существует."""
    filepath = os.path.join(DATA_DIR, f"{table_name}.json")
    try:
        os.remove(filepath)
    except FileNotFoundError:
        pass
