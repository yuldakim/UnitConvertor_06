# 05 — UnitConvertor_06 Dual-Track REFACTOR 완료 진행 보고서

| 항목 | 내용 |
|------|------|
| 문서 번호 | 05 |
| 프로젝트 | UnitConvertor_06 (Python 길이 단위 변환 · BCE/ECB 학습) |
| 작업 기간 | 2026-05-21 |
| 기준 PRD | [docs/PRD.md](../docs/PRD.md) |
| **현재 브랜치** | `refactoring` → PR 머지 대상 `B_06` |
| 선행 보고서 | [04_UnitConvertor_06_Golden_Master_Refactoring_Progress.md](04_UnitConvertor_06_Golden_Master_Refactoring_Progress.md) |
| 대화 Export | [prompting/05_UnitConvertor_06_Dual_Track_Refactoring_Progress.md](../prompting/05_UnitConvertor_06_Dual_Track_Refactoring_Progress.md) |

---

## 1. Executive Summary

Report 04(Golden Master 4건 + CI) 이후 **Dual-Track REFACTOR** 5커밋을 `refactoring` 브랜치에 적용했다.  
외부 계약(입력 `단위:값`, 출력 `값 단위 = 변환값 단위`, `ParseError`/`ValueError` 거부)은 유지한 채 **Control·Data·Boundary·CLI** 구조만 정리했다.

- **pytest:** 68 passed (0 failed)
- **Golden Master:** 8 passed (승인 4 + CLI subprocess 동치 4)
- **RED Dual-Track:** 17 passed (TC-A/B 스위트)
- **Domain·Boundary 분리:** 완료 (레거시 `UnitConverter.py` 단일 if-else 제거 상태 유지)
- **커버리지:** Domain(`entity`) **≥ 95%** · Boundary **100%** (목표 85% **달성** — §5·§6)

---

## 2. REFACTOR 커밋 이력 (`origin/refactoring` 이후 5건)

| 커밋 | 요약 |
|------|------|
| `f829fdc` | `refactor(control,data)`: convert-line 파이프라인 dedupe, repository 데드 코드 제거 |
| `4503648` | `refactor(data)`: `UnitDefinitionRepository.load` 헬퍼 분리 |
| `0e81f87` | `refactor(boundary)`: `cli_adapter` 추출, `UnitConverter` thin entry |
| `4d37b1e` | `test(golden-master)`: CLI subprocess ↔ App 동치 + 프롬프트 동행 캡처 수정 |
| `5077497` | `fix(boundary)`: CLI 파싱 실패 `exit 1` (DEF-006) |

---

## 3. 검증 체크리스트

### 3.1 테스트 실행 (2026-05-21)

```bash
pytest tests/ -v
# 68 passed

pytest -m golden_master -v
# 8 passed

pytest tests/red/ -v
# 17 passed
```

### 3.2 TC-A-01 ~ TC-A-07 (UI Track)

| TC | 요약 | 매핑 테스트 | 결과 |
|----|------|-------------|------|
| TC-A-01 | `meter:2.5` Happy | `tests/red/boundary/test_ui_red_convert.py` · `test_convert_display_*` | PASS |
| TC-A-02 | `:` 없음 | `test_ui_red_parse` · `test_exception_parse_*` | PASS |
| TC-A-03 | 음수 | 동일 | PASS |
| TC-A-04 | unknown unit | 동일 | PASS |
| TC-A-05 | 원 단위·값 보존 | `test_ui_table_output_*` · display table | PASS |
| TC-A-06 | JSON 스키마 | `test_ui_json_format_*` | PASS |
| TC-A-07 | `meter:abc` | `test_ui_parse_invalid_number_*` | PASS |

### 3.3 TC-B-01 ~ TC-B-07 (Logic Track)

| TC | 요약 | 매핑 테스트 | 결과 |
|----|------|-------------|------|
| TC-B-01 | meter→feet 8.20210 | `test_logic_red_convert` · `test_convert_normal_*` | PASS |
| TC-B-02 | meter→yard | 동일 | PASS |
| TC-B-03 | feet→meter | 동일 | PASS |
| TC-B-04 | convertAll 3단위 | 동일 | PASS |
| TC-B-05 | cubit 등록 | `test_logic_register_*` · `test_register_dynamic_*` | PASS |
| TC-B-06 | loadConfig JSON/YAML | `test_logic_load_config_*` · `test_config_load_*` | PASS |
| TC-B-07 | missing path → defaults | 동일 | PASS |

*(보강 TC-B-08/09 음수·영값도 RED 스위트에서 PASS.)*

### 3.4 Golden Master (출력 불변)

