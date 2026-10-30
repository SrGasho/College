from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union

from .node import Node


Number = Union[int, float]


@dataclass
class EvaluationResult:
    value: Number
    postorder: List[str]
    steps: List[Dict[str, Any]]


class EvaluationError(ValueError):
    def __init__(self, message: str, node_id: Optional[int] = None, steps: Optional[List[Dict[str, Any]]] = None, postorder: Optional[List[str]] = None):
        super().__init__(message)
        self.message = message
        self.node_id = node_id
        self.steps = steps or []
        self.postorder = postorder or []


def _parse_number(value: str) -> Number:
    number = float(value) if "." in value else int(value)
    return number


def _normalize_number(value: Number) -> Number:
    if isinstance(value, float) and value.is_integer():
        return int(value)
    return value


def evaluate_postorder(root: Node) -> EvaluationResult:
    steps: List[Dict[str, Any]] = []
    postorder: List[str] = []

    def visit(node: Node) -> Number:
        if not node.is_operator:
            result = _parse_number(node.value)
            postorder.append(node.value)
            steps.append({"action": "visit", "node_id": node.id, "value": node.value})
            return result

        left_result = visit(node.left)
        right_result = visit(node.right)
        postorder.append(node.value)

        if node.value == "/" and right_result == 0:
            steps.append({"action": "error", "node_id": node.id, "value": node.value, "message": "No es posible dividir entre cero."})
            raise EvaluationError("No es posible dividir entre cero.", node.id, list(steps), list(postorder))

        if node.value == "+":
            result = left_result + right_result
        elif node.value == "-":
            result = left_result - right_result
        elif node.value == "*":
            result = left_result * right_result
        else:
            result = left_result / right_result

        result = _normalize_number(result)
        steps.append({
            "action": "calculate",
            "node_id": node.id,
            "value": node.value,
            "left": _normalize_number(left_result),
            "right": _normalize_number(right_result),
            "result": result,
        })
        return result

    return EvaluationResult(_normalize_number(visit(root)), postorder, steps)
