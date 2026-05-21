"""동적 등록 — registerUnit 후 변환."""

from __future__ import annotations

import pytest

from entity.constants import FEET_PER_METER, NUMERIC_EPSILON
from entity.engine import ConversionEngine
from entity.exceptions import DuplicateUnitError, InvalidRatioError
from entity.registry import UnitRegistry

RATIO_METER_TO_FEET = FEET_PER_METER


@pytest.fixture
def registry_with_cubit() -> UnitRegistry:
    reg = UnitRegistry.with_defaults()
    reg.register_unit("cubit", 0.4572)
    return reg


def test_register_dynamic_cubit_then_convert_to_feet(registry_with_cubit: UnitRegistry) -> None:
    # Given: 1 cubit = 0.4572 meter, 1 meter = 3.28084 feet
    engine = ConversionEngine(registry_with_cubit)
    # When: 1 cubit → feet
    result = engine.convert("cubit", 1.0, "feet")
    # Then: 0.4572 m / 0.3048 ft ≈ 1.50039 ft
    expected = 0.4572 / 0.3048
    assert result == pytest.approx(expected, abs=NUMERIC_EPSILON)


def test_register_dynamic_convert_all_includes_cubit(registry_with_cubit: UnitRegistry) -> None:
    # Given: cubit registered
    engine = ConversionEngine(registry_with_cubit)
    # When: convert_all meter:1
    lines = engine.convert_all("meter", 1.0)
    # Then: 4 units
    units = [line.target_unit for line in lines]
    assert len(units) == 4
    assert "cubit" in units


def test_register_dynamic_cubit_meters_per_unit_stored(registry_with_cubit: UnitRegistry) -> None:
    # Given / When / Then
    assert registry_with_cubit.get_meters_per_unit("cubit") == pytest.approx(0.4572, abs=1e-6)


def test_register_dynamic_zero_factor_raises_invalid_ratio() -> None:
    # Given: invalid factor
    reg = UnitRegistry.with_defaults()
    # When / Then
    with pytest.raises(InvalidRatioError):
        reg.register_unit("bad", 0.0)


def test_register_dynamic_duplicate_unit_raises_duplicate_error() -> None:
    # Given: meter already registered
    reg = UnitRegistry.with_defaults()
    # When / Then
    with pytest.raises(DuplicateUnitError):
        reg.register("meter", 1.0)


def test_register_dynamic_meter_to_cubit_after_register(registry_with_cubit: UnitRegistry) -> None:
    # Given: 1 meter = 1/0.4572 cubit
    engine = ConversionEngine(registry_with_cubit)
    # When: 2.5 meter → cubit
    result = engine.convert("meter", 2.5, "cubit")
    # Then: 2.5 / 0.4572
    assert result == pytest.approx(2.5 / 0.4572, abs=NUMERIC_EPSILON)
