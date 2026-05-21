"""Golden Master capture, section parsing, and approve/compare helpers."""

from __future__ import annotations

import difflib
import io
import subprocess
import sys
from contextlib import redirect_stdout
from pathlib import Path

from control.converter_app import ConverterApp

GOLDEN_MASTER_PATH = Path(__file__).resolve().parent / "golden_master_expected.txt"

SCENARIOS: tuple[str, ...] = (
    "meter:2.5",
    "feet:1.0",
    "yard:1.0",
    "meter:0.0",
)

SECTION_SEPARATOR = "\n---\n"


def capture_scenario_output(scenario: str, app: ConverterApp | None = None) -> str:
    """Capture table output (UnitConverter print body) via StringIO + redirect_stdout."""
    converter = app or ConverterApp()
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        print(converter.handle_convert_line(scenario))
    return buffer.getvalue().replace("\r\n", "\n").rstrip("\n")


def capture_scenario_output_subprocess(
    scenario: str,
    *,
    project_root: Path | None = None,
) -> str:
    """Capture via UnitConverter.py CLI (subprocess.run, capture_output=True)."""
    root = project_root or Path(__file__).resolve().parent.parent
    proc = subprocess.run(
        [sys.executable, str(root / "UnitConverter.py")],
        input=f"{scenario}\n",
        capture_output=True,
        text=True,
        cwd=root,
        check=True,
    )
    lines = proc.stdout.replace("\r\n", "\n").splitlines()
    if lines and "Insert value" in lines[0]:
        return "\n".join(lines[1:]).rstrip("\n")
    return proc.stdout.replace("\r\n", "\n").rstrip("\n")


def parse_sections(document: str) -> dict[str, str]:
    """Parse [scenario] headers into {scenario: body} (body without header or --- lines)."""
    normalized = document.replace("\r\n", "\n").strip("\n")
    if not normalized:
        return {}

    sections: dict[str, str] = {}
    current_key: str | None = None
    body_lines: list[str] = []

    for line in normalized.split("\n"):
        if line.startswith("[") and line.endswith("]"):
            if current_key is not None:
                sections[current_key] = "\n".join(body_lines).rstrip("\n")
            current_key = line[1:-1]
            body_lines = []
            continue
        if line.strip() == "---":
            continue
        if current_key is not None:
            body_lines.append(line)

    if current_key is not None:
        sections[current_key] = "\n".join(body_lines).rstrip("\n")
    return sections


def build_golden_master_document(
    scenarios: tuple[str, ...] = SCENARIOS,
    app: ConverterApp | None = None,
) -> str:
    converter = app or ConverterApp()
    blocks: list[str] = []
    for scenario in scenarios:
        body = capture_scenario_output(scenario, converter)
        blocks.append(f"[{scenario}]\n{body}")
    return SECTION_SEPARATOR.join(blocks) + "\n"


def read_expected_file(path: Path) -> str:
    with path.open(encoding="utf-8") as handle:
        return handle.read().replace("\r\n", "\n")


def write_expected_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(content)


def format_section_diff(expected: str, actual: str) -> str:
    """Unified diff: --- expected / +++ actual / @@ hunks @@."""
    return "".join(
        difflib.unified_diff(
            expected.splitlines(keepends=True),
            actual.splitlines(keepends=True),
            fromfile="expected",
            tofile="actual",
        )
    )


def _fail_with_diff(scenario: str, expected: str, actual: str) -> None:
    diff = format_section_diff(expected, actual)
    raise AssertionError(
        f"Golden master mismatch [{scenario}] (GM section vs captured output).\n"
        f"{diff or '(no diff lines produced)'}"
    )


def approve_section(
    scenario: str,
    expected_path: Path = GOLDEN_MASTER_PATH,
    *,
    app: ConverterApp | None = None,
    auto_create: bool = True,
) -> None:
    """
    Approve pattern per section:
    - expected file missing → generate full baseline, then fail (review + git add)
    - file present → compare captured output to [scenario] section only
    """
    actual = capture_scenario_output(scenario, app)

    if not expected_path.is_file():
        if not auto_create:
            raise AssertionError(f"Golden master missing: {expected_path}")
        write_expected_file(expected_path, build_golden_master_document(app=app))
        raise AssertionError(
            f"Golden master created at {expected_path}. "
            "Review the file, then run: git add tests/golden_master_expected.txt"
        )

    document = read_expected_file(expected_path)
    sections = parse_sections(document)
    if scenario not in sections:
        raise AssertionError(
            f"Section [{scenario}] not found in {expected_path}. "
            f"Available: {sorted(sections)}"
        )

    expected = sections[scenario]
    if expected == actual:
        return

    _fail_with_diff(scenario, expected, actual)
