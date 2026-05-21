"""Track B — Domain / Logic RED: registerUnit · loadConfig."""

from __future__ import annotations

from pathlib import Path

import pytest

from control.converter_app import ConverterApp
from data.repository import UnitDefinitionRepository
from entity.constants import FEET_PER_METER
from entity.engine import ConversionEngine
from entity.registry import UnitRegistry


class TestLogicRedRegisterUnit:
    """TC-B-05"""

    def test_logic_register_unit_cubit_then_convert_to_feet(self) -> None:
        # TC-B-05: registerUnit("cubit", 0.4572) 후 convert
        registry = UnitRegistry.with_defaults()
        registry.register_unit("cubit", 0.4572)
        engine = ConversionEngine(registry)
        result = engine.convert("cubit", 1.0, "feet")
        assert result == pytest.approx(0.4572 / 0.3048, abs=1e-4)
        lines = engine.convert_all("meter", 1.0)
        assert len(lines) == 4


class TestLogicRedLoadConfig:
    """TC-B-06, TC-B-07"""

    def test_logic_load_config_valid_json_applies_ratios(self) -> None:
        pytest.fail("RED")

    def test_logic_load_config_valid_yaml_applies_ratios(self) -> None:
        pytest.fail("RED")

    def test_logic_load_config_missing_path_keeps_default_ratios(self) -> None:
        pytest.fail("RED")
