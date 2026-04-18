from __future__ import annotations

from .nodes import Node


class NodeVisitor:
    def visit(self, node: Node):
        method_name = f"visit_{node.__class__.__name__}"
        method = getattr(self, method_name, self.generic_visit)
        return method(node)

    def generic_visit(self, node: Node):
        return node
