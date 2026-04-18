from __future__ import annotations

from parsers.rpg_plex.ast.nodes import CompilerDirectiveNode
from parsers.rpg_plex.lexer.token_types import Token


def parse_directive(token: Token) -> CompilerDirectiveNode:
    parts = token.value.split(maxsplit=1)
    name = parts[0].upper() if parts else token.value.upper()
    args = parts[1] if len(parts) > 1 else ""
    return CompilerDirectiveNode(line=token.line, name=name, arguments=args)
