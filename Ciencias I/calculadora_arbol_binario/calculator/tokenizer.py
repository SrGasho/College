from dataclasses import dataclass
from typing import List


class ExpressionError(ValueError):
    pass


@dataclass(frozen=True)
class Token:
    type: str
    value: str
    position: int


def _starts_number(expression: str, position: int) -> bool:
    if position >= len(expression):
        return False
    character = expression[position]
    if character.isdigit():
        return True
    return character == "." and position + 1 < len(expression) and expression[position + 1].isdigit()


def tokenize(expression: str) -> List[Token]:
    if not isinstance(expression, str) or not expression.strip():
        raise ExpressionError("La expresión no puede estar vacía.")

    tokens: List[Token] = []
    position = 0
    previous_type = None

    while position < len(expression):
        character = expression[position]

        if character.isspace():
            position += 1
            continue

        if character in "+-" and previous_type in (None, "operator", "lparen") and _starts_number(expression, position + 1):
            start = position
            position += 1
            number_start = position
            dot_count = 0
            while position < len(expression) and (expression[position].isdigit() or expression[position] == "."):
                if expression[position] == ".":
                    dot_count += 1
                position += 1
            if dot_count > 1 or number_start == position:
                raise ExpressionError(f"Número inválido en la posición {start}.")
            token = Token("number", expression[start:position], start)
            tokens.append(token)
            previous_type = token.type
            continue

        if character.isdigit() or character == ".":
            start = position
            dot_count = 0
            digit_count = 0
            while position < len(expression) and (expression[position].isdigit() or expression[position] == "."):
                if expression[position] == ".":
                    dot_count += 1
                else:
                    digit_count += 1
                position += 1
            if dot_count > 1 or digit_count == 0:
                raise ExpressionError(f"Número inválido en la posición {start}.")
            token = Token("number", expression[start:position], start)
            tokens.append(token)
            previous_type = token.type
            continue

        if character in "+-*/":
            token = Token("operator", character, position)
            tokens.append(token)
            previous_type = token.type
            position += 1
            continue

        if character == "(":
            token = Token("lparen", character, position)
            tokens.append(token)
            previous_type = token.type
            position += 1
            continue

        if character == ")":
            token = Token("rparen", character, position)
            tokens.append(token)
            previous_type = token.type
            position += 1
            continue

        raise ExpressionError(f"Carácter no permitido: '{character}'.")

    return tokens
