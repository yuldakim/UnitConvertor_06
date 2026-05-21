"""Track A — UI / Boundary RED: 파싱·검증 예외."""

from __future__ import annotations

import pytest

from boundary.errors import ERR_INVALID_FORMAT
from boundary.parser import parse_convert_line
from entity.registry import UnitRegistry


class TestUiRedParseErrors:
    """TC-A-02, TC-A-03, TC-A-04, TC-A-07"""

    @pytest.fixture
    def registry(self) -> UnitRegistry:
        return UnitRegistry.with_defaults()

    def test_ui_parse_missing_colon_raises_value_error(
        self, registry: UnitRegistry
    ) -> None:
        # TC-A-02: "meter 2.5"
        with pytest.raises((ValueError, TypeError)) as exc_info:
            parse_convert_line("meter 2.5", registry)
        assert ERR_INVALID_FORMAT.message in str(exc_info.value)

    def test_ui_parse_negative_meter_raises_value_error(
        self, registry: UnitRegistry
    ) -> None:
        # TC-A-03: "meter:-1.0"
        with pytest.raises((ValueError, TypeError)) as exc_info:
            parse_convert_line("meter:-1.0", registry)
        assert "Value must be zero or positive: -1.0" in str(exc_info.value)

    def test_ui_parse_unknown_unit_parsec_raises_value_error(
        self, registry: UnitRegistry
    ) -> None:
        # TC-A-04: "parsec:1.0"
        with pytest.raises((ValueError, TypeError)) as exc_info:
            parse_convert_line("parsec:1.0", registry)
        assert "Unknown unit: parsec" in str(exc_info.value)

    def test_ui_parse_invalid_number_abc_raises_value_error(self) -> None:
        pytest.fail("RED")
