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

    def test_logic_load_config_valid_json_applies_ratios(
        self, config_json_path: Path
    ) -> None:
        # TC-B-06: loadConfig(valid json)
        registry = UnitDefinitionRepository.load(config_json_path)
        engine = ConversionEngine(registry)
        assert registry.get_meters_per_unit("feet") == pytest.approx(0.3048, abs=1e-6)
        assert engine.convert("meter", 1.0, "feet") == pytest.approx(
            FEET_PER_METER, abs=1e-4
        )

    def test_logic_load_config_valid_yaml_applies_ratios(self, tmp_path: Path) -> None:
        # TC-B-06: loadConfig(valid yaml)
        yaml = pytest.importorskip("yaml")
        path = tmp_path / "units.yaml"
        path.write_text(
            yaml.dump(
                {
                    "units": [
                        {"id": "meter", "meters_per_unit": 1.0},
                        {"id": "feet", "meters_per_unit": 0.3048},
                        {"id": "yard", "meters_per_unit": 0.9144},
                    ]
                }
            ),
            encoding="utf-8",
        )
        registry = UnitDefinitionRepository.load(path)
        engine = ConversionEngine(registry)
        assert engine.convert("meter", 1.0, "feet") == pytest.approx(
            FEET_PER_METER, abs=1e-4
        )

    def test_logic_load_config_missing_path_keeps_default_ratios(self) -> None:
        pytest.fail("RED")
