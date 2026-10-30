def create_table(metadata, table_name, columns):
    if table_name in metadata:
        print("Таблица уже существует")
        return metadata
    column_names = set()
    for item in columns:
        splitted_columns = item.split(":")

        if len(splitted_columns) != 2:
            print(f"Некорректное значение: {item}. Попробуйте снова.")
            return metadata

        column_name = splitted_columns[0]

        if column_name == "":
            print("Название колонки не может быть пустым")
            return metadata

        if column_name in column_names:
            print("Название колонки повторяется")
            return metadata
        column_names.add(column_name)

        if column_name == "ID":
            if splitted_columns[1] != "int":
                print('Неверный тип данных для колонки "ID"')
                return metadata
            continue

        if splitted_columns[1] not in ("int", "str", "bool"):
            print(f"Некорректное значение: {splitted_columns[1]}. Попробуйте снова.")
            return metadata
    table_columns = ["ID:int"] + [item for item in columns if item != "ID:int"]

    metadata[table_name] = table_columns
    print(
        f'Таблица "{table_name}" успешно создана со столбцами: '
        f"{', '.join(table_columns)}"
    )
    return metadata


def drop_table(metadata, table_name):
    if table_name in metadata:
        del metadata[table_name]
        print(f'Таблица "{table_name}" успешно удалена.')
    else:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
    return metadata


def list_tables(metadata):
    if metadata == {}:
        print("Таблиц нет")
        return
    for table_name in metadata:
        print(f"- {table_name}")
