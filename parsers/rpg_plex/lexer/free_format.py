from __future__ import annotations

from .token_types import Token, TokenType


def tokenize_free_line(line: str, line_number: int) -> list[Token]:
    raw = line.rstrip("\n")
    stripped = raw.strip()
    if not stripped:
        return []
    if stripped.startswith("//"):
        return [Token(type=TokenType.COMMENT, value=raw, line=line_number)]

    statements: list[Token] = []
    segment_start = 0
    for part in raw.split(";"):
        statement = part.strip()
        if statement:
            col = max(raw.find(statement, segment_start) + 1, 1)
            statements.append(
                Token(
                    type=TokenType.FREE_STATEMENT,
                    value=statement,
                    line=line_number,
                    column=col,
                    data={"statement": statement},
                )
            )
            segment_start = col
    return statements
