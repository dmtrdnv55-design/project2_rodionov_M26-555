# Primitive DB

Учебная база данных с консольным интерфейсом.

## Запуск проекта

Требуются Python 3.12 или новее и uv.

```bash
uv sync
uv run database
```

## Управление таблицами

Поддерживаемые типы столбцов: `int`, `str`, `bool`.
Столбец `ID:int` добавляется автоматически, если не указан.

| Команда | Описание |
|---|---|
| `create_table <имя> <столбец:тип> ...` | Создать таблицу |
| `drop_table <имя>` | Удалить таблицу |
| `list_tables` | Показать список таблиц |
| `help` | Показать справку |
| `exit` | Завершить программу |

Пример команд после запуска:

```text
create_table users name:str age:int is_active:bool
list_tables
drop_table users
exit
```

Структуры таблиц сохраняются в файле `db_meta.json`
в текущей рабочей папке и доступны после перезапуска.

## Проверка кода

```bash
uv run ruff check .
uv run ruff format --check .
```