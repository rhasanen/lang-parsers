# Lang-PLEX-RPG Specification

## 1. Purpose
`lang-parsers` introduces an RPG parser dedicated to CA/HCL PLEX-generated RPG ILE. The parser focuses on deterministic extraction of control flow, report layout behavior, I/O activity, business rules, and PLEX-identifying signatures.

PLEX output is template-driven and highly regular. This parser explicitly uses those regularities to increase confidence and lower ambiguity versus generic RPG parsing.

## 2. Architecture Overview

### 2.1 Module Structure
```
lang-parsers/
├── Lang-PLEX-RPG.md
├── pyproject.toml
├── parsers/
│   └── rpg_plex/
│       ├── __init__.py
│       ├── lexer/
│       │   ├── token_types.py
│       │   ├── base_lexer.py
│       │   ├── fixed_format.py
│       │   └── free_format.py
│       ├── parser/
│       │   ├── spec_parser.py
│       │   ├── free_parser.py
│       │   └── directive_parser.py
│       ├── ast/
│       │   ├── nodes.py
│       │   └── visitor.py
│       ├── analyzers/
│       │   ├── control_flow.py
│       │   ├── report_templates.py
│       │   ├── io_operations.py
│       │   ├── business_rules.py
│       │   └── plex_constructs.py
│       ├── output/
│       │   ├── schema.py
│       │   └── serializer.py
│       └── cli.py
└── tests/
    └── rpg_plex/
```

### 2.2 Parser Pipeline
1. **Phase 0: Format Detection**
   - Detect `FIXED`, `FREE`, `MIXED` via `/FREE` markers and free-form headers.
2. **Phase 1: Lexer**
   - Fixed-mode: column-aware tokenization for H/F/D/I/C/O/P specs.
   - Free-mode: semicolon-delimited statements.
   - Inline directive handling for `/FREE`, `/END-FREE`, `/COPY`, `/IF`.
3. **Phase 2: Parser**
   - Convert tokens into typed spec/statement nodes.
4. **Phase 3: AST Builder**
   - Build `ProgramNode` with procedure/subroutine/control block hierarchy.
5. **Phase 4: Analyzers**
   - Execute five focus-area analyzers over AST.
6. **Phase 5: Serializer**
   - Emit `AnalysisReport` JSON.

## 3. Focus Area Specifications

### 3.1 Control Flows
**Constructs**: IF/ELSE/ELSEIF/ENDIF, DOW/DOU/FOR/ENDDO, ITER/LEAVE, SELECT/WHEN/OTHER/ENDSL, GOTO/TAG, BEGSR/ENDSR, EXSR, LEAVESR.

**PLEX Signal**: Outermost loop such as `DOW *INLR = *OFF` or `*IN99 = *OFF` indicates cycle-mimic style.

**Outputs**:
- Nesting depth
- Subroutine call graph
- Unresolved GOTO targets
- Indicator use in conditions

### 3.2 Report Templates
**Constructs**: F-spec printer declarations, O-spec line types (H/D/T/E/F), EXCEPT/EXCPT opcodes, edit metadata.

**Outputs**:
- Printer-file page layout model
- EXCEPT→record linkage
- Unresolved EXCEPT records
- `is_plex_report_pattern` when names match `RPTnnn[HDT]`

### 3.3 Input and Output
**Constructs**: F-spec declarations and major RPG I/O opcodes (READ family, WRITE/UPDATE/DELETE, CHAIN, SETLL/SETGT, OPEN/CLOSE, EXFMT, CALLP/CALL).

**Outputs**:
- Per-file operation profile
- Sequential vs keyed access hints
- Entry parameter/prototype capture
- External call surface (including IBM i APIs)

### 3.4 Business Rules
**Constructs**: EVAL/EVALR, MONITOR/ON-ERROR/ENDMON, indicator tests/sets, validation IF patterns, COMMIT/ROLBK.

**Validation Heuristics**:
- REQUIRED_FIELD (`= *BLANK`, `= *ZEROS`)
- RANGE_CHECK (`< low OR > high`)
- LOOKUP_VALIDATE (`CHAIN` + `%FOUND` checks)

**Outputs**:
- Indicator set/test map
- Empty ON-ERROR detection
- Validation pattern catalog
- Assignment operand graph

### 3.5 PLEX Special Constructs
**Constructs**: `@`/`B_`/`F_` names, `/COPY` of standard members, LIKE inheritance, directives, H-spec activation group keywords, cycle remnants.

**Confidence Scoring (cap 1.0)**:
- Procedure name starts with `@` (**0.30**)
- `ERRHDLSR` / `@ErrorSR` found (**0.15**)
- `/COPY` from `QCPYLESRC` (**0.10**)
- `DFTACTGRP(*NO)` + `ACTGRP` in H-spec (**0.10**)
- Outermost `DOW *INLR/*IN99 = *OFF` (**0.10**)
- `/COPY` names matching `@PARMS`/`ERRDS`/`QUSEC` (**0.10**)
- `*ENTRY PLIST` or IBM-i style PR/PI signatures (**0.10**)
- DS names matching `@DS*` (**0.05**)

**Classification**:
- `>= 0.60`: high confidence PLEX
- `0.30–0.59`: possible PLEX
- `< 0.30`: unlikely PLEX

**Version Hints**:
- `/FREE` + PR/PI + `ACTGRP(*CALLER)` → likely 6.x/7.x
- Fixed + `*ENTRY PLIST` + `DFTACTGRP(*YES)` → 5.x or earlier
- `EXEC SQL` usage → 7.x + SQL extension

## 4. Output Schema
Top-level JSON object:
- `metadata`
- `summary`
- `control_flows`
- `report_templates`
- `io_operations`
- `business_rules`
- `plex_constructs`

The Python contract is maintained via `TypedDict` in `parsers/rpg_plex/output/schema.py`.

## 5. Error Handling and Recovery
- Parser never aborts on first malformed line.
- Parse errors are recorded in `metadata.parse_errors`.
- Unknown directives/specs are represented as generic nodes and preserved for analyzers.

## 6. CLI Contract
Command: `rpg-plex-parse <file> [--pretty]`
- Reads RPG source file.
- Runs full pipeline.
- Emits JSON to stdout.

## 7. Implementation Phases
1. Foundation scaffolding.
2. Core lex/parse + AST assembly.
3. Analyzer pass implementation.
4. Output/CLI integration.
5. Hardening, fixtures, and coverage growth.

## 8. Immediate Deliverables
- This specification file (`Lang-PLEX-RPG.md`).
- `docs/PLEX-RPG-plan.md` implementation plan.
- Importable parser package skeleton with end-to-end callable pipeline.
