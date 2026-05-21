"""GM-TC-01 … GM-TC-04: UnitConverter Golden Master / Approval regression tests."""

from __future__ import annotations

import pytest

from tests.golden_master import GOLDEN_MASTER_PATH, approve_section

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
