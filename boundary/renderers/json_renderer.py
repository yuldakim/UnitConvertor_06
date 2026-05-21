from __future__ import annotations

import json

from entity.display import round_display
from entity.engine import ConversionLine


def render_json(
    source_unit: str,
    source_magnitude: float,
    lines: list[ConversionLine],
) -> str:
    payload = {
        "source": {"unit": source_unit, "value": source_magnitude},
        "conversions": [
            {
                "unit": line.target_unit,
                "value": round_display(line.magnitude),
            }
            for line in lines
        ],
    }
    return json.dumps(payload)
