#!/usr/bin/env python3
"""Generate or refresh tests/golden_master_expected.txt from UnitConverter output."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from tests.golden_master import (  # noqa: E402
    SCENARIOS,
    build_golden_master_document,
    write_expected_file,
)

DEFAULT_OUTPUT = PROJECT_ROOT / "tests" / "golden_master_expected.txt"


def capture_via_subprocess(scenario: str) -> str:
    """Optional: full UnitConverter.py CLI via stdin (prompt + table output)."""
    proc = subprocess.run(
        [sys.executable, str(PROJECT_ROOT / "UnitConverter.py")],
        input=f"{scenario}\n",
        capture_output=True,
        text=True,
        cwd=PROJECT_ROOT,
        check=True,
    )
    lines = proc.stdout.splitlines()
    # Skip interactive prompt line; remainder is conversion table.
    if lines and "Insert value" in lines[0]:
        return "\n".join(lines[1:]).rstrip("\n")
    return proc.stdout.rstrip("\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate golden master baseline file.")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Output path (default: tests/golden_master_expected.txt)",
    )
    parser.add_argument(
        "--subprocess",
        action="store_true",
        help="Capture via UnitConverter.py subprocess instead of ConverterApp",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Exit 1 if output would change existing file (no write)",
    )
    args = parser.parse_args()

    if args.subprocess:
        blocks = []
        for scenario in SCENARIOS:
            body = capture_via_subprocess(scenario)
            blocks.append(f"[{scenario}]\n{body}")
        from tests.golden_master import SECTION_SEPARATOR

        content = SECTION_SEPARATOR.join(blocks) + "\n"  # noqa: same as build_golden_master_document
    else:
        content = build_golden_master_document()

    if args.check and args.output.is_file():
        existing = args.output.read_text(encoding="utf-8")
        if existing != content:
            print(f"Drift detected: {args.output}", file=sys.stderr)
            return 1
        print(f"OK (unchanged): {args.output}")
        return 0

    write_expected_file(args.output, content)
    print(f"Wrote golden master: {args.output}")
    print("Next: git add tests/golden_master_expected.txt")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
