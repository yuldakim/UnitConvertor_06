"""CLI stdin/stdout adapter — delegates conversion to Control (ConverterApp)."""

from __future__ import annotations

from boundary.parser import ParseError
from control.converter_app import ConverterApp

CONVERT_PROMPT = "Insert value for converting (ex: meter:2.5): "


def run_convert_cli(app: ConverterApp | None = None) -> None:
    converter = app or ConverterApp()
    input_str = input(CONVERT_PROMPT)
    try:
        print(converter.handle_convert_line(input_str))
    except ParseError as exc:
        print(exc.message)
