from __future__ import annotations

from entity.display import round_display
from entity.engine import ConversionLine


def format_source_value(value: float) -> str:
    """Preserve input magnitude without display rounding (e.g. 2.5, 5.0)."""
    if float(value).is_integer():
        return f"{float(value):.1f}"
    return f"{value}"


def render_table(
    source_unit: str,
    source_magnitude: float,
    lines: list[ConversionLine],
) -> str:
    source_str = format_source_value(source_magnitude)
    rows = []
    for line in lines:
        display = round_display(line.magnitude)
        display_str = f"{display:.1f}" if display != int(display) else f"{display:.1f}"
        rows.append(f"{source_str} {source_unit} = {display_str} {line.target_unit}")
    return "\n".join(rows)
