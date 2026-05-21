"""Boundary — table 표시·Happy path (1 meter = 3.28084 feet 표시 8.2)."""

from __future__ import annotations

from entity.constants import FEET_PER_METER

from control.converter_app import ConverterApp

RATIO_METER_TO_FEET = FEET_PER_METER


def test_convert_display_meter_2_5_table_three_lines(converter_app: ConverterApp) -> None:
    # Given: 1 meter = 3.28084 feet, input meter:2.5
    # When: handle_convert_line
    output = converter_app.handle_convert_line("meter:2.5")
    lines = output.splitlines()
    # Then: 3 lines, display 8.2 feet (ROUND_HALF_UP)
    assert len(lines) == 3
    assert "2.5 meter = 2.5 meter" in lines
    assert "2.5 meter = 8.2 feet" in lines
    assert "2.5 meter = 2.7 yard" in lines


def test_convert_display_preserves_source_value_in_output(converter_app: ConverterApp) -> None:
    # Given: source 2.5
    # When
    output = converter_app.handle_convert_line("meter:2.5")
    # Then: 원 입력값 보존
    assert output.startswith("2.5 meter = ")


def test_convert_display_zero_shows_0_0(converter_app: ConverterApp) -> None:
    # Given: value=0
    # When
    output = converter_app.handle_convert_line("meter:0")
    # Then
    assert "0.0 meter = 0.0 feet" in output


def test_convert_display_feet_input_reverse_line(converter_app: ConverterApp) -> None:
    # Given: 1 meter = 3.28084 feet, feet:8.2 input (display value)
    # When: convert line feet:8.2 — internal uses 8.2 feet
    output = converter_app.handle_convert_line("feet:8.2")
    # Then: contains meter line
    assert "8.2 feet = " in output
    assert "meter" in output


def test_convert_display_app_convert_matches_ratio(converter_app: ConverterApp) -> None:
    # Given: 1 meter = 3.28084 feet
    # When: app.convert API
    result = converter_app.convert("meter", 2.5, "feet")
    # Then
    assert abs(result - 2.5 * RATIO_METER_TO_FEET) < 1e-5
