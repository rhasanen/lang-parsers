from __future__ import annotations

from parsers.rpg_plex.ast.nodes import (
    DowNode,
    ExsrNode,
    ForNode,
    GotoNode,
    IfNode,
    SelectNode,
    SubroutineNode,
    TagNode,
)


LOOP_NODES = (DowNode, ForNode)


def analyze(program, report):
    tags = set()
    gotos = []
    subroutines = []
    sub_calls = []

    if_blocks = []
    loops = []
    selects = []
    nesting = 0
    max_nesting = 0

    for node in program.nodes:
        if isinstance(node, IfNode):
            if_blocks.append({"line": node.line, "condition": node.condition})
            nesting += 1
        elif isinstance(node, LOOP_NODES):
            loops.append({"line": node.line, "condition": getattr(node, "condition", "")})
            nesting += 1
        elif isinstance(node, SelectNode):
            selects.append({"line": node.line, "selector": node.selector})
            nesting += 1
        elif isinstance(node, TagNode):
            tags.add(node.name)
        elif isinstance(node, GotoNode):
            gotos.append({"line": node.line, "target": node.target})
        elif isinstance(node, SubroutineNode):
            subroutines.append({"line": node.line, "name": node.name})
        elif isinstance(node, ExsrNode):
            sub_calls.append({"line": node.line, "target": node.subroutine})

        max_nesting = max(max_nesting, nesting)

    unresolved = [g for g in gotos if g["target"] and g["target"] not in tags]

    report["control_flows"] = {
        "if_blocks": if_blocks,
        "loops": loops,
        "selects": selects,
        "gotos": gotos,
        "subroutines": subroutines,
        "subroutine_calls": sub_calls,
        "unresolved_gotos": unresolved,
        "indicator_conditions": [],
    }
    report["summary"]["max_control_flow_nesting_depth"] = max_nesting
