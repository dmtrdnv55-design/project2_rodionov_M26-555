def parse_value(text):
    """Преобразует текст в строку, целое число или логическое значение."""
    text = text.strip()
    if len(text) >= 2 and text[0] == text[-1] and text[0] in ('"', "'"):
        return text[1:-1]
    if text.lower() in ("true", "false"):
        return text.lower() == "true"
    try:
        return int(text)
    except ValueError:
        raise ValueError(
            f"Некорректное значение: {text}. Строки должны быть в кавычках."
        )


def parse_condition(text):
    """Разбирает условие вида «столбец = значение» в словарь."""
    parts = text.split("=", 1)
    if len(parts) != 2:
        raise ValueError("Условие должно иметь вид: столбец = значение")
    column_name = parts[0].strip()
    if column_name == "":
        raise ValueError("Название столбца не может быть пустым")
    value = parse_value(parts[1])
    return {column_name: value}


def parse_values(text):
    """Разбирает значения в скобках и отклоняет пустые элементы."""
    text = text.strip()
    if not text.startswith("(") or not text.endswith(")"):
        raise ValueError("Текст должен находиться в круглых скобках")

    parts = split_outside_quotes(text[1:-1], ",")
    if any(not part.strip() for part in parts):
        raise ValueError("Между запятыми должны быть значения")

    return [parse_value(part) for part in parts]


def split_outside_quotes(text, separator):
    """Разделяет текст по разделителю вне кавычек."""
    parts = []
    quote = None
    escaped = False
    start = 0
    index = 0

    while index < len(text):
        char = text[index]

        if quote is not None:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote:
                quote = None
        elif char in ('"', "'"):
            quote = char
        elif text.startswith(separator, index):
            parts.append(text[start:index])
            index += len(separator)
            start = index
            continue

        index += 1

    if quote is not None:
        raise ValueError("Не закрыты кавычки")

    parts.append(text[start:])
    return parts
