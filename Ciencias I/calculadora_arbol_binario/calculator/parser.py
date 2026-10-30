from typing import List, Tuple

from .node import Node
from .tokenizer import ExpressionError, Token, tokenize


_PRECEDENCE = {"+": 1, "-": 1, "*": 2, "/": 2}


def _to_postfix(tokens: List[Token]) -> List[Token]:
    output: List[Token] = []
    operators: List[Token] = []
    expects_operand = True

    for token in tokens:
        if token.type == "number":
            if not expects_operand:
                raise ExpressionError(f"Falta un operador antes de '{token.value}'.")
            output.append(token)
            expects_operand = False
            continue

        if token.type == "lparen":
            if not expects_operand:
                raise ExpressionError("Falta un operador antes del paréntesis de apertura.")
            operators.append(token)
            expects_operand = True
            continue

        if token.type == "rparen":
            if expects_operand:
                raise ExpressionError("El paréntesis contiene una operación incompleta.")
            while operators and operators[-1].type != "lparen":
                output.append(operators.pop())
            if not operators:
                raise ExpressionError("Hay un paréntesis de cierre sin pareja.")
            operators.pop()
            expects_operand = False
            continue

        if token.type == "operator":
            if expects_operand:
                raise ExpressionError(f"Falta un operando antes de '{token.value}'.")
            while operators and operators[-1].type == "operator" and _PRECEDENCE[operators[-1].value] >= _PRECEDENCE[token.value]:
                output.append(operators.pop())
            operators.append(token)
            expects_operand = True
            continue

        raise ExpressionError("Se encontró un elemento desconocido.")

    if expects_operand:
        raise ExpressionError("La expresión termina antes de completar una operación.")

    while operators:
        operator = operators.pop()
        if operator.type == "lparen":
            raise ExpressionError("Hay un paréntesis de apertura sin pareja.")
        output.append(operator)

    return output


def _build_tree(postfix: List[Token]) -> Node:
    stack: List[Node] = []
    next_id = 1

    for token in postfix:
        if token.type == "number":
            stack.append(Node(token.value, id=next_id))
            next_id += 1
            continue

        if len(stack) < 2:
            raise ExpressionError("La expresión no tiene suficientes operandos.")
        right = stack.pop()
        left = stack.pop()
        stack.append(Node(token.value, left=left, right=right, id=next_id))
        next_id += 1

    if len(stack) != 1:
        raise ExpressionError("La expresión no se pudo convertir en un árbol válido.")

    return stack[0]


def build_expression_tree(expression: str) -> Tuple[Node, List[str]]:
    tokens = tokenize(expression)
    postfix = _to_postfix(tokens)
    root = _build_tree(postfix)
    return root, [token.value for token in postfix]
