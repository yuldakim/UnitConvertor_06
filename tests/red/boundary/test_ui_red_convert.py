"""Track A — UI / Boundary RED: 정상 변환·포맷 보존."""

from __future__ import annotations

import json

import pytest

from control.converter_app import ConverterApp
from entity.constants import FEET_PER_METER


class TestUiRedConvertHappyPath:
    """TC-A-01, TC-A-05"""

    def test_ui_convert_meter_2_5_returns_conversion_result(
        self, converter_app: ConverterApp
    ) -> None:
        # TC-A-01: "meter:2.5" Happy path
        internal = converter_app.convert("meter", 2.5, "feet")
        assert internal == pytest.approx(2.5 * FEET_PER_METER, abs=1e-5)
        output = converter_app.handle_convert_line("meter:2.5")
        assert "2.5 meter = 8.2 feet" in output.splitlines()

    def test_ui_table_output_preserves_source_unit_and_value(
        self, converter_app: ConverterApp
    ) -> None:
        # TC-A-05: source 2.5 meter preserved in each line
        output = converter_app.handle_convert_line("meter:2.5")
        lines = output.splitlines()
        assert len(lines) == 3
        for line in lines:
            assert line.startswith("2.5 meter = ")


class TestUiRedJsonOutput:
    """TC-A-06"""

    def test_ui_json_format_meter_2_5_matches_schema(
        self, converter_app: ConverterApp
    ) -> None:
        # TC-A-06: JSON schema for meter:2.5
        raw = converter_app.handle_convert_line_json("meter:2.5")
        data = json.loads(raw)
        assert data["source"]["unit"] == "meter"
        assert data["source"]["value"] == 2.5
        assert len(data["conversions"]) == 3
        feet = next(c for c in data["conversions"] if c["unit"] == "feet")
        assert feet["value"] == 8.2
