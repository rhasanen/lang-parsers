from __future__ import annotations

import argparse
import json
from pathlib import Path

from .pipeline import parse_file


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Parse PLEX-generated RPG and emit analysis JSON")
    parser.add_argument("file", type=Path, help="Path to RPG/RPGLE source file")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    report = parse_file(args.file)

    if args.pretty:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(json.dumps(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
