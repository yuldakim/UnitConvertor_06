from __future__ import annotations

from entity.engine import ConversionEngine
from entity.registry import UnitRegistry

from boundary.parser import ConvertCommand, RegisterCommand, parse_convert_line, parse_register_line
from boundary.renderers.table import render_table
from data.repository import UnitDefinitionRepository


class ConverterApp:
    def __init__(self, registry: UnitRegistry | None = None) -> None:
        self._registry = registry or UnitRegistry.with_defaults()
        self._engine = ConversionEngine(self._registry)

    @property
    def registry(self) -> UnitRegistry:
        return self._registry

    @property
    def engine(self) -> ConversionEngine:
        return self._engine

    def register_unit(self, unit_id: str, meters_per_unit: float) -> None:
        self._registry.register_unit(unit_id, meters_per_unit)

    def load_config(self, path: str) -> None:
        self._registry = UnitDefinitionRepository.load(path)
        self._engine = ConversionEngine(self._registry)

    def convert(self, source_unit: str, magnitude: float, target_unit: str) -> float:
        return self._engine.convert(source_unit, magnitude, target_unit)

    def convert_all(self, source_unit: str, magnitude: float):
        return self._engine.convert_all(source_unit, magnitude)

    def handle_convert_line(self, line: str) -> str:
        command = parse_convert_line(line, self._registry)
        lines = self._engine.convert_all(command.unit_id, command.magnitude)
        return render_table(command.unit_id, command.magnitude, lines)

    def handle_register_line(self, line: str) -> str:
        command = parse_register_line(line)
        self._registry.register_unit(command.unit_id, command.meters_per_unit)
        return f"Registered: 1 {command.unit_id} = {command.meters_per_unit} meter"
