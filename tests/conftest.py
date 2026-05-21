from __future__ import annotations

from pathlib import Path

import pytest

from control.converter_app import ConverterApp
from entity.registry import UnitRegistry
from data.repository import UnitDefinitionRepository

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_JSON = PROJECT_ROOT / "config" / "units.json"


@pytest.fixture
def defaults_registry() -> UnitRegistry:
    return UnitRegistry.with_defaults()


@pytest.fixture
def converter_app(defaults_registry: UnitRegistry) -> ConverterApp:
    return ConverterApp(defaults_registry)


@pytest.fixture
def config_json_path() -> Path:
    return CONFIG_JSON
