from __future__ import annotations


class NegativeMagnitudeError(ValueError):
    def __init__(self, value: float) -> None:
        self.value = value
        super().__init__(f"Value must be zero or positive: {value}")


class UnknownUnitError(ValueError):
    def __init__(self, unit_id: str) -> None:
        self.unit_id = unit_id
        super().__init__(f"Unknown unit: {unit_id}")


class InvalidRatioError(ValueError):
    def __init__(self, ratio: float) -> None:
        self.ratio = ratio
        super().__init__(f"Meters per unit must be positive: {ratio}")


class DuplicateUnitError(ValueError):
    def __init__(self, unit_id: str) -> None:
        self.unit_id = unit_id
        super().__init__(f"Unit already registered: {unit_id}")
