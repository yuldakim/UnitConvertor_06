# 요구사항 서술 패키지 — 확장 가능한 Python 단위 변환 학습 시스템

| 메타 | 값 |
|------|-----|
| 저장소 | `UnitConvertor_06` (길이 단위 변환, Python 3.11+) |
| 아키텍처 | BCE Dual-Track: `boundary` / `control` / `entity` / `data` |
| 앵커 단위 | meter |
| 문서 버전 | 1.0 |

---

## Level 1 — Epic

### 제목

**확장 가능한 Python 단위 변환 학습 시스템**

### 목적 (4줄)

1. 학습자가 **meter 기준 길이 환산**을 구현하면서 **계약(입력·오류·출력)·Invariant**를 테스트로 고정하는 능력을 기른다.
2. **BCE 레이어 분리**와 **OCP/SRP**로 단위·포맷·설정 확장 시 기존 환산 로직 변경을 최소화하는 설계를 체득한다.
3. **Dual-Track TDD(RED→GREEN→refactor)** 로 Domain·Boundary·Data·Integration을 순차 검증한다.
4. **생성형 AI 보조 코딩** 환경에서도 회귀 앵커·커버리지·금지 패턴을 지키며 리팩터하는 습관을 만든다.

### 성공 기준 (측정 가능)

| ID | 기준 | 측정 방법 | 통과 임계값 |
|----|------|-----------|-------------|
| SC-01 | 계약 테스트 | 파싱·오류 문구·표/JSON/CSV 스키마 pytest | RED 목록 P0 전부 GREEN |
| SC-02 | 환산 정확도 | README 비율 + ε assert | `1m→3.28084ft`, `2.5m→ft 표시 8.2` (1자리 HALF_UP) |
| SC-03 | 레이어 커버리지 | pytest-cov 레이어별 | entity line ≥95%, boundary ≥90%, data ≥85% |
| SC-04 | 회귀 정책 | `pytest` + 앵커 TC | A-01, A-03, A-06, T-01, J-01, C-01 삭제·약화 0건 |
| SC-05 | 의존성 방향 | 정적 검토 | entity→boundary/control/data import 0건 |
| SC-06 | 확장성 | cubit 동적 등록 통합 TC | 등록 후 `meter:1` 4라인 출력 |

---

## Level 2 — User Journey (정본 1개)

### Persona

| 항목 | 설명 |
|------|------|
| 이름(가칭) | 민지 |
| 역할 | Python·클린 아키텍처 학습자 (6시간 AI 활용 실습) |
| 목표 | 단위 변환기를 테스트·계약·레이어로 나누어 완성 |
| 제약 | README 상수·고정 오류 문구·`.cursorrules` 준수 |

### 여정 단계 (7단계)

| # | 단계 | 행동 | Pain (1줄) | Opportunity (1줄) |
|---|------|------|------------|-------------------|
| J1 | 문제 인식 | Mom Test·README 정리 | AI·수동 계산에 조용한 오답 | Invariant로 성공 기준 고정 |
| J2 | 계약 정의 | 스키마·Gherkin·RED 목록 | 기능 나열만으로 테스트 불가 | 체크 가능 AC로 순서 결정 |
| J3 | 도메인 분리 | entity에 Registry·Engine | 한 파일에 I/O·환산·출력 혼재 | 순수 Domain 단위 테스트 |
| J4 | RED | 비율·검증·등록 RED | 구현 선행 시 테스트가 끌림 | 실패가 설계 피드백 |
| J5 | GREEN | Boundary→Data→Integration | Boundary 비율 하드코딩 유혹 | Mock Engine으로 계약 분리 |
| J6 | 확장 | JSON·포맷·동적 등록 | 설정 오류 시 크래시 | Data가 CFG_* 오류 명확화 |
| J7 | 회귀 보호 | refactor + cov + 앵커 | 리팩터 후 문구·반올림 깨짐 | GREEN 후만 구조 변경 |

---

## Level 3 — User Stories

### US-01 — 입력 검증

**As a** 학습자, **I want** `단위:값` 및 등록 명령 검증, **so that** 잘못된 입력이 환산되지 않는다.

**Acceptance Criteria**

- [ ] `meter:2.5` → `ConvertCommand(meter, 2.5)`
- [ ] 콜론 없음 → `ERR_INVALID_FORMAT` exact message
- [ ] `meter:abc` → `ERR_INVALID_NUMBER`
- [ ] `meter:-1` → `ERR_NEGATIVE_VALUE`
- [ ] 빈 입력 → `ERR_EMPTY_INPUT`
- [ ] 오류 시 exit ≠ 0

### US-02 — 레지스트리·OCP

**As a** 학습자, **I want** Registry 등록·조회, **so that** Engine 수정 없이 단위를 추가한다.

**Acceptance Criteria**

