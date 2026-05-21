# 제품 요구사항 문서 (PRD) — UnitConvertor_06

| 항목 | 값 |
|------|-----|
| 문서 ID | PRD-UC-06-001 |
| 기준 문서 | Phase 4 `requirements-package.md` (Epic, Journey, Stories, Gherkin) |
| 버전 | 1.0 |
| Python | 3.11+ |

---

## 1. 프로젝트 개요

### 1.1 한 줄 목적문 (What / Who / Why)

**What:** meter 허브 기준 길이 단위 변환 CLI  
**Who:** Python·클린 아키텍처 학습자(6시간 AI 실습)  
**Why:** 계약·테스트·BCE 레이어로 **정확한 환산**과 **확장(단위·포맷·설정)** 을 동시에 검증 가능하게 학습하기 위함

### 1.2 배경 및 문제 정의 (관찰)

학습자는 `UnitConverter.py` 형태의 단일 스크립트에서 시작하며, 입출력·환산·비율이 한곳에 있어 테스트와 확장이 어렵다. README는 `meter:2.5` 입력 시 feet·yard 등 **전 단위 출력**과 **고정 비율**을 요구하나, 음수·형식 오류·미등록 단위에 대한 **측정 가능한 거부 계약**은 코드에 명시되지 않은 경우가 많다. AI 보조 구현 시 **반올림·오류 문구·비율**이 조용히 바뀌면 회귀를 사람이 눈으로만 확인하게 되어, 6시간 실습 목표( OCP/SRP·TDD )와 충돌한다.

### 1.3 목표 (측정 가능)

| ID | 목표 | 통과 조건 |
|----|------|-----------|
| G-01 | 계약 고정 | RED P0 100% GREEN; 오류 message exact match TC 통과 |
| G-02 | 환산 정확 | `1 meter` → feet `3.28084` (ε≤1e-4); `2.5 meter` table 표시 `8.2 feet`, `2.7 yard` |
| G-03 | 레이어 품질 | pytest-cov: entity line≥95%, boundary≥90%, data≥85% |
| G-04 | 확장 | `1 cubit = 0.4572 meter` 등록 후 `meter:1` stdout 4줄; Engine 공개 API 변경 0건 |
| G-05 | 회귀 | 앵커 TC A-01,A-03,A-06,T-01,J-01,C-01 삭제·assert 완화 0건 |

### 1.4 비목표 (Non-Goal)

| ID | 비목표 | 범위 밖 근거 |
|----|--------|--------------|
| NG-01 | 질량·온도·속도 등 **다른 물리량** 변환 | Epic In/Out — 길이만 |
| NG-02 | **GUI·웹** 클라이언트 | CLI만; Journey J5는 콘솔 계약 |
| NG-03 | **원격 설정 서버·다국어 UI** | 로컬 `config/units.json` 수준; 운영 배포 파이프라인 없음 |

---

## 2. 사용자 및 이해관계자

### 2.1 타깃 사용자 (페르소나 1명)

| 필드 | 내용 |
|------|------|
| 이름 | 민지 |
| 역할 | Python·클린 아키텍처 학습자 |
| 기술 수준 | venv·pytest 사용 가능; BCE·TDD 용어 학습 중 |
| 성공 정의 | 6시간 내 RED→GREEN→refactor 완료 + 회고 가능 산출물 |
| 제약 | README 상수·Phase 4 Gherkin Background·`.cursorrules` forbidden 준수 |

### 2.2 주요 사용 시나리오 (Journey 기반)

| # | 시나리오 (Journey) | 트리거 | 기대 결과 | 측정 |
|---|-------------------|--------|-----------|------|
| S-01 | **J2→J5 계약 환산** (Happy path) | `meter:2.5`, format=table | exit 0; 3줄; `2.5 meter = 8.2 feet` 포함 | Gherkin Sc.1; US-03,04 |
| S-02 | **J4 입력 거부** | `meter 2.5` 또는 `mile:1` | exit ≠0; exact error message | Gherkin Sc.2–3; US-01 |
| S-03 | **J6 확장·설정** | cubit 등록 + malformed config | 등록 성공 시 4줄 환산; config 오류 시 CFG_PARSE_ERROR·환산 없음 | US-05,06; Gherkin Sc.4 |

---

## 3. 기능 요구사항

### 3.1 핵심 기능 목록

