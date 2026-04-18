from __future__ import annotations

from collections import defaultdict

from parsers.rpg_plex.ast.nodes import (
    CallpNode,
    ChainNode,
    DataQueueOpNode,
    ExfmtNode,
    FileDeclarationNode,
    ReadNode,
    SetgtNode,
    SetllNode,
    WriteNode,
)


DATA_QUEUE_APIS = {"QSNDDTAQ", "QRCVDTAQ", "QMHSNDPM", "QMHRCVPM"}


def analyze(program, report):
    file_declarations = []
    operations = []
    external_calls = []
    dq_ops = []
    per_file = defaultdict(set)

    for node in program.nodes:
        if isinstance(node, FileDeclarationNode):
            file_declarations.append(
                {"line": node.line, "name": node.name, "io_mode": node.io_mode, "device": node.device}
            )
        elif isinstance(node, ReadNode):
            operations.append({"line": node.line, "opcode": "READ", "file": node.file_name})
            per_file[node.file_name].add("read")
        elif isinstance(node, WriteNode):
            operations.append({"line": node.line, "opcode": "WRITE", "file": node.file_name})
            per_file[node.file_name].add("write")
        elif isinstance(node, ChainNode):
            operations.append({"line": node.line, "opcode": "CHAIN", "file": node.file_name})
            per_file[node.file_name].add("keyed")
        elif isinstance(node, SetllNode):
            operations.append({"line": node.line, "opcode": "SETLL", "file": node.file_name})
            per_file[node.file_name].add("keyed")
        elif isinstance(node, SetgtNode):
            operations.append({"line": node.line, "opcode": "SETGT", "file": node.file_name})
            per_file[node.file_name].add("keyed")
        elif isinstance(node, ExfmtNode):
            operations.append({"line": node.line, "opcode": "EXFMT", "record": node.record_name})
        elif isinstance(node, CallpNode):
            call_name = node.procedure.split("(", 1)[0].strip().upper()
            external_calls.append({"line": node.line, "name": call_name})
            if call_name in DATA_QUEUE_APIS:
                dq = DataQueueOpNode(line=node.line, text=node.text, api_name=call_name)
                dq_ops.append({"line": dq.line, "api_name": dq.api_name})

    file_operation_summary = [
        {"file": file_name, "modes": sorted(modes)} for file_name, modes in per_file.items() if file_name
    ]

    report["io_operations"] = {
        "file_declarations": file_declarations,
        "operations": operations,
        "data_queue_operations": dq_ops,
        "entry_prototype": None,
        "external_calls": external_calls,
        "file_operation_summary": file_operation_summary,
    }
    report["summary"]["file_declaration_count"] = len(file_declarations)
    report["summary"]["total_io_operations"] = len(operations)
