"""Boundary — parse_register_line and convert-line edge cases."""

from __future__ import annotations

import pytest

from boundary.parser import ParseError, parse_convert_line, parse_register_line
from entity.exceptions import InvalidRatioError
from entity.registry import UnitRegistry


def test_parse_register_line_valid() -> None:
    command = parse_register_line("1 cubit = 0.4572 meter")
    assert command.unit_id == "cubit"
    assert command.meters_per_unit == pytest.approx(0.4572)


def test_parse_register_line_invalid_format_raises_parse_error() -> None:
    with pytest.raises(ParseError) as exc_info:
        parse_register_line("cubit = 0.4572 meter")
    assert exc_info.value.code == "ERR_INVALID_REGISTER"


def test_parse_register_line_zero_factor_raises_invalid_ratio() -> None:
    with pytest.raises(InvalidRatioError):
        parse_register_line("1 bad = 0 meter")


def test_parse_convert_line_empty_unit_id_raises_invalid_format() -> None:
    with pytest.raises(ParseError) as exc_info:
        parse_convert_line(":2.5", UnitRegistry.with_defaults())
    assert exc_info.value.code == "ERR_INVALID_FORMAT"
