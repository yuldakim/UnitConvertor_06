# 결함 목록 (Defect List)

| 항목 | 값 |
|------|-----|
| 문서 ID | DEF-UC-06-001 |
| 기준 | [test_plan.md](test_plan.md), [PRD.md](PRD.md), pytest `tests/` |
| 최종 검증 | `pytest` **33 passed** (BCE 스택, 2026-05-21) |
| 레거시 CLI | `UnitConverter.py` — 일부 결함 **Open** (본 문서 참조) |

> **심각도:** Critical · Major · Minor · Info  
> **상태:** `Fixed` = BCE 경로 수정·회귀 GREEN / `Open` = 미수정(주로 레거시 CLI)

---

## 결함 테이블

| ID | Severity | 변환 타입 | 재현 절차 | 기대값 | 실제값 | 근본 원인 | 수정 요약 |
|----|----------|-----------|-----------|--------|--------|-----------|-----------|
| DEF-001 | Critical | meter→feet | `pytest` `test_convert_normal_meter_to_feet_happy_returns_8_20210`; Engine 미연결 시 | `8.20210` (ε≤1e-5) | `0.000000` | `convert()` 미구현·스텁 0 반환; `UnitConverter.py`는 테스트 대상 아님 | **Fixed** — `entity/engine.py:19-25` `source_meters/mpu_target`; `control/converter_app.py` wiring |
| DEF-002 | Minor | meter→feet (표시) | 레거시 `python UnitConverter.py` → `meter:2.5` | `2.5 meter = 8.2 feet` | `2.5 meter = 8.2021 feet` | `UnitConverter.py:30-32` print에 ROUND_HALF_UP 없음 | **Fixed (BCE)** — `boundary/renderers/table.py`, `entity/display.py`. **Open (레거시)** — `display_one()` + if-else 유지 |
| DEF-003 | Major | 입력 검증 (음수) | `meter:-1.0` 레거시 CLI 또는 parser 테스트 | `ValueError`, `Value must be zero or positive: -1` | 예외 없이 환산 출력 | `UnitConverter.py:16-32` 음수 검증 누락 | **Fixed (BCE)** — `boundary/parser.py:62-66`, `entity/engine.py:20-21`. **Open (레거시)** — `if value < 0:` print·return |
| DEF-004 | Major | meter→feet (경계) | `test_convert_boundary_large_value_finite_not_inf`, `meter:1e100` | 유한값, 비율 ≈ 3.28084 | `pytest.approx` rel/절대 실패 | 초대형 float 표현 차이; assert 방식 부적합 | **Fixed** — `tests/entity/test_convert_boundary_precision.py:48` 비율 검증 `result/large` |
| DEF-005 | Major | config 로드 | `load(empty.yaml)` `units: []` | `ConfigLoadError` | 빈 Registry, 예외 없음 | `data/repository.py` 빈 리스트 미검증 | **Fixed** — `if not config.units: raise ConfigLoadError` |
| DEF-006 | Major | 형식/미등록 | `meter 2.5`, `parsec:1.0` 레거시 `main()` | exact message, exit ≠ 0 | message만, exit 0 | `UnitConverter.py` `sys.exit(1)` 없음 | **Fixed (BCE)** — `boundary/parser.py`. **Open (레거시)** — 실패 시 `sys.exit(1)` |
| DEF-007 | Minor | feet→meter (역변환) | `feet:8.2` 레거시 CLI | PRD table 3줄(단위별 환산) | 허브×비율 3줄만 출력 | `UnitConverter.py:16-32` if-else 후 단일 허브 출력 | **Fixed (BCE)** — `convert_all` + `render_table`. **Open (레거시)** — App 위임 또는 동일 로직 |
| DEF-008 | Info | meter→feet | `pytest` GREEN 후 `python UnitConverter.py` | `8.2 feet` | `8.2021 feet` | 테스트는 BCE, CLI는 레거시 이중 경로 | **Open** — Quick Start·CLI를 `ConverterApp`으로 통일 또는 DEF-002·003 패치 |

---

## 레거시 CLI 최소 수정 참고 (if-else 유지)

`UnitConverter.py`만 GREEN에 가깝게 맞출 때 (구조체·Item 변경 없음):

```python
# DEF-003: line 14 직후
if value < 0:
    print(f"Value must be zero or positive: {value}")
    return

# DEF-002: print 직전 display 헬퍼 (decimal ROUND_HALF_UP)
# DEF-006: 실패 return 직전 import sys; sys.exit(1)
```

---

## 결함 ↔ 테스트 매핑

| ID | 관련 테스트 (GREEN 기준) |
|----|-------------------------|
| DEF-001 | `tests/entity/test_convert_normal_happy_path.py` |
| DEF-002 | `tests/boundary/test_convert_display_table.py` |
| DEF-003 | `tests/boundary/test_exception_parse_policy.py` |
| DEF-004 | `tests/entity/test_convert_boundary_precision.py` |
| DEF-005 | `tests/data/test_config_load_json_yaml.py` |
| DEF-006 | `tests/boundary/test_exception_parse_policy.py`, AC-02/03 |
| DEF-007 | `tests/entity/test_convert_normal_happy_path.py` (역변환), display |
| DEF-008 | 수동 CLI vs `pytest` (문서/운영) |

---

## 회귀 확인

```bash
pip install -e ".[dev]"
pytest -v --tb=short
# 기대: 33 passed
```

| 일자 | 실행 결과 | 비고 |
|------|-----------|------|
| 2026-05-21 | 33 passed | DEF-001,004,005 BCE 수정 반영 |
| — | — | DEF-002,003,006,007,008 레거시 `UnitConverter.py` 잔여 |

---

## 변경 이력

| 버전 | 일자 | 요약 |
|------|------|------|
| 1.0 | 2026-05-21 | 최초 작성 — RED/GREEN 세션 발견 결함 8건 |