- [ ] 기본 3단위 `with_defaults()`
- [ ] 중복 등록 → `DuplicateUnitError` / `ERR_DUPLICATE_UNIT`
- [ ] factor ≤ 0 → `NonPositiveFactorError` / `ERR_INVALID_FACTOR`
- [ ] 미등록 단위 환산 → `UnregisteredUnitError` / `ERR_UNKNOWN_UNIT`
- [ ] `ConversionBatch` 라인 수 = `registry.count()`

### US-03 — 환산 정확도

**As a** 사용자, **I want** meter 앵커 환산, **so that** README와 일치한다.

**Acceptance Criteria**

- [ ] `1 meter` → feet `3.28084` (ε ≤ 1e-4)
- [ ] `1 meter` → yard `1.09361` (ε ≤ 1e-4)
- [ ] `2.5 meter` → feet 표시 `8.2` (ROUND_HALF_UP 1자리)
- [ ] feet↔yard meter 경유 일치
- [ ] `0` 입력 → 전 타깃 `0`

### US-04 — 출력 포맷

**As a** 사용자, **I want** table/json/csv 선택, **so that** 소비 형태에 맞게 출력한다.

**Acceptance Criteria**

- [ ] table: 줄 수 = 등록 단위 수, 패턴 `{src} {unit} = {dst} {unit}`
- [ ] json: `source` + `conversions[]`, 1자리 number
- [ ] csv: 고정 헤더 4열
- [ ] unknown format → `ERR_UNKNOWN_FORMAT`
- [ ] 순서 = `list_unit_ids()` 고정

### US-05 — 설정 로드 실패

**As a** 운영자, **I want** JSON/YAML 로드, **so that** 비율을 코드 밖에서 바꾼다.

**Acceptance Criteria**

- [ ] 유효 `config/units.json` → 3단위 Registry
- [ ] 파일 없음 → `CFG_FILE_NOT_FOUND`
- [ ] malformed JSON → `CFG_PARSE_ERROR`
- [ ] 중복 id / non-positive factor → 로드 중단, Registry 불변
- [ ] `open()`은 data 레이어만

### US-06 — 동적 단위 등록

**As a** 사용자, **I want** `1 cubit = 0.4572 meter` 등록 후 환산, **so that** 런타임에 단위를 추가한다.

**Acceptance Criteria**

- [ ] 등록 성공 → `MSG_REGISTER_OK` exact
- [ ] 등록 후 `meter:1` → 4줄(cubit 포함)
- [ ] cubit 값 = meter 앵커 공식 (ε)
- [ ] 등록 실패 시 Registry 불변
- [ ] Engine 시그니처 불변 (OCP)

---

## Level 4 — Gherkin Feature

```gherkin
Feature: Length unit conversion CLI
  Background:
    Given anchor unit "meter"
    And unit ratios:
      | unit  | meters_per_unit |
      | meter | 1.0             |
      | feet  | 0.3048          |
      | yard  | 0.9144          |
    And display rounding is 1 decimal ROUND_HALF_UP

  Scenario: Happy path meter to table
    Given output format "table"
    When user submits "meter:2.5"
    Then exit code is 0
    And stdout has 3 conversion lines
    And line "2.5 meter = 8.2 feet"
    And line "2.5 meter = 2.7 yard"

  Scenario: Invalid format
    When user submits "meter 2.5"
    Then exit code is not 0
    And message is "Invalid format. Use unit:value (ex: meter:2.5)"

  Scenario: Unknown unit
    When user submits "mile:1"
    Then exit code is not 0
    And message is "Unknown unit: mile"

  Scenario: Config parse error
    Given "config/units.json" is malformed
    When application starts
    Then exit code is not 0
    And error code is "CFG_PARSE_ERROR"
    And no conversion output
```

---

## Level 5 — 정합성 체크리스트

| # | 검증 항목 | Epic | Journey | Story | Gherkin | ✓ |
|---|-----------|:----:|:-------:|:-----:|:-------:|---|
| 1 | README 비율 Background 고정 | SC-02 | J2,J3 | US-03 | Background | ☐ |
| 2 | Happy path 8.2 / 2.7 | SC-01,02 | J5 | US-03,04 | Sc.1 | ☐ |
| 3 | Invalid format exact | SC-01 | J2 | US-01 | Sc.2 | ☐ |
| 4 | Unknown unit exact | SC-01 | J4 | US-01,02 | Sc.3 | ☐ |
| 5 | Config error no convert | SC-03 | J6 | US-05 | Sc.4 | ☐ |
| 6 | OCP Registry only | SC-06 | J3,J6 | US-02,06 | — | ☐ |
| 7 | 3 formats | SC-01 | J5 | US-04 | Sc.1 | ☐ |
| 8 | TDD J4→J5→J7 | — | J4,J5,J7 | all | — | ☐ |
| 9 | Coverage SC-03 | SC-03 | J7 | all | — | ☐ |
| 10 | Regression anchors | SC-04 | J7 | US-03,04 | Sc.1 | ☐ |

| In | Out |
|----|-----|
| meter/feet/yard + 동적 등록 | 다른 물리량 |
| CLI | GUI/웹 |
| table/json/csv | PDF |
