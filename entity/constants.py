"""README / PRD contract ratios (1 meter = N target units for display reference)."""

from __future__ import annotations

# 1 meter = 3.28084 feet (display / README)
FEET_PER_METER: float = 3.28084
# 1 meter = 1.09361 yard (display / README)
YARD_PER_METER: float = 1.09361

# meters_per_unit: 1 {unit} = N meters (PRD §3.3)
METERS_PER_METER: float = 1.0
METERS_PER_FEET: float = 0.3048
METERS_PER_YARD: float = 0.9144

NUMERIC_EPSILON: float = 1e-4
DISPLAY_DECIMAL_PLACES: int = 1
