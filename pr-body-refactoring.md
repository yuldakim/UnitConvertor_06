## Summary
- Dual-Track REFACTOR 5 commits: control pipeline dedupe, data `load()` extract, `boundary/cli_adapter`, Golden Master CLI parity, DEF-006 exit code
- **68 pytest passed** (RED 17 + BCE 43 + GM 8); contracts unchanged (`unit:value`, table lines, `ParseError`)
- Legacy unit `if-else` removed; ratios only in `entity/constants.py`
- Report: `Report/05_UnitConvertor_06_Dual_Track_Refactoring_Progress.md`

## Test plan
- [x] `pytest tests/ -v` — 68 passed
- [x] `pytest -m golden_master -v` — 8 passed (output unchanged + CLI subprocess match)
- [x] `pytest tests/red/ -v` — 17 passed (TC-A-01~07, TC-B-01~07)
- [x] `--cov=entity --cov=boundary` — entity **~95%**, boundary **100%** (see report §5)
- [x] No inline `3.28084` / `1.09361` in production code outside `entity/constants.py`

## Coverage note
`--cov=unit_converter` N/A (packages: `entity`, `boundary`, `control`, `data`).
