"""정상 변환 — meter→feet, meter→yard, feet→meter (역변환)."""

from __future__ import annotations

import pytest

from entity.constants import FEET_PER_METER, NUMERIC_EPSILON, YARD_PER_METER
from entity.engine import ConversionEngine
from entity.registry import UnitRegistry

# 1 meter = 3.28084 feet (README)
RATIO_METER_TO_FEET = FEET_PER_METER
# 1 meter = 1.09361 yard (README)
RATIO_METER_TO_YARD = YARD_PER_METER


@pytest.fixture
def engine(defaults_registry: UnitRegistry) -> ConversionEngine:
    return ConversionEngine(defaults_registry)


def test_convert_normal_meter_to_feet_happy_returns_8_20210(engine: ConversionEngine) -> None:
    # Given: 1 meter = 3.28084 feet, source 2.5 meter
    # When: convert meter → feet
    result = engine.convert("meter", 2.5, "feet")
    # Then: 2.5 × 3.28084 ≈ 8.20210 (tolerance 1e-5)
    assert result == pytest.approx(2.5 * RATIO_METER_TO_FEET, abs=1e-5)
    assert result == pytest.approx(8.20210, abs=1e-5)


def test_convert_normal_meter_to_yard_happy_returns_2_734025(engine: ConversionEngine) -> None:
    # Given: 1 meter = 1.09361 yard, source 2.5 meter
    # When: convert meter → yard
    result = engine.convert("meter", 2.5, "yard")
    # Then: 2.5 × 1.09361 = 2.734025
    assert result == pytest.approx(2.5 * RATIO_METER_TO_YARD, abs=1e-5)


def test_convert_normal_feet_to_meter_reverse_returns_0_30480(engine: ConversionEngine) -> None:
    # Given: 1 feet = 0.3048 meter (meters_per_unit), 1 meter = 3.28084 feet
    # When: convert 1.0 feet → meter (역변환)
    result = engine.convert("feet", 1.0, "meter")
    # Then: 1 feet × 0.3048 / 1.0 = 0.3048
    assert result == pytest.approx(0.30480, abs=1e-5)


def test_convert_normal_one_meter_to_feet_matches_ratio_3_28084(engine: ConversionEngine) -> None:
    # Given: 1 meter = 3.28084 feet (ε 1e-4)
    # When: convert 1.0 meter → feet
    result = engine.convert("meter", 1.0, "feet")
    # Then: exact README ratio
    assert result == pytest.approx(RATIO_METER_TO_FEET, abs=NUMERIC_EPSILON)


def test_convert_normal_convert_all_meter_returns_three_targets(
    engine: ConversionEngine,
) -> None:
    # Given: default registry (meter, feet, yard), 1 meter = 3.28084 feet
    # When: convert_all from meter:1.0
    lines = engine.convert_all("meter", 1.0)
    # Then: 3 lines, feet ≈ 3.28084
    assert len(lines) == 3
    by_unit = {line.target_unit: line.magnitude for line in lines}
    assert by_unit["feet"] == pytest.approx(RATIO_METER_TO_FEET, abs=NUMERIC_EPSILON)
    assert by_unit["yard"] == pytest.approx(RATIO_METER_TO_YARD, abs=NUMERIC_EPSILON)
    assert by_unit["meter"] == pytest.approx(1.0, abs=NUMERIC_EPSILON)
