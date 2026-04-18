from __future__ import annotations

from typing import Any, TypedDict


class Metadata(TypedDict):
    source_file: str
    parse_date: str
    parser_version: str
    format_mode: str
    line_count: int
    parse_errors: list[str]


class Summary(TypedDict):
    procedure_count: int
    file_declaration_count: int
    printer_file_count: int
    plex_confidence_score: float
    plex_version_hint: str
    has_cycle_remnants: bool
    total_io_operations: int
    max_control_flow_nesting_depth: int


class AnalysisReport(TypedDict):
    metadata: Metadata
    summary: Summary
    control_flows: dict[str, Any]
    report_templates: dict[str, Any]
    io_operations: dict[str, Any]
    business_rules: dict[str, Any]
    plex_constructs: dict[str, Any]
