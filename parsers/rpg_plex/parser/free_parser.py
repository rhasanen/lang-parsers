from __future__ import annotations

from parsers.rpg_plex.ast.nodes import (
    CallpNode,
    EvalNode,
    GenericStatementNode,
    IfNode,
    MonitorNode,
    StatementNode,
)
from parsers.rpg_plex.lexer.token_types import Token


def parse_free_statement(token: Token) -> StatementNode:
    text = token.value.strip()
    upper = text.upper()

    if upper.startswith("IF "):
        return IfNode(line=token.line, text=text, condition=text[3:].strip())
    if upper.startswith("EVAL"):
        rhs = text.split(" ", 1)[1] if " " in text else ""
        target, _, expr = rhs.partition("=")
        return EvalNode(line=token.line, text=text, target=target.strip(), expression=expr.strip())
    if upper.startswith("CALLP "):
        return CallpNode(line=token.line, text=text, procedure=text[6:].strip())
    if upper.startswith("MONITOR"):
        return MonitorNode(line=token.line, text=text, has_on_error=False)

    return GenericStatementNode(line=token.line, text=text, opcode=text.split(" ", 1)[0].upper())
