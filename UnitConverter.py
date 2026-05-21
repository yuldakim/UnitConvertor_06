"""Legacy CLI entry — delegates to boundary.cli_adapter (no conversion logic here)."""

from __future__ import annotations

from boundary.cli_adapter import run_convert_cli


def main() -> None:
    run_convert_cli()


if __name__ == "__main__":
    main()
