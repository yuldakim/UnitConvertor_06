from __future__ import annotations

from decimal import ROUND_HALF_UP, Decimal

from entity.constants import DISPLAY_DECIMAL_PLACES


def round_display(value: float) -> float:
    """Boundary display contract: 1 decimal ROUND_HALF_UP."""
    quant = Decimal("0.1")
    return float(Decimal(str(value)).quantize(quant, rounding=ROUND_HALF_UP))
