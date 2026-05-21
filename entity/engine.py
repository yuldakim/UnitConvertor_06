from __future__ import annotations

from dataclasses import dataclass

from entity.exceptions import NegativeMagnitudeError
from entity.registry import UnitRegistry


@dataclass(frozen=True)
class ConversionLine:
    target_unit: str
    magnitude: float


class ConversionEngine:
    def __init__(self, registry: UnitRegistry) -> None:
        self._registry = registry

    def convert(self, source_unit: str, magnitude: float, target_unit: str) -> float:
        if magnitude < 0:
            raise NegativeMagnitudeError(magnitude)
        mpu_source = self._registry.get_meters_per_unit(source_unit)
        mpu_target = self._registry.get_meters_per_unit(target_unit)
        source_meters = magnitude * mpu_source
        return source_meters / mpu_target

    def convert_all(self, source_unit: str, magnitude: float) -> list[ConversionLine]:
        if magnitude < 0:
            raise NegativeMagnitudeError(magnitude)
        return [
            ConversionLine(unit_id, self.convert(source_unit, magnitude, unit_id))
            for unit_id in self._registry.list_unit_ids()
        ]
