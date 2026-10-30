import shlex

import prompt

from primitive_db.core import create_table, drop_table, list_tables
from primitive_db.utils import load_metadata, save_metadata


def show_help():
    print("***Процесс работы с таблицей***")
    print("Функции:")
    print("<command> exit - выйти из программы")
    print("<command> help - справочная информация")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> create_table <имя_таблицы> <столбец:тип> ... - создать таблицу")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")


def run():
    show_help()
    while True:
        metadata = load_metadata("db_meta.json")
        command = prompt.string("Введите команду: ")
        try:
            parts = shlex.split(command)
        except ValueError:
            print("Неверный формат: проверьте кавычки")
            continue

        if not parts:
            continue
        if parts[0] in ("help", "exit", "list_tables") and len(parts) != 1:
            print(f"Команда {parts[0]} не принимает аргументы")
            continue

        if parts[0] == "help":
            show_help()
        elif parts[0] == "exit":
            break
        elif parts[0] == "list_tables":
            list_tables(metadata)
        elif parts[0] == "create_table":
            if len(parts) < 3:
                print("Формат: create_table <имя_таблицы> <столбец:тип> ...")
                continue
            table_name = parts[1]
            columns = parts[2:]
            count_before = len(metadata)
            create_table(metadata, table_name, columns)
            if len(metadata) > count_before:
                save_metadata("db_meta.json", metadata)
        elif parts[0] == "drop_table":
            if len(parts) != 2:
                print("Формат: drop_table <имя_таблицы>")
                continue
            table_name = parts[1]
            count_before = len(metadata)
            drop_table(metadata, table_name)
            if len(metadata) < count_before:
                save_metadata("db_meta.json", metadata)
        else:
            print(f"Функции {parts[0]} нет. Попробуйте снова.")
