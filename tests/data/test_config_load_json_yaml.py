"""설정 로드 — JSON/YAML 정상·실패 케이스."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from data.repository import ConfigLoadError, UnitDefinitionRepository
from entity.constants import FEET_PER_METER, METERS_PER_FEET, YARD_PER_METER
from entity.engine import ConversionEngine

RATIO_METER_TO_FEET = FEET_PER_METER
RATIO_METER_TO_YARD = YARD_PER_METER


def test_config_load_json_valid_ratios_from_file(config_json_path: Path) -> None:
    # Given: valid config/units.json (1 meter = 3.28084 feet via 0.3048 mpu)
    # When: load
    registry = UnitDefinitionRepository.load(config_json_path)
    engine = ConversionEngine(registry)
    # Then: convert 1 meter → feet
    assert engine.convert("meter", 1.0, "feet") == pytest.approx(
        RATIO_METER_TO_FEET, abs=1e-4
    )


def test_config_load_json_missing_path_keeps_default_ratios(tmp_path: Path) -> None:
    # Given: 없는 경로
    missing = tmp_path / "no_units.json"
    # When: load → defaults
    registry = UnitDefinitionRepository.load(missing)
    engine = ConversionEngine(registry)
    # Then: 3.28084 / 1.09361 유지
    assert engine.convert("meter", 1.0, "feet") == pytest.approx(
        RATIO_METER_TO_FEET, abs=1e-4
    )
    assert engine.convert("meter", 1.0, "yard") == pytest.approx(
        RATIO_METER_TO_YARD, abs=1e-4
    )
    assert registry.get_meters_per_unit("feet") == METERS_PER_FEET


def test_config_load_json_malformed_raises_parse_error(tmp_path: Path) -> None:
    # Given: malformed JSON
    bad = tmp_path / "bad.json"
    bad.write_text("{not json", encoding="utf-8")
    # When / Then
    with pytest.raises(ConfigLoadError) as exc_info:
        UnitDefinitionRepository.load(bad)
    assert exc_info.value.code == "CFG_PARSE_ERROR"


def test_config_load_yaml_valid_ratios(tmp_path: Path) -> None:
    yaml = pytest.importorskip("yaml")
    # Given: YAML with same ratios
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
    # When
    registry = UnitDefinitionRepository.load(path)
    engine = ConversionEngine(registry)
    # Then: 1 meter = 3.28084 feet
    assert engine.convert("meter", 2.5, "feet") == pytest.approx(
        2.5 * RATIO_METER_TO_FEET, abs=1e-5
    )


def test_config_load_yaml_empty_units_raises(tmp_path: Path) -> None:
    # Given: invalid empty units list
    path = tmp_path / "empty.yaml"
    path.write_text("units: []\n", encoding="utf-8")
    # When / Then
    with pytest.raises(ConfigLoadError):
        UnitDefinitionRepository.load(path)


def test_config_load_json_custom_unit_in_file(tmp_path: Path) -> None:
    # Given: JSON with cubit
    path = tmp_path / "custom.json"
    path.write_text(
        json.dumps(
            {
                "units": [
                    {"id": "meter", "meters_per_unit": 1.0},
                    {"id": "cubit", "meters_per_unit": 0.4572},
                ]
            }
        ),
        encoding="utf-8",
    )
    # When
    registry = UnitDefinitionRepository.load(path)
    # Then
    assert registry.count() == 2
    assert registry.get_meters_per_unit("cubit") == 0.4572
