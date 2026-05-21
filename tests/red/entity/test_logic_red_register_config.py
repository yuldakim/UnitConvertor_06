"""Track B — Domain / Logic RED: registerUnit · loadConfig."""

from __future__ import annotations

import pytest


class TestLogicRedRegisterUnit:
    """TC-B-05"""

    def test_logic_register_unit_cubit_then_convert_to_feet(self) -> None:
        pytest.fail("RED")


class TestLogicRedLoadConfig:
    """TC-B-06, TC-B-07"""

    def test_logic_load_config_valid_json_applies_ratios(self) -> None:
        pytest.fail("RED")

    def test_logic_load_config_valid_yaml_applies_ratios(self) -> None:
        pytest.fail("RED")

    def test_logic_load_config_missing_path_keeps_default_ratios(self) -> None:
        pytest.fail("RED")
