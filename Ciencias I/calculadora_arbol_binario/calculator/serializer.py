from typing import Any, Dict, Optional

from .node import Node


def tree_to_dict(node: Optional[Node]) -> Optional[Dict[str, Any]]:
    if node is None:
        return None
    return {
        "id": node.id,
        "value": node.value,
        "type": "operator" if node.is_operator else "number",
        "left": tree_to_dict(node.left),
        "right": tree_to_dict(node.right),
    }
