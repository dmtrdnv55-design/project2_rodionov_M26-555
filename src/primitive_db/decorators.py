import time
from functools import wraps


def handle_db_errors(func):
    """Оборачивает функцию обработчиком ошибок базы данных."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as error:
            print(f"Ошибка валидации: {error}")
        except KeyError as error:
            print(f"Таблица или столбец {error} не найден")
        except FileNotFoundError:
            print("Файл данных не найден")

    return wrapper


def confirm_action(action_name):
    """Создаёт декоратор подтверждения указанного действия."""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            answer = input(f'Вы уверены, что хотите выполнить "{action_name}"? [y/n]: ')
            if answer.strip().lower() != "y":
                print("Операция отменена")
                return
            return func(*args, **kwargs)

        return wrapper

    return decorator


def log_time(func):
    """Создаёт обёртку для вывода времени выполнения функции."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.monotonic()
        result = func(*args, **kwargs)
        elapsed = time.monotonic() - start
        print(f"Функция {func.__name__} выполнилась за {elapsed:.3f} секунд.")
        return result

    return wrapper
