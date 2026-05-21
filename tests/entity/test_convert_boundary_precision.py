"""경계값 — value=0, 매우 큰 수, 소수점 6자리 정확도."""

from __future__ import annotations

import math

import pytest

from entity.constants import FEET_PER_METER, NUMERIC_EPSILON
from entity.engine import ConversionEngine
from entity.registry import UnitRegistry

RATIO_METER_TO_FEET = FEET_PER_METER


@pytest.fixture
def engine(defaults_registry: UnitRegistry) -> ConversionEngine:
    return ConversionEngine(defaults_registry)


def test_convert_boundary_zero_meter_to_feet_is_zero(engine: ConversionEngine) -> None:
    # Given: 1 meter = 3.28084 feet, value = 0 (영값 허용)
    # When: convert meter:0 → feet
    result = engine.convert("meter", 0.0, "feet")
    # Then: 0 feet
    assert result == 0.0


def test_convert_boundary_zero_convert_all_three_lines_zero(
    engine: ConversionEngine,
) -> None:
    # Given: value = 0
    # When: convert_all
    lines = engine.convert_all("meter", 0.0)
    # Then: all targets zero
    assert all(line.magnitude == 0.0 for line in lines)


def test_convert_boundary_large_value_finite_not_inf(engine: ConversionEngine) -> None:
    # Given: 1 meter = 3.28084 feet, very large magnitude
    large = 1e100
    # When: convert
    result = engine.convert("meter", large, "feet")
    # Then: finite positive (no overflow to inf)
    assert math.isfinite(result)
    assert result > 0
    # Then: 비율 관계 유지 (초대형 float에서는 절대 오차 대신 비율 검증)
    assert result / large == pytest.approx(RATIO_METER_TO_FEET, abs=1e-5)


def test_convert_boundary_six_decimal_input_preserves_precision(
    engine: ConversionEngine,
) -> None:
    # Given: 1 meter = 3.28084 feet, magnitude with 6 decimal places
    magnitude = 1.234567
    # When: convert
    result = engine.convert("meter", magnitude, "feet")
    expected = magnitude * RATIO_METER_TO_FEET
    # Then: within 1e-6 absolute (6자리 정확도 검증)
    assert result == pytest.approx(expected, abs=1e-6)


def test_convert_boundary_meter_2_55_feet_internal_before_round(
    engine: ConversionEngine,
) -> None:
    # Given: 2.55 meter, 1 meter = 3.28084 feet
    # When: internal convert (pre-display)
    result = engine.convert("meter", 2.55, "feet")
    # Then: 2.55 × 3.28084 = 8.366142 → display layer rounds to 8.4
    assert result == pytest.approx(2.55 * RATIO_METER_TO_FEET, abs=NUMERIC_EPSILON)
    assert result == pytest.approx(8.366142, abs=1e-4)
