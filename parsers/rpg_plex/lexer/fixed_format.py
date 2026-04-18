from __future__ import annotations

from .token_types import Token, TokenType


def _slice(line: str, start: int, end: int) -> str:
    return line[start:end].rstrip("\n")


def tokenize_fixed_line(line: str, line_number: int) -> Token | None:
    raw = line.rstrip("\n")
    if not raw.strip():
        return None

    if len(raw) >= 7 and raw[6] == "*":
        return Token(type=TokenType.COMMENT, value=raw, line=line_number, column=1)

    spec_type = raw[5].upper() if len(raw) > 5 else ""
    if spec_type == "":
        return Token(type=TokenType.UNKNOWN, value=raw, line=line_number, column=1)

    data: dict[str, str] = {"raw": raw}

    if spec_type == "C":
        data.update(
            {
                "factor1": _slice(raw, 11, 25).strip(),
                "opcode": _slice(raw, 25, 35).strip().upper(),
                "factor2": _slice(raw, 35, 49).strip(),
                "result": _slice(raw, 49, 63).strip(),
                "indicators": _slice(raw, 67, 70).strip(),
            }
        )

    if spec_type == "O":
        data.update(
            {
                "file": _slice(raw, 6, 16).strip(),
                "line_type": _slice(raw, 18, 19).strip(),
                "spacing": _slice(raw, 19, 29).strip(),
                "conditioning": _slice(raw, 29, 39).strip(),
                "field_name": _slice(raw, 31, 37).strip(),
                "end_position": _slice(raw, 39, 43).strip(),
                "edit_code": _slice(raw, 43, 44).strip(),
            }
        )

    if spec_type == "F":
        data.update(
            {
                "file": _slice(raw, 6, 16).strip(),
                "io_mode": _slice(raw, 13, 17).strip(),
                "device": _slice(raw, 36, 42).strip(),
            }
        )

    if spec_type == "H":
        data["keywords"] = raw[6:].strip()

    return Token(
        type=TokenType.SPEC_LINE,
        value=raw,
        line=line_number,
        column=1,
        spec_type=spec_type,
        data=data,
    )