| ID | 기능 | 우선순위 | User Story |
|----|------|----------|------------|
| F-01 | `unit:value` 변환·전 단위 출력 | **필수** | US-03, US-04 |
| F-02 | 입력 검증(형식·숫자·음수·빈줄) | **필수** | US-01 |
| F-03 | UnitRegistry + meter 앵커 환산 | **필수** | US-02, US-03 |
| F-04 | table 출력 (기본) | **필수** | US-04 |
| F-05 | json / csv 출력 선택 | **권장** | US-04 |
| F-06 | config/units.json 로드 | **권장** | US-05 |
| F-07 | `1 unit = factor meter` 동적 등록 | **권장** | US-06 |
| F-08 | units.yaml 로드 | **선택** | US-05 (JSON 동형 시) |

### 3.2 기능별 입·출력 계약 (문자열)

#### F-01 / F-04 — 변환 + table (필수)

| 방향 | 계약 |
|------|------|
| Input | `{unit_id}:{decimal}` — `unit_id` 소문자·공백 없음; `:` 정확히 1회; `decimal`은 `float` 파싱 가능 |
| Output (성공) | 줄마다 `{source_value} {source_unit} = {display_value} {target_unit}` |
| Output 규칙 | `source_value` = 입력 magnitude **반올림 없음**; `display_value` = **소수 1자리 ROUND_HALF_UP** |
| Output 개수 | 등록 단위 수 N → 정확히 N줄 |
| Exit | 성공 시 `0` |

**예시 (필수 통과):** 입력 `meter:2.5` → `2.5 meter = 8.2 feet`, `2.5 meter = 2.7 yard` (및 meter 라인)

#### F-02 — 입력 검증 (필수)

| 조건 | code | message (exact) |
|------|------|-----------------|
| 빈 문자열 | `ERR_EMPTY_INPUT` | `Input is empty.` |
| `:` 없음 또는 다중 `:` | `ERR_INVALID_FORMAT` | `Invalid format. Use unit:value (ex: meter:2.5)` |
| 숫자 파싱 실패 | `ERR_INVALID_NUMBER` | `Invalid number: {value_str}` |
| magnitude < 0 | `ERR_NEGATIVE_VALUE` | `Value must be zero or positive: {value}` |
| 미등록 unit_id | `ERR_UNKNOWN_UNIT` | `Unknown unit: {unit}` |
| Exit | 실패 시 **≠ 0** |

#### F-05 — json (권장)

| 필드 | 타입 | 규칙 |
|------|------|------|
| `source.unit` | string | 입력 unit_id |
| `source.value` | number | 입력 magnitude (반올림 없음) |
| `conversions[]` | array | 길이 = N; 순서 = `list_unit_ids()` |
| `conversions[].unit` | string | target unit_id |
| `conversions[].value` | number | 1자리 표시값 (예: 8.2) |

#### F-05 — csv (권장)

| 항목 | 계약 |
|------|------|
| 헤더 (1행) | `source_unit,source_value,target_unit,target_value` |
| 데이터 행 | N행; 각 행 `source_*` 동일; `target_value` 1자리 |

#### F-07 — 동적 등록 (권장)

| 방향 | 계약 |
|------|------|
| Input | `{integer} {unit_id} = {positive_decimal} meter` — 공백 허용 규칙: 단일 공백 구분; anchor는 `meter`만 |
| Output (성공) | `Registered: 1 {unit} = {factor} meter` (exact) |
| 사후 | 동일 세션 Registry에 unit 반영; 이후 F-01 적용 |

#### F-06 — 설정 로드 (권장)

| 방향 | 계약 |
|------|------|
| Input 파일 | `config/units.json` |
| 성공 | Background ratios와 동일한 3단위 로드 |
| 실패 | `CFG_FILE_NOT_FOUND`, `CFG_PARSE_ERROR`; **환산 stdout 0줄** |

### 3.3 제약 사항 (Gherkin Background와 일치)

| 항목 | 규칙 | 테스트 |
|------|------|--------|
| 앵커 | `meter` | Background `Given anchor unit "meter"` |
| 비율 (meters_per_unit) | meter `1.0`, feet `0.3048`, yard `0.9144` | Background table; ε≤1e-4 |
| README 표시 비율 | `1m = 3.28084ft`, `1m = 1.09361yd` | 내부 계산 TC; 표시는 1자리 |
| 입력 형식 (변환) | `unit:value` only | US-01 |
| 입력 형식 (등록) | `1 unit = factor meter` | US-06 |
| 음수 | magnitude `< 0` 거부; `0` 허용 | US-01, US-03 |
| 허용 단위 (기본) | `meter`, `feet`, `yard` | Background |
| 미지원 단위 | 환산 수행 안 함; `Unknown unit: {unit}` | Gherkin Sc.3 |
| 표시 반올림 | 1 decimal `ROUND_HALF_UP` | `2.5m → 8.2ft`, `2.7yd` |
| 명령 우선순위 | `=` 포함 등록 패턴 → else `:` 변환 → else 형식 오류 | 파싱 TC P-03, P-04 |