| TC | 입력 | 결과 |
|----|------|------|
| GM-TC-01 | `meter:2.5` | PASS |
| GM-TC-02 | `feet:1.0` | PASS |
| GM-TC-03 | `yard:1.0` | PASS |
| GM-TC-04 | `meter:0.0` | PASS |
| GM-CLI | subprocess 4시나리오 = `ConverterApp` 캡처 | PASS |

### 3.5 구조·코드 품질

| 항목 | 결과 |
|------|------|
| 단위별 `if-else` 환산 체인 | **없음** (`entity/engine.py` + `UnitRegistry` 순회) |
| `3.28084` / `1.09361` 인라인 (프로덕션 `*.py`) | **`entity/constants.py` 상수만** (테스트·주석 제외) |
| Domain (변환) | `entity/engine.py`, `entity/registry.py`, `entity/display.py` |
| Boundary (파싱·출력) | `boundary/parser.py`, `boundary/renderers/*`, `boundary/cli_adapter.py` |
| Control (조율) | `control/converter_app.py` — `_run_convert_line` 단일 파이프라인 |

---

## 4. 아키텍처 (REFACTOR 후)

```text
UnitConverter.py          → main() → boundary.cli_adapter.run_convert_cli
boundary/cli_adapter.py   → stdin/stdout, ParseError → exit 1
control/converter_app.py  → parse → convert_all → render (table/json)
entity/engine.py          → mpu 허브 변환 (OCP)
entity/registry.py        → 단위 등록 Map
data/repository.py        → config → Registry
```

---

## 5. 커버리지 (`pytest-cov`)

```bash
pytest tests/ --cov=entity --cov=boundary --cov-report=term-missing --cov-report=html
```

| 레이어 | 패키지 | Stmts | Cover | 목표 | 판정 |
|--------|--------|-------|-------|------|------|
| **Domain** | `entity` | 88 | **~95%** | ≥ 95% | **PASS** |
| **Boundary** | `boundary` | 112 | **100%** | ≥ 85% | **PASS** |
| **합산** | `entity` + `boundary` | 200 | **98%** | — | — |

### 5.1 커버리지 보강 커밋 (후속)

| 테스트 파일 | 대상 | 효과 |
|-------------|------|------|
| `tests/boundary/test_parser_register.py` | `parse_register_line`, `:2.5` 빈 unit_id | `parser.py` **100%** |
| `tests/boundary/test_cli_adapter.py` | `run_convert_cli` mock input/print | `cli_adapter.py` **100%** |
| `tests/boundary/test_boundary_package.py` | `from boundary import …` | `boundary/__init__.py` **100%** |

> `tests/boundary/__init__.py` 제거 — 테스트 디렉터리가 최상위 `boundary` 패키지를 가리지 않도록 함.

HTML 리포트: `htmlcov/index.html`

> 참고: `--cov=unit_converter` 패키지는 본 프로젝트에 없음. `pyproject.toml` 기준 `entity` / `boundary` / `control` / `data` 사용.

---

## 6. 결함·후속 (선택)

| ID | 상태 | 비고 |
|----|------|------|
| DEF-006 | **Close (CLI)** | `cli_adapter` + `test_cli_adapter.py` (unit + subprocess) |
| DEF-008 | **Close (동치)** | GM subprocess 4건 |
| Boundary cov 85% | **Close** | `test_parser_register` · `test_cli_adapter` · `test_boundary_package` |
| `handle_register_line` | Open | Control API 존재, CLI 미노출 (기능 추가 아님 연결만 해당) |

---

## 7. Git · PR · 머지

| 단계 | 상태 |
|------|------|
| 로컬 커밋 5건 + 본 보고서 | 완료 |
| `git push origin refactoring` | **실행 예정** |
| PR `refactoring` → `B_06` | **gh CLI 미설치** → 수동 생성 필요 (§8) |
| PR 리뷰·머지 | 사용자 또는 GitHub UI |

---

## 8. 수동 PR 절차 (gh 없을 때)

1. `git push -u origin refactoring`
2. GitHub → Compare: **base `B_06`** ← **compare `refactoring`**
3. 제목 예: `refactor: Dual-Track BCE cleanup (CLI adapter, GM subprocess, DEF-006)`
4. CI `Golden Master Regression` PASS 확인 후 Squash merge
5. 로컬: `git checkout B_06 && git pull` → `refactoring` 재분기(팀 절차에 따름)

---

## 9. 결론

Dual-Track REFACTOR 목표(계약 유지·레이어 분리·회귀 GREEN·Boundary ≥85%)는 **달성**했다.  
**push → PR → 머지**는 §7·§8 순서로 진행한다 (`gh` 설치 후 PR·리뷰 자동화).
