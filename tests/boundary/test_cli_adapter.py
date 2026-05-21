"""CLI adapter — subprocess exit code and stdout contract."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


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
