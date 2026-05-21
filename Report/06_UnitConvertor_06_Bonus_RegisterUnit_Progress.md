# 06 — UnitConvertor_06 Bonus Feature (registerUnit / cubit) 진행 보고서

| 항목 | 내용 |
|------|------|
| 문서 번호 | 06 |
| 프로젝트 | UnitConvertor_06 (Python 길이 단위 변환 · BCE/ECB 학습) |
| 작업 기간 | 2026-05-21 |
| **현재 브랜치** | `feature` → PR 머지 대상 `B_06` |
| 선행 보고서 | [05_UnitConvertor_06_Dual_Track_Refactoring_Progress.md](05_UnitConvertor_06_Dual_Track_Refactoring_Progress.md) |
| 대화 Export | [prompting/06_UnitConvertor_06_Bonus_RegisterUnit_Progress.md](../prompting/06_UnitConvertor_06_Bonus_RegisterUnit_Progress.md) |

---

## 1. Executive Summary

Phase 6 REFACTOR(Report 05) 이후 **Bonus 신규 기능** — 동적 단위 등록(`registerUnit`) 및 cubit 변환 — 을 **TDD RED → GREEN**으로 완료했다.

- **산출 모듈:** `decaying_unit.py` (camelCase facade: `registerUnit`, `convert`, `convertAll`)
- **테스트:** `tests/test_decaying_unit.py` — `@pytest.mark.bonus`, `test_decaying_unit_conversion()` (BT-01~06)
- **구현 방식:** `UnitRegistry` + `ConversionEngine` 위임 (meter 허브, OCP 레지스트리)
- **기존 계약:** `entity`/`control`의 `convert()` 시그니처 **변경 없음**
- **최종 검증:** `pytest tests/` **69 passed** (bonus 1 + 기존 68)
- **커버리지:** Domain(`entity`) **95%** · Boundary **100%** (목표 Domain ≥95%, Boundary ≥85% **달성**)
- **Golden Master:** **8 passed** (meter/feet/yard 출력 불변)
- **커밋:** `6234f34` — `feat(feature): add registerUnit with OCP registry`

---

## 2. TDD 사이클

### 2.1 RED

| 단계 | 내용 |
|------|------|
| 스텁 | `decaying_unit.py` — 모든 메서드 `NotImplementedError` |
| 테스트 | BT-01~06, ε=1e-5, 음수 비율 → `ValueError`/`TypeError` |
| 실행 | `pytest -m bonus -v` → **1 failed** (`NotImplementedError`) |

**BT 시나리오**

| ID | Given / When / Then |
|----|---------------------|
| BT-01 | `registerUnit("cubit", 0.4572)` 후 `convert("cubit", 1.0, "meter")` ≈ 0.4572 |
| BT-02 | `convert("meter", 1.0, "cubit")` ≈ 1/0.4572 |
| BT-03 | `convert("cubit", 1.0, "feet")` ≈ 0.4572 × 3.28084 |
| BT-04 | `registerUnit("bad", -0.4572)` → `ValueError` / `TypeError` |
| BT-05 | `convertAll("cubit", 1.0)` → meter/feet/yard/cubit 4단위 |
| BT-06 | cubit 등록 후 `convert("meter", 2.5, "feet")` ≈ 8.20210 (회귀) |

### 2.2 GREEN

| 단계 | 내용 |
|------|------|
| 구현 | `DecayingUnitConverter` — `UnitRegistry.with_defaults()` + `register_unit` + `ConversionEngine` |
| 실행 | `pytest -m bonus -v` → **1 passed** |
| 회귀 | `pytest` → **69 passed** |

**음수 비율 검증 (수동·BT-04)**

```text
registerUnit("cubit", -1.0) → InvalidRatioError (ValueError 하위)
```

---

## 3. 검증 체크리스트 (2026-05-21)

### 3.1 전체 테스트

```bash
pytest -v tests/
# 69 passed
```

### 3.2 Bonus (BT)

```bash
pytest -m bonus -v
# 1 passed (test_decaying_unit_conversion)
```

### 3.3 Golden Master

```bash
pytest -m golden_master -v
# 8 passed
```

### 3.4 TC-A / TC-B 회귀

| Track | 범위 | 결과 |
|-------|------|------|
| TC-A | `tests/boundary/*`, `tests/red/boundary/*` | PASS |
| TC-B | `tests/entity/*`, `tests/red/entity/*`, `tests/data/*` | PASS |
| RED Dual-Track | `tests/red/` 17건 | PASS |

### 3.5 커버리지

```bash
pytest tests/ --cov=entity --cov=boundary --cov=control --cov=data --cov-report=term-missing --cov-report=html
```

| 레이어 | 목표 | 실측 |
|--------|------|------|
| Domain (`entity`) | ≥ 95% | **95%** |
| Boundary | ≥ 85% | **100%** |
| BCE 합계 | — | **95%** |

HTML: `htmlcov/index.html`

> `--cov=unit_converter` 패키지는 존재하지 않음. `pyproject.toml`의 `entity`/`boundary`/`control`/`data` 사용.

---

## 4. 아키텍처 (Bonus facade)

```text
decaying_unit.py
  registerUnit()  → UnitRegistry.register_unit()
  convert()       → ConversionEngine.convert()     # meter 허브
  convertAll()    → ConversionEngine.convert_all() → dict[str, float]
  reset()         → 테스트 격리용 싱글톤 초기화
```

기존 BCE 경로(`control/converter_app.py`, `entity/engine.py`)는 **미변경**. Bonus API는 별도 모듈로 OCP 확장.

---

## 5. 변경 파일 목록

| 파일 | 변경 |
|------|------|
| `decaying_unit.py` | **신규** — Bonus facade GREEN |
| `tests/test_decaying_unit.py` | **신규** — BT-01~06 bonus 테스트 |
| `pyproject.toml` | `bonus` pytest 마커 등록 |
| `Report/06_UnitConvertor_06_Bonus_RegisterUnit_Progress.md` | **신규** — 본 보고서 |
| `prompting/06_UnitConvertor_06_Bonus_RegisterUnit_Progress.md` | **신규** — Export Transcript |

---

## 6. PR · 원격 반영

| 항목 | 값 |
|------|-----|
| 소스 브랜치 | `feature` |
| 타깃 브랜치 | `B_06` |
| 커밋 | `6234f34` + 본 문서·transcript 커밋 |

---

## 7. 잔여·권장

| 항목 | 권장 |
|------|------|
| README Bonus To-Do | `[x]` BT-01~06, bonus 마커 안내 추가 |
| `decaying_unit` ↔ CLI 연동 | 선택 — 현재 Control-only register와 분리 유지 |
| REFACTOR | 본 단계에서 **미수행** (GREEN만 완료) |

---

*End of Report 06*
