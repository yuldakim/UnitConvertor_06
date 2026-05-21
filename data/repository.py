from __future__ import annotations

import json
from pathlib import Path

from pydantic import BaseModel, Field, ValidationError

from entity.constants import FEET_PER_METER, METERS_PER_FEET, METERS_PER_METER, METERS_PER_YARD, YARD_PER_METER
from entity.registry import UnitRegistry

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None  # type: ignore[assignment]


class UnitDefinitionDTO(BaseModel):
    id: str
    meters_per_unit: float = Field(gt=0)


class UnitsConfigDTO(BaseModel):
    units: list[UnitDefinitionDTO]


class ConfigLoadError(ValueError):
    def __init__(self, code: str, message: str) -> None:
        self.code = code
        self.message = message
        super().__init__(message)


class UnitDefinitionRepository:
    @staticmethod
    def with_defaults() -> UnitRegistry:
        return UnitRegistry.with_defaults()

    @staticmethod
    def load(path: str | Path) -> UnitRegistry:
        file_path = Path(path)
        if not file_path.is_file():
            return UnitDefinitionRepository.with_defaults()

        try:
            raw_text = file_path.read_text(encoding="utf-8")
        except OSError as exc:
            raise ConfigLoadError(
                "CFG_FILE_NOT_FOUND",
                "Config file not found.",
            ) from exc

        try:
            if file_path.suffix.lower() in {".yaml", ".yml"}:
                if yaml is None:
                    raise ConfigLoadError(
                        "CFG_PARSE_ERROR",
                        "Failed to parse config file.",
                    )
                payload = yaml.safe_load(raw_text)
            else:
                payload = json.loads(raw_text)
            config = UnitsConfigDTO.model_validate(payload)
        except (json.JSONDecodeError, ValidationError, TypeError, ValueError) as exc:
            raise ConfigLoadError(
                "CFG_PARSE_ERROR",
                "Failed to parse config file.",
            ) from exc

        if not config.units:
            raise ConfigLoadError(
                "CFG_PARSE_ERROR",
                "Failed to parse config file.",
            )

        registry = UnitRegistry()
        for item in config.units:
            registry.register(item.id, item.meters_per_unit)
        return registry

    @staticmethod
    def default_feet_per_meter() -> float:
        return FEET_PER_METER

    @staticmethod
    def default_yard_per_meter() -> float:
        return YARD_PER_METER
