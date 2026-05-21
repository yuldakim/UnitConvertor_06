# Dual-Track RED 테스트 명세

| 항목 | 값 |
|------|-----|
| 문서 ID | RED-UC-06-DT-001 |
| 기준 | [PRD.md](../PRD.md) F-01~F-07, [test_plan.md](../test_plan.md), `.cursorrules` `tdd_rules.red_phase` |
| 현재 구현 상태 | `UnitConverter.py` 단일 `main()`, if-else, **예외·Domain API 없음** |
| 금지 | 구현 코드 / GREEN / REFACTOR |
| 비율 (고정) | **1 meter = 3.28084 feet**, **1 meter = 1.09361 yard** (`meters_per_unit`: feet `0.3048`, yard `0.9144`) |

**RED 통과 정의:** pytest 실행 시 아래 assert가 **의도적으로 실패** (미구현·계약 불일치).  
**실패 예시 (레거시):** `meter:2.5` → stdout `8.2021 feet` (반올림 없음); `meter:-1.0` → 예외 없음; `convert()` API **AttributeError**.

---

# UI RED Tests — Test ID / Given/When/Then / Invariant

## TC-A-01 — 정상 입력 Happy Path

| 필드 | 내용 |
|------|------|
| **테스트 이름** | `test_ui_convert_meter_2_5_returns_conversion_result` |
| **Given** | 기본 Registry(meter, feet, yard). 입력 문자열 `"meter:2.5"`. **1 meter = 3.28084 feet**. |
| **When** | Boundary가 문자열을 파싱하고 변환 결과(또는 table/JSON 렌더 입력)를 반환한다. |
| **Then** | 성공 응답; feet 환산 **내부값** `≈ 8.20210` (ε≤1e-5) 또는 프로젝트 출력 계약 `"2.5 meter = 8.202100 feet"` 라인 포함; exit `0`. |
| **보호 Invariant** | **F-01** 변환 성공; **D-INV-03** meter 앵커 환산; **G-02** 비율 고정 |
| **RED 실패 상태** | `main()` only → **반환값 없음**(print만); 테스트는 `ConversionResult`/`handle_convert_line` 기대 → **ImportError / assert None** |

---

## TC-A-02 — `:` 없는 입력 (잘못된 형식)

| 필드 | 내용 |
|------|------|
| **테스트 이름** | `test_ui_parse_missing_colon_raises_value_error` |
| **Given** | 입력 `"meter 2.5"` (`:` 0회). |
| **When** | `parse_convert_line(input)` 호출. |
| **Then** | **`ValueError` 또는 `TypeError`** 발생; message exact: `Invalid format. Use unit:value (ex: meter:2.5)` (PRD **ERR_INVALID_FORMAT**). |
| **보호 Invariant** | **F-02** 형식 검증; **US-01**; 파싱 **P-04** |
| **RED 실패 상태** | 레거시 `UnitConverter.py:4-6` → print 후 **return만**, 예외 없음 → `pytest.raises` **AssertionError** |

---

## TC-A-03 — 음수 입력

| 필드 | 내용 |
|------|------|
| **테스트 이름** | `test_ui_parse_negative_meter_raises_value_error` |
| **Given** | 입력 `"meter:-1.0"`. |
| **When** | 파싱·검증 단계 실행. |
| **Then** | **`ValueError` / `TypeError`**; message: `Value must be zero or positive: -1.0` (또는 `-1`). 환산 stdout **0줄**. |
| **보호 Invariant** | **F-02** **ERR_NEGATIVE_VALUE**; **D-INV-02** magnitude ≥ 0 |
| **RED 실패 상태** | 레거시에 음수 검증 없음 → **예외 미발생**, 잘못된 환산 출력 → assert 실패 |

---

## TC-A-04 — 없는 단위

| 필드 | 내용 |
|------|------|
| **테스트 이름** | `test_ui_parse_unknown_unit_parsec_raises_value_error` |
| **Given** | Registry 기본 3단위만. 입력 `"parsec:1.0"`. |
| **When** | 파싱 후 unit_id 등록 여부 확인. |
| **Then** | **`ValueError` / `TypeError`**; message exact: `Unknown unit: parsec`. |
| **보호 Invariant** | **F-02** **ERR_UNKNOWN_UNIT**; **U-03** |
| **RED 실패 상태** | 레거시 `UnitConverter.py:22-24` → print `Unknown unit` 후 return, **ValueError 아님** → `pytest.raises` 실패 |

