from dataclasses import dataclass
from typing import Optional


OPERATORS = {"+", "-", "*", "/"}


@dataclass
class Node:
    value: str
    left: Optional["Node"] = None
    right: Optional["Node"] = None
    id: int = 0

    @property
    def is_operator(self) -> bool:
        return self.value in OPERATORS
