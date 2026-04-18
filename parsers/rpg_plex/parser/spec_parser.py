from __future__ import annotations

from parsers.rpg_plex.ast.nodes import (
    ChainNode,
    DowNode,
    EvalNode,
    ExceptNode,
    ExfmtNode,
    ExsrNode,
    FileDeclarationNode,
    ForNode,
    GenericSpecNode,
    GenericStatementNode,
    GotoNode,
    IfNode,
    OFieldNode,
    ProcedureNode,
    ReadNode,
    SelectNode,
    SetgtNode,
    SetllNode,
    SubroutineNode,
    TagNode,
    WriteNode,
)
from parsers.rpg_plex.lexer.token_types import Token


IO_READ_OPS = {"READ", "READP", "READE", "READPE"}
IO_WRITE_OPS = {"WRITE", "UPDATE", "DELETE"}


def parse_spec_line(token: Token):
    spec_type = (token.spec_type or "").upper()
    data = token.data

    if spec_type == "F":
        return FileDeclarationNode(
            line=token.line,
            name=data.get("file", ""),
            io_mode=data.get("io_mode", ""),
            device=data.get("device", ""),
        )

    if spec_type == "O":
        return OFieldNode(
            line=token.line,
            file_name=data.get("file", ""),
            line_type=data.get("line_type", ""),
            field_name=data.get("field_name", ""),
            conditioning=data.get("conditioning", ""),
        )

    if spec_type == "P":
        raw = token.value
        name = raw[6:21].strip() if len(raw) > 21 else ""
        boundary = raw[23:24].strip() if len(raw) > 23 else "B"
        return ProcedureNode(line=token.line, name=name, boundary=boundary or "B")

    if spec_type == "C":
        factor1 = data.get("factor1", "")
        opcode = data.get("opcode", "").upper()
        factor2 = data.get("factor2", "")
        result = data.get("result", "")
        text = token.value

        if opcode == "IF":
            return IfNode(line=token.line, text=text, condition=factor2 or result)
        if opcode == "DOW":
            return DowNode(line=token.line, text=text, condition=factor2 or result)
        if opcode == "DOU":
            return DowNode(line=token.line, text=text, condition=factor2 or result)
        if opcode == "FOR":
            return ForNode(line=token.line, text=text, condition=factor2 or result)
        if opcode == "SELECT":
            return SelectNode(line=token.line, text=text, selector=factor2)
        if opcode == "EXSR":
            return ExsrNode(line=token.line, text=text, subroutine=factor2 or result)
        if opcode == "BEGSR":
            return SubroutineNode(line=token.line, name=factor2 or result)
        if opcode == "TAG":
            return TagNode(line=token.line, text=text, name=result or factor2)
        if opcode == "GOTO":
            return GotoNode(line=token.line, text=text, target=result or factor2)
        if opcode in IO_READ_OPS:
            return ReadNode(line=token.line, text=text, file_name=factor2 or result)
        if opcode in IO_WRITE_OPS:
            return WriteNode(line=token.line, text=text, file_name=factor2 or result)
        if opcode == "CHAIN":
            return ChainNode(line=token.line, text=text, file_name=factor2)
        if opcode == "SETLL":
            return SetllNode(line=token.line, text=text, file_name=factor2)
        if opcode == "SETGT":
            return SetgtNode(line=token.line, text=text, file_name=factor2)
        if opcode == "EXFMT":
            return ExfmtNode(line=token.line, text=text, record_name=factor2 or result)
        if opcode in {"EXCEPT", "EXCPT"}:
            return ExceptNode(line=token.line, text=text, record_name=factor2 or result)
        if opcode in {"EVAL", "EVALR"}:
            return EvalNode(line=token.line, text=text, target=result, expression=factor2)

        return GenericStatementNode(
            line=token.line,
            text=text,
            opcode=opcode,
            factor1=factor1,
            factor2=factor2,
            result=result,
        )

    return GenericSpecNode(line=token.line, spec_type=spec_type, raw=token.value, data=data)