---

## TC-A-05 — 원 입력 단위·값 포맷 보존

| 필드 | 내용 |
|------|------|
| **테스트 이름** | `test_ui_table_output_preserves_source_unit_and_value` |
| **Given** | `"meter:2.5"`, table 포맷. |
| **When** | stdout/table 문자열 렌더. |
| **Then** | 각 줄 `{source_value} {source_unit} = …`; **source_value** `2.5` 반올림 없음; **source_unit** `meter`; feet 줄에 `2.5 meter = … feet` 패턴. |
| **보호 Invariant** | **F-04** table 스키마 §6.1; **TC-A-06** (README Track A) |
| **RED 실패 상태** | 레거시는 패턴 유사하나 표시값 **full float** (`8.2021`); PRD 1자리 `8.2` 테스트 추가 시 **문자열 불일치** |

---

## TC-A-06 — JSON 출력 스키마

| 필드 | 내용 |
|------|------|
| **테스트 이름** | `test_ui_json_format_meter_2_5_matches_schema` |
| **Given** | `"meter:2.5"`, `format=json` (또는 JSON 렌더 요청). |
| **When** | `render_json(source, conversions)` 실행. |
| **Then** | 파싱 가능 JSON; `source.unit=="meter"`, `source.value==2.5`; `conversions.length==3`; 항목에 `feet` **표시값** `8.2` (PRD §6.2) 또는 내부 number `8.2`; 필드 누락 없음. |
| **보호 Invariant** | **F-05** JSON 스키마; **J-01~J-04** (권장) |
| **RED 실패 상태** | JSON 렌더 **미구현** → **ModuleNotFoundError / NotImplementedError** |

---

## TC-A-07 — (보강) 소수 파싱 실패

| 필드 | 내용 |
|------|------|
| **테스트 이름** | `test_ui_parse_invalid_number_abc_raises_value_error` |
| **Given** | `"meter:abc"`. |
| **When** | numeric parse. |
| **Then** | **`ValueError` / `TypeError`**; `Invalid number: abc`. |
| **보호 Invariant** | **F-02** **ERR_INVALID_NUMBER**; **P-05** |
| **RED 실패 상태** | 레거시는 print 후 return → **raises 실패** |

---

# Logic RED Tests — Test ID / Scenario / Invariant

## TC-B-01 — convert meter → feet

| 필드 | 내용 |
|------|------|
| **Test ID** | TC-B-01 |
| **Scenario** | `convert("meter", 2.5, "feet")` — **1 meter = 3.28084 feet** |
| **Invariant** | **D-INV-03** 환산식; **A-01** / **G-02** ε≤1e-4 (테스트 assert **1e-5**) |
| **기대** | `8.20210` (abs≤1e-5) |
| **RED 실패 상태** | `convert` **미존재** → `AttributeError`; 레거시는 함수 API 없음 |

---

## TC-B-02 — convert meter → yard

| 필드 | 내용 |
|------|------|
| **Test ID** | TC-B-02 |
| **Scenario** | `convert("meter", 1.0, "yard")` — **1 meter = 1.09361 yard** |
| **Invariant** | **D-INV-03**, **D-INV-04** yard 비율 |
| **기대** | `1.09361` (abs≤1e-5) |
| **RED 실패 상태** | API 미구현 → **AttributeError** |

---

## TC-B-03 — convert feet → meter (역변환)

| 필드 | 내용 |
|------|------|
| **Test ID** | TC-B-03 |
| **Scenario** | `convert("feet", 1.0, "meter")` — 1 feet = 0.3048 m |
| **Invariant** | **D-INV-03** 역변환 대칭; meter 앵커 |
| **기대** | `0.30480` (abs≤1e-5) |
| **RED 실패 상태** | API 미구현 → **AttributeError** |

---

## TC-B-04 — convertAll

| 필드 | 내용 |
|------|------|
| **Test ID** | TC-B-04 |
| **Scenario** | `convertAll("meter", 1.0)` → 등록된 **모든** 단위(meter, feet, yard) 목록 |
| **Invariant** | **D-INV-06** batch 크기 = `registry.count()`; **F-01** 전 단위 출력 |
| **기대** | 3건; feet≈`3.28084`, yard≈`1.09361`, meter=`1.0` |
| **RED 실패 상태** | `convertAll` 없음; 레거시는 print 3줄만 → **구조화 반환 없음** |

