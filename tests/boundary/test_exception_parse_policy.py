"""예외 — 잘못된 형식 / 음수 / 없는 단위 / 파싱 실패."""

from __future__ import annotations

import pytest

from boundary.errors import ERR_INVALID_FORMAT
from boundary.parser import ParseError, parse_convert_line
from entity.registry import UnitRegistry


@pytest.fixture
def registry() -> UnitRegistry:
    return UnitRegistry.with_defaults()


def test_exception_format_missing_colon_raises_value_error(registry: UnitRegistry) -> None:
    # Given: ":" 없는 입력 (1 meter = 3.28084 feet 계약과 무관한 형식)
    line = "meter 2.5"
    # When / Then: ValueError 계열 ParseError
    with pytest.raises((ValueError, TypeError)) as exc_info:
        parse_convert_line(line, registry)
    assert ERR_INVALID_FORMAT.message in str(exc_info.value)


def test_exception_negative_meter_raises_value_error(registry: UnitRegistry) -> None:
    # Given: 음수 magnitude
    line = "meter:-1.0"
    # When / Then
    with pytest.raises(ValueError) as exc_info:
        parse_convert_line(line, registry)
    assert "Value must be zero or positive: -1.0" in str(exc_info.value)


def test_exception_unknown_unit_parsec_raises_value_error(registry: UnitRegistry) -> None:
    # Given: 미등록 단위 parsec
    line = "parsec:1.0"
    # When / Then
    with pytest.raises(ValueError) as exc_info:
        parse_convert_line(line, registry)
    assert "Unknown unit: parsec" in str(exc_info.value)


def test_exception_invalid_number_abc_raises_value_error(registry: UnitRegistry) -> None:
    # Given: 소수점 파싱 불가
    line = "meter:abc"
    # When / Then
    with pytest.raises(ValueError) as exc_info:
        parse_convert_line(line, registry)
    assert "Invalid number: abc" in str(exc_info.value)


def test_exception_empty_input_raises_value_error(registry: UnitRegistry) -> None:
    # Given: 빈 문자열
    # When / Then
    with pytest.raises(ValueError) as exc_info:
        parse_convert_line("", registry)
    assert "Input is empty." in str(exc_info.value)


def test_exception_format_double_colon_raises_invalid_format(registry: UnitRegistry) -> None:
    # Given: 콜론 2회
    line = "meter:2:5"
    # When / Then
    with pytest.raises(ParseError) as exc_info:
        parse_convert_line(line, registry)
    assert exc_info.value.code == ERR_INVALID_FORMAT.code
