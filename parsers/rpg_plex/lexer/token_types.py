from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class FormatMode(str, Enum):
    FIXED = "FIXED"
    FREE = "FREE"
    MIXED = "MIXED"


class TokenType(str, Enum):
    SPEC_LINE = "SPEC_LINE"
    FREE_STATEMENT = "FREE_STATEMENT"
    DIRECTIVE = "DIRECTIVE"
    COMMENT = "COMMENT"
    UNKNOWN = "UNKNOWN"


@dataclass(slots=True)
class Token:
    type: TokenType
    value: str
    line: int
    column: int = 1
    spec_type: str | None = None
    data: dict[str, Any] = field(default_factory=dict)