---

## 4. 비기능 요구사항

### 4.1 기술 스택

| 구분 | 고정 스택 |
|------|-----------|
| 런타임 | Python **3.11+** |
| 테스트 | **pytest**, **pytest-cov** |
| 검증·DTO | **pydantic** v2 (설정 DTO·ErrorEnvelope·Command 모델) |
| 포맷 | black, isort (line 88) |
| 타입 | 공개 API 타입 힌트 필수 |

### 4.2 아키텍처 원칙

| 원칙 | 요구 |
|------|------|
| **SRP** | Registry / Engine / Parser / Renderer / Repository 각 1 변경 이유 |
| **OCP** | 신규 단위 = Registry·config 추가; 신규 포맷 = Renderer 추가; Engine 시그니처 불변 |
| **BCE 레이어** | `entity`(순수 환산), `control`(오케스트레이션), `boundary`(파싱·출력·오류문), `data`(파일 로드) |
| **의존성** | 허용: boundary→control→entity, data→entity / 금지: entity→boundary\|control\|data |

### 4.3 테스트 커버리지 목표

| 레이어 | line % | branch % |
|--------|--------|----------|
| entity (Domain) | ≥ 95 | ≥ 90 |
| boundary | ≥ 90 | ≥ 85 |
| data | ≥ 85 | ≥ 80 |
| 측정 | `pytest --cov=entity --cov=boundary --cov=control --cov=data` | PR·로컬 동일 |

### 4.4 확장성 원칙

| 확장 | 허용 변경 | 금지 변경 |
|------|-----------|-----------|
| 새 길이 단위 | `units.json` 항목 추가 또는 `register` | `ConversionEngine.convert` 시그니처 |
| 새 출력 포맷 | `OutputRenderer` 구현체 추가 | 기존 table/json/csv 스키마 |
| 비율 변경 | config 파일 값만 | Boundary에 literal `3.28084` |

---

## 5. 데이터 요구사항

### 5.1 단위 비율 상수 (meter 허브)

| unit_id | meters_per_unit | README 등가 |
|---------|-----------------|-------------|
| meter | 1.0 | 기준 |
| feet | 0.3048 | 1 m = 3.28084 ft |
| yard | 0.9144 | 1 m = 1.09361 yd |

**환산식 (entity):** `target_magnitude = source_magnitude × (mpu(source) / mpu(target))`  
**내부 비교:** 절대 오차 ε = `1e-4`  
**feet↔yard:** meter 경유와 동일 (교차 TC 필수)

### 5.2 설정 외부화

| 모드 | 용도 | 계약 |
|------|------|------|
| **File (기본)** | `config/units.json` | `{ "units": [ { "id": string, "meters_per_unit": float > 0 } ] }` |
| **YAML (선택)** | `config/units.yaml` | JSON과 동형 키 |
| **InMemory** | pytest·로컬 fallback | File 없을 때 defaults 3단위; **운영 기본은 File** |

로드 실패 시 Registry **변경 없음**; 앱 시작 실패 code: `CFG_FILE_NOT_FOUND` | `CFG_PARSE_ERROR`

### 5.3 동적 단위 등록 계약

```
REGISTER_LINE ::= "1" WS UNIT_ID WS "=" WS POSITIVE_DECIMAL WS "meter"
UNIT_ID       ::= [a-z][a-z0-9_]*
POSITIVE_DECIMAL ::= float > 0
```

| 결과 | 조건 |
|------|------|
| 성공 | `MSG_REGISTER_OK`: `Registered: 1 {unit} = {factor} meter` |
| 실패 | 중복 → `ERR_DUPLICATE_UNIT`; factor≤0 → `ERR_INVALID_FACTOR`; 형식 → `ERR_INVALID_REGISTER` |

---

## 6. 출력 요구사항

### 6.1 콘솔 기본 포맷 (table)

| 필드 | 규칙 |
|------|------|
| 기본 format | `table` (명시 없을 때) |
| 줄 패턴 | `{source_value} {source_unit} = {display_value} {target_unit}` |
| 순서 | `UnitRegistry.list_unit_ids()` 등록 순서 (문서화된 단일 규칙) |
| source_value | 입력값 그대로 (예: `2.5`) |
| display_value | ROUND_HALF_UP, **1자리** |
| 줄 수 | `registry.count()` |

### 6.2 JSON 스키마 (확장)

