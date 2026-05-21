## Summary
- Bonus feature: `decaying_unit.py` facade (`registerUnit`, `convert`, `convertAll`) via `UnitRegistry` + meter-hub `ConversionEngine`
- RED→GREEN: `tests/test_decaying_unit.py` (`@pytest.mark.bonus`, BT-01~06)
- Report 06 + prompting transcript export
- Existing `entity`/`control` `convert()` signatures unchanged

## Test plan
- [x] `pytest tests/` — 69 passed
- [x] `pytest -m bonus -v` — BT-01~06 PASS
- [x] `pytest -m golden_master -v` — 8 passed
- [x] TC-A / TC-B regression — PASS
- [x] Coverage: entity 95%, boundary 100%
- [x] `registerUnit("cubit", -1.0)` → ValueError (InvalidRatioError)

## Commits
- `6234f34` feat(feature): add registerUnit with OCP registry
- `785c739` docs: add Report 06 bonus registerUnit progress and transcript export
