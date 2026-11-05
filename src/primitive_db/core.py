from .constants import VALID_TYPES
from .decorators import confirm_action, handle_db_errors, log_time
from .utils import delete_table_data, load_table_data


@handle_db_errors
def create_table(metadata, table_name, columns):
    """Проверяет столбцы и добавляет таблицу в метаданные."""
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


@handle_db_errors
@confirm_action("удаление таблицы")
def drop_table(metadata, table_name):
    """Удаляет файл данных таблицы и её описание из метаданных."""
    if table_name not in metadata:
        raise ValueError(f'Таблица "{table_name}" не существует')

    delete_table_data(table_name)
    del metadata[table_name]
    print(f'Таблица "{table_name}" успешно удалена.')
    return metadata


def list_tables(metadata):
    """Выводит имена существующих таблиц."""
    if metadata == {}:
        print("Таблиц нет")
        return
    for table_name in metadata:
        print(f"- {table_name}")


@handle_db_errors
@log_time
def insert(metadata, table_name, values):
    """Проверяет значения и добавляет запись с новым ID."""
    if table_name not in metadata:
        raise ValueError(f"Таблица {table_name} не найдена")

    if len(values) != len(metadata[table_name]) - 1:
        raise ValueError(
            f"Количество значений не соответствует структуре таблицы {table_name}"
        )
    for column, value in zip(metadata[table_name][1:], values):
        column_name, column_type = column.split(":")
        if type(value) is not VALID_TYPES[column_type]:
            raise ValueError(
                f"Для столбца {column_name} требуется тип данных {column_type}"
            )
    table_data = load_table_data(table_name)
    new_id = max((row["ID"] for row in table_data), default=0) + 1
    new_row = {"ID": new_id}
    for column, value in zip(metadata[table_name][1:], values):
        column_name, column_type = column.split(":")
        new_row[column_name] = value
    table_data.append(new_row)
    return table_data


@handle_db_errors
@log_time
def select(table_data, where_clause=None):
    """Возвращает все записи или записи, подходящие под условие."""
    if where_clause is None:
        return table_data
    result = []
    for row in table_data:
        matches = True
        for column_name, expected_value in where_clause.items():
            if row[column_name] != expected_value:
                matches = False
                break

        if matches:
            result.append(row)

    return result


@handle_db_errors
def update(table_data, set_clause, where_clause):
    """Обновляет поля записей, подходящих под условие."""
    selected_rows = select(table_data, where_clause)
    if selected_rows is None:
        return
    for row in selected_rows:
        for column_name, new_value in set_clause.items():
            row[column_name] = new_value
    return table_data


@handle_db_errors
@confirm_action("удаление записей")
def delete(table_data, where_clause):
    """Возвращает список записей без выбранных для удаления."""
    if not where_clause:
        raise ValueError("Для удаления записей необходимо непустое условие where")
    selected_rows = select(table_data, where_clause)
    if selected_rows is None:
        return
    result = [row for row in table_data if row not in selected_rows]
    return result


def validate_clause(metadata, table_name, clause):
    """Проверяет существование столбцов и типы значений условия."""
    column_types = dict(column.split(":") for column in metadata[table_name])
    for column_name, value in clause.items():
        if column_name not in column_types:
            raise ValueError(f"Столбец {column_name} не найден")
        column_type = column_types[column_name]
        if type(value) is not VALID_TYPES[column_type]:
            raise ValueError(
                f"Для столбца {column_name} требуется тип данных {column_type}"
            )
