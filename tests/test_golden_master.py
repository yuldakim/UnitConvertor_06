"""GM-TC-01 … GM-TC-04: UnitConverter Golden Master / Approval regression tests."""

from __future__ import annotations

import pytest

from tests.golden_master import (
    GOLDEN_MASTER_PATH,
    SCENARIOS,
    approve_section,
    capture_scenario_output,
    capture_scenario_output_subprocess,
)

# GM-TC-01
@pytest.mark.golden_master
def test_golden_master_meter_2_5(converter_app) -> None:
    approve_section("meter:2.5", GOLDEN_MASTER_PATH, app=converter_app)


# GM-TC-02
@pytest.mark.golden_master
def test_golden_master_feet_1_0(converter_app) -> None:
    approve_section("feet:1.0", GOLDEN_MASTER_PATH, app=converter_app)


# GM-TC-03
@pytest.mark.golden_master
def test_golden_master_yard_1_0(converter_app) -> None:
    approve_section("yard:1.0", GOLDEN_MASTER_PATH, app=converter_app)


# GM-TC-04
@pytest.mark.golden_master
def test_golden_master_meter_0_0(converter_app) -> None:
    approve_section("meter:0.0", GOLDEN_MASTER_PATH, app=converter_app)


@pytest.mark.golden_master
@pytest.mark.parametrize("scenario", SCENARIOS)
def test_golden_master_cli_subprocess_matches_app(scenario: str, converter_app) -> None:
    """UnitConverter.py CLI path must match ConverterApp capture (DEF-008 guard)."""
    via_app = capture_scenario_output(scenario, converter_app)
    via_cli = capture_scenario_output_subprocess(scenario)
    assert via_cli == via_app
