from __future__ import annotations

from .fixed_format import tokenize_fixed_line
from .free_format import tokenize_free_line
from .token_types import FormatMode, Token, TokenType


DIRECTIVES = ("/COPY", "/FREE", "/END-FREE", "/IF", "/EJECT", "/ELSE", "/ENDIF")


def detect_format_mode(lines: list[str]) -> FormatMode:
    has_free_markers = any("/FREE" in line.upper() for line in lines)
    has_end_free_markers = any("/END-FREE" in line.upper() for line in lines)
    has_free_header = any(line.strip().lower().startswith("**free") for line in lines[:3])

    if has_free_header and not has_free_markers:
        return FormatMode.FREE
    if has_free_markers and has_end_free_markers:
        return FormatMode.MIXED
    if has_free_markers:
        return FormatMode.FREE
    return FormatMode.FIXED


def lex_source(lines: list[str]) -> tuple[FormatMode, list[Token]]:
    detected_mode = detect_format_mode(lines)
    mode = FormatMode.FIXED if detected_mode == FormatMode.MIXED else detected_mode

    tokens: list[Token] = []
    for line_number, line in enumerate(lines, start=1):
        stripped = line.strip()
        upper = stripped.upper()

        if any(upper.startswith(d) for d in DIRECTIVES):
            tokens.append(Token(type=TokenType.DIRECTIVE, value=stripped, line=line_number, column=1))
            if upper.startswith("/FREE"):
                mode = FormatMode.FREE
            elif upper.startswith("/END-FREE"):
                mode = FormatMode.FIXED
            continue

        if mode == FormatMode.FREE:
            tokens.extend(tokenize_free_line(line, line_number))
        else:
            token = tokenize_fixed_line(line, line_number)
            if token is not None:
                tokens.append(token)

    return detected_mode, tokens
