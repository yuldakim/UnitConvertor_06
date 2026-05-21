"""Track B — Domain / Logic RED: convert · convertAll."""

from __future__ import annotations

import pytest

from entity.engine import ConversionEngine
from entity.registry import UnitRegistry


class TestLogicRedConvert:
    """TC-B-01 ~ TC-B-04, TC-B-08, TC-B-09"""

    def test_logic_convert_meter_to_feet_within_1e_5(
        self, defaults_registry: UnitRegistry
    ) -> None:
        # TC-B-01: convert("meter", 2.5, "feet") — 1 m = 3.28084 ft
        engine = ConversionEngine(defaults_registry)
        result = engine.convert("meter", 2.5, "feet")
        assert result == pytest.approx(8.20210, abs=1e-5)

    def test_logic_convert_meter_to_yard_within_1e_5(self) -> None:
        pytest.fail("RED")

    def test_logic_convert_feet_to_meter_reverse_within_1e_5(self) -> None:
        pytest.fail("RED")

    def test_logic_convert_all_meter_returns_all_registered_units(self) -> None:
        pytest.fail("RED")

    def test_logic_convert_negative_meter_raises_value_error(self) -> None:
        pytest.fail("RED")

    def test_logic_convert_zero_meter_to_feet_is_zero(self) -> None:
        pytest.fail("RED")
