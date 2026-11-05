import shlex

import prompt
from prettytable import PrettyTable

from primitive_db.core import (
    create_table,
    delete,
    drop_table,
    insert,
    list_tables,
    select,
    update,
    validate_clause,
)
from primitive_db.utils import (
    load_metadata,
    load_table_data,
    save_metadata,
    save_table_data,
)

from .parser import parse_condition, parse_values


def show_help():
    print("***Процесс работы с таблицей***")
    print("Функции:")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> create_table <имя_таблицы> <столбец:тип> ... - создать таблицу")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")
    print(
        "<command> insert into <имя_таблицы>" \
        " values (<значение1>, <значение2>, ...) — добавить запись"
    )
    print("<command> select from <имя_таблицы> — показать все записи")
    print(
        "<command> select from <имя_таблицы>" \
        " where <столбец> = <значение> — найти записи"
    )
    print(
        "<command> update <имя_таблицы> set <столбец> = <значение>" \
        " where <столбец> = <значение> — обновить записи"
    )
    print(
        "<command> delete from <имя_таблицы>" \
        " where <столбец> = <значение> — удалить записи"
    )
    print("<command> info <имя_таблицы> — показать структуру и количество записей")
    print("<command> exit - выйти из программы")
    print("<command> help - справочная информация")
    print('Типы значений: числа — 30, строки — "Alex", логические — true или false.')
    print("ID создаётся автоматически, передавать его в insert не нужно.")


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
        elif parts[0] == "insert":
            insert_parts = command.split(maxsplit=4)
            if (
                len(insert_parts) != 5
                or insert_parts[1] != "into"
                or insert_parts[3] != "values"
            ):
                print(
                    "Формат: insert into <имя_таблицы>" \
                    " values (<значение1>, <значение2>, ...)"
                )
                continue
            table_name = insert_parts[2]
            try:
                values = parse_values(insert_parts[4])
            except ValueError as error:
                print(error)
                continue
            table_data = insert(metadata, table_name, values)
            if table_data is not None:
                save_table_data(table_name, table_data)
                print(f'Запись успешно добавлена в таблицу "{table_name}"')
        elif parts[0] == "select":
            select_parts = command.split(maxsplit=4)
            if len(select_parts) not in (3, 5) or select_parts[1] != "from":
                print(
                    "Формат: select from <имя_таблицы> [where <столбец> = <значение>]"
                )
                continue
            if len(select_parts) == 5 and select_parts[3] != "where":
                print(
                    "Формат: select from <имя_таблицы> [where <столбец> = <значение>]"
                )
                continue
            where_clause = None
            if len(select_parts) == 5:
                try:
                    where_clause = parse_condition(select_parts[4])
                except ValueError as error:
                    print(error)
                    continue
            if where_clause is not None:
                try:
                    validate_clause(metadata, table_name, where_clause)
                except ValueError as error:
                    print(error)
                    continue
            table_name = parts[2]
            if table_name not in metadata:
                print(f"Таблица {table_name} не найдена")
                continue
            table_data = load_table_data(table_name)
            selected_rows = select(table_data, where_clause)
            table = PrettyTable()
            column_names = [column.split(":")[0] for column in metadata[table_name]]
            table.field_names = column_names
            for row in selected_rows:
                table.add_row([row[column] for column in column_names])
            print(table)
            select_parts = command.split(maxsplit=4)
        elif parts[0] == "update":
            update_parts = command.split(maxsplit=3)
            if len(update_parts) != 4 or update_parts[2] != "set":
                print(
                    "Формат: update <имя_таблицы> set <столбец1> = <новое_значение1>" \
                    " where <столбец> = <значение>"
                )
                continue
            clauses = update_parts[3].split(" where ", 1)
            if len(clauses) != 2:
                print(
                    "Формат: update <имя_таблицы> set <столбец1> = <новое_значение1>" \
                    " where <столбец> = <значение>"
                )
                continue
            try:
                set_clause = parse_condition(clauses[0])
                where_clause = parse_condition(clauses[1])
            except ValueError as error:
                print(error)
                continue
            table_name = update_parts[1]
            if table_name not in metadata:
                print(f"Таблица {table_name} не найдена")
                continue
            try:
                validate_clause(metadata, table_name, set_clause)
                validate_clause(metadata, table_name, where_clause)
            except ValueError as error:
                print(error)
                continue
            table_data = load_table_data(table_name)
            table_data = update(table_data, set_clause, where_clause)
            save_table_data(table_name, table_data)
            print(f'Обновление таблицы "{table_name}" выполнено')
        elif parts[0] == "delete":
            delete_parts = command.split(maxsplit=4)
            if (
                len(delete_parts) != 5
                or delete_parts[1] != "from"
                or delete_parts[3] != "where"
            ):
                print("Формат: delete from <имя_таблицы> where <столбец> = <значение>")
                continue
            table_name = delete_parts[2]
            if table_name not in metadata:
                print(f"Таблица {table_name} не найдена")
                continue
            try:
                where_clause = parse_condition(delete_parts[4])
                validate_clause(metadata, table_name, where_clause)
            except ValueError as error:
                print(error)
                continue
            table_data = load_table_data(table_name)
            table_data = delete(table_data, where_clause)
            save_table_data(table_name, table_data)
            print(f'Удаление записей из таблицы "{table_name}" выполнено')
        elif parts[0] == "info":
            if len(parts) != 2:
                print("Формат: info <имя_таблицы>")
                continue
            table_name = parts[1]
            if table_name not in metadata:
                print(f"Таблица {table_name} не найдена")
                continue
            table_data = load_table_data(table_name)
            print(f"Таблица: {table_name}")
            print(f"Столбцы: {', '.join(metadata[table_name])}")
            print(f"Количество записей: {len(table_data)}")
        else:
            print(f"Функции {parts[0]} нет. Попробуйте снова.")
