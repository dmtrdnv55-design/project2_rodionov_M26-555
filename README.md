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

## Демонстрация

[![asciinema](https://asciinema.org/a/LhCkadYDUDFjQf9d.svg)](https://asciinema.org/a/LhCkadYDUDFjQf9d)

## CRUD-операции

Пример работы с записями:

```text
create_table users name:str age:int is_active:bool
insert into users values ("Alex", 30, true)
select from users
select from users where age = 30
update users set age = 31 where name = "Alex"
delete from users where name = "Alex"
info users
```

- `insert` — добавление записи. ID создаётся автоматически.
- `select` — просмотр всех записей или выборка по условию.
- `update` — обновление записей по условию.
- `delete` — удаление записей по условию.
- `info` — структура таблицы и количество записей.

Поддерживаются типы `int`, `str`, `bool`.
Строковые значения указываются в кавычках, логические — `true` или `false`.
Все поля обязательны.

Структура таблиц хранится в `db_meta.json`, записи — в `data/<имя_таблицы>.json`.
Данные сохраняются между запусками программы.

### Демонстрация CRUD-операций

[![asciicast](https://asciinema.org/a/ci9ljTdqaFUsaAqw.svg)](https://asciinema.org/a/ci9ljTdqaFUsaAqw)

## Декораторы и кэширование

- `handle_db_errors` обрабатывает ошибки валидации, отсутствующих ключей и файлов.
- `confirm_action` запрашивает подтверждение перед удалением таблиц и записей. Для подтверждения нужно ввести `y`.
- `log_time` выводит время выполнения `insert` и `select`.
- `create_cacher` создаёт кэш с помощью замыкания. Повторные одинаковые запросы `select` используют сохранённый результат фильтрации.
- После успешного изменения данных или структуры таблиц кэш сбрасывается.

Кэш действует в пределах текущего запуска программы.

### Финальная демонстрация

[![asciicast](https://asciinema.org/a/H9E3NeDI2MCf7vSS.svg)](https://asciinema.org/a/H9E3NeDI2MCf7vSS)