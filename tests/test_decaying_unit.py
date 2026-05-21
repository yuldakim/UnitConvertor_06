"""RED — bonus decaying unit (cubit) dynamic registration."""

from __future__ import annotations

import pytest

import decaying_unit as du

CUBIT_METERS_PER_UNIT = 0.4572
FEET_PER_METER = 3.28084
METER_TO_FEET_2_5 = 8.20210
EPS = 1e-5


@pytest.fixture(autouse=True)
def _isolated_decaying_unit_state() -> None:
    du.reset()
    yield
    du.reset()


@pytest.mark.bonus
def test_decaying_unit_conversion() -> None:
    """BT-01~06: cubit 등록·변환·검증·회귀 (RED — decaying_unit 미구현)."""

    # BT-01: registerUnit("cubit", 0.4572) 후 cubit→meter
    du.registerUnit("cubit", CUBIT_METERS_PER_UNIT)
    assert du.convert("cubit", 1.0, "meter") == pytest.approx(
        CUBIT_METERS_PER_UNIT, abs=EPS
    )

    # BT-02: meter→cubit 역변환 (1/0.4572 ≈ 2.1872)
    assert du.convert("meter", 1.0, "cubit") == pytest.approx(
        1.0 / CUBIT_METERS_PER_UNIT, abs=EPS
    )

    # BT-03: cubit→feet 교차 변환
    expected_feet = CUBIT_METERS_PER_UNIT * FEET_PER_METER
    assert du.convert("cubit", 1.0, "feet") == pytest.approx(expected_feet, abs=EPS)

    # BT-04: 음수 비율 등록 → ValueError / TypeError
    du.reset()
    with pytest.raises((ValueError, TypeError)):
        du.registerUnit("bad", -0.4572)

    # BT-05: convertAll("cubit", 1.0) → 전 단위
    du.registerUnit("cubit", CUBIT_METERS_PER_UNIT)
    results = du.convertAll("cubit", 1.0)
    assert set(results.keys()) == {"meter", "feet", "yard", "cubit"}
    assert results["meter"] == pytest.approx(CUBIT_METERS_PER_UNIT, abs=EPS)
    assert results["feet"] == pytest.approx(expected_feet, abs=EPS)
    assert results["cubit"] == pytest.approx(1.0, abs=EPS)

    # BT-06: meter→feet 회귀 보호 (cubit 등록 후에도 불변)
    assert du.convert("meter", 2.5, "feet") == pytest.approx(METER_TO_FEET_2_5, abs=EPS)
