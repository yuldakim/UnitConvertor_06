"""Boundary package exports."""

from __future__ import annotations

from boundary import __all__ as boundary_all
from boundary import parse_convert_line, parse_register_line


def test_boundary_public_exports() -> None:
    assert callable(parse_convert_line)
    assert callable(parse_register_line)
    assert "parse_convert_line" in boundary_all
    assert "parse_register_line" in boundary_all
