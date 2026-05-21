from __future__ import annotations

from pydantic import BaseModel


class ErrorEnvelope(BaseModel):
    code: str
    message: str


ERR_EMPTY_INPUT = ErrorEnvelope(code="ERR_EMPTY_INPUT", message="Input is empty.")
ERR_INVALID_FORMAT = ErrorEnvelope(
    code="ERR_INVALID_FORMAT",
    message="Invalid format. Use unit:value (ex: meter:2.5)",
)
ERR_INVALID_NUMBER = "ERR_INVALID_NUMBER"  # message built dynamically
ERR_NEGATIVE_VALUE = "ERR_NEGATIVE_VALUE"
ERR_UNKNOWN_UNIT = "ERR_UNKNOWN_UNIT"
CFG_PARSE_ERROR = ErrorEnvelope(code="CFG_PARSE_ERROR", message="Failed to parse config file.")
CFG_FILE_NOT_FOUND = ErrorEnvelope(code="CFG_FILE_NOT_FOUND", message="Config file not found.")


def invalid_number_message(value_str: str) -> str:
    return f"Invalid number: {value_str}"


def negative_value_message(value: float) -> str:
    return f"Value must be zero or positive: {value}"


def unknown_unit_message(unit: str) -> str:
    return f"Unknown unit: {unit}"
