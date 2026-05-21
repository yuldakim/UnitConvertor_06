from __future__ import annotations

from entity.constants import METERS_PER_FEET, METERS_PER_METER, METERS_PER_YARD
from entity.exceptions import DuplicateUnitError, InvalidRatioError, UnknownUnitError


class UnitRegistry:
    def __init__(self) -> None:
        self._meters_per_unit: dict[str, float] = {}
        self._order: list[str] = []

    def register(self, unit_id: str, meters_per_unit: float, *, allow_replace: bool = False) -> None:
        if meters_per_unit <= 0:
            raise InvalidRatioError(meters_per_unit)
        if unit_id in self._meters_per_unit and not allow_replace:
            raise DuplicateUnitError(unit_id)
        if unit_id not in self._meters_per_unit:
            self._order.append(unit_id)
        self._meters_per_unit[unit_id] = meters_per_unit

    def register_unit(self, unit_id: str, meters_per_unit: float) -> None:
        """Alias for dynamic registration (1 unit = N meter)."""
        self.register(unit_id, meters_per_unit)

    def get_meters_per_unit(self, unit_id: str) -> float:
        if unit_id not in self._meters_per_unit:
            raise UnknownUnitError(unit_id)
        return self._meters_per_unit[unit_id]

    def list_unit_ids(self) -> list[str]:
        return list(self._order)

    def count(self) -> int:
        return len(self._order)

    @classmethod
    def with_defaults(cls) -> UnitRegistry:
        registry = cls()
        registry.register("meter", METERS_PER_METER)
        registry.register("feet", METERS_PER_FEET)
        registry.register("yard", METERS_PER_YARD)
        return registry