```json
{
  "source": { "unit": "string", "value": "number" },
  "conversions": [
    { "unit": "string", "value": "number" }
  ]
}
```

- `conversions.length` = N  
- `value` = 표시값 (1자리 number, 예: 8.2)

### 6.3 CSV 스키마 (확장)

| 열 | 설명 |
|----|------|
| source_unit | 입력 unit_id (행마다 동일) |
| source_value | 입력 magnitude |
| target_unit | 대상 unit_id |
| target_value | 1자리 표시값 |

- 1행 헤더 고정; 데이터 N행

### 6.4 Table vs JSON/CSV

| format | 소비자 | 필수 여부 |
|--------|--------|-----------|
| table | 사람(터미널) | **필수** |
| json | 스크립트 | 권장 |
| csv | 스프레드시트 | 권장 |

---

## 7. 성공 지표

### 7.1 인수 기준 (체크박스 — Story AC 정합)

- [ ] **AC-01 (US-01,03,04):** `meter:2.5` table → exit 0, 3줄, `2.5 meter = 8.2 feet`, `2.5 meter = 2.7 yard` (Gherkin Sc.1)
- [ ] **AC-02 (US-01):** `meter 2.5` → message exact `Invalid format. Use unit:value (ex: meter:2.5)`, exit ≠ 0 (Sc.2)
- [ ] **AC-03 (US-01,02):** `mile:1` → message exact `Unknown unit: mile`, exit ≠ 0 (Sc.3)
- [ ] **AC-04 (US-05):** malformed `config/units.json` → `CFG_PARSE_ERROR`, conversion stdout 0줄 (Sc.4)
- [ ] **AC-05 (US-06, SC-06):** `1 cubit = 0.4572 meter` 등록 후 `meter:1` → 4줄, cubit 라인 존재
- [ ] **AC-06 (SC-03):** coverage entity≥95% / boundary≥90% / data≥85% (pytest-cov 리포트)

### 7.2 회귀 보호 규칙

| 규칙 ID | 정책 | 위반 시 |
|---------|------|---------|
| RR-01 | 앵커 TC `A-01,A-03,A-06,T-01,J-01,C-01` 삭제·assert 완화 금지 | PR reject |
| RR-02 | Gherkin·US에 정의된 **error message exact** 변경 시 TC·문서 동시 수정 | otherwise reject |
| RR-03 | Background ratios·`ROUND_HALF_UP` 1자리 변경 시 PRD·Gherkin·RED 동시 갱신 | otherwise reject |
| RR-04 | refactor는 **전체 pytest GREEN** 이후만; GREEN 중 API·스키마 변경 금지 | revert |
| RR-05 | 계약 변경은 **RED 추가 → GREEN** 순서; skip/xfail로 통과 위장 금지 | reject |

---

## 8. 용어 정의 (Glossary)

| 용어 | 정의 |
|------|------|
| **Anchor unit (meter)** | 모든 `meters_per_unit`의 기준; 환산식 분모·분자의 허브 |
| **meters_per_unit** | `1 {unit}` 이 몇 meter인지 나타내는 양수 계수 (float) |
| **UnitRegistry** | 등록된 단위 집합; `register` / `list_unit_ids` / `count` |
| **ConversionEngine** | Registry와 Quantity를 받아 `ConversionBatch`를 생성하는 순수 환산기 |
| **ConversionBatch** | 동일 입력에 대한 전 target 단위 `ConversionLine` 목록 |
| **ErrorEnvelope** | `code` + `message`(exact) + optional `field`; 실패 시 boundary 출력 계약 |
| **Boundary** | CLI 파싱·렌더링·오류 매핑; 비율·파일 I/O 없음 |
| **Control** | use-case 실행·Registry wiring; 환산식·포맷 문자열 없음 |
| **Data layer** | `config/units.json` 로드 → Registry 스냅샷 |
| **Display value** | 사용자에게 보이는 1자리 ROUND_HALF_UP 값 (내부값과 구분) |
| **RED / GREEN / refactor** | 테스트 선행 실패 → 최소 구현 통과 → 구조 정리(행위 불변) |
| **Regression anchor** | 회귀 방지용 고정 TC 집합 (A-01, A-03, A-06, T-01, J-01, C-01) |

---

## 부록 — Phase 4 추적

| PRD | Phase 4 |
|-----|---------|
| G-01~G-05 | Epic SC-01~SC-06 |
| S-01~S-03 | Journey J2~J6 |
| F-01~F-08 | US-01~US-06 |
| AC-01~AC-06 | Story AC + Gherkin 4 Scenario |
| §5.1 table | Gherkin Background ratios |
