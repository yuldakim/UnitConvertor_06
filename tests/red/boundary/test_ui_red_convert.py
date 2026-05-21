"""Track A — UI / Boundary RED: 정상 변환·포맷 보존."""

from __future__ import annotations

import pytest


class TestUiRedConvertHappyPath:
    """TC-A-01, TC-A-05"""

    def test_ui_convert_meter_2_5_returns_conversion_result(self) -> None:
        pytest.fail("RED")

    def test_ui_table_output_preserves_source_unit_and_value(self) -> None:
        pytest.fail("RED")


class TestUiRedJsonOutput:
    """TC-A-06"""

    def test_ui_json_format_meter_2_5_matches_schema(self) -> None:
        pytest.fail("RED")
