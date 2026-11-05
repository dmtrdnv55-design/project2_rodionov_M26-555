import shlex


def parse_value(text):
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
    parts = text.split("=", 1)
    if len(parts) != 2:
        raise ValueError("Условие должно иметь вид: столбец = значение")
    column_name = parts[0].strip()
    if column_name == "":
        raise ValueError("Название столбца не может быть пустым")
    value = parse_value(parts[1])
    return {column_name: value}


def parse_values(text):
    text = text.strip()
    if not text.startswith("(") or not text.endswith(")"):
        raise ValueError("Текст должен находиться в круглых скобках")
    text = text[1:-1]
    lexer = shlex.shlex(text, posix=False)
    lexer.whitespace = ", \t\r\n"
    lexer.whitespace_split = True
    lexer.commenters = ""

    return [parse_value(part) for part in lexer]
