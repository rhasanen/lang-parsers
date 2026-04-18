from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class Node:
    line: int


@dataclass(slots=True)
class ProgramNode(Node):
    nodes: list[Node] = field(default_factory=list)


@dataclass(slots=True)
class SpecNode(Node):
    spec_type: str
    raw: str


@dataclass(slots=True)
class StatementNode(Node):
    text: str


@dataclass(slots=True)
class GenericSpecNode(SpecNode):
    data: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class GenericStatementNode(StatementNode):
    opcode: str | None = None
    factor1: str | None = None
    factor2: str | None = None
    result: str | None = None


@dataclass(slots=True)
class ProcedureNode(Node):
    name: str
    boundary: str = "B"


@dataclass(slots=True)
class SubroutineNode(Node):
    name: str


@dataclass(slots=True)
class IfNode(StatementNode):
    condition: str = ""


@dataclass(slots=True)
class DowNode(StatementNode):
    condition: str = ""


@dataclass(slots=True)
class DouNode(StatementNode):
    condition: str = ""


@dataclass(slots=True)
class ForNode(StatementNode):
    condition: str = ""


@dataclass(slots=True)
class SelectNode(StatementNode):
    selector: str = ""


@dataclass(slots=True)
class GotoNode(StatementNode):
    target: str = ""


@dataclass(slots=True)
class TagNode(StatementNode):
    name: str = ""


@dataclass(slots=True)
class ExsrNode(StatementNode):
    subroutine: str = ""


@dataclass(slots=True)
class IterNode(StatementNode):
    pass


@dataclass(slots=True)
class LeaveNode(StatementNode):
    pass


@dataclass(slots=True)
class OSpecGroupNode(Node):
    file_name: str


@dataclass(slots=True)
class OFieldNode(Node):
    file_name: str
    line_type: str
    field_name: str
    conditioning: str = ""


@dataclass(slots=True)
class ExceptNode(StatementNode):
    record_name: str = ""


@dataclass(slots=True)
class FileDeclarationNode(Node):
    name: str
    io_mode: str = ""
    device: str = ""


@dataclass(slots=True)
class ReadNode(StatementNode):
    file_name: str = ""


@dataclass(slots=True)
class WriteNode(StatementNode):
    file_name: str = ""


@dataclass(slots=True)
class ChainNode(StatementNode):
    file_name: str = ""


@dataclass(slots=True)
class SetllNode(StatementNode):
    file_name: str = ""


@dataclass(slots=True)
class SetgtNode(StatementNode):
    file_name: str = ""


@dataclass(slots=True)
class ExfmtNode(StatementNode):
    record_name: str = ""


@dataclass(slots=True)
class DataQueueOpNode(StatementNode):
    api_name: str = ""


@dataclass(slots=True)
class CallpNode(StatementNode):
    procedure: str = ""


@dataclass(slots=True)
class PrototypeNode(Node):
    name: str
    parameters: list[str] = field(default_factory=list)


@dataclass(slots=True)
class EvalNode(StatementNode):
    target: str = ""
    expression: str = ""


@dataclass(slots=True)
class MonitorNode(StatementNode):
    has_on_error: bool = False


@dataclass(slots=True)
class IndicatorNode(Node):
    name: str
    action: str


@dataclass(slots=True)
class ValidationPatternNode(Node):
    pattern_type: str
    detail: str


@dataclass(slots=True)
class PlexProcedureSignatureNode(Node):
    name: str


@dataclass(slots=True)
class PlexErrorHandlerNode(Node):
    name: str


@dataclass(slots=True)
class PlexCopyMemberNode(Node):
    member: str


@dataclass(slots=True)
class CompilerDirectiveNode(Node):
    name: str
    arguments: str = ""
