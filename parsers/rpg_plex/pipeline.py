from __future__ import annotations

from pathlib import Path

from .analyzers import business_rules, control_flow, io_operations, plex_constructs, report_templates
from .ast.nodes import ProgramNode, ProcedureNode
from .lexer.base_lexer import lex_source
from .lexer.token_types import TokenType
from .output.serializer import create_empty_report
from .parser.directive_parser import parse_directive
from .parser.free_parser import parse_free_statement
from .parser.spec_parser import parse_spec_line


def _build_program(nodes):
    return ProgramNode(line=1, nodes=nodes)


def parse_text(text: str, source_file: str = "<memory>"):
    lines = text.splitlines(keepends=True)
    format_mode, tokens = lex_source(lines)

    parse_errors: list[str] = []
    nodes = []

    for token in tokens:
        try:
            if token.type == TokenType.DIRECTIVE:
                nodes.append(parse_directive(token))
            elif token.type == TokenType.FREE_STATEMENT:
                nodes.append(parse_free_statement(token))
            elif token.type == TokenType.SPEC_LINE:
                nodes.append(parse_spec_line(token))
        except Exception as exc:  # pragma: no cover - defensive parse collection
            parse_errors.append(f"line {token.line}: {exc}")

    program = _build_program(nodes)
    report = create_empty_report(
        source_file=source_file,
        format_mode=format_mode.value,
        line_count=len(lines),
        parse_errors=parse_errors,
    )

    report["summary"]["procedure_count"] = sum(1 for n in program.nodes if isinstance(n, ProcedureNode))

    control_flow.analyze(program, report)
    report_templates.analyze(program, report)
    io_operations.analyze(program, report)
    business_rules.analyze(program, report)
    plex_constructs.analyze(program, report)

    return report


def parse_file(path: str | Path):
    file_path = Path(path)
    text = file_path.read_text(encoding="utf-8")
    return parse_text(text, source_file=str(file_path))
