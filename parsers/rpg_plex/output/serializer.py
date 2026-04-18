from __future__ import annotations

from datetime import datetime, timezone

from .schema import AnalysisReport


PARSER_VERSION = "0.1.0"


def create_empty_report(source_file: str, format_mode: str, line_count: int, parse_errors: list[str]) -> AnalysisReport:
    return {
        "metadata": {
            "source_file": source_file,
            "parse_date": datetime.now(tz=timezone.utc).isoformat(),
            "parser_version": PARSER_VERSION,
            "format_mode": format_mode,
            "line_count": line_count,
            "parse_errors": parse_errors,
        },
        "summary": {
            "procedure_count": 0,
            "file_declaration_count": 0,
            "printer_file_count": 0,
            "plex_confidence_score": 0.0,
            "plex_version_hint": "unknown",
            "has_cycle_remnants": False,
            "total_io_operations": 0,
            "max_control_flow_nesting_depth": 0,
        },
        "control_flows": {
            "if_blocks": [],
            "loops": [],
            "selects": [],
            "gotos": [],
            "subroutines": [],
            "subroutine_calls": [],
        },
        "report_templates": {"printer_files": []},
        "io_operations": {
            "file_declarations": [],
            "operations": [],
            "data_queue_operations": [],
            "entry_prototype": None,
            "external_calls": [],
        },
        "business_rules": {
            "assignments": [],
            "monitor_blocks": [],
            "indicator_usage": {},
            "validation_patterns": [],
            "global_fields": [],
        },
        "plex_constructs": {
            "plex_procedures": [],
            "copy_members": [],
            "like_define_graph": [],
            "compiler_directives": [],
            "data_structures": [],
            "error_handler_blocks": [],
            "cycle_analysis": {},
            "plex_version_hint": "unknown",
        },
    }
