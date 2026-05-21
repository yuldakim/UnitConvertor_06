"""Legacy CLI entry — delegates to BCE ConverterApp (no conversion logic here)."""

from __future__ import annotations

from boundary.parser import ParseError
from control.converter_app import ConverterApp


def main() -> None:
    input_str = input("Insert value for converting (ex: meter:2.5): ")
    app = ConverterApp()
    try:
        print(app.handle_convert_line(input_str))
    except ParseError as exc:
        print(exc.message)


if __name__ == "__main__":
    main()
