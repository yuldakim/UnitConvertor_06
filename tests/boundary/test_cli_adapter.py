"""CLI adapter — subprocess exit code and stdout contract."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

from boundary.cli_adapter import CONVERT_PROMPT, run_convert_cli
from boundary.parser import ParseError
from control.converter_app import ConverterApp

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


def test_run_convert_cli_prints_table_on_valid_input(converter_app) -> None:
    captured: list[str] = []

    def fake_print(*args: object) -> None:
        captured.append("\n".join(str(a) for a in args))

    with patch("boundary.cli_adapter.input", return_value="meter:2.5"):
        with patch("boundary.cli_adapter.print", side_effect=fake_print):
            run_convert_cli(converter_app)
    assert "8.2 feet" in "\n".join(captured)


def test_run_convert_cli_parse_error_exits_with_message(converter_app) -> None:
    captured: list[str] = []

    def fake_print(*args: object) -> None:
        captured.append(str(args[0]) if args else "")

    with patch("boundary.cli_adapter.input", return_value="parsec:1.0"):
        with patch("boundary.cli_adapter.print", side_effect=fake_print):
            with pytest.raises(SystemExit) as exc_info:
                run_convert_cli(converter_app)
    assert exc_info.value.code == 1
    assert "parsec" in "".join(captured)


def test_convert_prompt_constant() -> None:
    assert "meter:2.5" in CONVERT_PROMPT


def test_cli_parse_error_exits_nonzero() -> None:
    proc = subprocess.run(
        [sys.executable, str(PROJECT_ROOT / "UnitConverter.py")],
        input="parsec:1.0\n",
        capture_output=True,
        text=True,
        cwd=PROJECT_ROOT,
    )
    assert proc.returncode != 0
    assert "parsec" in proc.stdout or proc.stderr


def test_cli_happy_path_exits_zero() -> None:
    proc = subprocess.run(
        [sys.executable, str(PROJECT_ROOT / "UnitConverter.py")],
        input="meter:2.5\n",
        capture_output=True,
        text=True,
        cwd=PROJECT_ROOT,
    )
    assert proc.returncode == 0
    assert "8.2 feet" in proc.stdout
