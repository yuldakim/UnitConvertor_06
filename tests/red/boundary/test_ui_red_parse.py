"""Track A — UI / Boundary RED: 파싱·검증 예외."""

from __future__ import annotations

import pytest


class TestUiRedParseErrors:
    """TC-A-02, TC-A-03, TC-A-04, TC-A-07"""

    def test_ui_parse_missing_colon_raises_value_error(self) -> None:
        pytest.fail("RED")

    def test_ui_parse_negative_meter_raises_value_error(self) -> None:
        pytest.fail("RED")

    def test_ui_parse_unknown_unit_parsec_raises_value_error(self) -> None:
        pytest.fail("RED")

    def test_ui_parse_invalid_number_abc_raises_value_error(self) -> None:
        pytest.fail("RED")
