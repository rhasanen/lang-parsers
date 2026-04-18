from __future__ import annotations

import re

from parsers.rpg_plex.ast.nodes import CompilerDirectiveNode, ProcedureNode, SubroutineNode


COPY_MEMBERS = {"QCPYLESRC", "ERRDS", "@PARMS", "QUSEC"}
ERR_HANDLERS = {"ERRHDLSR", "@ERRORSR"}


def _cap_score(value: float) -> float:
    return min(1.0, max(0.0, value))


def analyze(program, report):
    score = 0.0
    copy_members = []
    directives = []
    plex_procedures = []
    error_handlers = []
    has_cycle_remnants = False

    for node in program.nodes:
        if isinstance(node, ProcedureNode):
            plex_procedures.append({"line": node.line, "name": node.name})
            if node.name.startswith("@"):
                score += 0.30
        if isinstance(node, SubroutineNode):
            if node.name.upper() in ERR_HANDLERS:
                error_handlers.append({"line": node.line, "name": node.name})
                score += 0.15
        if isinstance(node, CompilerDirectiveNode):
            directives.append({"line": node.line, "name": node.name, "arguments": node.arguments})
            if node.name == "/COPY":
                member = node.arguments.split(",")[-1].strip().upper() if node.arguments else ""
                copy_members.append({"line": node.line, "member": member})
                if "QCPYLESRC" in node.arguments.upper():
                    score += 0.10
                if member in COPY_MEMBERS:
                    score += 0.10

        text = getattr(node, "text", "")
        upper = text.upper()
        if "DOW" in upper and ("*INLR" in upper or "*IN99" in upper) and "*OFF" in upper:
            has_cycle_remnants = True
            score += 0.10

        if "*ENTRY" in upper and "PLIST" in upper:
            score += 0.10
        if re.search(r"\b@DS\w*", upper):
            score += 0.05

    full_text = "\n".join(getattr(node, "text", "") for node in program.nodes).upper()
    if "DFTACTGRP(*NO)" in full_text and "ACTGRP" in full_text:
        score += 0.10

    if "/FREE" in full_text and ("PR" in full_text or "PI" in full_text) and "ACTGRP(*CALLER)" in full_text:
        version_hint = "6.x / 7.x"
    elif "*ENTRY" in full_text and "DFTACTGRP(*YES)" in full_text:
        version_hint = "5.x or earlier"
    elif "EXEC SQL" in full_text:
        version_hint = "7.x with SQL extension"
    else:
        version_hint = "unknown"

    report["plex_constructs"] = {
        "plex_procedures": plex_procedures,
        "copy_members": copy_members,
        "like_define_graph": [],
        "compiler_directives": directives,
        "data_structures": [],
        "error_handler_blocks": error_handlers,
        "cycle_analysis": {"has_cycle_remnants": has_cycle_remnants},
        "plex_version_hint": version_hint,
    }
    report["summary"]["plex_confidence_score"] = _cap_score(score)
    report["summary"]["has_cycle_remnants"] = has_cycle_remnants
    report["summary"]["plex_version_hint"] = version_hint
