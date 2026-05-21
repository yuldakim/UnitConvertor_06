from __future__ import annotations

import re
from dataclasses import dataclass

from entity.exceptions import NegativeMagnitudeError, UnknownUnitError
from entity.registry import UnitRegistry

from boundary.errors import (
    ERR_EMPTY_INPUT,
    ERR_INVALID_FORMAT,
    invalid_number_message,
    negative_value_message,
    unknown_unit_message,
)

_REGISTER_PATTERN = re.compile(
    r"^1\s+([a-z][a-z0-9_]*)\s*=\s*([0-9]+(?:\.[0-9]+)?)\s+meter\s*$"
)


@dataclass(frozen=True)
class ConvertCommand:
    unit_id: str
    magnitude: float


@dataclass(frozen=True)
class RegisterCommand:
    unit_id: str
    meters_per_unit: float


class ParseError(ValueError):
    def __init__(self, message: str, *, code: str = "ERR_INVALID_FORMAT") -> None:
        self.code = code
        self.message = message
        super().__init__(message)


def parse_convert_line(line: str, registry: UnitRegistry | None = None) -> ConvertCommand:
    if line is None or not str(line).strip():
        raise ParseError(ERR_EMPTY_INPUT.message, code=ERR_EMPTY_INPUT.code)

    text = line.strip()
    if text.count(":") != 1:
        raise ParseError(ERR_INVALID_FORMAT.message, code=ERR_INVALID_FORMAT.code)

    unit_id, value_str = text.split(":", 1)
    unit_id = unit_id.strip()
    value_str = value_str.strip()

    if not unit_id:
        raise ParseError(ERR_INVALID_FORMAT.message, code=ERR_INVALID_FORMAT.code)

    try:
        magnitude = float(value_str)
    except ValueError as exc:
        raise ParseError(
            invalid_number_message(value_str),
            code="ERR_INVALID_NUMBER",
        ) from exc

    if magnitude < 0:
        raise ParseError(
            negative_value_message(magnitude),
            code="ERR_NEGATIVE_VALUE",
        )

    if registry is not None:
        try:
            registry.get_meters_per_unit(unit_id)
        except UnknownUnitError as exc:
            raise ParseError(
                unknown_unit_message(unit_id),
                code="ERR_UNKNOWN_UNIT",
            ) from exc

    return ConvertCommand(unit_id=unit_id, magnitude=magnitude)


def parse_register_line(line: str) -> RegisterCommand:
    text = line.strip()
    match = _REGISTER_PATTERN.match(text)
    if not match:
        raise ParseError(
            ERR_INVALID_FORMAT.message,
            code="ERR_INVALID_REGISTER",
        )
    unit_id = match.group(1)
    factor = float(match.group(2))
    if factor <= 0:
        from entity.exceptions import InvalidRatioError

        raise InvalidRatioError(factor)
    return RegisterCommand(unit_id=unit_id, meters_per_unit=factor)
