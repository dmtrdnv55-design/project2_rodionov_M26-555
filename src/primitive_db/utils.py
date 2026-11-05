import json
import os


def load_metadata(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            metadata = json.load(f)
    except FileNotFoundError:
        metadata = {}
    return metadata


def save_metadata(filepath, data):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def load_table_data(table_name):
    try:
        with open(f"data/{table_name}.json", "r", encoding="utf-8") as f:
            table_data = json.load(f)
    except FileNotFoundError:
        table_data = []
    return table_data


def save_table_data(table_name, data):
    os.makedirs("data", exist_ok=True)
    with open(f"data/{table_name}.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def create_cacher():
    cache = {}

    def cache_result(key, value_func):
        if key in cache:
            return cache[key]
        else:
            cache[key] = value_func()
            return cache[key]

    return cache_result
