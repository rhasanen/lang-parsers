from __future__ import annotations

from collections import defaultdict

from parsers.rpg_plex.ast.nodes import ExceptNode, OFieldNode


def _is_plex_report_pattern(name: str) -> bool:
    if len(name) < 7:
        return False
    prefix = name[:3].upper()
    suffix = name[-1:].upper()
    return prefix == "RPT" and name[3:6].isdigit() and suffix in {"H", "D", "T"}


def analyze(program, report):
    groups: dict[str, dict] = defaultdict(lambda: {"exception_records": [], "except_invocations": [], "is_plex_report_pattern": False})

    for node in program.nodes:
        if isinstance(node, OFieldNode):
            item = groups[node.file_name or "<unknown>"]
            item["exception_records"].append(
                {
                    "line": node.line,
                    "line_type": node.line_type,
                    "field_name": node.field_name,
                    "conditioning": node.conditioning,
                }
            )
            if node.field_name:
                item["is_plex_report_pattern"] = item["is_plex_report_pattern"] or _is_plex_report_pattern(node.field_name)
        elif isinstance(node, ExceptNode):
            item = groups[node.record_name or "<unknown>"]
            item["except_invocations"].append({"line": node.line, "record": node.record_name})

    printer_files = [{"name": name, **details} for name, details in groups.items()]
    report["report_templates"] = {"printer_files": printer_files}
    report["summary"]["printer_file_count"] = len(printer_files)
