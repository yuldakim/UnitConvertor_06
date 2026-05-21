# 04 — UnitConvertor_06 Golden Master·Refactoring 준비 진행 보고서

| 항목 | 내용 |
|------|------|
| 문서 번호 | 04 |
| 프로젝트 | UnitConvertor_06 (Python 길이 단위 변환 학습 시스템) |
| 작업 기간 | 2026-05-21 |
| 기준 PRD | [docs/PRD.md](../docs/PRD.md) (PRD-UC-06-001) |
| **현재 브랜치** | `refactoring` → PR 머지 후 `B_06` 기준 재생성 예정 |
| 선행 보고서 | [03_UnitConvertor_06_Green_TDD_Implementation_Progress.md](03_UnitConvertor_06_Green_TDD_Implementation_Progress.md) |
| 작성 | AI 보조 세션 (Golden Master · 브랜치 정리 · CI) |

---

## 1. Executive Summary

Report 03(GREEN 50건 PASS) 이후 **Refactoring 전 회귀 안전장치**로 Golden Master(Approval) 테스트를 구축했다. 자체 approve 패턴(`golden_master_expected.txt` + 섹션별 `approve_section`)을 채택했으며 **approvaltests 라이브러리는 미사용**.

브랜치: 원격·로컬 `green` 삭제 → `B_06`에서 `refactoring` 생성·푸시. 본 세션 산출물을 `refactoring` → `B_06` PR로 통합하고, 머지 후 **깨끗한 `refactoring` 브랜치를 `B_06`에서 재분기**한다.

**GM To-Do:** GM-01~GM-09 전항 완료 · **GM-08** `B_06` branch protection + required check `Golden Master Regression`.

---

## 2. 브랜치·Git 상태

| 항목 | 값 |
|------|-----|
| 기준 브랜치 | `B_06` (GREEN·TC 커밋 누적) |
| 작업 브랜치 | `refactoring` (Golden Master + README + CI) |
| 삭제 | `green` (로컬·`origin/green`) |
| 원격 | `origin/refactoring`, `origin/B_06` |

### 브랜치 정리 (본 세션)

1. `green` 브랜치 삭제 (로컬·원격)
2. `B_06` HEAD에서 `refactoring` 생성 및 `origin/refactoring` 푸시
3. Golden Master·CI·README 변경 커밋 → PR(`refactoring` → `B_06`)
4. PR 머지 후 `B_06` pull → `refactoring` 삭제·재생성 → 체크아웃

---

## 3. Golden Master 회귀 테스트

### 3.1 산출물

| 파일 | 역할 |
|------|------|
| `tests/golden_master_expected.txt` | 4시나리오 섹션 기준 출력 |
| `tests/golden_master.py` | 캡처·파싱·approve·unified diff |
| `tests/test_golden_master.py` | GM-TC-01~04 (`@pytest.mark.golden_master`) |
| `scripts/generate_golden_master.py` | 기준 파일 생성·`--check` |

### 3.2 입력 시나리오 (4)

| TC | 입력 | 기준 섹션 |
|----|------|-----------|
| GM-TC-01 | `meter:2.5` | `[meter:2.5]` |
| GM-TC-02 | `feet:1.0` | `[feet:1.0]` |
| GM-TC-03 | `yard:1.0` | `[yard:1.0]` |
| GM-TC-04 | `meter:0.0` | `[meter:0.0]` |

표시 계약: 소수 1자리 ROUND_HALF_UP (예: `8.2 feet`, `2.7 yard`).

### 3.3 Approve 패턴

- 캡처: `io.StringIO` + `contextlib.redirect_stdout` + `ConverterApp.handle_convert_line`
- 기준 없음 → 전체 `golden_master_expected.txt` 생성 후 FAIL (리뷰·`git add` 안내)
- 기준 있음 → 섹션 body만 `open().read()` 비교
- 불일치 → `--- expected` / `+++ actual` / `@@` unified diff 후 FAIL

### 3.4 테스트 실행 결과

```bash
pytest -m golden_master -v
# 4 passed, 50 deselected
```

---

## 4. README Golden Master To-Do

[README.md](../README.md) **RED**와 **GREEN** 사이에 `## Golden Master 회귀 안전장치` 섹션 추가.

| ID | 내용 | 상태 |
|----|------|------|
| GM-01 | `golden_master_expected.txt` (meter:2.5) | ✅ |
| GM-02 | feet / yard / meter:0.0 시나리오 | ✅ |
| GM-03 | git 버전 관리 (`tests/golden_master_expected.txt`) | ✅ |
| GM-04 | `test_golden_master.py` 작성 | ✅ |
| GM-05 | approve 패턴 | ✅ |
| GM-06 | `pytest -m golden_master -v` PASS | ✅ |
| GM-07 | `.github/workflows/golden_master.yml` | ✅ |
| GM-08 | PR required status check | ✅ `B_06` protection API 적용 |
| GM-09 | Refactoring 후 Golden Master PASS | ✅ (현재 baseline) |

---

## 5. CI · GM-08 (Required Status Check)

### 5.1 워크플로

파일: [.github/workflows/golden_master.yml](../.github/workflows/golden_master.yml)

- 트리거: `push` / `pull_request` on `main`, `B_06`, `refactoring`
- Job 이름(CI 표시): **`Golden Master Regression`**
- 명령: `pip install -e ".[dev]"` → `pytest -m golden_master -v`

### 5.2 GM-08 Branch protection (적용 완료)

- 대상 브랜치: **`B_06`**
- Required status check: **`Golden Master Regression`**
- PR #2 머지 후 GitHub API로 protection rule 설정 완료
- Actions 워크플로 최초 GREEN 실행 후 체크가 PR UI에 표시됨 (규칙은 선적용)

---

## 6. approvaltests vs 자체 Golden Master

| | 자체 구현 (채택) | approvaltests (미채택) |
|--|------------------|-------------------------|
| 기준 파일 | `golden_master_expected.txt` (섹션 형식) | `*.approved.txt` per test |
| 비교 | `approve_section` + `difflib` | `verify(actual)` |
| 의존성 | 없음 | `approvaltests` 패키지 |

---

## 7. 변경 파일 요약

| 구분 | 경로 |
|------|------|
| 신규 | `tests/golden_master_expected.txt`, `tests/golden_master.py`, `tests/test_golden_master.py` |
| 신규 | `scripts/generate_golden_master.py`, `.github/workflows/golden_master.yml` |
| 신규 | `Report/04_...`, `prompting/04_...` |
| 수정 | `README.md`, `pyproject.toml` (marker, coverage source) |
| 삭제 | `tests/test_golden_master_approval.py` (→ `test_golden_master.py`로 대체) |

---

## 8. 다음 작업

- [x] GM-08: `B_06` branch protection + `Golden Master Regression` required check
- [ ] REFACTOR 단계 (Golden Master 4건 PASS 유지)
- [ ] 전체 `pytest tests/` + cov 90%+ (Report 03 잔여)
- [ ] 레거시 CLI 결함 DEF-002,003,006~008

---

## 9. 승인·검토

- [ ] QA: `pytest -m golden_master -v` 4 passed 로그
- [ ] QA: CI workflow `Golden Master` job PASS (push 후)
- [x] Admin: GM-08 branch protection 설정 완료 (`B_06`)
- [ ] 학습자: `B_06` 머지 후 새 `refactoring` 브랜치에서 작업 재개

---

*문서 끝.*