---

## TC-B-05 — registerUnit 후 변환

| 필드 | 내용 |
|------|------|
| **Test ID** | TC-B-05 |
| **Scenario** | `registerUnit("cubit", 0.4572)` (1 cubit = 0.4572 m) 후 `convert("cubit", 1.0, "feet")` |
| **Invariant** | **D-INV-01** ratio>0; **F-07** / **OCP** Engine 시그니처 불변 |
| **기대** | cubit→feet 유한값; `convertAll("meter",1)` 시 **4단위** |
| **RED 실패 상태** | `registerUnit` 없음; 동적 등록 CLI 계약 없음 → **AttributeError** |

---

## TC-B-06 — loadConfig 유효 JSON/YAML

| 필드 | 내용 |
|------|------|
| **Test ID** | TC-B-06 |
| **Scenario** | `loadConfig("config/units.json")` 또는 유효 `.yaml` |
| **Invariant** | **F-06** Background 비율; **T-DA-01** |
| **기대** | feet `meters_per_unit==0.3048`; `convert("meter",1,"feet")≈3.28084` |
| **RED 실패 상태** | `loadConfig` / Repository **없음** → **AttributeError** |

---

## TC-B-07 — loadConfig 없는 경로 → 기본값

| 필드 | 내용 |
|------|------|
| **Test ID** | TC-B-07 |
| **Scenario** | `loadConfig("/nonexistent/units.json")` |
| **Invariant** | **F-06** 실패 시 기본 3단위; README **3.28084 / 1.09361** 유지 |
| **기대** | 예외 없이 defaults; `convert("meter",1,"feet")≈3.28084` |
| **RED 실패 상태** | loadConfig 없음; 하드코딩 if-else만 존재 → API **AttributeError** |

---

## TC-B-08 — (보강) 음수 Domain

| 필드 | 내용 |
|------|------|
| **Test ID** | TC-B-08 |
| **Scenario** | `convert("meter", -1.0, "feet")` |
| **Invariant** | **D-INV-02** |
| **기대** | **`ValueError`** |
| **RED 실패 상태** | Domain 검증 없음 → 잘못된 음수 결과 또는 **예외 없음** |

---

## TC-B-09 — (보강) 영값

| 필드 | 내용 |
|------|------|
| **Test ID** | TC-B-09 |
| **Scenario** | `convert("meter", 0.0, "feet")` |
| **Invariant** | **D-INV-02** (0 허용) |
| **기대** | `0.0` |
| **RED 실패 상태** | API 없으면 AttributeError; 있으면 통과 가능 |

---

# RED 실행 매트릭스 (레거시 baseline)

| Test ID | Track | 레거시 `UnitConverter.py` 예상 결과 |
|---------|-------|-------------------------------------|
| TC-A-01 | UI | FAIL — 구조화 반환 없음 |
| TC-A-02 | UI | FAIL — ValueError 없음 |
| TC-A-03 | UI | FAIL — 음수 허용 출력 |
| TC-A-04 | UI | FAIL — ValueError 없음 |
| TC-A-05 | UI | FAIL — 표시/정밀도 계약 불일치 |
| TC-A-06 | UI | FAIL — JSON 미구현 |
| TC-A-07 | UI | FAIL — ValueError 없음 |
| TC-B-01~09 | Logic | FAIL — `convert*` / `registerUnit` / `loadConfig` 없음 |

---

# pytest 파일 배치 (RED 전용, 작성 시)

```
tests/red/
  boundary/test_ui_red_*.py    # TC-A-01 ~ A-07
  entity/test_logic_red_*.py   # TC-B-01 ~ B-09
```

**규칙:** `pytest.raises((ValueError, TypeError))` 허용; **skip/xfail로 GREEN 위장 금지** (RR-05).  
**Engine Mock:** UI Track만 Fake Engine 주입; Logic Track은 **실객체 Registry** (`.cursorrules`).

---

# 추적

| 문서 | 연계 |
|------|------|
| [test_plan.md](../test_plan.md) | P0 시나리오·경계값 |
| [defect_list.md](../defect_list.md) | DEF-001~008 |
| README RED To-Do | TC-A-01~07, TC-B-01~07 체크 시 본 ID 사용 |
