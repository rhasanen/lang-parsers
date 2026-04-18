from __future__ import annotations

import re

from parsers.rpg_plex.ast.nodes import EvalNode, GenericStatementNode, IfNode, MonitorNode


INDICATOR_RE = re.compile(r"\*IN\d{2}|\*INLR", re.IGNORECASE)


def _validation_pattern(text: str) -> str | None:
    upper = text.upper()
    if "*BLANK" in upper or "*ZEROS" in upper:
        return "REQUIRED_FIELD"
    if " OR " in upper and ("<" in upper and ">" in upper):
        return "RANGE_CHECK"
    if "%FOUND" in upper:
        return "LOOKUP_VALIDATE"
    return None


def analyze(program, report):
    assignments = []
    monitor_blocks = []
    indicator_usage: dict[str, dict[str, list[int]]] = {}
    validation_patterns = []

    for node in program.nodes:
        if isinstance(node, EvalNode):
            assignments.append(
                {
                    "line": node.line,
                    "target": node.target,
                    "expression": node.expression,
                }
            )

        if isinstance(node, MonitorNode):
            monitor_blocks.append(
                {
                    "line": node.line,
                    "has_on_error": node.has_on_error,
                    "empty_on_error": not node.has_on_error,
                }
            )

        text = getattr(node, "text", "")
        indicators = {i.upper() for i in INDICATOR_RE.findall(text)}
        for indicator in indicators:
            usage = indicator_usage.setdefault(indicator, {"set": [], "tested": []})
            if "=" in text:
                usage["set"].append(node.line)
            if isinstance(node, IfNode) or (isinstance(node, GenericStatementNode) and (node.opcode or "").upper() == "IF"):
                usage["tested"].append(node.line)

        pattern = _validation_pattern(text)
        if pattern and isinstance(node, (IfNode, GenericStatementNode)):
            validation_patterns.append({"line": node.line, "pattern": pattern, "text": text})

    report["business_rules"] = {
        "assignments": assignments,
        "monitor_blocks": monitor_blocks,
        "indicator_usage": indicator_usage,
        "validation_patterns": validation_patterns,
        "global_fields": [],
    }
