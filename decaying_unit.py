"""Bonus: dynamic unit registration facade (meter-hub via UnitRegistry)."""

from __future__ import annotations

from entity.engine import ConversionEngine
from entity.registry import UnitRegistry


class DecayingUnitConverter:
    """Stateful converter: registerUnit adds units; convert uses meter hub."""

    def __init__(self) -> None:
        self._registry = UnitRegistry.with_defaults()
        self._engine = ConversionEngine(self._registry)

    def registerUnit(self, unit_id: str, meters_per_unit: float) -> None:
        self._registry.register_unit(unit_id, meters_per_unit)

    def convert(self, source_unit: str, magnitude: float, target_unit: str) -> float:
        return self._engine.convert(source_unit, magnitude, target_unit)

    def convertAll(self, source_unit: str, magnitude: float) -> dict[str, float]:
        lines = self._engine.convert_all(source_unit, magnitude)
        return {line.target_unit: line.magnitude for line in lines}


_default: DecayingUnitConverter | None = None


def _get_default() -> DecayingUnitConverter:
    global _default
    if _default is None:
        _default = DecayingUnitConverter()
    return _default


def reset() -> None:
    """Clear module singleton (test isolation)."""
    global _default
    _default = None


def registerUnit(unit_id: str, meters_per_unit: float) -> None:
    _get_default().registerUnit(unit_id, meters_per_unit)


def convert(source_unit: str, magnitude: float, target_unit: str) -> float:
    return _get_default().convert(source_unit, magnitude, target_unit)


def convertAll(source_unit: str, magnitude: float) -> dict[str, float]:
    return _get_default().convertAll(source_unit, magnitude)
