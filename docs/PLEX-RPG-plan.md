# PLEX RPG Parser Implementation Plan

## Goal
Establish the first concrete `lang-parsers` module: a deterministic parser/analyzer for CA/HCL PLEX-generated RPG ILE source.

## Scope
- Create foundational Python project scaffolding (`pyproject.toml`).
- Introduce importable parser package under `parsers/rpg_plex/`.
- Define parser pipeline and typed AST/output contracts.
- Implement initial parser/analyzer stubs to make end-to-end flow executable.
- Provide CLI entrypoint (`rpg-plex-parse`).
- Add test directory skeleton for unit and integration fixtures.

## Module Layout
- `parsers/rpg_plex/lexer/`
  - `token_types.py`
  - `base_lexer.py`
  - `fixed_format.py`
  - `free_format.py`
- `parsers/rpg_plex/parser/`
  - `spec_parser.py`
  - `free_parser.py`
  - `directive_parser.py`
- `parsers/rpg_plex/ast/`
  - `nodes.py`
  - `visitor.py`
- `parsers/rpg_plex/analyzers/`
  - `control_flow.py`
  - `report_templates.py`
  - `io_operations.py`
  - `business_rules.py`
  - `plex_constructs.py`
- `parsers/rpg_plex/output/`
  - `schema.py`
  - `serializer.py`
- `parsers/rpg_plex/cli.py`

## Execution Pipeline
1. Format detector: FIXED/FREE/MIXED.
2. Lexer: line tokenization with /FREE mode switching.
3. Parser: typed spec/statement nodes + directives.
4. AST builder: fold flat statements into a `ProgramNode` hierarchy.
5. Analyzers: 5 focus-area visitors produce report sections.
6. Serializer: emit JSON document conforming to `AnalysisReport`.

## Focus Areas
1. Control flow modeling and subroutine relationships.
2. Printer/report template extraction from O-spec + EXCEPT.
3. File and I/O operation classification.
4. Business rule and indicator/validation pattern extraction.
5. PLEX-specific construct detection with confidence scoring.

## PLEX Heuristics Baseline
- Procedure names prefixed with `@`/`B_`/`F_`.
- Standard `/COPY` members (e.g., `QCPYLESRC`, `ERRDS`, `@PARMS`, `QUSEC`).
- Conventional error subroutines (`ERRHDLSR`, `@ErrorSR`).
- Fixed-format cycle remnants (`DOW *INLR/*IN99 = *OFF`).
- IBM i activation-group metadata in H-spec.

## Output Contract
Emit top-level sections:
- `metadata`
- `summary`
- `control_flows`
- `report_templates`
- `io_operations`
- `business_rules`
- `plex_constructs`

## Initial Implementation Notes
- Python 3.11+.
- Use `dataclasses` for AST nodes and small typed contracts.
- Keep parser deterministic; avoid speculative grammar.
- Prioritize resilient parsing with non-fatal parse errors in metadata.

## Verification
- Import smoke test: `from parsers.rpg_plex import parse_file`.
- CLI smoke test: `rpg-plex-parse <fixture>`.
- Unit/integration tests scaffolded under `tests/rpg_plex/`.
