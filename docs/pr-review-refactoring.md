# PR 리뷰 초안 (`refactoring` → `B_06`)

> `gh auth login` 후:  
> `gh pr comment <번호> --body-file docs/pr-review-refactoring.md`

## Summary

- Dual-Track REFACTOR 완료: BCE 레이어 분리 유지, 외부 계약 불변.
- **68 tests passed**; Golden Master 8 (CLI subprocess 동치 포함).
- **boundary coverage 100%** (entity ~95%).

## Approval checklist

- [x] TC-A-01~07, TC-B-01~07 (RED + BCE)
- [x] Golden Master 출력 불변 + CLI = ConverterApp
- [x] No unit `if-else`; ratios in `entity/constants` only
- [x] `parse_register_line` / `run_convert_cli` tested
- [x] DEF-006: CLI exit 1 on parse error

## Notes

- `handle_register_line` remains Control-only (no CLI exposure) — intentional, not a blocker.
- Recommend **Squash merge** after CI `Golden Master Regression` is green.

## Suggested review comment (short)

LGTM — refactor-only diff, tests green, GM subprocess guard closes DEF-008. Boundary cov 100%. Safe to merge into `B_06` after CI.
