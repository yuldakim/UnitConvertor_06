## Summary
- tests/red TC-A-01~07, TC-B-01~07 GREEN (pytest 50 passed, 0 failed)
- JSON renderer and `ConverterApp.handle_convert_line_json` for TC-A-06
- `UnitConverter.main` delegates to BCE (no inline conversion ratios)
- entity 99% / boundary 89% line coverage (targets 95% / 85%)

## Test plan
- [x] `pytest -v tests/` — 50 passed
- [x] `--cov=entity --cov=boundary` — thresholds met
- [x] no 3.28084 / 1.09361 in boundary or control
- [x] main() has no conversion logic
