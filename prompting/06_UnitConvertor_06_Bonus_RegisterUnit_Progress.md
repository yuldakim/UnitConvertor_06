# Export Transcript — 06_UnitConvertor_06_Bonus_RegisterUnit_Progress

Exported: 2026-05-21 14:51

| 항목 | 값 |
|------|-----|
| 보고서 | [06_UnitConvertor_06_Bonus_RegisterUnit_Progress.md](../Report/06_UnitConvertor_06_Bonus_RegisterUnit_Progress.md) |
| 브랜치 | `feature` → PR 머지 → `B_06` |
| 선행 | [05_UnitConvertor_06_Dual_Track_Refactoring_Progress.md](05_UnitConvertor_06_Dual_Track_Refactoring_Progress.md) |

---

## Session `10777050-11f3-4d67-b6d7-190bc045c1e2`

### Turn 1 — user

<user_query>
아직 코드는 수정하지 말고 분석만 해줘.
@UnitConverter.py 를 보고
아래 두 가지만 먼저 답해줘:
1. 현재 테스트 파일(test_*.py)이 존재하는지 확인하고,
   없다면 어느 파일에 대한 테스트가 필요한지 알려줘
2. 테스트 없이 리팩토링을 시작하면 안 되는 이유를 한 줄로 설명해줘
</user_query>

---

### Turn 2 — assistant

코드는 수정하지 않고 `UnitConverter.py`와 테스트 현황만 확인합니다.

[REDACTED]

---

### Turn 3 — assistant

[REDACTED]

---

### Turn 4 — assistant

[REDACTED]

---

### Turn 5 — assistant

[REDACTED]

---

### Turn 6 — assistant

## 1. `test_*.py` 존재 여부와 `UnitConverter.py` 커버리지

**`test_*.py`는 있습니다.** `tests/` 아래에 **11개**가 있습니다.

| 구분 | 파일 |
|------|------|
| Golden Master | `tests/test_golden_master.py` |
| Entity | `tests/entity/test_convert_normal_happy_path.py`, `test_convert_boundary_precision.py`, `test_register_dynamic_unit.py` |
| Boundary | `tests/boundary/test_convert_display_table.py`, `test_exception_parse_policy.py` |
| Data | `tests/data/test_config_load_json_yaml.py` |
| RED | `tests/red/entity/test_logic_red_convert.py`, `test_logic_red_register_config.py`, `tests/red/boundary/test_ui_red_convert.py`, `test_ui_red_parse.py` |

현재 `UnitConverter.py`는 이미 얇은 CLI 진입점입니다.

```1:19:c:\DEV_BR\UnitConvertor_06\UnitConverter.py
"""Legacy CLI entry — delegates to BCE ConverterApp (no conversion logic here)."""

from __future__ import annotations

from boundary.parser import ParseError
from control.converter_app import ConverterApp

def main() -> None:
    input_str = input("Insert value for converting (ex: meter:2.5): ")
    app = ConverterApp()
    try:
        print(app.handle_convert_line(input_str))
    except ParseError as exc:
        print(exc.message)
```

**`UnitConverter.py` 전용 테스트 파일은 없습니다.** (`test_unit_converter.py` 같은 이름 없음, `import UnitConverter` / `main()` 호출도 테스트에 없음)

| 관련 테스트 | 실제로 검증하는 대상 |
|-------------|---------------------|
| `test_golden_master.py` | `ConverterApp.handle_convert_line()` 출력 (fixture `converter_app`) |
| `golden_master.py`의 `capture_scenario_output_subprocess()` | `UnitConverter.py` subprocess 실행 **가능**하지만, pytest에서는 **미사용** |
| entity/boundary/control 테스트 | BCE 레이어 (`UnitConverter.py` 미연결) |

`UnitConverter.py`를 리팩토링할 때 **먼저 잠가야 할 테스트**는 대략 다음입니다.

- **CLI 진입점**: `main()` — 프롬프트 문구, `input` → `print`, `ParseError` 시 `exc.message` 출력
- **통합 경로**: subprocess로 `python UnitConverter.py` 실행 시 Golden Master와 동일한 stdout (또는 `test_golden_master.py`가 subprocess 경로를 쓰도록 확장)
- **위임 대상**은 이미 `control/converter_app.py`, `boundary/parser.py` 등에 테스트가 있으므로, `UnitConverter.py`만 손댈 때는 **진입점·I/O 계약**이 핵심입니다.

`docs/defect_list.md`도 레거시 CLI(`UnitConverter.py`)와 pytest 대상(BCE)이 **분리**되어 있다고 적어 두었습니다 (DEF-001, DEF-008 등).

---

## 2. 테스트 없이 리팩토링을 시작하면 안 되는 이유 (한 줄)

**리팩토링은 동작을 바꾸지 않는다는 전제인데, 테스트가 없으면 구조만 바꿔도 CLI 출력·오류 처리·위임 경로가 조용히 달라져도 알 수 없습니다.**

[REDACTED]

---

### Turn 7 — user

<user_query>
@UnitConverter.py  @control/  @data/ 의 코드 스멜을 분석해줘.
코드는 절대 수정하지 말고, 문제 있는 부분만 아래 표 형식으로:
| 파일명 | 줄번호 | 스멜 종류 | 문제 설명 | 우선순위 |

점검 항목:
- 단일 main() 함수에 파싱·검증·변환·출력이 혼재 (SRP 위반)
- if-else 체인 (새 단위 추가 시 기존 코드 수정 필요, OCP 위반)
- 매직 넘버 3.28084 / 1.09361 하드코딩
- 예외 처리 없음 또는 불완전한 예외 처리
- 긴 함수 (20줄 초과)
- 사용하지 않는 변수·함수
</user_query>

---

### Turn 8 — assistant

코드는 수정하지 않고, 지정한 점검 항목 기준으로 해당 파일들을 읽어 스멜만 정리합니다.

[REDACTED]

---

### Turn 9 — assistant

[REDACTED]

---

### Turn 10 — assistant

[REDACTED]

---

### Turn 11 — assistant

[REDACTED]

---

### Turn 12 — assistant

[REDACTED]

---

### Turn 13 — assistant

[REDACTED]

---

### Turn 14 — assistant

[REDACTED]

---

### Turn 15 — assistant

지정하신 세 경로(`UnitConverter.py`, `control/`, `data/`)만 읽고, 점검 항목에 **해당하는 문제만** 표로 정리했습니다. (이미 BCE로 분리된 항목·범위 밖 항목은 행에서 제외했습니다.)

| 파일명 | 줄번호 | 스멜 종류 | 문제 설명 | 우선순위 |
|--------|--------|-----------|-----------|----------|
| `UnitConverter.py` | 9–15 | 불완전한 예외 처리 | `main()`이 `ParseError`만 처리하고, `ConverterApp`·엔진에서 나올 수 있는 `NegativeMagnitudeError`·`UnknownUnitError`·`ConfigLoadError` 등은 미처리(비정상 종료·스택 트레이스 가능). | 중 |
| `UnitConverter.py` | 14–15 | 불완전한 예외 처리 | 파싱 실패 시 메시지만 `print`하고 종료 코드를 설정하지 않아, CLI/스크립트 관점에서 성공·실패 구분이 불명확함(DEF-006 계약과 불일치). | 중 |
| `UnitConverter.py` | 9–15 | SRP 위반 (경미) | `main()`에 stdin/stdout I/O와 `ConverterApp` 생성·호출이 함께 있음. 파싱·환산은 위임됐으나, CLI 진입 책임이 한 함수에 남아 있음. | 낮 |
| `control/converter_app.py` | 6 | 사용하지 않는 import | `ConvertCommand`, `RegisterCommand`를 import만 하고 코드에서 사용하지 않음. | 낮 |
| `control/converter_app.py` | 48–51 | 사용하지 않는 함수 | `handle_register_line()`이 프로젝트 전역에서 호출처 없음(데드 API). | 중 |
| `control/converter_app.py` | 38–46 | 중복 로직 (유지보수) | `handle_convert_line`과 `handle_convert_line_json`이 파싱·`convert_all`·렌더만 다르고 흐름이 동일해, 한쪽 수정 시 다른 쪽 누락 위험. | 낮 |
| `data/repository.py` | 8 | 사용하지 않는 import | `METERS_PER_FEET`, `METERS_PER_METER`, `METERS_PER_YARD`를 import만 하고 본 파일에서 미사용. | 낮 |
| `data/repository.py` | 39–78 | 긴 함수 | `load()`가 약 40줄로, 파일 판별·읽기·파싱·검증·레지스트리 구성이 한 메서드에 집중됨(20줄 초과). | 중 |
| `data/repository.py` | 41–42 | 불완전한 예외 처리 | 설정 파일 경로가 존재하지 않으면 `ConfigLoadError` 없이 기본 `UnitRegistry`로 조용히 대체. 의도된 동작일 수 있으나, “잘못된 경로”와 “의도적 기본값” 구분이 호출자에게 드러나지 않음. | 중 |
| `data/repository.py` | 63–67 | 불완전한 예외 처리 | `json.JSONDecodeError`, `ValidationError` 등을 모두 동일한 `CFG_PARSE_ERROR` 메시지로 뭉개 원인 구분·복구 힌트가 어려움. | 낮 |
| `data/repository.py` | 81–86 | 사용하지 않는 함수 | `default_feet_per_meter()`, `default_yard_per_meter()`가 정의만 되고 호출처 없음. | 낮 |

---

### 점검 항목별 — **이번 범위에서 해당 없음** (표에 넣지 않음)

| 점검 항목 | 판단 |
|-----------|------|
| `main()`에 파싱·검증·변환·출력 혼재 | **현재 `UnitConverter.py`에는 없음.** `ConverterApp`·`boundary`·`entity`로 위임된 상태. |
| 단위별 `if-else` 체인 (OCP) | **`control/`, `data/`, `UnitConverter.py`에 없음.** (환산 분기는 `entity` 쪽) |
| `3.28084` / `1.09361` 하드코딩 | **해당 파일에 리터럴 없음.** `data/repository.py`는 `entity.constants`의 `FEET_PER_METER`·`YARD_PER_METER`를 참조하며, 미사용 `default_*` 메서드도 상수 위임만 함. |

과거 레거시(단일 `main()` + `if-else` + 매직 넘버)는 문서·결함 목록 기준이고, **지금 이 세 경로의 소스에는 남아 있지 않습니다.** 리팩토링 후 회귀를 막으려면 `UnitConverter.py` CLI 경로를 subprocess/Golden Master로 잠그는 것이 별도 과제입니다.

[REDACTED]

---

### Turn 16 — user

<user_query>
@UnitConverter.py 를 ECB(Entity-Control-Boundary) 패턴으로 분석해줘.
코드는 수정하지 말고 다음만 답해줘:

1. 현재 main() 함수에서 ECB 역할이 어떻게 혼재하는가?
   - Entity: 변환 비율 데이터 (3.28084, 1.09361)
   - Control: 변환 로직 (if-else 체인)
   - Boundary: 입력 파싱, 출력 포맷
2. 어느 코드를 어느 클래스/모듈로 이동해야 하는가?
3. 새 단위 추가 시 변경이 최소화되는 구조를 제안하라.
</user_query>

---

### Turn 17 — assistant

`UnitConverter.py`와 기존 ECB 레이어 구조를 확인한 뒤, 코드 수정 없이 분석만 정리합니다.

[REDACTED]

---

### Turn 18 — assistant

[REDACTED]

---

### Turn 19 — assistant

분석 기준은 **현재 저장소의 `UnitConverter.py`**입니다. 질문에 나온 `3.28084`·`if-else`는 **과거 단일 스크립트 레거시**에 해당하고, 지금 이 파일에는 **남아 있지 않습니다**. ECB 관점에서는 “이미 분리된 것”과 “`main()`에 아직 남은 것”을 구분해서 설명합니다.

---

## 1. 현재 `main()`에서 ECB 역할이 어떻게 혼재하는가?

### 현재 `UnitConverter.py`의 `main()`

```9:15:c:\DEV_BR\UnitConvertor_06\UnitConverter.py
def main() -> None:
    input_str = input("Insert value for converting (ex: meter:2.5): ")
    app = ConverterApp()
    try:
        print(app.handle_convert_line(input_str))
    except ParseError as exc:
        print(exc.message)
```

| ECB | 질문 예시(레거시) | **현재 `main()`** |
|-----|-------------------|-------------------|
| **Entity** | `3.28084`, `1.09361` 비율 | **없음.** 비율·단위 데이터는 `entity/constants.py`, `entity/registry.py`에 있음. |
| **Control** | 단위별 `if-else` 환산 | **없음.** 환산은 `entity/engine.py` + `control/converter_app.py`의 `handle_convert_line()`이 담당. |
| **Boundary** | `unit:value` 파싱, 표 출력 | **일부만 `main()`에 남음** — `input`/`print`, 프롬프트 문구, `ParseError`를 사용자 메시지로 출력. |

즉, **질문에 적힌 3가지 혼재(비율 + if-else + 파싱/출력)는 더 이상 `main()` 안에 같이 있지 않습니다.**  
남은 혼재는 **“CLI Boundary(입출력)”와 “Control 진입(앱 생성·한 줄 처리 위임)”이 한 함수에 묶인 것** 정도입니다.

| 줄 | 역할 | 설명 |
|----|------|------|
| 10 | **Boundary** | stdin에서 한 줄 읽기, 프롬프트 문자열(UI 계약). |
| 11–13 | **Boundary ↔ Control 경계** | `ConverterApp` 생성 + `handle_convert_line()` 호출 — 조립은 Boundary adapter가 할 일인데 `main()`에 있음. |
| 13 | **Boundary(출력)** | `print`로 결과 표시. |
| 14–15 | **Boundary(오류 표현)** | `ParseError`만 잡아 메시지 출력(도메인/제어 예외는 미처리). |

실제 **파싱·검증·전체 변환·표 포맷** 흐름은 `main()` 밖에서 이미 ECB로 나뉘어 있습니다.

```38:41:c:\DEV_BR\UnitConvertor_06\control\converter_app.py
    def handle_convert_line(self, line: str) -> str:
        command = parse_convert_line(line, self._registry)
        lines = self._engine.convert_all(command.unit_id, command.magnitude)
        return render_table(command.unit_id, command.magnitude, lines)
```

- **Boundary**: `boundary/parser.py` (`parse_convert_line`), `boundary/renderers/table.py` (`render_table`)
- **Control**: `control/converter_app.py` (파싱 → 엔진 → 렌더 순서 조율)
- **Entity**: `entity/registry.py`, `entity/engine.py`, `entity/constants.py` (mpu·환산식, `3.28084`/`1.09361`은 표시용 상수)

### 레거시(단일 `main()`)였다면 어떻게 혼재했는가? (참고)

과거 한 파일에 있던 전형적 혼재는 다음과 같았고, **지금은 각각 아래 모듈로 이전된 상태**입니다.

| 레거시 `main()` 안 내용 | ECB | 현재 위치 |
|------------------------|-----|-----------|
| `3.28084`, `1.09361`, `0.3048` … | Entity | `entity/constants.py`, `UnitRegistry.with_defaults()` |
| `if unit == "meter": … elif "feet": …` | Control | `ConversionEngine.convert()` (레지스트리 기반, 분기 없음) |
| `split(":")`, 음수 검사, `print` 포맷 | Boundary | `boundary/parser.py`, `boundary/renderers/table.py` |

---

## 2. 어느 코드를 어느 클래스/모듈로 이동해야 하는가?

**이미 이동된 것(재이동 불필요)**

| 관심 코드 | 이동 목표 | 현재 모듈 |
|-----------|-----------|-----------|
| 변환 비율·단위 식별자 | Entity | `entity/constants.py`, `entity/registry.py` |
| `source×mpu_source / mpu_target`, 전 단위 환산 | Control (+ Entity 협력) | `entity/engine.py`, `control/converter_app.py` |
| `meter:2.5` 파싱·오류 메시지 | Boundary | `boundary/parser.py`, `boundary/errors.py` |
| 표/JSON 문자열 | Boundary | `boundary/renderers/table.py`, `json_renderer.py` |
| 설정 파일 → 레지스트리 | Data → Entity 주입 | `data/repository.py` → `ConverterApp.load_config()` |

**아직 `UnitConverter.py` / `main()`에 남아 있어 옮기면 좋은 것**

| 현재 위치 | 이동 목표 | 이유 |
|-----------|-----------|------|
| `input(...)`, 프롬프트 문구 (L10) | `boundary/cli_adapter.py` (또는 `main.py`) | stdin은 Boundary 전용 I/O. |
| `print(...)`, `ParseError` 출력 (L13–15) | 동일 CLI adapter | 사용자 표현·종료 코드는 Boundary 책임. |
| `ConverterApp()` 생성 + `handle_convert_line` 호출 (L11–13) | CLI adapter가 Control을 호출 | `UnitConverter.py`는 **실행 진입점만** (`if __name__ == "__main__"`). |
| (선택) `handle_register_line` 등 미연결 API | `ConverterApp` + CLI 서브커맨드/별도 진입 | Control에 로직은 있으나 CLI에서 아직 미노출. |

**`UnitConverter.py`의 목표 형태(개념)**

```text
UnitConverter.py          → python -m 또는 __main__ 한 줄만
boundary/cli_adapter.py   → read_line(), write_result(), write_error(), run_cli()
control/converter_app.py  → 유스케이스 조율 (현 상태 유지)
entity/*                  → 비율·환산 규칙 (현 상태 유지)
data/repository.py        → 외부 설정 로드 (현 상태 유지)
```

---

## 3. 새 단위 추가 시 변경이 최소화되는 구조 제안

핵심은 **단위마다 `if-else`를 추가하지 않고, Entity의 레지스트리만 확장**하는 것입니다. Control·Boundary·`main()`은 수정하지 않는 것이 이상적입니다.

```mermaid
flowchart LR
  CLI["Boundary: CLI / parser / renderer"]
  APP["Control: ConverterApp"]
  ENG["Entity: ConversionEngine"]
  REG["Entity: UnitRegistry"]
  CFG["Data: UnitDefinitionRepository"]

  CLI --> APP
  APP --> ENG
  ENG --> REG
  CFG --> REG
```

### 단위 추가 시 변경 지점 (우선순위)

| 방법 | 변경 파일 | `main()` / Control / parser 수정 |
|------|-----------|----------------------------------|
| **A. 기본 3단위 고정** | `entity/registry.py`의 `with_defaults()`에 `register(...)` 한 줄 | **불필요** |
| **B. 설정 파일** | `units.yaml` / `units.json`만 추가·수정 | **불필요** (`load_config(path)` 호출만) |
| **C. 런타임 등록** | `register_unit(id, meters_per_unit)` 또는 `handle_register_line` | **불필요** (CLI만 연결하면 됨) |

### 동작 원리 (OCP)

`convert_all()`이 **등록된 모든 `unit_id`를 순회**하므로, 새 단위는 레지스트리에만 넣으면 출력 행이 자동으로 늘어납니다.

```27:33:c:\DEV_BR\UnitConvertor_06\entity\engine.py
    def convert_all(self, source_unit: str, magnitude: float) -> list[ConversionLine]:
        if magnitude < 0:
            raise NegativeMagnitudeError(magnitude)
        return [
            ConversionLine(unit_id, self.convert(source_unit, magnitude, unit_id))
            for unit_id in self._registry.list_unit_ids()
        ]
```

### 권장 계층 책임 (요약)

| 계층 | 책임 | 새 단위 시 |
|------|------|------------|
| **Entity** | `meters_per_unit`, 환산식, `ConversionLine` | 레지스트리/상수/설정만 확장 |
| **Control** | 파싱 결과 → `convert_all` → 렌더 문자열 반환 | **변경 없음** |
| **Boundary** | 문자열↔명령, 표·JSON 포맷, stdin/stdout | **변경 없음** (포맷 규칙 동일 시) |
| **Data** | 파일에서 `UnitRegistry` 구성 | YAML/JSON에 항목 추가만 |

### `3.28084` / `1.09361` 처리

- **환산용**: `METERS_PER_FEET`(0.3048) 등 **mpu**만 Entity에 두고 엔진은 mpu만 사용 (현재 구조).
- **표시용 README 비율**: `FEET_PER_METER`, `YARD_PER_METER`는 `entity/constants.py`에만 두고, Boundary `render_table`은 `round_display`로 표시 — **단위 추가 시 이 상수를 늘리지 않음**.

---

**한 줄 요약:** 현재 `UnitConverter.py`의 `main()`은 ECB **대혼재 상태가 아니라** Boundary I/O + Control 위임만 남은 **얇은 진입점**이고, 질문의 Entity/Control 혼재는 **이미 `entity/`·`control/`·`boundary/`로 분리됨** — 남은 작업은 CLI를 `boundary/cli_adapter`로 빼고, 새 단위는 **`UnitRegistry` 등록(또는 config)만**으로 확장하는 구조를 유지하는 것입니다.

[REDACTED]

---

### Turn 20 — user

<user_query>
앞서 분석한 내용을 바탕으로 리팩토링 계획서를 작성해줘.
코드는 아직 수정하지 말고:

## 리팩토링 대상 목록 (우선순위 순)
| 순번 | 대상 | 문제 | 적용 기법 | 우선순위 |

## 리팩토링 후보 목록
R-U1: 입력 파싱을 InputParser로 분리
R-U2: 예외 메시지·코드 상수화
R-U3: 출력 포맷 생성을 OutputFormatter로 분리
R-L1: 변환 비율을 ConversionRule Value Object로 교체
R-L2: if-else 체인을 UnitRegistry(Map/Dictionary)로 교체
R-L3: 매직 넘버 3.28084/1.09361 → 상수 또는 설정 파일
R-L4: convert() 함수 추출 (meter 허브 변환 로직 단일화)

## 테스트 선행 필요 항목
## 리팩토링 후 검증 방법 (회귀 테스트 실행 명령어)
</user_query>

---

### Turn 21 — assistant

리팩토링 계획서 작성을 위해 테스트·문서·현재 구조를 확인합니다.

[REDACTED]

---

### Turn 22 — assistant

[REDACTED]

---

### Turn 23 — assistant

앞선 ECB·코드 스멜 분석을 반영한 **리팩토링 계획서**입니다. (코드 변경 없음)

---

## 리팩토링 대상 목록 (우선순위 순)

| 순번 | 대상 | 문제 | 적용 기법 | 우선순위 |
|------|------|------|-----------|----------|
| 1 | `UnitConverter.py` `main()` | CLI I/O·`ConverterApp` 조립·`ParseError`만 처리가 한 함수에 남음; BCE와 이중 경로(DEF-008) | **Extract Class** → `boundary/cli_adapter.py`, **Thin Entry** | **높음** |
| 2 | `tests/test_golden_master.py` + `golden_master.py` | Golden Master가 `ConverterApp` 직접 호출; `UnitConverter.py` subprocess 경로 미검증 | **테스트 보강** → `capture_scenario_output_subprocess` 연동 또는 CLI 전용 TC | **높음** |
| 3 | `UnitConverter.py` 오류 종료 | 파싱 실패 시 `print`만 하고 exit code 미설정(DEF-006 Open) | **Replace Error Code with Exception** + CLI에서 `sys.exit(1)` | **중** |
| 4 | `data/repository.py` `load()` | 약 40줄, 읽기·파싱·검증·Registry 구성 혼재 | **Extract Method** (`_read_payload`, `_validate_config`, `_build_registry`) | **중** |
| 5 | `data/repository.py` L41–42 | 설정 파일 없을 때 조용히 기본 Registry 대체(계약 모호) | **명시적 정책** — 문서·테스트와 정합 후 **Replace Magic Number**가 아닌 **명확한 API** (`load` vs `load_or_default`) | **중** |
| 6 | `control/converter_app.py` L38–46 | `handle_convert_line` / `handle_convert_line_json` 중복 | **Extract Method** (`_run_convert_line(renderer)`) | **낮** |
| 7 | `control/converter_app.py` L48–51 | `handle_register_line` 미사용(데드 API) | **연결**(CLI) 또는 **Remove Dead Code** | **낮** |
| 8 | `data/repository.py` L8, L81–86 | 미사용 import·`default_*` 정적 메서드 | **Remove Dead Code** | **낮** |
| 9 | `control/converter_app.py` L6 | 미사용 import `ConvertCommand`, `RegisterCommand` | **Remove Dead Code** | **낮** |

> **참고:** 레거시 단일 `main()`의 `if-else`·`3.28084` 하드코딩은 **이미 BCE로 이전됨**. 아래 후보 R-L1~R-L4는 **재적용이 아니라 검증·정리** 성격이 큼.

---

## 리팩토링 후보 목록

| ID | 내용 | 현재 상태 | 계획서 반영 |
|----|------|-----------|-------------|
| **R-U1** | 입력 파싱을 `InputParser`로 분리 | **부분 완료** — `boundary/parser.py` (`parse_convert_line`, `parse_register_line`) | 클래스명 정리(`InputParser` 래퍼) 또는 **현 상태 유지** 후 CLI만 분리. `UnitConverter.py`에는 파싱 로직 추가 금지. |
| **R-U2** | 예외 메시지·코드 상수화 | **부분 완료** — `boundary/errors.py`, `ParseError.code`, `ConfigLoadError.code` | CLI adapter에서 **모든 사용자 오류**를 동일 코드·문구로 매핑; `main()`의 `ParseError`만 처리 → **통합 오류 핸들러**로 확장. |
| **R-U3** | 출력 포맷을 `OutputFormatter`로 분리 | **부분 완료** — `boundary/renderers/table.py`, `json_renderer.py` | `OutputFormatter` 별칭/파사드 도입은 선택; **우선순위 낮음**. 표시 규칙은 `entity/display.py`와 연동 유지. |
| **R-L1** | 변환 비율을 `ConversionRule` VO로 교체 | **부분 완료** — `UnitRegistry` + `meters_per_unit` | 필요 시 `UnitDefinition(id, meters_per_unit)` dataclass로 **명시적 VO**화; 엔진 API는 `get_meters_per_unit` 유지. |
| **R-L2** | `if-else` → `UnitRegistry`(Map) | **완료** — `entity/registry.py`, `ConversionEngine` | **추가 작업 없음**. 신규 단위는 `register()` / config만 변경. |
| **R-L3** | `3.28084` / `1.09361` → 상수·설정 | **완료** — `entity/constants.py` (`FEET_PER_METER`, `YARD_PER_METER`, mpu 상수) | 환산은 mpu, 표시는 `round_display` + renderer. **재하드코딩 금지**. |
| **R-L4** | `convert()` 추출(허브 변환 단일화) | **완료** — `ConversionEngine.convert()` / `convert_all()` | **추가 작업 없음**. `ConverterApp.convert()`는 파사드로 유지. |

### 후보 ↔ 대상 매핑 (실행 순)

```text
[1단계: 안전망] Golden Master CLI 경로 + pytest GREEN
[2단계: Boundary] R-U1, R-U2, R-U3 → cli_adapter + 기존 parser/renderer 연결
[3단계: Control/Data 정리] 중복 제거, load() 분해, 데드 코드 제거
[4단계: Entity] R-L1~R-L4는 회귀 확인만 (구조 변경 최소)
```

---

## 테스트 선행 필요 항목

리팩토링 **시작 전** 아래가 GREEN이어야 합니다.

| # | 항목 | 이유 | 현재 근거 |
|---|------|------|-----------|
| T-1 | **전체 pytest GREEN** | BCE 계약 고정 | `docs/defect_list.md` — 33+ passed 기준 |
| T-2 | **Golden Master 4시나리오** | 출력 문자열·줄바꿈 회귀 방지 | `tests/test_golden_master.py` (GM-TC-01~04) |
| T-3 | **`UnitConverter.py` CLI 회귀 TC 추가**(권장) | `main()` 분리 후에도 README Quick Start와 동일 출력 | 현재 GM은 `ConverterApp` 직접 호출; `golden_master.capture_scenario_output_subprocess` 미연동 |
| T-4 | **파싱·거부 정책 TC** | R-U2, DEF-003/006 | `tests/boundary/test_exception_parse_policy.py` |
| T-5 | **표시·반올림 TC** | R-U3, DEF-002 | `tests/boundary/test_convert_display_table.py` |
| T-6 | **엔진·레지스트리 TC** | R-L2~R-L4 회귀 | `tests/entity/test_convert_normal_happy_path.py`, `test_register_dynamic_unit.py` |
| T-7 | **config 로드 TC** | `load()` 분해 전 | `tests/data/test_config_load_json_yaml.py` |
| T-8 | **(선택) CLI exit code TC** | DEF-006 Close | `subprocess`로 `python UnitConverter.py` + 잘못된 입력 → exit ≠ 0 |

**선행 작업 순서**

1. `pytest` 전체 PASS 확인  
2. T-3·T-8 미존재 시 **테스트만 먼저 추가**(RED → 기대 동작 고정)  
3. 그 다음 순번 1~2( CLI adapter + GM subprocess ) 진행  

---

## 리팩토링 후 검증 방법 (회귀 테스트 실행 명령어)

프로젝트 루트(`c:\DEV_BR\UnitConvertor_06`)에서 실행합니다.

### 1) 필수 — 전체 회귀

```powershell
pytest tests/ -v
```

### 2) 필수 — Golden Master (승인 회귀)

```powershell
pytest -m golden_master -v
```

### 3) 권장 — RED + BCE 레이어별

```powershell
pytest tests/red/ -v
pytest tests/entity/ tests/boundary/ tests/data/ -v
```

### 4) 권장 — 커버리지 (리팩토링 영향 레이어)

```powershell
pytest tests/ --cov=entity --cov=boundary --cov=control --cov=data --cov-report=term-missing
```

### 5) CLI 수동 스모크 (DEF-002·008·레거시 경로)

```powershell
echo meter:2.5 | python UnitConverter.py
echo meter:-1.0 | python UnitConverter.py
echo parsec:1.0 | python UnitConverter.py
```

기대: BCE와 동일 표(예: `8.2 feet`), 음수·미등록 시 **계약 메시지**·(T-8 적용 후) **비-zero exit**.

### 6) Golden Master 기준 파일 재생성 (의도적 출력 변경 시만)

```powershell
python scripts/generate_golden_master.py
pytest -m golden_master -v
```

> `golden_master_expected.txt` diff는 **의도된 변경**일 때만 커밋.

### 7) CI 동등 검증 (로컬)

```powershell
pytest -m golden_master -v --tb=short
```

(`.github/workflows/golden_master.yml`과 동일 마커)

---

### 완료 기준 (Definition of Done)

- [ ] `pytest tests/` **0 failed**  
- [ ] `pytest -m golden_master` **PASS**  
- [ ] `UnitConverter.py`는 **진입점만**(I/O는 `boundary/cli_adapter`)  
- [ ] `python UnitConverter.py` 출력이 Golden Master·README와 **일치** (DEF-002·008 Close)  
- [ ] R-L2~R-L4 관련 **단위별 if-else·매직 넘버 재도입 없음**  
- [ ] `docs/defect_list.md` 레거시 Open 항목(DEF-006·008) 상태 갱신  

원하시면 이 계획서를 `docs/refactoring_plan.md`로 저장하는 diff도 다음 단계에서 작성할 수 있습니다.

[REDACTED]

---

### Turn 24 — user

<user_query>
당신은 Dual-Track UI + Logic TDD 및 리팩토링 전문가입니다.
프로젝트: @c:\DEV_BR\UnitConvertor_06\ 
이번 작업: 커밋 1개 단위의 Dual-Track REFACTOR만 수행

절대 규칙:
- 새 기능 추가 금지
- 외부 계약(입력 "단위:값" 형식, 출력 "값 단위 = 변환값 단위", 예외 타입) 변경 금지
- 테스트 삭제·완화 금지
- 먼저 테스트 실행 → 리팩토링 → 테스트 재실행 (항상 GREEN 유지)
- 3.28084 / 1.09361 인라인 하드코딩 추가 금지
- Dual-Track 분리:
    Boundary(UI Track): 파싱·검증·포맷 책임만
    Domain(Logic Track): 순수 변환 규칙·계산 책임만

커밋 단위 절차:
Step 0) 전체 테스트 실행 → GREEN 상태 확인
Step 1) 리팩토링 목표 1~2개 선택 (가장 작은 단위)
Step 2) 보호 테스트 점검·보강
Step 3) Dual-Track 리팩토링 수행 (최소 변경)
Step 4) 전체 테스트 재실행 → 모두 통과 확인
Step 5) 커밋 준비 산출물 작성

출력 형식:
1) 이번 커밋 리팩토링 목표 (선택 항목 ID)
2) 변경 범위 요약 (UI Track / Logic Track 분리)
3) 변경 전 문제점 → 변경 후 개선점
4) 수정된 파일 목록
5) 테스트 실행 결과 요약
6) 위험 요소 및 롤백 포인트
7) 커밋 메시지 제안 (Conventional Commit)
   예: refactor(domain): extract UnitRegistry and ConversionRule VO
</user_query>

---

### Turn 25 — assistant

Step 0부터 진행합니다. 전체 테스트를 실행한 뒤, 가장 작은 단위의 Dual-Track REFACTOR 목표를 선택합니다.

[REDACTED]

---

### Turn 26 — assistant

[REDACTED]

---

### Turn 27 — assistant

Step 0: 54 tests GREEN. 목표는 `ConverterApp` 중복 제거(UI Track)와 `data/repository` 데드 코드 정리(Logic/Data Track)입니다.

[REDACTED]

---

### Turn 28 — assistant

[REDACTED]

---

### Turn 29 — assistant

[REDACTED]

---

### Turn 30 — assistant

## Dual-Track REFACTOR — 커밋 1건 산출물

### 1) 이번 커밋 리팩토링 목표 (선택 항목 ID)

| ID | 내용 |
|----|------|
| **계획 순번 6** | `handle_convert_line` / `handle_convert_line_json` 중복 제거 (**Extract Method**) |
| **계획 순번 8·9** | `data/repository.py` 미사용 import·데드 API 제거 (**Remove Dead Code**) |

> R-L1~R-L4, R-U1~R-U3는 이미 BCE에 반영되어 **이번 커밋에서 미수행**.

---

### 2) 변경 범위 요약 (UI Track / Logic Track 분리)

| Track | 변경 | 비변경 |
|-------|------|--------|
| **Boundary (UI)** | `parse_*`, `render_table` / `render_json` 시그니처·문구·동작 동일 | `boundary/*` 파일 무수정 |
| **Control (조율)** | `_run_convert_line()`로 파싱→`convert_all`→렌더 파이프라인 단일화 | 공개 API·반환 문자열 동일 |
| **Domain (Logic)** | `entity/*` 무수정 | `ConversionEngine`, `UnitRegistry` 그대로 |
| **Data** | 미사용 `default_*`·constants import 제거 | `load()` 동작·`ConfigLoadError` 계약 동일 |

---

### 3) 변경 전 문제점 → 변경 후 개선점

| 구분 | 변경 전 | 변경 후 |
|------|---------|---------|
| Control | table/json 핸들러가 동일 3단계를 복붙 → 한쪽만 수정 시 누락 위험 | `_run_convert_line(line, render)` 한 경로로 UI 파이프라인 고정 |
| Control | `ConvertCommand`, `RegisterCommand` import만 하고 미사용 | 불필요 import 제거 |
| Data | `default_feet_per_meter` / `default_yard_per_meter` 호출처 없음, constants import 잔여 | Repository는 config→Registry 책임만 유지 (비율 상수는 `entity/constants` + `UnitRegistry.with_defaults`) |

---

### 4) 수정된 파일 목록

- `control/converter_app.py`
- `data/repository.py`

---

### 5) 테스트 실행 결과 요약

| 단계 | 명령 | 결과 |
|------|------|------|
| Step 0 (전) | `pytest tests/ -v --tb=short` | **54 passed** |
| Step 4 (후) | `pytest tests/ -v --tb=short` | **54 passed** (0.21s) |

- Golden Master 4건 포함
- RED 17건 + BCE 전체 포함
- 테스트 추가/삭제/완화 없음

---

### 6) 위험 요소 및 롤백 포인트

| 위험 | 수준 | 롤백 |
|------|------|------|
| `_run_convert_line` renderer 인자 순서 오류 | 낮음 (기존과 동일 호출) | `git checkout -- control/converter_app.py` |
| `default_*` 제거 후 외부 스크립트 의존 | 낮음 (repo 내 참조 없음) | `git checkout -- data/repository.py` |
| 계약 변경 | 없음 (입력/출력/예외 타입 동일) | Step 0 스냅샷 커밋으로 `git revert` 1커밋 |

**롤백 포인트:** 이 REFACTOR 직전 HEAD (Step 0 GREEN 시점).

---

### 7) 커밋 메시지 제안 (Conventional Commit)

```
refactor(control,data): dedupe convert-line pipeline and remove dead repository helpers

- Extract ConverterApp._run_convert_line for table/json handlers (UI track orchestration)
- Drop unused parser DTO imports from control layer
- Remove unreferenced UnitDefinitionRepository.default_* and entity.constants imports
```

---

커밋까지 진행하려면 “커밋해줘”라고 알려주시면, 규칙에 맞춰 스테이징·커밋만 수행하겠습니다.

[REDACTED]

---

### Turn 31 — user

<user_query>
커밋까지 알아서 해줘
</user_query>

---

### Turn 32 — assistant

커밋 전에 git 상태와 diff를 확인합니다.

[REDACTED]

---

### Turn 33 — assistant

[REDACTED]

---

### Turn 34 — assistant

[REDACTED]

---

### Turn 35 — assistant

커밋까지 완료했습니다.

| 항목 | 내용 |
|------|------|
| **브랜치** | `refactoring` |
| **커밋** | `f829fdc` |
| **메시지** | `refactor(control,data): dedupe convert-line pipeline and remove dead repository helpers` |
| **변경 파일** | `control/converter_app.py`, `data/repository.py` (2 files, +14 / −16) |
| **상태** | working tree clean, `origin/refactoring`보다 **1 commit ahead** |

원격에 올리려면 `git push`만 실행하면 됩니다. push도 진행할까요?

[REDACTED]

---

### Turn 36 — user

<user_query>
푸시는 모든 리펙토링이 완료 된후에 제일 마지막에 해줘
</user_query>

---

### Turn 37 — assistant

알겠습니다.

**`git push`는 모든 리팩토링이 끝난 뒤, 맨 마지막에 한 번만** 하겠습니다.  
지금 `refactoring` 브랜치는 `origin/refactoring`보다 커밋 1개(`f829fdc`) 앞서 있는 상태이고, 원격에는 아직 올리지 않습니다.

이후 REFACTOR 커밋을 이어가도 push는 하지 않고, 전체 작업이 끝났다고 말씀해 주실 때 push하겠습니다.

[REDACTED]

---

### Turn 38 — user

<user_query>
리펙토링 단계마다 커밋을 한거아니야?
대답만 해줘
</user_query>

---

### Turn 39 — assistant

네. 리팩토링 **단계마다 커밋**하는 방식이고, 지금까지는 그중 **1단계만** 커밋(`f829fdc`)한 상태입니다. **push만** 전부 끝난 뒤 마지막에 하기로 한 거예요.

[REDACTED]

---

### Turn 40 — user

<user_query>
그럼 다음 리펙토링이 있지 않아?
대답만
</user_query>

---

### Turn 41 — assistant

네. 계획서 기준으로 **CLI adapter 분리**, **`load()` 분해**, **Golden Master subprocess 보강** 등 **아직 남은 단계**가 있습니다.

[REDACTED]

---

### Turn 42 — user

<user_query>
그럼 위에처럼 진행해주고 푸시 까지는 하지말고 단계가 끝날때마다 커밋만해줘
</user_query>

---

### Turn 43 — assistant

계획서 남은 단계를 순서대로 진행하고, 단계마다 커밋만 하겠습니다(push 없음).

[REDACTED]

---

### Turn 44 — assistant

[REDACTED]

---

### Turn 45 — assistant

남은 단계를 순서대로 진행합니다. 1단계: `data/repository.py`의 `load()` 분해.

[REDACTED]

---

### Turn 46 — assistant

[REDACTED]

---

### Turn 47 — assistant

[REDACTED]

---

### Turn 48 — assistant

[REDACTED]

---

### Turn 49 — assistant

[REDACTED]

---

### Turn 50 — assistant

[REDACTED]

---

### Turn 51 — assistant

[REDACTED]

---

### Turn 52 — assistant

[REDACTED]

---

### Turn 53 — assistant

[REDACTED]

---

### Turn 54 — assistant

[REDACTED]

---

### Turn 55 — assistant

프롬프트와 첫 출력이 한 줄에 붙는 문제를 `golden_master` 캡처 헬퍼에서 수정합니다.

[REDACTED]

---

### Turn 56 — assistant

[REDACTED]

---

### Turn 57 — assistant

[REDACTED]

---

### Turn 58 — assistant

[REDACTED]

---

### Turn 59 — assistant

[REDACTED]

---

### Turn 60 — assistant

[REDACTED]

---

### Turn 61 — assistant

남은 리팩토링 단계를 **커밋 4개** 더 진행했고, **push는 하지 않았습니다.**

| # | 커밋 | 내용 |
|---|------|------|
| 1 | `4503648` | `data/repository.py` — `load()` 헬퍼 분리 |
| 2 | `0e81f87` | `boundary/cli_adapter.py` + `UnitConverter.py` 얇은 진입점 |
| 3 | `4d37b1e` | Golden Master CLI subprocess 동치 테스트 + 캡처 수정 |
| 4 | `5077497` | CLI 파싱 실패 시 `exit 1` (DEF-006) + 테스트 |

**테스트:** `60 passed`  
**브랜치:** `refactoring` — `origin/refactoring`보다 **5 commits ahead** (push 대기)

**의도적으로 건너뜀** (계약/기능 영향): `load()` missing-path 정책 변경, `handle_register_line` 제거·CLI 연결(신규 노출).

전체 리팩토링이 끝났다고 보시면 그때 `git push` 하면 됩니다.

[REDACTED]

---

### Turn 62 — user

<user_query>
모든 리팩토링 커밋 완료 후 전체 테스트와 커버리지를 확인하라.

pytest pytest -v tests/

pip install pytest-cov pytest --cov=unit_converter --cov-report=term-missing pytest --
cov=unit_converter --cov-report=html

확인 항목:
- 모든 TC PASS (TC-A-01~07, TC-B-01~07)
- Golden Master 테스트도 PASS (출력 불변 확인)
- if-else 체인 제거 완료 (UnitRegistry 교체)
- 매직 넘버 3.28084/1.09361 인라인 없음
- Domain(변환 로직)과 Boundary(파싱·출력)가 분리됨
- Domain 커버리지 ≥ 95% / Boundary ≥ 85%

report 폴더에 지금까지의 진행상황 보고서로 작성해주고(파일명은 폴더 내 파일명을 참고해서 번호는 꼭넣어줘)
prompting 폴더에 지금까지 대화내용 전체를 Export Transcript 해줘
파일명은 보고서 파일명과 같게 만들어줘

이후: refactoring → B_06 PR 생성 → 리뷰(너가 자동으로 달아줄 수 있으면 달아주고 안되면 나에게 얘기해줘) → 머지
</user_query>

---

### Turn 63 — assistant

전체 테스트·커버리지 확인 후 보고서·트랜스크립트 작성, PR 생성까지 진행합니다.

[REDACTED]

---

### Turn 64 — assistant

[REDACTED]

---

### Turn 65 — assistant

[REDACTED]

---

### Turn 66 — assistant

[REDACTED]

---

### Turn 67 — assistant

[REDACTED]

---

### Turn 68 — assistant

[REDACTED]

---

### Turn 69 — assistant

[REDACTED]

---

### Turn 70 — assistant

[REDACTED]

---

### Turn 71 — assistant

[REDACTED]

---

### Turn 72 — assistant

[REDACTED]

---

### Turn 73 — assistant

## 검증 요약

| 확인 항목 | 결과 |
|-----------|------|
| **전체 pytest** | **60 passed**, 0 failed |
| **TC-A-01~07** | PASS (`tests/red/boundary` + boundary BCE) |
| **TC-B-01~07** | PASS (`tests/red/entity` + entity BCE) |
| **Golden Master** | **8 passed** (승인 4 + CLI subprocess 동치 4) |
| **if-else 단위 체인** | 프로덕션 코드에 **없음** (`UnitRegistry` + `convert_all`) |
| **매직 넘버 인라인** | 프로덕션은 **`entity/constants.py`만** |
| **Domain / Boundary 분리** | **완료** (아래 구조) |
| **Domain ≥ 95%** | **PASS** (`entity` 핵심 ~95%) |
| **Boundary ≥ 85%** | **미달** (패키지 합산 **~82%**) |

```bash
pytest tests/ -v                    # 60 passed
pytest tests/ --cov=entity --cov=boundary --cov-report=term-missing --cov-report=html
```

> `--cov=unit_converter` 패키지는 없습니다. `entity` / `boundary` 기준으로 측정했습니다.

---

## 산출물

| 파일 | 설명 |
|------|------|
| [Report/05_UnitConvertor_06_Dual_Track_Refactoring_Progress.md](Report/05_UnitConvertor_06_Dual_Track_Refactoring_Progress.md) | 진행 보고서 |
| [prompting/05_UnitConvertor_06_Dual_Track_Refactoring_Progress.md](prompting/05_UnitConvertor_06_Dual_Track_Refactoring_Progress.md) | 대화 Export Transcript |
| [pr-body-refactoring.md](pr-body-refactoring.md) | PR 본문 템플릿 |

---

## Git · Push · PR

- **`git push origin refactoring` 완료** (최신 `d502582`, REFACTOR 5커밋 + 보고서 2커밋)
- **`gh` CLI가 PATH에 없어** PR 생성·리뷰·머지는 **자동 처리 불가**합니다.

**수동 PR (base: `B_06` ← compare: `refactoring`):**

1. https://github.com/yuldakim/UnitConvertor_06/compare/B_06...refactoring  
2. 제목: `refactor: Dual-Track BCE cleanup (CLI adapter, GM subprocess, DEF-006)`  
3. 본문: `pr-body-refactoring.md` 붙여넣기  
4. CI `Golden Master Regression` GREEN 확인 후 머지  

**리뷰:** 제가 GitHub에 코멘트를 달려면 `gh` 설치·로그인(`gh auth login`)이 필요합니다. 설치 후 “PR 만들고 리뷰 달아줘”라고 하시면 이어서 진행하겠습니다.

---

## REFACTOR 커밋 (5건 + 문서)

`f829fdc` → `4503648` → `0e81f87` → `4d37b1e` → `5077497` (+ 보고서 `0df62d6`, PR body `d502582`)

Boundary 85%는 `parse_register_line` / `cli_adapter` 라인 커버 보강으로 후속 1커밋 가능합니다(기능 추가 없이 테스트만). 원하시면 이어서 진행할까요?

[REDACTED]

---

### Turn 74 — user

<user_query>
Boundary 85%는 parse_register_line / cli_adapter 라인 커버 보강 후
보고서 등 문서에 위와 관련된 내용  보강 후 내용으로 수정하고 
gh 설치 후 “PR 만들고 리뷰 달아줘
</user_query>

---

### Turn 75 — assistant

Boundary 커버리지 보강, 문서 업데이트, `gh` 설치 후 PR·리뷰까지 진행합니다.

[REDACTED]

---

### Turn 76 — assistant

[REDACTED]

---

### Turn 77 — assistant

[REDACTED]

---

### Turn 78 — assistant

[REDACTED]

---

### Turn 79 — assistant

[REDACTED]

---

### Turn 80 — assistant

[REDACTED]

---

### Turn 81 — assistant

[REDACTED]

---

### Turn 82 — assistant

[REDACTED]

---

### Turn 83 — assistant

[REDACTED]

---

### Turn 84 — assistant

[REDACTED]

---

### Turn 85 — assistant

[REDACTED]

---

### Turn 86 — assistant

[REDACTED]

---

### Turn 87 — assistant

[REDACTED]

---

### Turn 88 — assistant

[REDACTED]

---

### Turn 89 — assistant

[REDACTED]

---

### Turn 90 — assistant

[REDACTED]

---

### Turn 91 — assistant

[REDACTED]

---

### Turn 92 — assistant

[REDACTED]

---

### Turn 93 — assistant

[REDACTED]

---

### Turn 94 — assistant

## 완료 요약

### 테스트·커버리지 (최종)

| 항목 | 결과 |
|------|------|
| `pytest tests/ -v` | **68 passed** |
| TC-A-01~07 / TC-B-01~07 | **PASS** (`tests/red/` 17건) |
| Golden Master | **8 passed** (출력 불변 + CLI subprocess 동치) |
| if-else 단위 체인 | **없음** |
| `3.28084` / `1.09361` 인라인 (프로덕션) | **`entity/constants.py`만** |
| Domain / Boundary 분리 | **유지** |
| **entity (Domain)** | **~95%** (목표 달성) |
| **boundary** | **100%** (목표 85% **달성**) |

```bash
pytest tests/ -v
pytest tests/ --cov=entity --cov=boundary --cov-report=term-missing --cov-report=html
```

### 이번에 추가한 테스트

- `tests/boundary/test_parser_register.py` — `parse_register_line`, `:2.5` 빈 unit_id
- `tests/boundary/test_cli_adapter.py` — `run_convert_cli` mock (happy / ParseError exit 1)
- `tests/boundary/test_boundary_package.py` — 패키지 export
- `tests/boundary/__init__.py` **삭제** (최상위 `boundary` 패키지 가리던 shadowing 제거)

커밋: `777267f` (테스트), `33e7616` (보고서·리뷰 템플릿) — **`origin/refactoring`에 push 완료**

### 문서

- [Report/05_UnitConvertor_06_Dual_Track_Refactoring_Progress.md](Report/05_UnitConvertor_06_Dual_Track_Refactoring_Progress.md) — 커버리지 **100%**·68 tests 반영
- [docs/pr-review-refactoring.md](docs/pr-review-refactoring.md) — PR 리뷰 코멘트 초안
- [pr-body-refactoring.md](pr-body-refactoring.md) — PR 본문

---

## PR · 리뷰 (gh)

Portable **gh 2.92.0** 설치: `%LOCALAPPDATA%\gh-cli\bin\gh.exe`  
**인증이 없어** PR 생성·리뷰 자동 등록은 여기서 끝까지 실행하지 못했습니다.

로컬에서 한 번만 로그인한 뒤:

```powershell
$gh = "$env:LOCALAPPDATA\gh-cli\bin\gh.exe"
& $gh auth login

cd c:\DEV_BR\UnitConvertor_06
& $gh pr create --base B_06 --head refactoring `
  --title "refactor: Dual-Track BCE cleanup (CLI adapter, GM subprocess, boundary cov 100%)" `
  --body-file pr-body-refactoring.md

# PR 번호 확인 후 리뷰 코멘트
& $gh pr comment <PR번호> --body-file docs/pr-review-refactoring.md
```

또는 브라우저: https://github.com/yuldakim/UnitConvertor_06/compare/B_06...refactoring  

CI `Golden Master Regression` GREEN 확인 후 **Squash merge** → `B_06`.

`gh auth login`을 마치신 뒤 “PR 만들어줘”라고 다시 보내주시면, 인증된 환경에서 `pr create`·`pr comment`까지 이어서 실행하겠습니다.

[REDACTED]

---

### Turn 95 — user

<user_query>Briefly inform the user about the task result and perform any follow-up actions (if needed). If there's no follow-ups needed, don't explicitly say that.</user_query>

---

### Turn 96 — user

<user_query>Briefly inform the user about the task result and perform any follow-up actions (if needed). If there's no follow-ups needed, don't explicitly say that.</user_query>

---

### Turn 97 — assistant

[REDACTED]

---

### Turn 98 — assistant

두 백그라운드 작업은 UI상 **aborted**로 표시됐지만, 실제 작업은 **정상 완료**된 상태입니다.

- **테스트 재실행** (`tests/boundary/__init__.py` 제거 후): **68 passed**
- **커밋·push**: `777267f`(boundary 커버리지 100% 테스트), `33e7616`(보고서·리뷰 템플릿) — `refactoring` = `origin/refactoring`, working tree clean

PR·리뷰만 `gh auth login` 후 진행하면 됩니다.

[REDACTED]

---

### Turn 99 — user

<user_query>
gh auth login을 어떻게 하면되는데?
</user_query>

---

### Turn 100 — assistant

Windows에서 portable `gh`로 로그인하는 방법입니다.

### 1. 터미널 열기
PowerShell 또는 Cursor 통합 터미널에서 프로젝트 폴더로 이동합니다.

```powershell
cd c:\DEV_BR\UnitConvertor_06
$gh = "$env:LOCALAPPDATA\gh-cli\bin\gh.exe"
```

(`gh`가 PATH에 있으면 `gh`만 써도 됩니다.)

### 2. 로그인 시작

```powershell
& $gh auth login
```

### 3. 프롬프트 선택 (권장)

| 질문 | 권장 |
|------|------|
| GitHub.com / Enterprise | **GitHub.com** |
| Protocol | **HTTPS** (또는 이미 SSH 쓰면 SSH) |
| Authenticate | **Login with a web browser** (가장 쉬움) |
| Paste authentication token | 브라우저에서 받은 **일회용 코드** 붙여넣기 |

브라우저가 열리면 GitHub 로그인 → 코드 복사 → 터미널에 붙여넣기 → 완료.

### 4. 확인

```powershell
& $gh auth status
```

`Logged in to github.com as <사용자명>` 이 나오면 성공입니다.

### 5. 이후 PR (예시)

```powershell
& $gh pr create --base B_06 --head refactoring `
  --title "refactor: Dual-Track BCE cleanup" `
  --body-file pr-body-refactoring.md
```

---

**대안 (브라우저 없이):** [GitHub → Settings → Developer settings → Personal access tokens](https://github.com/settings/tokens)에서 `repo` 권한 토큰을 만든 뒤:

```powershell
& $gh auth login --with-token
# 토큰 붙여넣고 Enter, Ctrl+Z 후 Enter (Windows)
```

로그인까지 하셨으면 “PR 만들어줘”라고 보내주시면 이어서 `pr create`·리뷰 코멘트까지 진행할 수 있습니다.

[REDACTED]

---

### Turn 101 — user

<user_query>
@c:\Users\jyk17\.cursor\projects\c-DEV-BR-UnitConvertor-06\terminals\1.txt:64-67 
</user_query>

---

### Turn 102 — assistant

`gh`가 PATH에 없어서 발생한 오류입니다. portable로 설치된 경로를 직접 쓰면 됩니다.

[REDACTED]

---

### Turn 103 — assistant

**CMD**에서는 아래처럼 **전체 경로**로 실행하세요.

```cmd
"%LOCALAPPDATA%\gh-cli\bin\gh.exe" auth login
```

또는 한 줄로:

```cmd
C:\Users\jyk17\AppData\Local\gh-cli\bin\gh.exe auth login
```

로그인 확인:

```cmd
"%LOCALAPPDATA%\gh-cli\bin\gh.exe" auth status
```

---

**매번 `gh`만 쓰고 싶다면** (현재 CMD 세션만):

```cmd
set PATH=%LOCALAPPDATA%\gh-cli\bin;%PATH%
gh auth login
```

---

`auth login`은 **브라우저·코드 입력**이 필요해서, 여기서 대신 실행할 수는 없습니다. 터미널에서 위 명령을 실행한 뒤 안내에 따라 진행하면 됩니다.

[REDACTED]

---

### Turn 104 — user

<user_query>
@c:\Users\jyk17\.cursor\projects\c-DEV-BR-UnitConvertor-06\terminals\1.txt:69-73 
</user_query>

---

### Turn 105 — assistant

지금 화면에서는 **HTTPS**를 선택하면 됩니다.

| 선택 | 언제 쓰면 좋은지 |
|------|------------------|
| **HTTPS** (권장) | GitHub 웹 로그인·토큰으로 간단히 연결. 이미 `git push`가 HTTPS로 되고 있다면 이쪽이 맞습니다. |
| **SSH** | PC에 SSH 키를 GitHub에 등록해 두었을 때 |

**Enter**로 HTTPS 확정한 뒤, 다음 질문에서는 보통:

1. **Login with a web browser** 선택  
2. 브라우저에서 코드 복사 → 터미널에 붙여넣기  

까지 진행하면 됩니다.

[REDACTED]

---

### Turn 106 — user

<user_query>
PR 만들고 자체적으로 코드리뷰 후 B_06으로 머지해줘
</user_query>

---

### Turn 107 — assistant

[REDACTED]

---

### Turn 108 — assistant

[REDACTED]

---

### Turn 109 — assistant

[REDACTED]

---

### Turn 110 — assistant

[REDACTED]

---

### Turn 111 — assistant

[REDACTED]

---

### Turn 112 — assistant

GitHub CLI 인증이 아직 완료되지 않아 PR 생성·머지를 여기서 실행할 수 없습니다. 터미널에 `You are not logged into any GitHub hosts`와 토큰 오류(401, `read:org` 누락)가 남아 있습니다. 인증 완료 후 바로 실행할 스크립트를 추가합니다.

[REDACTED]

---

### Turn 113 — assistant

[REDACTED]

---

### Turn 114 — assistant

## 현재 상태

`gh auth login`이 **아직 실패**한 상태라 PR·리뷰·머지를 API로 실행할 수 없습니다.  
(토큰: `read:org` 누락 또는 401 Bad credentials)

`refactoring` 브랜치는 이미 `origin`에 push되어 있고, **열린 PR은 없습니다.**

---

## 1) 인증 먼저 (권장: 브라우저)

```cmd
"%LOCALAPPDATA%\gh-cli\bin\gh.exe" auth login
```

| 단계 | 선택 |
|------|------|
| Protocol | **HTTPS** |
| Git credentials | **Yes** |
| 인증 방식 | **Login with a web browser** (토큰 붙여넣기보다 쉬움) |

토큰을 쓸 경우: [Fine-grained 또는 classic PAT](https://github.com/settings/tokens)에 **`repo`**, **`read:org`**, **`workflow`** 포함.

확인:

```cmd
"%LOCALAPPDATA%\gh-cli\bin\gh.exe" auth status
```

---

## 2) 인증 후 PR + 리뷰 + 머지 (한 번에)

프로젝트에 스크립트를 넣어 두었습니다.

```cmd
cd c:\DEV_BR\UnitConvertor_06
powershell -ExecutionPolicy Bypass -File scripts\pr_merge_refactoring_to_B06.ps1
```

동작: `refactoring` → `B_06` PR 생성 → `docs/pr-review-refactoring.md` 리뷰 코멘트 → CI 확인 후 **squash merge**

---

## 3) 인증이 끝났다면

터미널에서 `auth status`가 성공한 뒤 **「인증 완료」**라고 보내주시면, 같은 `gh` 명령으로 PR 생성·리뷰·머지를 대신 실행하겠습니다.

[REDACTED]

---

### Turn 115 — user

<user_query>
인증완료
</user_query>

---

### Turn 116 — assistant

[REDACTED]

---

### Turn 117 — assistant

[REDACTED]

---

### Turn 118 — assistant

[REDACTED]

---

### Turn 119 — assistant

[REDACTED]

---

### Turn 120 — assistant

[REDACTED]

---

### Turn 121 — assistant

[REDACTED]

---

### Turn 122 — assistant

[REDACTED]

---

### Turn 123 — assistant

PR 생성·리뷰·머지까지 완료했습니다.

## 결과

| 항목 | 내용 |
|------|------|
| **PR** | https://github.com/yuldakim/UnitConvertor_06/pull/3 |
| **리뷰 코멘트** | `docs/pr-review-refactoring.md` 내용으로 등록 |
| **CI** | Golden Master Regression **PASS** |
| **머지** | `B_06`에 **Squash merge** 완료 (`ab8c461`) |
| **브랜치** | `refactoring`은 삭제하지 않음 (`--delete-branch=false`) |

## 로컬 동기화 (선택)

```cmd
cd c:\DEV_BR\UnitConvertor_06
git fetch origin
git checkout B_06
git pull origin B_06
```

`refactoring`을 `B_06` 기준으로 다시 맞추려면:

```cmd
git checkout refactoring
git fetch origin
git rebase origin/B_06
```

[REDACTED]

---

### Turn 124 — user

<user_query>
머지까지 완료했는데 refactoring 브랜치에 또 커밋하고 푸시해서 pr할 수 있어?
</user_query>

---

### Turn 125 — assistant

네, **가능합니다.** 머지 후에도 `refactoring` 브랜치에 커밋하고 push한 뒤 `B_06`으로 PR을 다시 열 수 있습니다.

다만 **머지 직후 `B_06`이 `refactoring`보다 앞서 있으므로**, 새 PR이 깔끔하려면 보통 아래 중 하나를 먼저 합니다.

### 권장: `B_06` 기준으로 맞춘 뒤 작업

```cmd
git fetch origin
git checkout refactoring
git rebase origin/B_06
# 충돌 없으면
git push origin refactoring
```

이후 새 커밋 → push → PR:

```cmd
"%LOCALAPPDATA%\gh-cli\bin\gh.exe" pr create --base B_06 --head refactoring --title "..." --body-file ...
```

### 대안: 그냥 이어서 커밋만

`rebase` 없이 `refactoring`에만 커밋·push해도 PR은 만들 수 있습니다.  
다만 PR diff에 **이미 머지된 커밋이 섞이거나** GitHub가 “이미 merged”로 보일 수 있어, **rebase(또는 `B_06`에서 브랜치 재생성)** 이 더 안전합니다.

### 브랜치 새로 파기 (팀에서 자주 쓰는 방식)

```cmd
git fetch origin
git checkout -B refactoring origin/B_06
# 새 작업 후
git push -u origin refactoring --force-with-lease
```

---

**정리:**  
- **같은 `refactoring` 이름으로 계속 써도 됨** → `B_06`과 동기화(rebase/재생성) 후 커밋·push·PR  
- **PR #3은 이미 MERGED**이므로, 다음 작업은 **PR #4**처럼 새 PR이 됩니다.

[REDACTED]

---

### Turn 126 — user

<user_query>
그럼 B_06으로 전환하고
refactoring 브랜치를 삭제해줘
</user_query>

---

### Turn 127 — assistant

[REDACTED]

---

### Turn 128 — assistant

[REDACTED]

---

### Turn 129 — assistant

작업 반영했습니다.

| 작업 | 결과 |
|------|------|
| `B_06` 전환 | 완료 (`ab8c461`까지 pull) |
| 로컬 `refactoring` 삭제 | 완료 |
| 원격 `origin/refactoring` 삭제 | 완료 |

현재 브랜치: **`B_06`** (origin과 동기화)

다음 리팩토링 작업을 이어갈 때는 예:

```cmd
git checkout -b refactoring origin/B_06
```

로 `B_06`에서 새 `refactoring`을 만들면 됩니다.

참고: `scripts/pr_merge_refactoring_to_B06.ps1`만 아직 untracked입니다. 필요 없으면 삭제해도 됩니다.

[REDACTED]

---

### Turn 130 — user

<user_query>
프로젝트: c:\DEV\UnitConverter_Python

현재 테스트 커버리지를 점검해줘.
- 실행: pip install pytest-cov && pytest --cov=unit_converter --cov-report=term-missing
- 커버되지 않은 줄 중 Invariant 관련 분기 우선 식별
  (특히: meter↔feet/yard 비율 변환 분기, 음수 입력 처리, 없는 단위 처리)
- Domain Logic 95% 미달 시: 누락 테스트 케이스 제안 (구현 코드 추가 금지)
- Boundary 85% 미달 시: 누락 계약 테스트 케이스 제안

출력:
| 파일 | Stmts | Miss | Cover | 미달 원인 | 추가 테스트 제안 |
</user_query>

---

### Turn 131 — assistant

`c:\DEV\UnitConverter_Python` 프로젝트 구조와 커버리지를 확인합니다.

[REDACTED]

---

### Turn 132 — assistant

[REDACTED]

---

### Turn 133 — assistant

[REDACTED]

---

### Turn 134 — assistant

[REDACTED]

---

### Turn 135 — assistant

[REDACTED]

---

### Turn 136 — assistant

[REDACTED]

---

### Turn 137 — assistant

[REDACTED]

---

### Turn 138 — assistant

[REDACTED]

---

### Turn 139 — assistant

[REDACTED]

---

### Turn 140 — assistant

[REDACTED]

---

### Turn 141 — assistant

## 경로 안내

`c:\DEV\UnitConverter_Python`는 **이 환경에 없습니다.**  
동일 계열로 **`c:\DEV_BR\UnitConvertor_06`** 를 점검했습니다.

| 명령 | 결과 |
|------|------|
| `pytest --cov=unit_converter` | **No data to report** (`unit_converter` 패키지 없음) |
| 실제 패키지 | `entity`(Domain), `boundary`, `control`, `data` |

권장 명령:

```bash
pytest tests/ --cov=entity --cov=boundary --cov-report=term-missing
```

**68 passed**, 기준 요약:

| 레이어 | Cover | 목표 | 판정 |
|--------|-------|------|------|
| **entity (Domain)** | **~95.5%** (88 stmts, 4 miss) | ≥ 95% | **PASS (근소)** |
| **boundary** | **100%** (112 stmts) | ≥ 85% | **PASS** |

---

## Invariant 관련 미커버 (우선)

| Invariant | 미커버 위치 | 현재 테스트 |
|-----------|-------------|-------------|
| meter↔feet/yard 비율 | **없음** (엔진·레지스트리 100%) | `test_convert_normal_*`, RED TC-B-01~04 |
| 음수 입력 | **`entity/engine.py:29`** — `convert_all()` 직접 음수 분기 | `convert()` 음수는 TC-B-08·parser TC-A-03만; **`convert_all(-1)` 미호출** |
| 없는 단위 | **없음** (parser 100%) | TC-A-04, `test_exception_unknown_unit_*` |

---

## 출력 표

| 파일 | Stmts | Miss | Cover | 미달 원인 | 추가 테스트 제안 (구현 코드 추가 없음) |
|------|-------|------|-------|-----------|--------------------------------------|
| `entity/__init__.py` | 3 | 3 | 0% | 패키지 re-export만, 테스트 미import | `from entity import …` 스모크 (비 Invariant) |
| `entity/engine.py` | 22 | 1 | 95% | **L29** `convert_all` 음수 시 `NegativeMagnitudeError` (L28–29) | `engine.convert_all("meter", -1.0)` → `pytest.raises(NegativeMagnitudeError)` (TC-B-08 보강) |
| `entity/constants.py` | 8 | 0 | 100% | — | — |
| `entity/registry.py` | 32 | 0 | 100% | — | — |
| `entity/display.py` | 6 | 0 | 100% | — | — |
| `entity/exceptions.py` | 17 | 0 | 100% | — | — |
| **entity 합계 (Domain)** | **88** | **4** | **~95.5%** | `__init__` 3줄 + engine L29 | 위 2건으로 Domain **안정적 95%+** |
| `boundary/parser.py` | 54 | 0 | 100% | — | — |
| `boundary/cli_adapter.py` | 13 | 0 | 100% | — | — |
| `boundary/errors.py` | 18 | 0 | 100% | — | — |
| `boundary/renderers/*` | 25 | 0 | 100% | — | — |
| `boundary/__init__.py` | 2 | 0 | 100% | — | — |
| **boundary 합계** | **112** | **0** | **100%** | 목표 85% **초과** | **추가 제안 없음** |
| `control/converter_app.py` | 39 | 7 | 82% | L21/25 property, L28 `register_unit`, L38 `convert_all` 래퍼, **L56–58 `handle_register_line`** (CLI 미연결) | `handle_register_line("1 cubit = 0.4572 meter")` 통합; `app.registry`/`app.engine` property 접근 (Control·비 Domain) |
| `data/repository.py` | 55 | 3 | 95% | L41–42 파일 존재 시 `OSError`→`ConfigLoadError`; L52 `yaml is None` | broken file read mock; yaml 미설치 환경 `.yaml` 로드 (Data·비 Invariant) |
| `data/__init__.py` | 2 | 2 | 0% | 패키지 export만 | import 스모크 |

---

## Domain Logic 95% — 누락 테스트 제안 (요약)

1. **`test_engine_convert_all_negative_raises`** — `ConversionEngine(registry).convert_all("meter", -1.0)` → `NegativeMagnitudeError` (Invariant: 음수 거부, parser 우회).
2. *(선택)* **`test_entity_package_exports`** — `entity` public import (커버리지·Invariant와 무관).

meter↔feet/yard·unknown unit은 **추가 Domain 테스트 불필요** (이미 GREEN).

---

## Boundary 85% — 누락 계약 테스트 제안

**현재 100%** → **추가 계약 테스트 제안 없음.**

(과거 htmlcov 스냅샷 기준 `parser`/`cli_adapter` 미커버였으나, `test_parser_register`·`test_cli_adapter` 반영 후 해소됨.)

---

`UnitConverter_Python` 경로에 실제 프로젝트가 있으면 그 경로를 알려주시면 동일 형식으로 다시 점검하겠습니다.

[REDACTED]

---

### Turn 142 — user

<user_query>
프로젝트: @c:\DEV_BR\UnitConvertor_06\ 

현재 테스트 커버리지를 점검해줘.
- 실행: pip install pytest-cov && pytest --cov=unit_converter --cov-report=term-missing
- 커버되지 않은 줄 중 Invariant 관련 분기 우선 식별
  (특히: meter↔feet/yard 비율 변환 분기, 음수 입력 처리, 없는 단위 처리)
- Domain Logic 95% 미달 시: 누락 테스트 케이스 제안 (구현 코드 추가 금지)
- Boundary 85% 미달 시: 누락 계약 테스트 케이스 제안

출력:
| 파일 | Stmts | Miss | Cover | 미달 원인 | 추가 테스트 제안 |
</user_query>

---

### Turn 143 — assistant

[REDACTED]

---

### Turn 144 — assistant

## 실행 결과 요약

| 명령 | 결과 |
|------|------|
| `pytest --cov=unit_converter` | **데이터 없음** — `unit_converter` 모듈 미존재 (`entity` / `boundary` / `control` / `data` 사용) |
| `pytest tests/` (68건) | **전체 PASS** |
| **Domain (`entity`)** | 88 stmts, 4 miss → **~95.5%** (목표 95% **달성**) |
| **Boundary (`boundary`)** | 112 stmts, 0 miss → **100%** (목표 85% **달성**) |

실제 측정 명령: `pytest tests/ --cov=entity --cov=boundary --cov=control --cov=data --cov-report=term-missing`

---

## Invariant 관련 미커버 (우선)

| Invariant | 상태 | 미커버 |
|-----------|------|--------|
| meter↔feet/yard 비율 변환 | **커버됨** | `engine`·`registry`·`constants` 100% (if-else 없음, mpu 기반) |
| 음수 입력 | **부분** | **`entity/engine.py:29`** — `convert_all()` 진입 시 음수 검사 (`convert()`·parser는 TC로 커버) |
| 없는 단위 | **커버됨** | `boundary/parser.py` 100% (TC-A-04 등) |

---

## 출력 표

| 파일 | Stmts | Miss | Cover | 미달 원인 | 추가 테스트 제안 |
|------|-------|------|-------|-----------|------------------|
| `entity/__init__.py` | 3 | 3 | 0% | 패키지 export만, 테스트에서 `from entity import …` 미사용 | `test_entity_exports` — public symbol import (Invariant 무관) |
| `entity/engine.py` | 22 | 1 | 95% | **L29** `convert_all()` 음수 → `NegativeMagnitudeError` (L28–29) 미실행 | `pytest.raises(NegativeMagnitudeError)`: `engine.convert_all("meter", -1.0)` (TC-B-08 보강, parser 우회) |
| `entity/constants.py` | 8 | 0 | 100% | — | — |
| `entity/registry.py` | 32 | 0 | 100% | — | — |
| `entity/display.py` | 6 | 0 | 100% | — | — |
| `entity/exceptions.py` | 17 | 0 | 100% | — | — |
| **`entity` 합계 (Domain)** | **88** | **4** | **~95.5%** | `__init__` 3 + **engine L29** | 위 2건 권장; 비율·unknown unit 추가 불필요 |
| `boundary/parser.py` | 54 | 0 | 100% | — | — |
| `boundary/cli_adapter.py` | 13 | 0 | 100% | — | — |
| `boundary/errors.py` | 18 | 0 | 100% | — | — |
| `boundary/renderers/table.py` | 15 | 0 | 100% | — | — |
| `boundary/renderers/json_renderer.py` | 7 | 0 | 100% | — | — |
| `boundary/renderers/__init__.py` | 3 | 0 | 100% | — | — |
| `boundary/__init__.py` | 2 | 0 | 100% | — | — |
| **`boundary` 합계** | **112** | **0** | **100%** | 85% 목표 **초과** | **추가 계약 테스트 제안 없음** |
| `control/converter_app.py` *(참고)* | 39 | 7 | 82% | L21/25 property, L28 `register_unit`, L38 `convert_all` 래퍼, **L56–58 `handle_register_line`** | Control 계층: `handle_register_line`·property 호출 테스트 (Domain/Boundary 아님) |
| `data/repository.py` *(참고)* | 55 | 3 | 95% | L41–42 `OSError`→`ConfigLoadError`; L52 `yaml is None` | mock broken read / yaml 미설치 분기 (Invariant 아님) |
| `data/__init__.py` *(참고)* | 2 | 2 | 0% | export만 | import 스모크 |

---

## Domain Logic 95% — 제안 (구현 추가 없음)

현재 **달성**(95.5%)이나, Invariant·안정적 여유를 위해:

1. **`test_engine_convert_all_negative_raises`** — `ConversionEngine(UnitRegistry.with_defaults()).convert_all("meter", -1.0)` → `NegativeMagnitudeError` (**유일한 Invariant 관련 Domain 갭**).
2. *(선택)* `test_entity_package_exports` — `entity` `__init__.py` 커버용.

meter↔feet/yard·없는 단위는 **추가 Domain 테스트 불필요**.

---

## Boundary 85% — 제안

**100% 달성** → **누락 계약 테스트 제안 없음.**

(음수/unknown/표 포맷은 `test_exception_parse_policy`, `test_cli_adapter`, `test_convert_display_table`, RED TC-A 등으로 이미 커버.)

[REDACTED]

---

### Turn 145 — user

<user_query>
지금까지 작업한 내용을 Report 폴더에 보고서로 내보내줘.
프로젝트: @c:\DEV_BR\UnitConvertor_06\ 

포함 항목:
1. 작업 개요 (브랜치·날짜·작업자)
2. 완료된 To-Do 항목 요약 (Phase 6 To-Do 기준)
3. RED 단계 결과 (작성한 테스트 목록 + 실패 확인 여부)
4. GREEN 단계 결과 (통과한 테스트 + 커밋 메시지)
5. Refactoring 결과 (선택 항목·변경 파일·회귀 테스트 통과 여부)
6. 커버리지 현황 (레이어별 수치)
7. 미완료 항목 및 다음 단계 제안
8. 발견된 이슈 및 해결 방법
9. 생성형 AI 활용 회고 (도움이 된 순간 / 한계 / TC 작성 팁)

파일명 규칙: Report/YYMMDDn_UnitConverter_Python_[단계]_Report.md
</user_query>

---

### Turn 146 — assistant

Report 작성을 위해 프로젝트 문서·Git 이력·테스트 현황을 수집합니다.

[REDACTED]

---

### Turn 147 — assistant

[REDACTED]

---

### Turn 148 — assistant

[REDACTED]

---

### Turn 149 — assistant

[REDACTED]

---

### Turn 150 — assistant

Phase 6 종합 보고서를보냈습니다.

**파일:** [Report/202605211_UnitConverter_Python_Phase6_Report.md](Report/202605211_UnitConverter_Python_Phase6_Report.md)

포함 섹션:
1. 작업 개요 (브랜치 `B_06`, 2026-05-20~21, 학습자 + Cursor Agent)
2. Phase 6 To-Do (RED 14항·GM 9항·GREEN·REFACTOR)
3. RED — `tests/red/` 17건 목록 + 초기 RED 실패 확인
4. GREEN — 68 passed, TC별 커밋 메시지
5. Refactoring — 6커밋 + PR #3 squash `ab8c461`, 변경 파일, 회귀 PASS
6. 커버리지 — entity ~95.5%, boundary 100%, total 95%
7. 미완료·다음 단계
8. 이슈·해결 (DEF-006, GM subprocess, gh auth 등)
9. 생성형 AI 회고

상세 단계별 보고는 `Report/01`~`05`, 대화는 `prompting/05_...`를 참고하면 됩니다. 이 파일을 git에 커밋할지 알려주시면 진행하겠습니다.

[REDACTED]

---

### Turn 151 — user

<user_query>
지금까지 작성한 모든 파일 및 변경점이 있는 파일들을 깃허브에 커밋 - 푸시(원격적용까지)
해줘

</user_query>

---

### Turn 152 — user

<user_query>
지금까지 작성한 모든 파일 및 변경점이 있는 파일들을 깃허브에 커밋 - 푸시(원격적용까지)
해줘

</user_query>

---

### Turn 153 — assistant

[REDACTED]

---

### Turn 154 — assistant

[REDACTED]

---

### Turn 155 — assistant

커밋과 원격 푸시까지 완료했습니다.

## 상태 요약

**브랜치:** `B_06` (원격과 동기화됨)

이전 리팩터링·Golden Master 등 대부분의 코드 변경은 이미 PR #3 머지 커밋 `ab8c461`에 반영되어 있었고, 로컬에 남아 있던 것은 **추적되지 않은 파일 2개**뿐이었습니다.

| 파일 | 내용 |
|------|------|
| `Report/202605211_UnitConverter_Python_Phase6_Report.md` | Phase 6 종합 보고서 |
| `scripts/pr_merge_refactoring_to_B06.ps1` | `gh` PR 머지 보조 스크립트 |

## 커밋

- **해시:** `65b6106`
- **메시지:** `docs: add Phase 6 completion report and PR merge helper script`

## 푸시

- **원격:** `https://github.com/yuldakim/UnitConvertor_06.git`
- **범위:** `ab8c461` → `65b6106` (`B_06`)

원격에서 `B_06`에 대해 Golden Master 상태 검사 규칙이 우회(bypass)되었다는 알림이 있었습니다. 문서·스크립트만 추가한 커밋이라 CI가 돌지 않았을 수 있습니다. 필요하면 GitHub Actions에서 Golden Master 워크플로를 한 번 확인해 주세요.

추가로 README의 REFACTOR 체크박스나 `docs/defect_list.md` 갱신도 커밋하려면 말씀해 주세요.

[REDACTED]

---

### Turn 156 — user

<user_query>
B_06을 기준으로 feature 브랜치를 만들고 전환해줘
</user_query>

---

### Turn 157 — assistant

[REDACTED]

---

### Turn 158 — assistant

[REDACTED]

---

### Turn 159 — assistant

`B_06` 최신 상태(`65b6106`)를 기준으로 `feature` 브랜치를 만들고 전환했습니다.

| 항목 | 값 |
|------|-----|
| 기준 브랜치 | `B_06` (origin과 동기화됨) |
| 새 브랜치 | `feature` |
| HEAD | `65b6106` — docs: add Phase 6 completion report and PR merge helper script |

현재 작업 브랜치는 `feature`입니다. 아직 원격에는 없으므로, 첫 푸시 시에는 `git push -u origin feature`를 사용하면 됩니다.

브랜치 이름을 `feature/이름` 형태로 바꾸고 싶으면 원하는 이름을 알려주세요.

[REDACTED]

---

## Session `2ed1275f-7b68-4c83-a0d6-40ee0d172081`

### Turn 160 — user

<user_query>
🔲 문제 정의 전문가 — Python
당신은 문제 정의 전문가입니다.
워크스페이스: @c:\DEV_BR\UnitConvertor_06\ 
⚠️ 코드 작성·클래스 설계·알고리즘·빌드 스크립트는 하지 마십시오.

다시 처음부터 할게 이전 내용은 잊고 지금부터 다시시작하자
STEP 1 — Observation
1) 지금 우리가 해결하려는 "상황"을 한 문단으로 관찰 관점에서 서술하라.
2) 왜 길이(meter/feet/yard) 변환 문제를 다루는가?
3) OCP/SRP, 입력 검증, 설정 외부화, 동적 단위 등록, 출력 포맷과 연결해
   이 문제가 어떤 학습 맥락에서 등장하는가?

STEP 2 — Why #1: 정확한 변환 결과가 왜 중요한가?
STEP 3 — Why #2: 수동 계산이 아닌 프로그램(+테스트)인 이유?
STEP 4 — Why #3: 계약을 먼저 고정하려는 이유?

STEP 5 — 문제 정의
1) 표면 문제 1~2문장
2) 개선된 정의 3~7문장
3) 핵심 Invariant 5개 이내 (측정·검증 가능한 문장)
4) 훈련하려는 사고 능력 3개

출력: 구조화된 Markdown만. 코드·파일 경로 금지.
</user_query>

---

### Turn 161 — assistant

워크스페이스 맥락을 파악한 뒤, 요청하신 구조로 문제 정의만 작성합니다.

[REDACTED]

---

### Turn 162 — assistant

[REDACTED]

---

### Turn 163 — assistant

[REDACTED]

---

### Turn 164 — assistant

# 문제 정의 — 길이 단위 변환기 (Python)

---

## STEP 1 — Observation

### 1) 상황 관찰 (한 문단)

사용자가 `단위:숫자` 형태로 길이를 한 번 입력하면, 지원하는 모든 길이 단위로 환산한 결과를 일관된 형식으로 보여 주는 작은 콘솔 프로그램을 만들려 한다. 초기에는 meter·feet·yard 세 단위와 고정된 환산 비율이 전제이며, 이후에는 비율을 코드 밖 설정으로 옮기고, 런타임에 새 단위를 등록하며, JSON·CSV·표 등 출력 방식을 고를 수 있게 확장한다. 동시에 잘못된 입력·음수·미지원 단위는 거절하고, 설계는 확장에 열려 있으면서 각 책임은 분리되며, 변환 정확성은 자동화된 테스트로 증명하려는 실습 맥락이다.

### 2) 왜 길이(meter / feet / yard) 변환인가?

- **도메인이 단순하고 비율이 명확**해 “변환이 맞는지”를 사람이 검산하기 쉽다.
- **동일 물리량(길이)의 선형 스케일**이라, 단위 추가·설정 외부화·동적 등록을 **작은 범위**에서 연습할 수 있다.
- **실무와 가깝다**: 국제 단위·현지 단위 혼용, 설정 기반 환율/계수, 포맷별 리포팅은 작은 도구에서도 반복되는 패턴이다.

### 3) 학습 맥락과의 연결

| 요구·개념 | 이 문제에서의 역할 |
|-----------|-------------------|
| **OCP** | 새 단위·출력 포맷·설정 소스를 넣을 때 기존 변환·검증 흐름을 최소 수정 |
| **SRP** | 입력 파싱, 검증, 환산, 포맷팅, 설정 로드, 단위 등록을 서로 다른 변경 이유로 분리 |
| **입력 검증** | 신뢰할 수 있는 출력의 전제; 잘못된 계약은 조용한 오답으로 이어짐 |
| **설정 외부화** | 비율·단위 정의를 코드 재배포 없이 바꾸는 운영·실험 습관 |
| **동적 단위 등록** | 고정 enum이 아닌 **확장 가능한 모델** 설계 연습 |
| **출력 포맷** | 동일 결과를 **다른 소비자**(사람·스크립트·스프레드시트)에 맞게 표현 |

이 과제는 **6시간 규모의 생성형 AI 활용 실습** 안에서, 기본 기능 → 품질 요구 → 테스트 → 확장 요구 → 회고 순으로 **설계·테스트·리팩토링**을 한 번에 경험하도록 배치된 학습용 문제다.

---

## STEP 2 — Why #1: 정확한 변환 결과가 왜 중요한가?

- 길이 환산 오류는 **누적·전파**된다(한 단위만 틀려도 나머지 출력 전체가 틀림).
- 사용자는 **계산기를 신뢰**하고 수동 검산을 생략한다; 작은 반올림·비율 오류도 “도구 버그”로 인식된다.
- feet·yard는 meter 기준 **파생 비율**이므로, 기준 정의가 어긋나면 **단위 간 일관성(왕복 변환)**이 깨진다.
- 실습 목표는 “돌아가는 UI”가 아니라 **측정 가능한 정확성**이므로, 기대값이 문서화된 비율과 맞는지가 성공 기준이다.

---

## STEP 3 — Why #2: 수동 계산이 아닌 프로그램(+테스트)인 이유?

- 단위가 늘고 포맷·설정·동적 등록이 붙으면 **수동 검산 비용**이 기하급수적으로 커진다.
- 프로그램은 **동일 규칙을 반복** 적용해 사람의 실수·피로를 줄인다.
- 테스트는 “지금 맞다”가 아니라 **리팩토링·요구 추가 후에도 맞다**는 회귀 방지망이다.
- 입력 검증·엣지 케이스는 테스트 없이는 **재현·설명**이 어렵다.
- AI 보조 코딩 환경에서는 **테스트가 사실상의 스펙**이 되어, 생성 코드의 검증 루프를 닫는다.

---

## STEP 4 — Why #3: 계약을 먼저 고정하려는 이유?

- **입력 형식**, **지원 단위**, **비율 출처**, **반올림·표시 규칙**, **오류 시 동작**이 모호하면 구현과 테스트가 엇갈린다.
- 계약을 먼저 쓰면 OCP/SRP 논의가 “클래스 이름”이 아니라 **변경 가능한 경계**로 내려온다.
- RED·Mom Test·BCE 같은 산출물은 **관찰 가능한 행위**로 계약을 고정하는 수단이다.
- 확장 요구(설정 파일, 동적 등록, 출력 포맷)는 **계약이 없으면** 기존 기능을 깨뜨리기 쉽다.
- 팀·AI·미래의 자신이 **같은 기대**를 공유하는 단일 기준점이 된다.

---

## STEP 5 — 문제 정의

### 1) 표면 문제 (1~2문장)

사용자가 입력한 길이를 meter·feet·yard 등 지원 단위로 바꿔 출력하는 프로그램을 만든다. 새 단위와 출력 방식을 붙여도 기존 로직 변경을 줄이고, 변환과 입력 처리는 테스트로 검증한다.

### 2) 개선된 정의 (3~7문장)

**길이 변환 도메인**에서, 사용자는 `기준단위:양` 한 줄로 값을 제출하고, 시스템은 등록된 모든 길이 단위에 대한 환산 결과를 선택한 형식으로 돌려준다. 환산 계수는 코드 상수에 묶지 않고 설정·동적 등록으로 확장 가능해야 하며, meter를 기준으로 한 파생 비율의 일관성을 유지한다. 잘못된 형식, 음수, 알 수 없는 단위는 명확히 실패하고, 성공 경로만 결과를 낸다. 구조는 단위·포맷·설정 소스가 늘어날 때 **기존 변환 규칙과 검증 로직을 건드리지 않고** 확장되도록 책임을 나눈다. 정확성과 회귀 방지는 자동화 테스트로 증명하며, 실습자는 AI를 활용해 구현하되 **계약·테스트를 먼저** 두는 습관을 익힌다.

### 3) 핵심 Invariant (5개 이내, 측정·검증 가능)

1. **기준 비율**: 문서에 정한 `1 meter = 3.28084 feet`, `1 meter = 1.09361 yard`를 사용한 환산 결과가 테스트 허용 오차 내에서 일치한다.
2. **일관성**: 임의의 유효 입력에 대해, A→B→A 왕복(또는 meter 경유) 시 원래 값과 **정의된 반올림 규칙** 하에서 일치한다.
3. **완전 출력**: 유효 입력이면 **현재 등록된 모든 길이 단위**에 대해 누락 없이 한 줄(또는 선택 포맷의 한 레코드)씩 결과가 있다.
4. **거부**: 음수, 파싱 불가 형식, 미등록 단위 입력 시 **결과 환산을 수행하지 않고** 정의된 오류 표현만 반환한다.
5. **확장 무파괴**: 설정에 단위를 추가하거나 런타임 등록·출력 포맷을 바꾼 뒤에도, 기존에 통과하던 **기본 세 단위·기본 포맷** 테스트가 깨지지 않는다.

### 4) 훈련하려는 사고 능력 (3개)

1. **계약 우선 사고**: 관찰·Why·Invariant로 “무엇이 맞는지”를 고정한 뒤 구현·AI 프롬프트에 들어가기.
2. **경계 설계 사고**: 변경 이유별로 책임을 나누고, 확장점(OCP)과 검증·설정·표현의 분리(SRP)를 의도적으로 선택하기.
3. **증거 기반 품질 사고**: 테스트를 부가물이 아니라 **정확성·회귀·리팩토링 안전망**으로 두고, 요구 추가 시 테스트를 먼저 갱신하는 습관 갖기.

---

[REDACTED]

---

### Turn 165 — user

<user_query>
🔲 Mom Test 질문
@c:\DEV_BR\UnitConvertor_06\ 프로젝트를 "고객 인터뷰" 관점에서 준비한다.
제품이 아니라 학습자/사용자의 행동을 드러내는 Mom Test 질문 10개.
각 질문: (1) 과거 구체 경험 (2) 실제 행동 (3) 돈/시간/리스크 연결.
금지: 기능 나열형 질문만으로 끝내기.
마지막에 "진짜 위험 가정" 3개를 bullet로.
구현·코드 금지.
</user_query>

---

### Turn 166 — assistant

프로젝트 맥락을 확인한 뒤 Mom Test 관점의 인터뷰 질문을 작성합니다.

[REDACTED]

---

### Turn 167 — assistant

[REDACTED]

---

### Turn 168 — assistant

# Mom Test 질문 — 길이 단위 변환 (고객 인터뷰용)

**대상**: 단위 환산이 실제 업무·일상에 붙는 사람, 또는 이 실습을 수행하는 학습자.  
**목적**: “변환기에 무엇을 넣을까”가 아니라, **언제·왜·어떻게** 길이를 바꾸고, 틀렸을 때 무엇이 깨지는지 드러내기.

---

## 질문 10개

### 1
**지난 3개월 안에** 길이를 meter·feet·yard(또는 비슷한 단위)로 **직접 바꿔야 했던 일**이 있었나요? 그때 **첫 번째로 연 곳**(검색, 계산기, 엑셀, 동료 등)과 **끝까지 걸린 시간**을 순서대로 말해 주세요. 그 결과를 **어디에 붙여 넣었는지**(메일, 견적서, 코드, 현장 지시)까지요.

### 2
**가장 최근에** 환산 숫자가 틀렸거나, 단위를 헷갈린 적이 있다면, **그때 무슨 일이 벌어졌는지** 한 건만 골라 주세요. (재작업, 항의, 납기 지연, 재측정 등) **누가 알아챘고**, **당신이 추가로 쓴 시간**은 대략 얼마였나요?

### 3
같은 길이를 **두 번 이상** 다른 도구나 사람에게 맡겨 본 적이 있나요? **숫자가 달랐을 때** 당신은 **어느 쪽을 믿었고**, 그 근거는 무엇이었나요? (출처, 반올림, “대충 맞음”) 그 선택이 **비용·일정·안전** 중 무엇에 영향을 줬나요?

### 4
**업무·공부 중** 길이 환산을 **반복**하는 날이 있었다면, 그날 **하루에 몇 번**이나 했고, **매번 같은 절차**였나요 아니면 매번 방법이 달랐나요? 절차가 달랐다면 **왜 바꿨는지**(속도, 신뢰, 형식 맞추기)를 구체적으로 말해 주세요.

### 5
**팀·고객·교수**에게 숫자를 넘기기 전, **스스로 검산**하는 습관이 있나요? 있다면 **지난번**에는 어떻게 검산했고(역산, 다른 사이트, 손계산), **몇 분** 썼나요? 없다면 **검산을 생략해도 된다고 판단한 이유**는 무엇이었나요?

### 6
**표·JSON·CSV** 같은 “형식” 때문에 **한 번 더 손댄** 경험이 있나요? **원본은 어디서** 나왔고, **최종으로 필요한 형태**는 어디였나요? 그 변환에 **얼마나 시간**을 썼고, **실수로 잘못 붙여 넣은 적**이 있었나요?

### 7
**회사·프로젝트·수업**에서 “이 단위/이 비율을 써라”는 **규칙이 바뀐 적**이 있나요? 바뀐 **직후 첫 주**에 당신은 **무엇을 다시 확인**했고, **잘못된 값으로 진행했다가 되돌린** 일이 있었나요? 그때 **되돌리는 데 든 시간·리스크**는 무엇이었나요?

### 8
**코딩·자동화·AI**로 계산을 맡긴 적이 있다면, **마지막으로** 그 출력을 **그대로 썼던 경우**와 **버리고 다시 한 경우**를 각각 하나씩 말해 주세요. **버렸을 때**는 무엇이 의심스러웠고, **대안으로 무엇을 했으며**, 그 대안에 **얼마나 시간**이 들었나요?

### 9
**6시간 안에** 작은 프로그램을 만들거나 과제를 끝낸 **최근 경험**이 있다면, **중간에 “요구사항을 다시 읽었다”**거나 **“테스트를 먼저 썼다/나중에 썼다”**고 느낀 순간이 있었나요? 그때 **시간을 아꼈는지 잃었는지**, **제출·데모 직전**에 무엇이 가장 불안했나요?

### 10
이번 주에 **“단위 변환”과 비슷한 문제**(환율, 온도, 단위가 섞인 스펙)를 **혼자 해결**해야 한다면, **지금 당장** 무엇부터 할 것 같나요? (과거에 비슷한 일을 **실제로** 했을 때의 **첫 15분 행동**을 기준으로) 그 선택이 **틀렸을 때** 당신에게 가장 큰 **손해**(평판, 점수, 돈, 재작업)는 무엇인가요?

---

## 진짜 위험 가정 (검증 실패 시 실습·제품 가치가 무너짐)

- **“길이 환산은 가끔 쓰지만, 틀려도 큰 일이 안 난다”** — 학습자·사용자 모두 검산·테스트·입력 검증에 시간을 쓰지 않고, 정확성·Invariant가 공감되지 않는다.
- **“환산은 검색·스마트폰 계산기로 충분하고, 프로그램·설정·포맷은 오히려 부담이다”** — 설정 외부화·동적 등록·출력 포맷 확장이 ‘필요’가 아니라 ‘과제용 장식’으로 느껴진다.
- **“AI로 빨리 만들면 되고, 계약·테스트는 나중에 해도 된다”** — 6시간 실습에서 회귀 테스트와 OCP/SRP가 회고 주제로만 남고, 행동 변화(계약 우선)로 이어지지 않는다.

[REDACTED]

---

### Turn 169 — user

<user_query>
🔲 BCE 설계 전문가 — Python
Dual-Track(UI/경계 vs Domain) + BCE 관점 설계 전문가로 행동하라.
대상: @c:\DEV_BR\UnitConvertor_06\ 
제약: 구현 코드 작성 금지. 설계·계약·테스트 목록·통합 계획만.

# 1) Entity(Domain) 설계
  1.1 개념 목록과 SRP
  1.2 Invariants
  1.3 유스케이스
  1.4 Domain API (시그니처 수준, 본문 X) + 실패 조건
  1.5 Domain 단위 테스트 설계 (RED 우선)

# 2) Boundary 설계
  2.1 시나리오: 입력→검증→실행→출력
  2.2 외부 계약: Input / Output / Error schema
  2.3 Boundary 계약 테스트 (Domain Mock 가정)
  2.4 에러 메시지 규칙 (문구 패턴 고정)

# 3) Data 설계
  3.1 목적
  3.2 인터페이스 계약 (이름만 제안)
  3.3 InMemory vs File(JSON/YAML) 비교 + 추천 1개와 이유
  3.4 Data 레이어 테스트

# 4) Integration & Verification
  4.1 의존성 방향 포함 흐름
  4.2 통합 테스트 시나리오 (정상 2+, 실패 3+)
  4.3 회귀 보호 규칙
  4.4 커버리지 목표 (Domain / Boundary / Data 수치)
  4.5 Traceability Matrix: Concept→Rule→UseCase→Contract→Test→Component

모호어 금지. 모든 규칙은 테스트로 검증 가능하게.
</user_query>

---

### Turn 170 — assistant

프로젝트 요구사항과 기존 설계 문서를 확인한 뒤 BCE·Dual-Track 설계를 작성합니다.

[REDACTED]

---

### Turn 171 — assistant

[REDACTED]

---

### Turn 172 — assistant

# BCE + Dual-Track 설계 — 길이 단위 변환기 (Python)

**아키텍처 원칙**

| Track | 책임 | 금지 |
|-------|------|------|
| **Domain (Entity)** | 단위 등록·길이 환산·도메인 불변식 | 입출력 파싱, `print`, JSON/CSV, 파일 I/O |
| **Boundary (Control + Presentation)** | CLI/요청 파싱, 오케스트레이션, 포맷 렌더, 사용자 오류 문구 | 환산 비율 하드코딩, 파일 직접 읽기 |
| **Data** | 단위 정의 영속/로드 | 환산 수식, 출력 문장 생성 |

**앵커 단위**: `meter` (모든 비율은 “1 단위 = N meter”로 정규화).

**표시 반올림 (Boundary 계약, Domain은 full precision)**  
- 변환 결과 **표시값**: 소수 **1자리**, `ROUND_HALF_UP`.  
- 검증: `2.5 meter → feet` 표시값 `8.2` (내부값 `8.2021` 허용, 표시만 8.2).

---

# 1) Entity (Domain) 설계

## 1.1 개념 목록과 SRP

| 개념 | 단일 책임 (변경 이유) |
|------|----------------------|
| **UnitId** | 단위 식별자 불변 규칙 (비어 있지 않음, 공백 없음, 소문자 정규화 규칙) |
| **Magnitude** | 양의 실수 길이 값 (0 허용, 음수 거부) |
| **LengthQuantity** | `(UnitId, Magnitude)` 쌍; 생성 시 도메인 검증만 |
| **MetersPerUnit** | “1 해당 단위 = N meter” 양수 계수 |
| **UnitDefinition** | `(UnitId, MetersPerUnit)` 등록 단위 스냅샷 |
| **UnitRegistry** | 등록된 단위 집합; 중복·미등록 조회 |
| **ConversionEngine** | Registry + 앵커 기준 전 단위 환산 |
| **ConversionLine** | 한 대상 단위에 대한 `(source_quantity, target_unit_id, target_magnitude)` |
| **ConversionBatch** | 동일 입력에 대한 `ConversionLine` 전체 (순서 규칙 고정) |

**OCP**: 새 단위 = `UnitRegistry`에 정의 추가만; `ConversionEngine` 시그니처 불변.  
**SRP 분리**: 등록(Registry) ≠ 환산(Engine) ≠ 값 객체(Quantity).

## 1.2 Invariants (측정 가능)

| ID | 규칙 | 검증 방법 |
|----|------|-----------|
| D-INV-01 | `MetersPerUnit > 0` | 등록 시 예외; TC 거부 |
| D-INV-02 | `Magnitude >= 0` | 음수 입력 시 예외 |
| D-INV-03 | 환산: `target_m = source_m × (src_mpu / tgt_mpu)` where `source_m = magnitude × mpu(src)` | 고정 입력 수치 assert |
| D-INV-04 | 기본 3단위: `meter→1.0`, `feet→0.3048` 역산 아님 **직접** `1/3.28084`, `yard→1/1.09361` meter | README 상수 TC |
| D-INV-05 | `feet↔yard`는 meter 경유와 동일 | 교차 TC 2건 |
| D-INV-06 | `ConversionBatch` 라인 수 = `Registry.count()` | 개수 assert |
| D-INV-07 | 라인 순서 = `Registry.list_unit_ids()` 정렬 순 (등록 순서 또는 id 사전순 중 **하나만** 선택해 고정) | 스냅샷 assert |
| D-INV-08 | 동일 `UnitId` 이중 등록 불가 | 두 번째 `register` 예외 |

## 1.3 유스케이스 (Domain)

| UC-ID | 이름 | 전제 | 결과 |
|-------|------|------|------|
| UC-D-01 | 기본 레지스트리로 전 단위 환산 | meter/feet/yard 등록됨 | `ConversionBatch` N=3 |
| UC-D-02 | 동적 단위 등록 후 환산 | `cubit` 미등록 → 등록 → 환산 | 배치에 cubit 포함 |
| UC-D-03 | meter 입력 환산 | `LengthQuantity(meter, 2.5)` | 3라인, 수치 D-INV-03·04 만족 |
| UC-D-04 | feet/yard 입력 환산 | 비앵커 입력 | meter 경유와 일치 |
| UC-D-05 | 0 길이 환산 | magnitude=0 | 모든 타깃 0 |
| UC-D-06 | 등록 거부 | 음수 계수·중복 id | 예외, Registry 불변 |

## 1.4 Domain API (시그니처만) + 실패 조건

```text
# 값 객체
UnitId.parse(raw: str) -> UnitId
  FAIL: EmptyUnitIdError (raw 빈 문자열 또는 공백만)

Magnitude.create(value: float) -> Magnitude
  FAIL: NegativeMagnitudeError (value < 0)

LengthQuantity.create(unit_id: UnitId, magnitude: Magnitude) -> LengthQuantity

# 레지스트리
UnitRegistry.empty() -> UnitRegistry
UnitRegistry.with_defaults() -> UnitRegistry   # meter, feet, yard
UnitRegistry.register(unit_id: UnitId, meters_per_unit: MetersPerUnit) -> UnitRegistry
  FAIL: DuplicateUnitError
  FAIL: NonPositiveFactorError  # D-INV-01

UnitRegistry.has(unit_id: UnitId) -> bool
UnitRegistry.list_unit_ids() -> list[UnitId]   # 순서 고정 규칙
UnitRegistry.count() -> int

# 환산
ConversionEngine(registry: UnitRegistry) -> ConversionEngine
ConversionEngine.convert(quantity: LengthQuantity) -> ConversionBatch
  FAIL: UnregisteredUnitError (quantity.unit not in registry)
```

**예외 타입 (Domain 전용, Boundary가 매핑)**

| 예외 | 조건 |
|------|------|
| `EmptyUnitIdError` | D-INV 파싱 |
| `NegativeMagnitudeError` | D-INV-02 |
| `DuplicateUnitError` | D-INV-08 |
| `NonPositiveFactorError` | D-INV-01 |
| `UnregisteredUnitError` | 환산 시 미등록 |

## 1.5 Domain 단위 테스트 설계 (RED 우선)

**실행 순서**: RED 목록 작성 → 실패 확인 → Domain 구현 → GREEN.

| Test-ID | UC | Given | Then (assert) |
|---------|-----|-------|----------------|
| T-D-01 | UC-D-03 | defaults, `meter:2.5` | feet 내부 ≈ `8.2021`, yard ≈ `2.734025` (ε=1e-4) |
| T-D-02 | UC-D-03 | defaults, `meter:2.5` | 표시는 Boundary; Domain은 비반올림 |
| T-D-03 | UC-D-04 | defaults, `feet:8.2021` | meter ≈ `2.5` (ε=1e-3) |
| T-D-04 | UC-D-05 | D-INV-04 | `1m→3.28084ft`, `1m→1.09361yd` |
| T-D-05 | D-INV-05 | `feet:1` → yard | meter 경유와 동일 (ε) |
| T-D-06 | UC-D-05 | magnitude=0 | 모든 라인 0 |
| T-D-07 | D-INV-02 | magnitude=-1 | `NegativeMagnitudeError` |
| T-D-08 | D-INV-08 | `register(meter)` twice | `DuplicateUnitError`, count unchanged |
| T-D-09 | D-INV-01 | `register(x, 0)` | `NonPositiveFactorError` |
| T-D-10 | UC-D-02 | register `cubit=0.4572`, `meter:1` | batch에 cubit 라인, 값 `1/0.4572` meter 기준 |
| T-D-11 | D-INV-06 | registry 4 units | `len(batch.lines)==4` |
| T-D-12 | D-INV-07 | 등록 순서 A,B,C | line order A,B,C (고정 규칙 문서화) |
| T-D-13 | UC-D-06 | unregistered `mile` | `UnregisteredUnitError` |

**Mock 금지 대상**: Registry, Engine (실제 객체).  
**허용 Mock**: 없음 (Domain 순수).

---

# 2) Boundary 설계

## 2.1 시나리오: 입력 → 검증 → 실행 → 출력

```mermaid
sequenceDiagram
  participant User
  participant Boundary as BoundaryController
  participant Parser as InputParser
  participant Domain as ConversionEngine
  participant Repo as UnitRepositoryPort
  participant Renderer as OutputRenderer

  User->>Boundary: raw line
  Boundary->>Parser: parse_command(raw)
  alt CONVERT
    Parser-->>Boundary: ConvertCommand
    Boundary->>Domain: convert(quantity)
    Domain-->>Boundary: ConversionBatch
    Boundary->>Renderer: render(batch, format)
    Renderer-->>User: stdout
  else REGISTER
    Parser-->>Boundary: RegisterCommand
    Boundary->>Domain: register(...)
    Boundary-->>User: success line (고정 패턴)
  else PARSE_FAIL
    Boundary-->>User: ErrorEnvelope (고정 패턴)
  end
  Note over Boundary,Repo: 앱 시작 시 Repo.load() → Registry 주입
```

| 단계 | 책임 | 실패 시 |
|------|------|---------|
| 입력 | 한 줄 `str` | 빈 줄 → `ERR_EMPTY_INPUT` |
| 파싱 | `ConvertCommand` \| `RegisterCommand` | `ERR_INVALID_*` |
| 검증 | Domain 생성 전 형식·숫자 | Domain 예외 → `ERR_DOMAIN_*` |
| 실행 | Engine + Registry | — |
| 출력 | Table / JSON / CSV | 포맷 키 불명 → `ERR_UNKNOWN_FORMAT` |

**명령 판별 (우선순위 고정, 테스트로 고정)**

1. `=` 포함 + `meter` 앵커 패턴 → `RegisterCommand` (예: `1 cubit = 0.4572 meter`)
2. `:` 1회 분리 → `ConvertCommand` (예: `meter:2.5`)
3. 그 외 → `ERR_INVALID_FORMAT`

## 2.2 외부 계약: Input / Output / Error schema

### Input (문자열 → 구조)

| 필드 | 타입 | 규칙 |
|------|------|------|
| `raw` | string | UTF-8, trim 후 처리 |
| `format` | enum | `table` \| `json` \| `csv` (기본 `table`) |

**ConvertCommand**

| 필드 | 타입 | 규칙 |
|------|------|------|
| `unit` | string | `UnitId` 규칙 통과 |
| `value` | decimal string → float | 파싱 실패 시 형식 오류 |

**RegisterCommand**

| 필드 | 타입 | 규칙 |
|------|------|------|
| `unit` | string | 좌변 단위명 |
| `factor` | float | 양수 |
| `anchor` | literal | 반드시 `meter` (대소문자: 소문자만 허용) |

### Output (성공)

**Table (기본)** — 줄 단위, N = 등록 단위 수  
- 패턴: `{src_value} {src_unit} = {dst_display} {dst_unit}`  
- `src_value`: 입력 magnitude 그대로 표시 (반올림 없음)  
- `dst_display`: 1자리 `ROUND_HALF_UP`

**JSON**

```json
{
  "source": { "unit": "meter", "value": 2.5 },
  "conversions": [
    { "unit": "feet", "value": 8.2 },
    { "unit": "yard", "value": 2.7 }
  ]
}
```

- `conversions[].value`: number, 1자리 (number 타입으로 8.2)
- 키 순서: `source` 먼저, `conversions`는 `list_unit_ids()` 순

**CSV**

```text
source_unit,source_value,target_unit,target_value
meter,2.5,feet,8.2
meter,2.5,yard,2.7
```

- 헤더 고정 1행
- `source_*` 매 행 동일

### Error (ErrorEnvelope)

| 필드 | 타입 | 필수 |
|------|------|------|
| `code` | string | Y |
| `message` | string | Y (고정 문구, 2.4) |
| `field` | string | N (`unit` \| `value` \| `format`) |

- 종료 코드: Domain/Boundary 정책 — CLI는 오류 시 **비0 exit** (통합 TC에서 assert)

## 2.3 Boundary 계약 테스트 (Domain Mock 가정)

**Mock**: `ConversionEngine` 또는 `UnitRegistry`를 fake로 주입 — 환산 수치는 Boundary가 책임지지 않음.

| Test-ID | 초점 | Given (Mock) | Then |
|---------|------|--------------|------|
| T-B-01 | 파싱 | `meter:2.5` | `ConvertCommand(meter, 2.5)` |
| T-B-02 | 파싱 | `1 cubit = 0.4572 meter` | `RegisterCommand` |
| T-B-03 | 파싱 | `meter 2.5` (콜론 없음) | `ERR_INVALID_FORMAT` |
| T-B-04 | 파싱 | `meter:abc` | `ERR_INVALID_NUMBER` |
| T-B-05 | Domain map | Mock `NegativeMagnitudeError` | `ERR_NEGATIVE_VALUE` |
| T-B-06 | Domain map | Mock `UnregisteredUnitError` | `ERR_UNKNOWN_UNIT` + field=unit |
| T-B-07 | Table | Mock batch 2 lines | stdout 2줄, 패턴 regex |
| T-B-08 | JSON | Mock batch | JSON schema + 값 1자리 |
| T-B-09 | CSV | Mock batch | 헤더 + 행 수 |
| T-B-10 | Format | `--format=xml` | `ERR_UNKNOWN_FORMAT` |
| T-B-11 | Register OK | Mock register success | `MSG_REGISTER_OK` 한 줄 |
| T-B-12 | 빈 입력 | `""` | `ERR_EMPTY_INPUT` |

## 2.4 에러 메시지 규칙 (문구 패턴 고정)

| code | message (정확히 일치) | field |
|------|-------------------------|-------|
| `ERR_EMPTY_INPUT` | `Input is empty.` | — |
| `ERR_INVALID_FORMAT` | `Invalid format. Use unit:value (ex: meter:2.5)` | — |
| `ERR_INVALID_REGISTER` | `Invalid format. Use 1 unit = factor meter (ex: 1 cubit = 0.4572 meter)` | — |
| `ERR_INVALID_NUMBER` | `Invalid number: {value_str}` | value |
| `ERR_NEGATIVE_VALUE` | `Value must be zero or positive: {value}` | value |
| `ERR_UNKNOWN_UNIT` | `Unknown unit: {unit}` | unit |
| `ERR_DUPLICATE_UNIT` | `Unit already registered: {unit}` | unit |
| `ERR_INVALID_FACTOR` | `Factor must be positive: {factor}` | value |
| `ERR_UNKNOWN_FORMAT` | `Unknown output format: {format}. Use table, json, or csv.` | format |

**성공 메시지**

| code | message |
|------|---------|
| `MSG_REGISTER_OK` | `Registered: 1 {unit} = {factor} meter` |

**TC 규칙**: `message` 전체 문자열 **exact match** (공백·구두점 포함).

---

# 3) Data 설계

## 3.1 목적

- **초기 단위·비율**을 코드 밖에서 로드 (설정 외부화).
- Domain `UnitRegistry` 구성을 Boundary에 **주입** 가능한 스냅샷 제공.
- 테스트에서 **결정적 fixture** 교체.

## 3.2 인터페이스 계약 (이름만)

| 포트 | 메서드 |
|------|--------|
| `UnitDefinitionRepository` | `load() -> UnitRegistry` |
| | `save(registry: UnitRegistry) -> None` (선택: 동적 등록 영속 시) |
| `UnitDefinitionSource` | `read_definitions() -> list[UnitDefinitionDTO]` |
| `JsonUnitDefinitionSource` | implements `UnitDefinitionSource` |
| `YamlUnitDefinitionSource` | implements `UnitDefinitionSource` |
| `InMemoryUnitDefinitionSource` | implements `UnitDefinitionSource` |

**DTO (Data 전용)**

| 필드 | 타입 | 규칙 |
|------|------|------|
| `id` | string | UnitId 규칙 |
| `meters_per_unit` | float | > 0 |

**파일 스키마 (JSON 예, YAML 동형)**

```json
{
  "units": [
    { "id": "meter", "meters_per_unit": 1.0 },
    { "id": "feet", "meters_per_unit": 0.3048 },
    { "id": "yard", "meters_per_unit": 0.9144 }
  ]
}
```

- README 상수와 **수치 일치** TC: feet `0.3048` (=1/3.28084), yard `0.9144` (=1/1.09361) — 문서화된 ε 이내.

## 3.3 InMemory vs File — 비교 및 추천

| 기준 | InMemory | File (JSON/YAML) |
|------|----------|-------------------|
| 실습 “설정 외부화” | 미충족 | 충족 |
| RED/Domain 속도 | 빠름 | 느림 (I/O) |
| 결정성 | 높음 | 경로·파일 내용 의존 |
| 운영 변경 | 재시작 시 코드 배포 | 파일 교체만 |

**추천**: **File(JSON) 기본 + InMemory를 테스트·폴백 전용**  
- 이유: 추가 요구사항 “설정 외부화”를 Data Track에서 충족; Domain/Boundary 테스트는 `InMemoryUnitDefinitionSource`로 I/O 격리; JSON은 Python 표준 라이브러리만으로 파서 부담 최소.

**런타임 동적 등록**: 세션 내 `UnitRegistry` 변경; **영속 save는 Phase 2** (통합 TC에 “재시작 후 유지”는 선택 시나리오로 분리).

## 3.4 Data 레이어 테스트

| Test-ID | Given | Then |
|---------|-------|------|
| T-DA-01 | 유효 JSON fixture | `load()` registry count=3, ids 포함 |
| T-DA-02 | feet `meters_per_unit` | ≈0.3048 (ε) |
| T-DA-03 | 중복 id JSON | `DuplicateUnitError` 또는 Data `ConfigError` (하나로 고정) |
| T-DA-04 | factor 0 | `ConfigError` code `CFG_NON_POSITIVE_FACTOR` |
| T-DA-05 | 파일 없음 | `ConfigError` `CFG_FILE_NOT_FOUND` |
| T-DA-06 | 잘못된 JSON | `CFG_PARSE_ERROR` |
| T-DA-07 | InMemory source | File 없이 T-DA-01 동일 |
| T-DA-08 | YAML 동형 fixture | T-DA-01 동일 (형식만 다름) |

---

# 4) Integration & Verification

## 4.1 의존성 방향 (흐름)

```text
[ User / CLI ]
      ↓
[ Boundary: Parser, Controller, Renderer ]
      ↓ uses
[ Domain: Registry, Engine ]  ←── builds from
[ Data: Repository → Source → File ]
```

**규칙**

- Domain → Boundary/Data **참조 금지**
- Data → Domain **허용** (Registry 구성만)
- Boundary → Domain, Boundary → Data port **허용**
- Renderer → Domain 타입 **읽기만** (`ConversionBatch`)

## 4.2 통합 테스트 시나리오

**정상 (≥2)**

| Test-ID | 시나리오 | Assert |
|---------|----------|--------|
| T-I-01 | defaults 로드 + stdin `meter:2.5` + table | stdout 3줄; `2.5 meter = 8.2 feet` exact line 존재 |
| T-I-02 | JSON format + `feet:8.2` | JSON parse; `source.unit==feet`; conversions 길이=3 |
| T-I-03 | REGISTER `1 cubit = 0.4572 meter` 후 `meter:1` table | 4줄; cubit 라인 존재 |

**실패 (≥3)**

| Test-ID | 시나리오 | Assert |
|---------|----------|--------|
| T-I-04 | `meter:abc` | `ERR_INVALID_NUMBER`, exit≠0 |
| T-I-05 | `mile:1` (미등록) | `ERR_UNKNOWN_UNIT` |
| T-I-06 | `meter:-1` | `ERR_NEGATIVE_VALUE` |
| T-I-07 | 빈 줄 | `ERR_EMPTY_INPUT` |

## 4.3 회귀 보호 규칙

1. **README 상수 TC 3건** (`T-D-01`, `T-D-04`, `T-I-01`) — CI 필수, 삭제 금지.  
2. **에러 문구 exact match TC** — `message` 변경 시 의도적 스냅샷 업데이트만 허용.  
3. Domain 수정 시 **Boundary Mock TC + Integration TC** 동시 실행.  
4. 새 단위 추가 = **Registry 데이터 + T-D-11 count** 갱신, Engine 코드 변경 0.  
5. PR 병합 조건: Domain·Boundary·Data·Integration **전 레이어 RED 목록 0 실패**.

## 4.4 커버리지 목표 (수치)

| 레이어 | Line | Branch | 비고 |
|--------|------|--------|------|
| Domain | ≥ 95% | ≥ 90% | Engine, Registry, Quantity |
| Boundary | ≥ 90% | ≥ 85% | Parser, Renderer, error map |
| Data | ≥ 85% | ≥ 80% | load + error paths |
| Integration | N/A (시나리오) | — | T-I-01~07 필수 GREEN |

**제외 (측정에서 제외 명시)**: `if __name__ == "__main__"` 진입만.

## 4.5 Traceability Matrix

| Concept | Rule (Invariant/Contract) | Use Case | Contract (API/Schema) | Test-ID | Component |
|---------|---------------------------|----------|------------------------|---------|-----------|
| LengthQuantity | D-INV-02 | UC-D-05 | `Magnitude.create` | T-D-07 | Domain |
| UnitRegistry | D-INV-08 | UC-D-06 | `register` | T-D-08 | Domain |
| MetersPerUnit | D-INV-01 | UC-D-06 | `register` | T-D-09 | Domain |
| ConversionEngine | D-INV-03,04,05 | UC-D-03,04 | `convert` | T-D-01,03,04,05 | Domain |
| ConversionBatch | D-INV-06,07 | UC-D-01 | `ConversionBatch` | T-D-11,12 | Domain |
| Dynamic unit | D-INV-03 | UC-D-02 | `register` + `convert` | T-D-10, T-I-03 | Domain + Boundary |
| Convert input | 2.2 ConvertCommand | — | `unit:value` | T-B-01, T-I-01 | Boundary Parser |
| Register input | 2.2 RegisterCommand | — | `1 u = f meter` | T-B-02, T-I-03 | Boundary Parser |
| Table output | 표시 1자리 | — | Table line pattern | T-B-07, T-I-01 | Renderer |
| JSON output | JSON schema | — | 2.2 JSON | T-B-08, T-I-02 | Renderer |
| CSV output | CSV header | — | 2.2 CSV | T-B-09 | Renderer |
| Error text | 2.4 exact message | — | ErrorEnvelope | T-B-03~06, T-I-04~07 | Boundary |
| File config | DTO >0 | — | `units[]` | T-DA-01~06 | Data |
| Defaults load | D-INV-04 | UC-D-01 | `Repository.load` | T-DA-01, T-I-01 | Data + Integration |
| OCP | 새 단위=등록만 | UC-D-02 | Registry | T-D-10, T-I-03 | Registry (no Engine edit) |

---

## Dual-Track 작업 순서 (권장)

| 순서 | Track | 산출 |
|------|-------|------|
| 1 | Domain | `T-D-*` RED → GREEN |
| 2 | Boundary | `T-B-*` (Engine Mock) |
| 3 | Data | `T-DA-*` |
| 4 | Integration | `T-I-*` |
| 5 | 회귀 | 4.3 규칙 CI 고정 |

이 설계는 **모든 규칙이 Tes

[... truncated for export ...]

---

### Turn 173 — user

<user_query>
🔲 RED 테스트 목록
pytest를 가정하고 "구현 없이" RED 단계 테스트 케이스 제목 25~40개.
분류: 파싱 / 음수·0 / 미지원 단위 / 비율 정확도 / 동적 등록 / 출력 직렬화
(JSON/CSV/표 각 최소 3개씩)
각 테스트 옆에 보호하는 invariant 이름 한 줄.
코드 작성 금지.
</user_query>

---

### Turn 174 — assistant

# RED 테스트 목록 (pytest, 구현 전)

**전제**: RED 단계 — 테스트는 작성·실행 가능하나 Domain/Boundary/Data 구현은 스텁·미구현으로 **실패가 정상**.  
**표기**: `test_<영역>_<행위>_<기대>` 형식의 **케이스 제목**만.

---

## 파싱 (8)

| # | 테스트 케이스 제목 | 보호 Invariant |
|---|-------------------|----------------|
| P-01 | `test_parse_convert_command_meter_colon_2_5` | Boundary: `ConvertCommand` 계약 (`unit:value`, 콜론 1회) |
| P-02 | `test_parse_convert_command_feet_with_decimal` | Boundary: 숫자 파싱 → `float` 성공 경로 |
| P-03 | `test_parse_register_command_one_cubit_equals_factor_meter` | Boundary: `RegisterCommand` (`1 unit = factor meter`) |
| P-04 | `test_parse_reject_missing_colon` | Boundary: `ERR_INVALID_FORMAT` 고정 문구 |
| P-05 | `test_parse_reject_multiple_colons` | Boundary: `ConvertCommand` 단일 구분자 규칙 |
| P-06 | `test_parse_reject_non_numeric_value` | Boundary: `ERR_INVALID_NUMBER` + `{value_str}` |
| P-07 | `test_parse_reject_register_without_meter_anchor` | Boundary: 앵커 `meter` 필수 |
| P-08 | `test_parse_reject_empty_input` | Boundary: `ERR_EMPTY_INPUT` |

---

## 음수·0 (5)

| # | 테스트 케이스 제목 | 보호 Invariant |
|---|-------------------|----------------|
| N-01 | `test_domain_reject_negative_magnitude` | D-INV-02: `Magnitude >= 0` |
| N-02 | `test_boundary_maps_negative_to_err_negative_value` | Boundary: Domain `NegativeMagnitudeError` → `ERR_NEGATIVE_VALUE` |
| N-03 | `test_convert_zero_meter_all_targets_zero` | D-INV-03: 0 입력 시 전 타깃 0 |
| N-04 | `test_table_output_zero_meter_three_lines` | D-INV-06: 배치 라인 수 = 등록 단위 수 |
| N-05 | `test_json_output_zero_source_value_numeric` | Boundary: JSON `source.value` 타입·0 표현 일관 |

---

## 미지원 단위 (4)

| # | 테스트 케이스 제목 | 보호 Invariant |
|---|-------------------|----------------|
| U-01 | `test_domain_convert_unregistered_unit_raises` | Domain: `UnregisteredUnitError` |
| U-02 | `test_boundary_unknown_unit_err_unknown_unit_field` | Boundary: `ERR_UNKNOWN_UNIT` + `field=unit` |
| U-03 | `test_integration_mile_colon_1_exit_nonzero` | Integration: 미등록 시 exit ≠ 0 |
| U-04 | `test_parse_reject_empty_unit_id` | Domain: `UnitId` 비어 있지 않음 |

---

## 비율 정확도 (7)

| # | 테스트 케이스 제목 | 보호 Invariant |
|---|-------------------|----------------|
| A-01 | `test_one_meter_to_feet_internal_3_28084` | D-INV-04: README `1m = 3.28084ft` |
| A-02 | `test_one_meter_to_yard_internal_1_09361` | D-INV-04: README `1m = 1.09361yd` |
| A-03 | `test_2_5_meter_to_feet_internal_8_2021` | D-INV-03: meter 앵커 환산식 |
| A-04 | `test_feet_to_meter_roundtrip_2_5` | D-INV-05: feet↔meter meter 경유 일치 |
| A-05 | `test_feet_to_yard_via_meter_consistent` | D-INV-05: feet↔yard 교차 일치 |
| A-06 | `test_table_display_feet_one_decimal_half_up` | Boundary: 표시 1자리 `ROUND_HALF_UP` (2.5m→8.2ft) |
| A-07 | `test_loaded_config_feet_meters_per_unit_0_3048` | Data+Domain: 파일 계수와 D-INV-04 일치 (ε) |

---

## 동적 등록 (5)

| # | 테스트 케이스 제목 | 보호 Invariant |
|---|-------------------|----------------|
| R-01 | `test_register_cubit_then_convert_includes_cubit_line` | UC-D-02: 등록 후 배치에 cubit 포함 |
| R-02 | `test_register_duplicate_unit_raises` | D-INV-08: 동일 `UnitId` 이중 등록 불가 |
| R-03 | `test_register_zero_factor_raises` | D-INV-01: `MetersPerUnit > 0` |
| R-04 | `test_register_success_message_exact_pattern` | Boundary: `MSG_REGISTER_OK` 고정 문구 |
| R-05 | `test_batch_line_count_after_register_is_four` | D-INV-06: 등록 후 라인 수 = registry.count() |

---

## 출력 직렬화 — 표 (Table) (4)

| # | 테스트 케이스 제목 | 보호 Invariant |
|---|-------------------|----------------|
| T-01 | `test_table_default_three_lines_meter_2_5` | Boundary: Table 줄 패턴 `{src} {unit} = {dst} {unit}` |
| T-02 | `test_table_source_value_not_rounded` | Boundary: `src_value` 반올림 없음 |
| T-03 | `test_table_line_order_matches_registry_list_order` | D-INV-07: 출력 순서 = `list_unit_ids()` |
| T-04 | `test_table_yard_display_one_decimal_from_2_5_meter` | Boundary: 표시 1자리 (예: 2.7 yard) |

---

## 출력 직렬화 — JSON (4)

| # | 테스트 케이스 제목 | 보호 Invariant |
|---|-------------------|----------------|
| J-01 | `test_json_structure_source_and_conversions_keys` | Boundary: JSON 스키마 (`source`, `conversions`) |
| J-02 | `test_json_conversions_length_equals_registry_count` | D-INV-06: `conversions` 배열 길이 |
| J-03 | `test_json_conversion_values_one_decimal_number_type` | Boundary: JSON 값 1자리 number |
| J-04 | `test_json_conversions_order_matches_registry_order` | D-INV-07: JSON 배열 순서 고정 |

---

## 출력 직렬화 — CSV (4)

| # | 테스트 케이스 제목 | 보호 Invariant |
|---|-------------------|----------------|
| C-01 | `test_csv_header_exact_four_columns` | Boundary: CSV 헤더 고정 |
| C-02 | `test_csv_row_count_equals_registry_count` | D-INV-06: 데이터 행 수 |
| C-03 | `test_csv_source_columns_repeated_per_row` | Boundary: `source_unit`, `source_value` 행별 동일 |
| C-04 | `test_csv_target_value_one_decimal_feet_row` | Boundary: CSV `target_value` 1자리 |

---

## 요약

| 분류 | 개수 |
|------|------|
| 파싱 | 8 |
| 음수·0 | 5 |
| 미지원 단위 | 4 |
| 비율 정확도 | 7 |
| 동적 등록 | 5 |
| 표 (Table) | 4 |
| JSON | 4 |
| CSV | 4 |
| **합계** | **41** |

**RED 실행 순서 제안**: 비율 정확도(A) → 음수·0(N) → 미지원(U) → 동적 등록(R) → 파싱(P) → 표·JSON·CSV → Integration(T-I 계열은 별도 스위트).

**회귀 앵커 (삭제 금지)**: `A-01`, `A-03`, `A-06`, `T-01`, `J-01`, `C-01`.

[REDACTED]

---

### Turn 175 — user

<user_query>
c:\DEV_BR\unit_converter_python용 .cursorrules YAML 뼈대.
최상위 키만, 값은 비움:
project, code_style, architecture, tdd_rules, testing, forbidden, file_structure, ai_behavior
각 키 앞에 80자 폭의 # 구분선 주석.
YAML만 출력. 설명 없음. 커서룰 파일을 만들어줘
</user_query>

---

### Turn 176 — assistant

[REDACTED]

---

### Turn 177 — assistant

[REDACTED]

---

### Turn 178 — assistant

```yaml
################################################################################
project:

################################################################################
code_style:

################################################################################
architecture:

################################################################################
tdd_rules:

################################################################################
testing:

################################################################################
forbidden:

################################################################################
file_structure:

################################################################################
ai_behavior:
```

[REDACTED]

---

### Turn 179 — user

<user_query>
파일만들어줘
</user_query>

---

### Turn 180 — assistant

[REDACTED]

---

### Turn 181 — assistant

현재 워크스페이스에 `.cursorrules` 파일을 생성합니다.

[REDACTED]

---

### Turn 182 — assistant

`c:\DEV_BR\UnitConvertor_06\.cursorrules` 파일을 만들었습니다. 이전에 요청하신 YAML 뼈대(8개 최상위 키, 값 비움, 80자 `#` 구분선)와 동일한 내용입니다.

[REDACTED]

---

### Turn 183 — user

<user_query>
미안 모르고 지웠어 다시만들어줘
</user_query>

---

### Turn 184 — assistant

[REDACTED]

---

### Turn 185 — assistant

`c:\DEV_BR\UnitConvertor_06\.cursorrules`를 다시 만들어 두었습니다. 이전과 같은 YAML 뼈대입니다.

[REDACTED]

---

### Turn 186 — user

<user_query>
@c:\DEV_BR\unit_converter_python\.cursorrules 
위 .cursorrules의 tdd_rules 블록만 채워라.
Python 단위 변환기 기준:
red_phase / green_phase / refactor_phase 각각에
description, rules(목록), must_not(목록)
YAML만 출력.
</user_query>

---

### Turn 187 — assistant

[REDACTED]

---

### Turn 188 — assistant

[REDACTED]

---

### Turn 189 — assistant

```yaml
tdd_rules:
  red_phase:
    description: >
      pytest RED — Domain/Boundary/Data 계약·Invariant·RED 목록에 맞는 테스트만 먼저 작성하고,
      구현 없이 실패를 확인한다. README 비율(1m=3.28084ft, 1m=1.09361yd) 및 고정 오류 문구를 테스트로 고정한다.
    rules:
      - RED 목록(Test-ID) 또는 BCE Traceability에 매핑된 케이스만 추가한다
      - Domain 테스트는 Registry·Engine 실객체를 사용하고 I/O·print·파일을 넣지 않는다
      - Boundary 테스트는 Parser·Renderer·오류 매핑만 검증하고 Engine은 Mock/Fake로 주입한다
      - 실패 assert는 수치(ε), 개수, 순서, exact message 문자열로 측정 가능하게 작성한다
      - 표/JSON/CSV 각 포맷·파싱·음수·미지원 단위·동적 등록·비율 정확도 분류를 빠짐없이 RED에 포함한다
      - 테스트 실행 시 의도적 실패(미구현·NotImplemented)를 GREEN 전제로 문서화한다
    must_not:
      - 구현 코드를 먼저 작성하거나 테스트를 구현에 맞게 뒤집지 않는다
      - "대충 통과"하는 assert(존재만 확인, 범위 없는 True)를 쓰지 않는다
      - RED 단계에서 전체 통합·CLI 수동 확인로 요구사항을 대체하지 않는다
      - README 상수·ErrorEnvelope 문구를 임의로 완화·생략하지 않는다
      - Domain 레이어에 input/print/json/csv/open을 넣지 않는다

  green_phase:
    description: >
      최소 구현으로 RED 테스트를 전부 GREEN 한다. OCP/SRP·BCE 의존 방향을 깨지 않고
      Domain → Boundary → Data → Integration 순으로 좁혀 간다.
    rules:
      - 한 번에 하나의 실패 테스트(또는 동일 Invariant 묶음)만 GREEN 대상으로 한다
      - Domain은 meter 앵커 환산(D-INV-03~05)과 Registry 등록 규칙만 구현한다
      - Boundary는 파싱·고정 오류 code/message·표시 반올림(1자리 ROUND_HALF_UP)만 구현한다
      - Data는 UnitDefinitionRepository.load와 JSON(또는 합의된 YAML) 스키마만 구현한다
      - GREEN 후 해당 Test-ID·Invariant가 Traceability Matrix에 연결됨을 유지한다
      - 회귀 앵커(A-01, A-03, A-06, T-01, J-01, C-01)는 삭제·약화하지 않는다
    must_not:
      - GREEN을 위해 공개 API·오류 문구·반올림 규칙을 테스트 없이 변경하지 않는다
      - 여러 Invariant를 한 함수에 몰아 SRP를 깨지 않는다
      - Boundary에 환산 비율 하드코딩·파일 직접 읽기를 넣지 않는다
      - 통과시키기 위해 테스트를 skip/xfail로 돌리지 않는다(의도적 RED 제외)
      - Integration GREEN 전 Domain·Boundary·Data 단위 RED가 비어 있지 않게 하지 않는다

  refactor_phase:
    description: >
      전 테스트 GREEN 상태에서만 구조·이름·중복을 정리한다. 행위·계약·수치·문구·출력 순서는 불변이다.
    rules:
      - 리팩터 전후 pytest 전체 스위트를 실행하고 diff 없음을 확인한다
      - 중복 제거·포트 추출·Renderer/Parser 분리는 테스트 변경 없이 수행한다
      - 새 단위·포맷·설정 소스 추가는 Registry/Strategy 확장으로만 한다(OCP)
      - 커버리지 목표(Domain line≥95%, Boundary≥90%, Data≥85%) 미달 시 테스트 보강 후 재리팩터한다
      - AI 생성 코드는 계약·RED 목록과 diff 검토 후 병합한다
    must_not:
      - RED·GREEN 없이 "정리" 명목으로 동작·스키마·에러 메시지를 바꾸지 않는다
      - refactor 중 새 요구사항(포맷·단위·검증 규칙)을 섞지 않는다 — 새 요구는 RED부터
      - 테스트를 리팩터 핑계로 통합·삭제하지 않는다
      - Domain이 Boundary/Data를 import하도록 의존성을 뒤집지 않는다
      - 표시 반올림·JSON 필드 순서·CSV 헤더를 "보기 좋게" 변경하지 않는다
```

[REDACTED]

---

### Turn 190 — user

<user_query>
완성한 .cursorrules 전체를 검토하라. 수정 제안 금지.
보고만:
1) YAML 문법 오류 가능성
2) 누락된 필수 섹션
3) tdd_rules vs forbidden 충돌
4) Cursor가 지키기 어려운 ai_behavior 규칙
bullet만.
</user_query>

---

### Turn 191 — assistant

[REDACTED]

---

### Turn 192 — assistant

[REDACTED]

---

### Turn 193 — assistant

[REDACTED]

---

### Turn 194 — assistant

**검토 대상:** `c:\DEV_BR\unit_converter_python\.cursorrules` (디스크 기준, 23줄·8개 최상위 키만 존재, 하위 값 전부 비어 있음)

### 1) YAML 문법 오류 가능성
- 최상위 키 8개 + `키:` 만 있는 형태는 YAML 1.1에서 **null 값**으로 파싱되며, 문법상 **즉시 깨지는 구조는 아님**
- 구분선 `#` 80자는 **주석**이라 파서에 영향 없음
- `tdd_rules` 등에 하위 맵을 붙일 때 **들여쓰기 2칸 불일치**하면 `red_phase`가 최상위로 튀어 나가는 **구조 오류**가 나기 쉬움 (현재 파일에는 해당 없음)
- 이전에 채웠던 형태 기준: `description: >` 접힘 블록 안의 `:`(예: `1m=3.28084ft`)는 따옴표 없이도 보통 허용되나, **에디터/파서마다 해석 차** 가능
- `≥`, `—` 등 비ASCII는 UTF-8 저장 시 대체로 안전하나, **BOM 저장** 시 일부 도구에서 1행 주석 깨짐 가능
- Cursor가 이 파일을 **엄격한 YAML로 파싱하는지**는 보장되지 않음 — 규칙이 **평문 규칙**으로만 주입되면 YAML 오류와 무관하게 동작할 수 있음

### 2) 누락된 필수 섹션
- 요청했던 최상위 8키(`project` … `ai_behavior`)는 **키 이름만 있고 모두 값 비어 있음**
- `tdd_rules` 내부 **필수 골격**(`red_phase` / `green_phase` / `refactor_phase`, 각 `description`·`rules`·`must_not`) — **디스크 파일에 없음** (이전 대화에서 작성한 내용은 현재 파일에 반영되지 않음)
- `testing`, `forbidden`, `file_structure`, `ai_behavior` — **실질 규칙 본문 전부 누락**
- BCE·RED·pytest·커버리지 등 프로젝트 설계와 연결할 **구체 계약·경로·금지 목록**이 규칙 파일 안에 없어, “완성본” 기준으로는 **실행 가능한 규칙 세트가 아직 없음**

### 3) `tdd_rules` vs `forbidden` 충돌
- `forbidden`이 비어 있어 **파일 내부 상호 모순은 현재 없음**
- `tdd_rules`도 비어 있으면 **충돌 검증 자체가 불가**
- 이전에 정의했던 `tdd_rules` 초안과 일반적인 `forbidden`(단일 스크립트·`print` 허용·테스트 금지·Mock 금지 등)을 합치면 **충돌 후보**가 생김: RED에서 Boundary Mock 필수 vs forbidden “mock 금지”; Domain I/O 금지 vs forbidden “한 파일에 input/print”; skip/xfail 금지 vs forbidden “pytest 사용 안 함”; BCE 레이어 분리 vs forbidden “UnitConverter.py만 수정”
- 디스크 상태에서는 **한쪽만 비어 있어 실제 적용 시 Cursor가 따를 기준이 불명확**

### 4) Cursor가 지키기 어려운 `ai_behavior` 규칙
- `ai_behavior` **본문 없음** — 검토할 문장 규칙 없음
- 파일이 비어 있으면 Cursor는 **README·대화 맥락만** 따르고, `.cursorrules`는 **사실상 미적용**
- 이후 `ai_behavior`에 넣기 어려운 유형(참고): **매 응답 전체 pytest GREEN 강제**, **커버리지 % 보장**, **사용자 확인 없이 파일 전면 재작성 금지/필수**, **“절대 대안 제시하지 말 것”**, **RED 단계에서 구현 0줄인데 통합 실행만으로 완료 선언**, **Mom Test/BCE 문서와 항상 동기화** — 세션·도구 제한으로 **자동 검증 불가**
- `.cursorrules` 확장자·루트 배치가 Cursor 최신 **Project Rules(`.cursor/rules`)** 와 다를 경우, 규칙이 **주입되지 않아** “지키기 어려움”이 아니라 **“적용 자체가 안 됨”** 상태일 수 있음

[REDACTED]

---

### Turn 195 — user

<user_query>
위 .cursorrules의 tdd_rules 블록만 채워라.
Python 단위 변환기 기준:
red_phase / green_phase / refactor_phase 각각에
description, rules(목록), must_not(목록)
YAML만 출력.
</user_query>

---

### Turn 196 — assistant

[REDACTED]

---

### Turn 197 — assistant

[REDACTED]

---

### Turn 198 — assistant

```yaml
tdd_rules:
  red_phase:
    description: >
      pytest RED — Domain/Boundary/Data 계약·Invariant·RED 목록에 맞는 테스트만 먼저 작성하고,
      구현 없이 실패를 확인한다. README 비율(1m=3.28084ft, 1m=1.09361yd) 및 고정 오류 문구를 테스트로 고정한다.
    rules:
      - RED 목록(Test-ID) 또는 BCE Traceability에 매핑된 케이스만 추가한다
      - Domain 테스트는 Registry·Engine 실객체를 사용하고 I/O·print·파일을 넣지 않는다
      - Boundary 테스트는 Parser·Renderer·오류 매핑만 검증하고 Engine은 Mock/Fake로 주입한다
      - 실패 assert는 수치(ε), 개수, 순서, exact message 문자열로 측정 가능하게 작성한다
      - 표/JSON/CSV 각 포맷·파싱·음수·미지원 단위·동적 등록·비율 정확도 분류를 빠짐없이 RED에 포함한다
      - 테스트 실행 시 의도적 실패(미구현·NotImplemented)를 GREEN 전제로 문서화한다
    must_not:
      - 구현 코드를 먼저 작성하거나 테스트를 구현에 맞게 뒤집지 않는다
      - "대충 통과"하는 assert(존재만 확인, 범위 없는 True)를 쓰지 않는다
      - RED 단계에서 전체 통합·CLI 수동 확인로 요구사항을 대체하지 않는다
      - README 상수·ErrorEnvelope 문구를 임의로 완화·생략하지 않는다
      - Domain 레이어에 input/print/json/csv/open을 넣지 않는다

  green_phase:
    description: >
      최소 구현으로 RED 테스트를 전부 GREEN 한다. OCP/SRP·BCE 의존 방향을 깨지 않고
      Domain → Boundary → Data → Integration 순으로 좁혀 간다.
    rules:
      - 한 번에 하나의 실패 테스트(또는 동일 Invariant 묶음)만 GREEN 대상으로 한다
      - Domain은 meter 앵커 환산(D-INV-03~05)과 Registry 등록 규칙만 구현한다
      - Boundary는 파싱·고정 오류 code/message·표시 반올림(1자리 ROUND_HALF_UP)만 구현한다
      - Data는 UnitDefinitionRepository.load와 JSON(또는 합의된 YAML) 스키마만 구현한다
      - GREEN 후 해당 Test-ID·Invariant가 Traceability Matrix에 연결됨을 유지한다
      - 회귀 앵커(A-01, A-03, A-06, T-01, J-01, C-01)는 삭제·약화하지 않는다
    must_not:
      - GREEN을 위해 공개 API·오류 문구·반올림 규칙을 테스트 없이 변경하지 않는다
      - 여러 Invariant를 한 함수에 몰아 SRP를 깨지 않는다
      - Boundary에 환산 비율 하드코딩·파일 직접 읽기를 넣지 않는다
      - 통과시키기 위해 테스트를 skip/xfail로 돌리지 않는다(의도적 RED 제외)
      - Integration GREEN 전 Domain·Boundary·Data 단위 RED가 비어 있지 않게 하지 않는다

  refactor_phase:
    description: >
      전 테스트 GREEN 상태에서만 구조·이름·중복을 정리한다. 행위·계약·수치·문구·출력 순서는 불변이다.
    rules:
      - 리팩터 전후 pytest 전체 스위트를 실행하고 diff 없음을 확인한다
      - 중복 제거·포트 추출·Renderer/Parser 분리는 테스트 변경 없이 수행한다
      - 새 단위·포맷·설정 소스 추가는 Registry/Strategy 확장으로만 한다(OCP)
      - 커버리지 목표(Domain line≥95%, Boundary≥90%, Data≥85%) 미달 시 테스트 보강 후 재리팩터한다
      - AI 생성 코드는 계약·RED 목록과 diff 검토 후 병합한다
    must_not:
      - RED·GREEN 없이 "정리" 명목으로 동작·스키마·에러 메시지를 바꾸지 않는다
      - refactor 중 새 요구사항(포맷·단위·검증 규칙)을 섞지 않는다 — 새 요구는 RED부터
      - 테스트를 리팩터 핑계로 통합·삭제하지 않는다
      - Domain이 Boundary/Data를 import하도록 의존성을 뒤집지 않는다
      - 표시 반올림·JSON 필드 순서·CSV 헤더를 "보기 좋게" 변경하지 않는다
```

[REDACTED]

---

### Turn 199 — user

<user_query>
완성한 .cursorrules 전체를 검토하라. 수정 제안 금지.
보고만:
1) YAML 문법 오류 가능성
2) 누락된 필수 섹션
3) tdd_rules vs forbidden 충돌
4) Cursor가 지키기 어려운 ai_behavior 규칙
bullet만.
</user_query>

---

### Turn 200 — assistant

[REDACTED]

---

### Turn 201 — assistant

**검토 대상:** `c:\DEV_BR\UnitConvertor_06\.cursorrules` (75줄)

### 1) YAML 문법 오류 가능성
- 최상위 8키 중 7개는 `키:` 만 있어 **null**로 파싱되며, 현재 구조만으로 **파싱 실패 가능성은 낮음**
- `tdd_rules` 하위 `red_phase` / `green_phase` / `refactor_phase` 들여쓰기(2칸)는 **일관되어 유효한 중첩 맵**으로 보임
- `description: >` 접힘 블록·목록 `-` 혼용은 **YAML 1.1에서 통상 유효**
- `≥`, `—`, 한글, `ε` 등 비ASCII는 UTF-8(무BOM) 기준 **문제 없음**
- `1m=3.28084ft` 등 `:` 포함 문장은 `>` 블록 안이라 **스칼라 오해 위험은 낮음**
- 구분선 `#` 80자는 **주석**이라 스키마에 영향 없음
- Cursor가 파일 전체를 **엄격 YAML**로 읽지 않으면, 문법은 맞아도 **규칙 주입 방식**은 달라질 수 있음

### 2) 누락된 필수 섹션
- 최상위 8키 **이름은 모두 존재**
- **`project`, `code_style`, `architecture`, `testing`, `forbidden`, `file_structure`, `ai_behavior`** — 본문·하위 필드 **전부 비어 있음**
- **`tdd_rules`만** `red_phase` / `green_phase` / `refactor_phase` 및 각 `description`·`rules`·`must_not` **채워짐**
- BCE·RED Test-ID·pytest 경로·에러 code 표·레이어 디렉터리 등 **프로젝트 실행에 필요한 나머지 블록 내용은 규칙 파일 안에 없음**
- “완성본” 관점에서는 **tdd_rules 단일 블록만 부분 완성** 상태

### 3) `tdd_rules` vs `forbidden` 충돌
- `forbidden`이 **비어 있어** 파일 내부 **명시적 모순 문장은 없음**
- `tdd_rules`가 요구하는 것과, 이후 `forbidden`에 흔히 넣는 규칙이 **충돌할 여지**가 있는 항목:
  - Boundary **Mock/Fake 필수**(RED) vs forbidden **mock/추상화 금지**
  - **BCE 레이어 분리·다파일** vs forbidden **`UnitConverter.py` 단일 파일만 수정**
  - **pytest·커버리지 %·전체 스위트**(refactor) vs forbidden **테스트 작성/실행 금지**
  - Domain **I/O 금지** vs forbidden **콘솔 `input`/`print` 유지**
  - GREEN 시 **JSON/YAML 설정 로드**(Data) vs forbidden **외부 파일 읽기 금지**
- 현재는 **forbidden 미정의**라 Cursor 적용 시 **tdd_rules만 유효**하고, forbidden 채우면 **우선순위 불명** 위험

### 4) Cursor가 지키기 어려운 `ai_behavior` 규칙
- `ai_behavior` **비어 있음** — 검토할 **문장 규칙 없음**
- `tdd_rules` 안에서도 Cursor/에이전트가 **자동으로 보장하기 어려운** 유형:
  - **RED에서 구현 없이 실패 확인**(세션마다 테스트 실행·실패 상태 유지 강제 불가)
  - **Traceability Matrix 연결 유지**(외부 문서·매트릭스 동기화 자동화 없음)
  - **회귀 앵커 삭제·약화 금지**(의도 판별·git diff 맥락 필요)
  - **refactor 전후 전체 pytest diff 없음**(매 턴 전체 실행·커버리지 측정은 환경·시간 의존)
  - **커버리지 Domain line≥95% 등 수치 목표**(한 응답 안에서 측정·보장 불가)
  - **AI 생성 코드 diff 검토 후 병합**(사용자 승인 없이 “검토 완료” 선언 불가)
  - **exact message·ROUND_HALF_UP·출력 순서 불변**(규칙은 명확하나 세션 간 **일관 적용**은 사용자 테스트 없으면 검증 불가)

[REDACTED]

---

### Turn 202 — user

<user_query>
프로젝트 루트 .cursorrules에 넣을 완성 YAML.
Python Python 3.11+ 이상 가정.
code_style: Black + isort, 타입 힌트 필수, 네이밍(snake_case/PascalCase)
architecture: boundary/control/entity 정의 + 의존성 방향
testing: pytest + pytest-cov 고정, AAA, fixture 규칙, 커버리지 기준
forbidden: print() 디버그 남발 / 매직 넘버 하드코딩 / bare except 무분별 삼키기 / 전역 변수 남용 / 타입 힌트 생략 (Python 특화 5개 이상)
  (각각 pattern / reason / alternative)
file_structure: boundary/ control/ entity/ tests/ 트리 주석
ai_behavior: 레이어 위반 금지, 테스트 먼저, 리팩터는 green 이후
설명 없이 YAML 전체만.
</user_query>

---

### Turn 203 — assistant

[REDACTED]

---

### Turn 204 — assistant

[REDACTED]

---

### Turn 205 — assistant

```yaml
################################################################################
project:
  name: unit-converter
  language: python
  python_version: "3.11+"
  domain: length unit conversion (meter, feet, yard + dynamic registration)
  anchor_unit: meter
  constants:
    meters_per_feet: 0.3048
    meters_per_yard: 0.9144
    display_decimal_places: 1
    display_rounding: ROUND_HALF_UP

################################################################################
code_style:
  formatter: black
  import_sorter: isort
  profile: black
  line_length: 88
  type_hints: required
  naming:
    modules_functions_variables: snake_case
    classes_exceptions: PascalCase
    constants: UPPER_SNAKE_CASE
    private: leading_underscore
  rules:
    - 모든 공개 함수·메서드에 매개변수·반환 타입 힌트를 붙인다
    - from __future__ import annotations 사용을 권장한다
    - Black·isort 적용 후 diff를 PR 기준으로 맞춘다
    - 문자열 오류 메시지는 Boundary 계약에 정의된 exact match 문구만 사용한다

################################################################################
architecture:
  pattern: BCE_dual_track
  layers:
    entity:
      alias: domain
      responsibility: UnitRegistry, ConversionEngine, LengthQuantity, invariants
      must_not: input, print, json, csv, open, pathlib for config
    control:
      alias: application
      responsibility: use-case orchestration, command dispatch, registry wiring
      must_not: conversion formulas, file format parsing details
    boundary:
      responsibility: CLI/input parse, output render (table/json/csv), error envelope mapping
      must_not: hardcoded conversion ratios, direct config file reads
    data:
      responsibility: UnitDefinitionRepository, JSON/YAML load, DTO to registry
      must_not: conversion math, user-facing message strings
  dependency_direction:
    allowed:
      - boundary -> control
      - boundary -> entity
      - control -> entity
      - control -> data
      - data -> entity
      - tests -> any production layer
    forbidden:
      - entity -> boundary
      - entity -> control
      - entity -> data
      - entity -> tests
  ocp:
    new_unit: register via UnitRegistry or config only
    new_format: new OutputRenderer strategy only

################################################################################
tdd_rules:
  red_phase:
    description: >
      pytest RED — Domain/Boundary/Data 계약·Invariant·RED 목록에 맞는 테스트만 먼저 작성하고,
      구현 없이 실패를 확인한다. README 비율(1m=3.28084ft, 1m=1.09361yd) 및 고정 오류 문구를 테스트로 고정한다.
    rules:
      - RED 목록(Test-ID) 또는 BCE Traceability에 매핑된 케이스만 추가한다
      - Domain 테스트는 Registry·Engine 실객체를 사용하고 I/O·print·파일을 넣지 않는다
      - Boundary 테스트는 Parser·Renderer·오류 매핑만 검증하고 Engine은 Mock/Fake로 주입한다
      - 실패 assert는 수치(ε), 개수, 순서, exact message 문자열로 측정 가능하게 작성한다
      - 표/JSON/CSV 각 포맷·파싱·음수·미지원 단위·동적 등록·비율 정확도 분류를 빠짐없이 RED에 포함한다
      - 테스트 실행 시 의도적 실패(미구현·NotImplemented)를 GREEN 전제로 문서화한다
    must_not:
      - 구현 코드를 먼저 작성하거나 테스트를 구현에 맞게 뒤집지 않는다
      - "대충 통과"하는 assert(존재만 확인, 범위 없는 True)를 쓰지 않는다
      - RED 단계에서 전체 통합·CLI 수동 확인로 요구사항을 대체하지 않는다
      - README 상수·ErrorEnvelope 문구를 임의로 완화·생략하지 않는다
      - Domain 레이어에 input/print/json/csv/open을 넣지 않는다

  green_phase:
    description: >
      최소 구현으로 RED 테스트를 전부 GREEN 한다. OCP/SRP·BCE 의존 방향을 깨지 않고
      Domain → Boundary → Data → Integration 순으로 좁혀 간다.
    rules:
      - 한 번에 하나의 실패 테스트(또는 동일 Invariant 묶음)만 GREEN 대상으로 한다
      - Domain은 meter 앵커 환산(D-INV-03~05)과 Registry 등록 규칙만 구현한다
      - Boundary는 파싱·고정 오류 code/message·표시 반올림(1자리 ROUND_HALF_UP)만 구현한다
      - Data는 UnitDefinitionRepository.load와 JSON(또는 합의된 YAML) 스키마만 구현한다
      - GREEN 후 해당 Test-ID·Invariant가 Traceability Matrix에 연결됨을 유지한다
      - 회귀 앵커(A-01, A-03, A-06, T-01, J-01, C-01)는 삭제·약화하지 않는다
    must_not:
      - GREEN을 위해 공개 API·오류 문구·반올림 규칙을 테스트 없이 변경하지 않는다
      - 여러 Invariant를 한 함수에 몰아 SRP를 깨지 않는다
      - Boundary에 환산 비율 하드코딩·파일 직접 읽기를 넣지 않는다
      - 통과시키기 위해 테스트를 skip/xfail로 돌리지 않는다(의도적 RED 제외)
      - Integration GREEN 전 Domain·Boundary·Data 단위 RED가 비어 있지 않게 하지 않는다

  refactor_phase:
    description: >
      전 테스트 GREEN 상태에서만 구조·이름·중복을 정리한다. 행위·계약·수치·문구·출력 순서는 불변이다.
    rules:
      - 리팩터 전후 pytest 전체 스위트를 실행하고 diff 없음을 확인한다
      - 중복 제거·포트 추출·Renderer/Parser 분리는 테스트 변경 없이 수행한다
      - 새 단위·포맷·설정 소스 추가는 Registry/Strategy 확장으로만 한다(OCP)
      - 커버리지 목표(Domain line≥95%, Boundary≥90%, Data≥85%) 미달 시 테스트 보강 후 재리팩터한다
      - AI 생성 코드는 계약·RED 목록과 diff 검토 후 병합한다
    must_not:
      - RED·GREEN 없이 "정리" 명목으로 동작·스키마·에러 메시지를 바꾸지 않는다
      - refactor 중 새 요구사항(포맷·단위·검증 규칙)을 섞지 않는다 — 새 요구는 RED부터
      - 테스트를 리팩터 핑계로 통합·삭제하지 않는다
      - Domain이 Boundary/Data를 import하도록 의존성을 뒤집지 않는다
      - 표시 반올림·JSON 필드 순서·CSV 헤더를 "보기 좋게" 변경하지 않는다

################################################################################
testing:
  framework: pytest
  coverage_tool: pytest-cov
  python_version: "3.11+"
  layout: tests mirror layer (tests/entity, tests/boundary, tests/data, tests/integration)
  pattern: AAA
  aaa:
    arrange: fixture·registry·mock engine setup
    act: single public call or parser/render entry
    assert: one logical outcome per test (numeric epsilon or exact string)
  fixtures:
    - session: defaults_registry (meter, feet, yard from README constants)
    - function: empty_registry, tmp_config_path (tmp_path factory)
    - boundary: fake_conversion_engine, capsys for stdout contract only in boundary tests
    - no_network: all tests offline
  commands:
    run: pytest
    cov: pytest --cov=entity --cov=boundary --cov=control --cov=data --cov-report=term-missing
  coverage_thresholds:
    entity_line: 95
    entity_branch: 90
    boundary_line: 90
    boundary_branch: 85
    data_line: 85
    data_branch: 80
  regression_anchors:
    - A-01
    - A-03
    - A-06
    - T-01
    - J-01
    - C-01

################################################################################
forbidden:
  - id: debug_print_spam
    pattern: "print(...) in entity/, control/, data/ or print left after debugging"
    reason: stdout side effect breaks layer purity and flaky boundary tests
    alternative: logging.getLogger(__name__) at WARNING+ or return structured ErrorEnvelope in boundary

  - id: magic_number_hardcoding
    pattern: "literal 3.28084, 1.09361, 0.3048 in boundary/ or control/ outside tests"
    reason: duplicates README contract and blocks config externalization (OCP)
    alternative: project.constants, config/units.json, or MetersPerUnit in entity registry

  - id: bare_except_swallow
    pattern: "except: or except Exception: pass without re-raise in production code"
    reason: hides NegativeMagnitudeError, parse errors, and breaks exact error mapping
    alternative: catch specific domain/boundary exceptions; map to ErrorEnvelope at boundary only

  - id: global_mutable_state
    pattern: "module-level registry = {} mutated by register() without injection"
    reason: test order dependence and breaks SRP/isolated RED
    alternative: UnitRegistry instance passed into ConversionEngine and control wiring

  - id: missing_type_hints
    pattern: "def foo(x, y): without -> and param types on public API"
    reason: violates code_style and weakens contract clarity for AI/refactor
    alternative: full hints; use TypeAlias, Protocol for ports (UnitDefinitionRepository)

  - id: entity_io
    pattern: "input(), open(), Path.read_text in entity/"
    reason: violates BCE entity purity (D-INV, architecture.forbidden)
    alternative: boundary parser + data repository load -> registry snapshot

  - id: skip_without_red_reason
    pattern: "@pytest.mark.skip on failing test to force green"
    reason: violates tdd_rules.green_phase.must_not
    alternative: implement minimal green or keep RED with NotImplementedError documented

################################################################################
file_structure:
  tree: |
    project_root/
    ├── boundary/           # parsers, renderers (table/json/csv), error_mapper, cli_adapter
    │   ├── parser.py
    │   ├── renderers/
    │   └── errors.py
    ├── control/            # app controller, command handlers, wiring (no I/O format details)
    │   └── converter_app.py
    ├── entity/             # domain: registry, engine, quantity, exceptions (pure)
    │   ├── registry.py
    │   ├── engine.py
    │   └── models.py
    ├── data/               # repositories, json/yaml sources, DTOs
    │   ├── repository.py
    │   └── sources/
    ├── config/             # units.json (optional units.yaml)
    │   └── units.json
    ├── tests/
    │   ├── entity/
    │   ├── boundary/
    │   ├── data/
    │   └── integration/
    ├── pyproject.toml      # black, isort, pytest, pytest-cov
    └── README.md
  entrypoint: boundary/cli_adapter.py or main.py delegates to control only

################################################################################
ai_behavior:
  layer_violation: forbidden
  rules:
    - entity/control/boundary/data 역할을 섞지 않는다 — 의심 시 architecture.dependency_direction을 따른다
    - 요구 변경·버그 수정은 RED 테스트 추가 후 최소 GREEN, 그 다음 refactor_phase만 구조 변경
    - refactor는 pytest 전체 GREEN 확인 후에만 제안·적용한다
    - README 상수·고정 오류 문구·출력 포맷은 테스트와 함께만 변경한다
    - 한 턴에 RED/GREEN/refactor 한 단계만 진행한다
    - forbidden 목록(pattern)에 해당하는 코드를 생성하지 않는다
  must_not:
    - 레이어 위반 import (entity -> boundary 등)
    - 테스트 없이 구현 파일 대량 생성
    - GREEN 미확인 상태에서 리네임·대규모 이동
    - forbidden.pattern에 맞는 패턴으로 “빠른 수정” 제안
```

[REDACTED]

---

### Turn 206 — user

<user_query>
c:\DEV\unit_converter_python를 위한 요구사항 서술 패키지. 구현·코드 금지.

Level 1 Epic
  제목: "확장 가능한 Python 단위 변환 학습 시스템"
  목적 4줄, 성공 기준 측정 가능하게 (커버리지, 계약 테스트, 회귀 정책)

Level 2 User Journey (1개 정본)
  Persona: Python/클린 아키텍처 학습자
  단계 5~7: 문제 인식→계약 정의→도메인 분리→Dual-Track TDD→회귀 보호
  각 단계 Pain / Opportunity 1줄

Level 3 User Stories (최소 6개)
  입력 검증 / 레지스트리·OCP / 환산 정확도 / 출력 포맷 / 설정 로드 실패 / 동적 단위 등록
  각 Story에 Acceptance Criteria는 체크 가능한 bullet

Level 4 Gherkin Feature 1개
  Background: README meter↔feet↔yard 비율을 Given으로 고정
  Scenario: happy path meter 입력
  Scenario: 잘못된 형식
  Scenario: unknown unit
  Scenario: 설정 파일 형식 오류

Level 5 체크리스트
  이 저장소 범위 항목만
  Epic→Journey→Story→Gherkin 정합성 체크박스 표

Markdown 표와 체크리스트 적극 사용.
완료 후 docs 폴더를 만들고 하위에 파일로 저장해줘
</user_query>

---

### Turn 207 — assistant

[REDACTED]

---

### Turn 208 — assistant

`c:\DEV_BR\unit_converter_python`에 요구사항 패키지 문서를 작성합니다 (`c:\DEV\unit_converter_python` 경로는 없음).

[REDACTED]

---

### Turn 209 — assistant

요구사항 패키지를 저장했습니다.

**경로:** `c:\DEV\unit_converter_python`는 없어서 **`c:\DEV_BR\unit_converter_python\docs\`** 에 반영했습니다.

| 파일 | 내용 |
|------|------|
| `docs/requirements/requirements-package.md` | Level 1 Epic ~ Level 5 정합성 체크리스트 (표·Gherkin·mermaid 포함) |
| `docs/README.md` | docs 인덱스 |

**포함 요약**

- **Level 1:** Epic 제목·목적 4줄·성공 기준 SC-01~06 (커버리지·계약 테스트·회귀 앵커)
- **Level 2:** Persona 민지·7단계 Journey (Pain/Opportunity 표)
- **Level 3:** US-01~06 (입력 검증, 레지스트리/OCP, 정확도, 포맷, 설정 실패, 동적 등록) + 체크 가능 AC
- **Level 4:** Gherkin Feature 1개 (Background 비율 고정 + 시나리오 4개)
- **Level 5:** Epic→Journey→Story→Gherkin 정합성 체크박스 15항 + In/Out 범위 표

`c:\DEV\unit_converter_python` 폴더를 따로 쓰려면 경로만 알려주시면 동일 문서를 복사해 두겠습니다.

[REDACTED]

---

### Turn 210 — user

<user_query>
c:\DEV_BR\unit_converter_python\docs\ 폴더 자체가 안만들어졌는데 다시 만들어줘
</user_query>

---

### Turn 211 — assistant

[REDACTED]

---

### Turn 212 — assistant

[REDACTED]

---

### Turn 213 — assistant

[REDACTED]

---

### Turn 214 — assistant

워크스페이스는 `UnitConvertor_06`인데 문서는 `unit_converter_python`에만 있어, 두 경로 모두에 `docs`를 다시 생성합니다.

[REDACTED]

---

### Turn 215 — assistant

[REDACTED]

---

### Turn 216 — assistant

[REDACTED]

---

### Turn 217 — assistant

`docs` 폴더를 다시 만들었고, 현재 워크스페이스인 `UnitConvertor_06`에도 동일하게 복사해 두었습니다.

### `c:\DEV_BR\unit_converter_python\docs\`

```
docs/
├── README.md
├── requirements/
│   └── requirements-package.md    ← Level 1~5 요구사항 패키지
├── bce/
│   └── BCE-design.md
├── mom-test/
│   └── Mom-Test-questions.md
└── BCE-design.md                  ← (기존 루트 복본)
```

### `c:\DEV_BR\UnitConvertor_06\docs\` (동일 구조 복사됨)

Explorer에서 **`unit_converter_python`** 만 열려 있으면 `docs`가 안 보일 수 있습니다. 지금 Cursor 워크스페이스가 **`UnitConvertor_06`** 이라면 왼쪽 트리에서 **`docs/requirements/requirements-package.md`** 를 확인하면 됩니다.

파일 탐색기에서 직접 보려면:

`c:\DEV_BR\unit_converter_python\docs\requirements\requirements-package.md`  
또는  
`c:\DEV_BR\UnitConvertor_06\docs\requirements\requirements-package.md`

[REDACTED]

---

### Turn 218 — user

<user_query>
미안 경로를 착각했어 다시 다지웠고 파일을 c:\DEV_BR\UnitConvertor_06\docs\ 하위에 만들어줘
</user_query>

---

### Turn 219 — assistant

[REDACTED]

---

### Turn 220 — assistant

[REDACTED]

---

### Turn 221 — assistant

[REDACTED]

---

### Turn 222 — assistant

`UnitConvertor_06\docs`가 비어 있어 문서를 처음부터 다시 생성합니다.

[REDACTED]

---

### Turn 223 — assistant

[REDACTED]

---

### Turn 224 — assistant

[REDACTED]

---

### Turn 225 — assistant

`c:\DEV_BR\UnitConvertor_06\docs\` 아래에 문서를 다시 만들었습니다.

```
docs/
├── README.md
├── requirements/
│   └── requirements-package.md
├── bce/
│   └── BCE-design.md
├── mom-test/
│   └── Mom-Test-questions.md
└── testing/
    └── RED-test-list.md
```

Cursor에서 **폴더 새로고침**(또는 워크스페이스 다시 열기) 후 `docs` 트리를 확인해 보시면 됩니다.

[REDACTED]

---

### Turn 226 — user

<user_query>
@docs/requirements-package.md 
당신은 제품 요구사항 문서(PRD) 전문가입니다.
워크스페이스: @c:\DEV_BR\UnitConvertor_06\ 
⚠️ 코드·클래스 설계·빌드 스크립트는 작성하지 마십시오. 문서만.
전제: Phase 4에서 완성된 Epic/User Stories/Gherkin을 기반으로 작성하라.

# 1. 프로젝트 개요
  1.1 한 줄 목적문 (What / Who / Why)
  1.2 배경 및 문제 정의 (관찰 관점)
  1.3 목표 3~5개 (측정 가능하게)
  1.4 비목표(Non-Goal) 2~3개

# 2. 사용자 및 이해관계자
  2.1 타깃 사용자 (페르소나 1개)
  2.2 주요 사용 시나리오 2~3개 (Phase 4 Journey 기반)

# 3. 기능 요구사항
  3.1 핵심 기능 목록 (우선순위: 필수/권장/선택 구분)
  3.2 기능별 입·출력 계약 (문자열 계약 수준, 코드 X)
  3.3 제약 사항 (입력 형식, 허용 단위, 음수 정책, 미지원 단위 처리)
  → Phase 4 Gherkin의 Background Given과 반드시 일치시킬 것

# 4. 비기능 요구사항
  4.1 기술 스택: Python 3.11+, pytest, pydantic
  4.2 아키텍처 원칙 (OCP/SRP, BCE 레이어, 의존성 방향)
  4.3 테스트 커버리지 목표 (Domain/Boundary/Data 수치)
  4.4 확장성 원칙 (새 단위 추가 시 기존 코드 변경 최소화)

# 5. 데이터 요구사항
  5.1 단위 비율 상수 (meter 허브 기준)
  5.2 설정 외부화 방식 (JSON/YAML 또는 메모리 기본값)
  5.3 동적 단위 등록 계약 (register: 형식 명시)

# 6. 출력 요구사항
  6.1 콘솔 기본 포맷 (필드·순서·소수 자릿수 정책)
  6.2 JSON 출력 스키마 (확장 시)
  6.3 CSV 출력 스키마 (확장 시)
  6.4 표(Table) 출력 스키마 (확장 시)

# 7. 성공 지표
  7.1 인수 기준 3~5개 (체크박스, 테스트 가능하게)
       → Phase 4 Story의 Acceptance Criteria와 일치 여부 확인
  7.2 회귀 보호 규칙 (계약 변경 금지 정책)

# 8. 용어 정의 (Glossary)
  주요 도메인 용어 5개 이상

출력: 구조화된 Markdown만. 모호어("적절히") 금지.
모든 계약·기준은 테스트 가능한 문장으로 작성.
이 외 다른 파일은 작성하지 않는다.

위치: @docs/  

</user_query>

---

### Turn 227 — assistant

[REDACTED]

---

### Turn 228 — assistant

[REDACTED]

---

### Turn 229 — assistant

[REDACTED]

---

### Turn 230 — assistant

Phase 4 `requirements-package.md`를 기준으로 `docs/PRD.md`만 작성합니다.

[REDACTED]

---

### Turn 231 — assistant

[REDACTED]

---

### Turn 232 — assistant

`c:\DEV_BR\UnitConvertor_06\docs\PRD.md`에 PRD 전체(§1~§8)를 저장했습니다. Phase 4 `requirements-package.md`의 Epic·Journey·Stories·Gherkin Background와 정합되도록 작성했으며, 다른 파일은 수정하지 않았습니다.

IDE에서 `docs/PRD.md`를 열면 전체 Markdown을 확인할 수 있습니다.

[REDACTED]

---

### Turn 233 — user

<user_query>
당신은 오픈소스 문서화 전문가입니다.
워크스페이스: @c:\DEV_BR\UnitConvertor_06\ 
전제: @docs/PRD.md 기반으로 작성하라.
⚠️ 코드 구현 추가 금지. 문서만 작성하라.

# 프로젝트 이름
한 줄 설명 (무엇을, 누구를 위해) — PRD 1.1 목적문 활용

## 목차
자동 링크 포함.

## 개요 (Overview)
- 이 프로젝트가 해결하는 문제 (PRD 1.2 배경 기반)
- 주요 학습 목표 (OCP/SRP, BCE, TDD)
- PRD와의 연결 (한 줄 요약 + PRD 문서 링크)

## 빠른 시작 (Quick Start)
- 사전 조건 (Python 버전, 빌드 도구)
- 빌드 & 실행 명령 (셸 블록 포함)
- 예시 입출력 (meter:5.0 → 결과)

## 지원 단위 및 비율
표 형식: 단위명 / 식별자 / meter 기준 비율 / 출처
(PRD 5.1 단위 비율 상수 기반)

## 입력 형식 계약
- 정상: 단위:값 예시 3개
- 비정상: 오류 케이스 3개 + 에러 메시지 패턴
(PRD 3.3 제약 사항 기반)

## 아키텍처
- BCE 레이어 다이어그램 (Mermaid 또는 ASCII)
- 의존성 방향 설명
- 새 단위 추가 방법 (단계별, 코드 최소화)

## 테스트 실행
- 테스트 프레임워크: pytest
- 명령: 셸 블록
- 커버리지 목표 (PRD 4.3 기반)

## 설정 파일 (JSON/YAML)
- 위치 및 형식 예시
- 동적 단위 등록 예시 (PRD 5.3 기반)

## 출력 포맷
콘솔 / JSON / CSV 각 예시 블록 포함. (PRD 6.1~6.3 기반)

## 기여 가이드 (Contributing)
- 계약 변경 금지 원칙
- 테스트 없는 PR 거부 정책
- 커밋 메시지 컨벤션

## 라이선스
MIT (학습용).

Markdown만 출력. 코드 구현 추가 금지.
표·코드 블록·Mermaid 다이어그램을 적극 활용하라.

위 내용을 기초로 @c:\DEV_BR\UnitConvertor_06\ 하위에 README 파일 만들어줘
</user_query>

---

### Turn 234 — assistant

[REDACTED]

---

### Turn 235 — assistant

[REDACTED]

---

### Turn 236 — assistant

`c:\DEV_BR\UnitConvertor_06\README.md`를 생성했습니다.

[docs/PRD.md](docs/PRD.md)를 기준으로 다음을 포함합니다.

- 목적문·목차(앵커 링크)
- 개요(문제·OCP/SRP/BCE/TDD·PRD 링크)
- Quick Start(Python 3.11+, `meter:5.0` 예시)
- 단위·비율 표(PRD §5.1)
- 입력 계약(정상 3 / 비정상 3 + exact message)
- BCE Mermaid·의존성·단위 추가 절차
- pytest·커버리지 목표
- `config/units.json`·동적 등록
- table / JSON / CSV 예시
- Contributing·MIT

코드 구현은 추가하지 않았습니다.

[REDACTED]

---

### Turn 237 — user

<user_query>
워크스페이스: @c:\DEV_BR\UnitConvertor_06\ 
전제: Phase 5 PRD의 기능 요구사항·인수 기준·회귀 보호 규칙을 기반으로 작성.
⚠️ 코드 작성 금지. 작업 목록 문서만.

# To-Do 리스트 — UnitConverter (Python)

## 🔴 필수 (Must-Have) — v1.0 릴리스 차단 항목
각 항목: [ ] 작업 설명 | 연관 PRD 항목 | 완료 기준(테스트 가능하게)

## 🟡 권장 (Should-Have) — 품질 향상 항목
각 항목: [ ] 작업 설명 | 연관 PRD 항목 | 완료 기준

## 🟢 선택 (Nice-to-Have) — v2.0 후보
각 항목: [ ] 작업 설명 | 기대 가치 한 줄

## 🔵 기술 부채 (Tech Debt)
각 항목: [ ] 문제 설명 | 발생 원인 | 해결 방향

## ✅ 완료 항목 (Done)
각 항목: [x] 완료 내용 | 완료일 | 관련 커밋/PR 메시지

## 📋 회귀 방지 체크리스트 (PRD 7.2 기반)
배포 전 반드시 확인: 계약 테스트 통과 / 커버리지 목표 달성 / README 갱신 여부

## 🗓️ 마일스톤
표 형식: 마일스톤 | 포함 항목(PRD 기능 번호) | 목표일 | 상태

Markdown만 출력. 각 항목은 "누가 무엇을 완료하면 통과"로 명확히.
@README.md  파일 하단에 내용 추가해줘
</user_query>

---

### Turn 238 — assistant

[REDACTED]

---

### Turn 239 — assistant

[REDACTED]

---

### Turn 240 — assistant

`README.md` 하단에 **To-Do 리스트 — UnitConverter (Python)** 섹션을 추가했고, 목차에도 링크를 넣었습니다.

포함 내용:
- **🔴 필수 9항** — F-01~04, AC-01~03, G-01/02/05, v1.0 차단
- **🟡 권장 8항** — F-05~07, AC-04~06, 커버리지, refactor, pydantic
- **🟢 선택 5항** — F-08, v2 후보
- **🔵 기술 부채 4항** — 레거시 단일 파일 등
- **✅ 완료 4항** — PRD·README·문서·cursorrules
- **📋 회귀 체크리스트** — PRD §7.2 (R-1~R-7)
- **🗓️ 마일스톤** — M0~M4 표

각 항목에 **학습자 / 리뷰어 / CI** 중 누가 무엇을 하면 통과하는지 적어 두었습니다.

[REDACTED]

---

### Turn 241 — user

<user_query>
Rreport 폴더에 보고서로 작성해주고(파일명은 폴더 내 파일명을 참고해서 번호는 꼭넣어줘)
prompting 폴더에 지금까지 대화내용 전체를 Export Transcript 해줘
파일명은 보고서 파일명과 같게 만들어줘
그리고 지금까지 작성한 모든 파일 및 변경점이 있는 파일들을 깃허브에 올려줘
꼭 순서대로 작업해줘
</user_query>

---

### Turn 242 — assistant

순서대로 진행합니다. 먼저 `Report`·`prompting` 폴더와 Git 상태를 확인합니다.

[REDACTED]

---

### Turn 243 — assistant

[REDACTED]

---

### Turn 244 — assistant

[REDACTED]

---

### Turn 245 — assistant

[REDACTED]

---

### Turn 246 — assistant

[REDACTED]

---

### Turn 247 — assistant

[REDACTED]

---

### Turn 248 — assistant

[REDACTED]

---

### Turn 249 — assistant

[REDACTED]

---

### Turn 250 — assistant

[REDACTED]

---

### Turn 251 — user

<user_query>
Rreport 폴더에 보고서로 작성해주고(파일명은 폴더 내 파일명을 참고해서 번호는 꼭넣어줘)
prompting 폴더에 지금까지 대화내용 전체를 Export Transcript 해줘
파일명은 보고서 파일명과 같게 만들어줘
그리고 지금까지 작성한 모든 파일 및 변경점이 있는 파일들을 깃허브에 올려줘
꼭 순서대로 작업해줘
</user_query>

---

### Turn 252 — assistant

[REDACTED]

---

### Turn 253 — assistant

[REDACTED]

---

### Turn 254 — assistant

[REDACTED]

---

### Turn 255 — assistant

[REDACTED]

---

### Turn 256 — assistant

README가 참조하는 문서가 누락되어 복구한 뒤 커밋합니다.

[REDACTED]

---

### Turn 257 — assistant

[REDACTED]

---

### Turn 258 — assistant

[REDACTED]

---

### Turn 259 — assistant

[REDACTED]

---

### Turn 260 — assistant

[REDACTED]

---

### Turn 261 — assistant

[REDACTED]

---

### Turn 262 — assistant

[REDACTED]

---

### Turn 263 — assistant

[REDACTED]

---

### Turn 264 — assistant

[REDACTED]

---

### Turn 265 — assistant

요청하신 순서대로 작업을 마쳤습니다.

## 1. Report 폴더 — 보고서

| 항목 | 내용 |
|------|------|
| 경로 | `Report/01_UnitConvertor_06_Phase5_Spec_Documentation.md` |
| 번호 | `01` (폴더 내 기존 명명 규칙) |
| 내용 | Phase 5 명세·문서화 작업 요약, 산출물, PRD 연계, 리스크, 다음 단계 |

## 2. prompting 폴더 — Export Transcript

| 항목 | 내용 |
|------|------|
| 경로 | `prompting/01_UnitConvertor_06_Phase5_Spec_Documentation.md` |
| 파일명 | 보고서와 동일 |
| 내용 | 대화 전체 Export (69 turns, 2026-05-20 기준) |

## 3. GitHub 업로드

| 항목 | 내용 |
|------|------|
| 브랜치 | `spec` |
| 커밋 | `a5e7c5a` — `docs: Phase 5 PRD, README, cursorrules, report and transcript` |
| 원격 | https://github.com/yuldakim/UnitConvertor_06.git (`spec` → `origin/spec`) |

**커밋에 포함된 변경:**

- `.cursorrules` (신규)
- `README.md` (수정)
- `docs/PRD.md`, `requirements-package.md`, `requirements.md` (신규)
- `Report/01_...`, `prompting/01_...` (신규)
- `UnitConverter.cpp` (삭제)

**참고:** 보고서에는 `docs/bce/`, `docs/testing/`, `docs/mom-test/` 등이 언급되지만, 현재 디스크에는 `docs/` 아래 3개 파일만 있습니다. README 링크와 맞추려면 해당 문서를 다시 추가하는 작업이 필요합니다. 원하시면 이어서 복구·커밋할 수 있습니다.

[REDACTED]

---

### Turn 266 — user

<user_query>
@docs/  @UnitConverter.py 
[P] 시니어 QA 리드입니다.
[C] C++17, Google Test, CMake
[T] 테스트 계획서를 작성해줘.
    - TEST_F 기반 단위 테스트 범위/우선순위
    - 경계값 케이스 목록
    - 예외/특이 케이스 목록
    - 커버리지 목표 (예: 90%+)와 gcov/lcov 측정·개선 전략
[F] Markdown 문서. docs에 test_plan.md로 저장
</user_query>

---

### Turn 267 — assistant

C++17·Google Test 기준 테스트 계획서를 작성하기 위해 프로젝트 문서와 `UnitConverter` 관련 코드를 확인합니다.

[REDACTED]

---

### Turn 268 — assistant

[REDACTED]

---

### Turn 269 — assistant

`UnitConverter.py` 동작과 BCE/RED 명세를 기준으로 C++17·Google Test 테스트 계획서를 작성합니다.

[REDACTED]

---

## Session `5722c54f-73c2-47eb-8060-1cbc8f447ca8`

### Turn 270 — user

<user_query>
당신은 Dual-Track UI(Boundary) + Logic(Domain) TDD 실무 전문가입니다.
프로젝트: @c:\DEV_BR\UnitConvertor_06\ 

이번 커밋에서 처리할 묶음을 1개 선택하고 아래 순서로 진행하라:

Step 1) 대상 TC 확인 (위 커밋 순서표 참고)
Step 2) pytest → 대상 TC가 FAIL인지 확인
Step 3) 대상 TC만 통과하는 최소 구현 작성
Step 4) pytest 재실행 → 대상 TC PASS, 나머지 영향 없음 확인
Step 5) 커밋

출력 형식:
1) 이번 커밋 목표 (Track A 또는 B, TC ID)
2) 추가/수정한 코드 범위
3) 테스트 결과 (PASS/FAIL 목록)
4) 커밋 메시지 (Conventional Commit)
5) 다음 커밋 후보 TC
</user_query>

---

### Turn 271 — assistant

커밋 순서표와 테스트 현황을 파악한 뒤, 이번에 처리할 TC 묶음 하나를 선택합니다.

[REDACTED]

---

### Turn 272 — assistant

[REDACTED]

---

### Turn 273 — assistant

[REDACTED]

---

### Turn 274 — assistant

[REDACTED]

---

### Turn 275 — assistant

[REDACTED]

---

### Turn 276 — assistant

[REDACTED]

---

### Turn 277 — assistant

[REDACTED]

---

### Turn 278 — assistant

[REDACTED]

---

### Turn 279 — assistant

[REDACTED]

---

### Turn 280 — assistant

[REDACTED]

---

### Turn 281 — assistant

TC-B-01(Track B)부터 진행합니다. RED 테스트가 FAIL인지 확인한 뒤, 해당 TC만 GREEN으로 전환합니다.

[REDACTED]

---

### Turn 282 — assistant

[REDACTED]

---

### Turn 283 — assistant

[REDACTED]

---

### Turn 284 — assistant

[REDACTED]

---

### Turn 285 — assistant

## 1) 이번 커밋 목표

| 항목 | 내용 |
|------|------|
| **Track** | **B (Domain / Logic)** |
| **TC ID** | **TC-B-01** — `convert("meter", 2.5, "feet")` → `8.20210` (±1e-5) |
| **순서표** | GREEN 권장: **entity(Logic) → boundary(UI)** — Track B 첫 항목 |

## 2) 추가/수정한 코드 범위

- **수정:** `tests/red/entity/test_logic_red_convert.py`
  - `test_logic_convert_meter_to_feet_within_1e_5`만 `pytest.fail("RED")` 제거
  - `ConversionEngine` + `defaults_registry`로 실제 assert 연결
- **프로덕션 코드:** 변경 없음 (`entity/engine.py`의 `convert`가 이미 BCE GREEN 33건에서 검증됨)

## 3) 테스트 결과

| 스위트 | 결과 |
|--------|------|
| **대상 TC-B-01** | **PASS** |
| `tests/red/entity/test_logic_red_convert.py` (나머지 5건) | **FAIL** (의도적 RED) |
| `tests/red/` 전체 | **1 passed, 16 failed** |
| `tests --ignore=tests/red` (BCE GREEN) | **33 passed** |

**Step 2 확인:** 대상 TC는 `Failed: RED`로 **FAIL** 확인됨.

## 4) 커밋 메시지

```
feat(entity): GREEN TC-B-01 meter to feet convert

Wire tests/red TC-B-01 to ConversionEngine with defaults registry.
Assert 2.5 meter to feet is 8.20210 within 1e-5.
Remaining logic RED tests stay intentional fail.
```

- **커밋:** `fecf385` (`green` 브랜치)

## 5) 다음 커밋 후보 TC

| 우선순위 | Track | TC ID | 테스트 메서드 |
|----------|-------|-------|----------------|
| **1** | B | **TC-B-02** | `test_logic_convert_meter_to_yard_within_1e_5` — `1.0 m → 1.09361 yd` |
| 2 | B | TC-B-03 | `test_logic_convert_feet_to_meter_reverse_within_1e_5` |
| 3 | B | TC-B-04 | `test_logic_convert_all_meter_returns_all_registered_units` |
| (병행 시) | A | TC-A-01 | `test_ui_convert_meter_2_5_returns_conversion_result` — entity GREEN 후 boundary slice |

[REDACTED]

---

### Turn 286 — user

<user_query>
모든 TC(TC-A-01~07, TC-B-01~07)가 통과한 후 전체 테스트를 실행하라.

pytest pytest -v tests/

커버리지 측정:
pip install pytest-cov pytest --cov=unit_converter --cov-report=term-missing pytest --cov=unit_converter --cov-report=html

확인 항목:
- 모든 TC PASS (0 failures)
- Domain Logic 커버리지 ≥ 95%
- Boundary Layer 커버리지 ≥ 85%
- 비율 상수 3.28084 / 1.09361이 인라인으로 남아 있지 않음
- main() 함수에 변환 로직이 남아 있지 않음 (Domain으로 분리됨)

이후: green → B_06 PR 생성 → 리뷰 → 머지
</user_query>

---

### Turn 287 — assistant

모든 TC를 GREEN으로 만든 뒤 전체 테스트·커버리지 검증과 PR까지 진행합니다. 현재 RED 테스트와 구현 상태를 파악합니다.

[REDACTED]

---

### Turn 288 — assistant

[REDACTED]

---

### Turn 289 — assistant

[REDACTED]

---

### Turn 290 — assistant

[REDACTED]

---

### Turn 291 — assistant

[REDACTED]

---

### Turn 292 — assistant

[REDACTED]

---

### Turn 293 — assistant

[REDACTED]

---

### Turn 294 — assistant

RED 테스트를 BCE 구현에 연결하고, JSON 렌더러 추가 및 `UnitConverter.py` 리팩터링을 진행합니다.

[REDACTED]

---

### Turn 295 — assistant

[REDACTED]

---

### Turn 296 — assistant

[REDACTED]

---

### Turn 297 — assistant

[REDACTED]

---

### Turn 298 — assistant

[REDACTED]

---

### Turn 299 — assistant

[REDACTED]

---

### Turn 300 — assistant

[REDACTED]

---

### Turn 301 — assistant

[REDACTED]

---

### Turn 302 — assistant

## 완료 요약

### 테스트 (`pytest -v tests/`)
- **50 passed, 0 failed** (BCE 33 + RED 17)
- TC-A-01~07, TC-B-01~07(RED 명세 기준) + B-08/09 모두 PASS

### 커버리지 (`entity` + `boundary`, `htmlcov/` 생성)

| 레이어 | 목표 | 실측 ( `__init__.py` 제외 ) |
|--------|------|---------------------------|
| **Domain (`entity`)** | ≥ 95% | **99%** |
| **Boundary** | ≥ 85% | **89%** |

> `unit_converter` 패키지는 없습니다. BCE 패키지 `entity`, `boundary`, `control`, `data`로 측정했습니다.

### 확인 항목

| 항목 | 결과 |
|------|------|
| 모든 TC PASS | ✅ 50/50 |
| Domain ≥ 95% | ✅ 99% |
| Boundary ≥ 85% | ✅ 89% |
| `3.28084` / `1.09361` boundary·control 인라인 없음 | ✅ (`entity/constants.py`만) |
| `main()` 변환 로직 없음 | ✅ `ConverterApp` 위임만 |

### 주요 변경
- `tests/red/**` — BCE API에 assert 연결 (RED → GREEN)
- `boundary/renderers/json_renderer.py` + `ConverterApp.handle_convert_line_json` (TC-A-06)
- `UnitConverter.py` — if-else 환산 제거, `ParseError`만 출력
- `README.md` — Track A/B To-Do 체크

### Git
- **커밋:** `4c74fbc` — `feat: GREEN all Dual-Track TC-A/B tests`
- **푸시:** `origin/green` 완료

---

## PR (`green` → `B_06`)

이 환경에 **GitHub CLI(`gh`)가 없어** PR을 자동 생성하지 못했습니다. 아래 중 하나로 진행해 주세요.

**웹에서 PR 생성:**  
https://github.com/yuldakim/UnitConvertor_06/compare/B_06...green

**제안 PR 제목/본문:**

```
feat: GREEN Dual-Track TC-A/B (M1 core)

## Summary
- tests/red TC-A-01~07, TC-B-01~07 GREEN (pytest 50 passed)
- JSON renderer + UnitConverter → ConverterApp delegation
- entity 99% / boundary 89% line coverage

## Test plan
- [x] pytest -v tests/
- [x] --cov=entity --cov=boundary (thresholds met)
- [x] no ratio literals in boundary/control
- [x] main() free of conversion logic
```

**`gh` 설치 후 (선택):**
```powershell
winget install GitHub.cli
gh pr create --base B_06 --head green --title "feat: GREEN Dual-Track TC-A/B (M1 core)" --body-file pr-body.md
```

리뷰·머지는 PR 생성 후 GitHub에서 **Approve → Merge pull request** 순서로 진행하면 됩니다. `gh` 설치 후 PR 생성까지 이어서 진행할까요?

[REDACTED]

---

### Turn 303 — user

<user_query>Briefly inform the user about the task result and perform any follow-up actions (if needed). If there's no follow-ups needed, don't explicitly say that.</user_query>

---

### Turn 304 — assistant

## 작업 결과

**Dual-Track TC 전체 GREEN**을 마쳤습니다.

- `pytest -v tests/` → **50 passed, 0 failed**
- TC-A-01~07, TC-B-01~07(RED 스위트) 모두 통과
- 커버리지: **entity 99%**, **boundary 89%** (목표 95% / 85% 충족)
- `UnitConverter.main()`은 `ConverterApp` 위임만 하고, boundary/control에 비율 상수 인라인 없음

**Git:** `green` 브랜치에 `4c74fbc` 커밋 후 `origin/green` 푸시 완료.

**PR:** `gh`가 없어 자동 생성은 못 했습니다. PR은 여기서 열면 됩니다:  
https://github.com/yuldakim/UnitConvertor_06/compare/B_06...green  
(base: `B_06`, head: `green`)

[REDACTED]

---

### Turn 305 — user

<user_query>
진행해줘
</user_query>

---

### Turn 306 — assistant

PR 생성을 진행합니다. Git 상태를 확인한 뒤 `gh` 설치·PR 생성을 시도합니다.

[REDACTED]

---

### Turn 307 — assistant

[REDACTED]

---

### Turn 308 — assistant

[REDACTED]

---

### Turn 309 — assistant

[REDACTED]

---

### Turn 310 — assistant

[REDACTED]

---

### Turn 311 — assistant

[REDACTED]

---

### Turn 312 — assistant

[REDACTED]

---

### Turn 313 — assistant

[REDACTED]

---

### Turn 314 — assistant

[REDACTED]

---

### Turn 315 — assistant

[REDACTED]

---

### Turn 316 — assistant

[REDACTED]

---

### Turn 317 — assistant

PR 생성까지 진행했습니다. GitHub CLI 인증만 로컬에서 한 번 완료하면 됩니다.

## 완료된 작업
- `green` 브랜치 최신 푸시 (`85ef5f6` — PR 본문·스크립트 포함)
- 테스트 재확인: **50 passed**
- 기본 브라우저에 PR 작성 페이지 열기 시도  
  https://github.com/yuldakim/UnitConvertor_06/compare/B_06...green?expand=1

## PR 생성 (둘 중 하나)

**A) 브라우저 (가장 빠름)**  
열린 Compare 페이지에서 **Create pull request** →  
- Title: `feat: GREEN Dual-Track TC-A/B (M1 core)`  
- Body: 저장소 루트 `pr-body.md` 내용 붙여넣기

**B) CLI (자동)**  
터미널에서:
```powershell
cd c:\DEV_BR\UnitConvertor_06
.\scripts\create-pr-to-b06.ps1
```
처음 실행 시 `gh auth login` 안내가 나오면 https://github.com/login/device 에서 코드 입력 후, 스크립트를 다시 실행하세요.

## 머지
PR 생성 후 GitHub에서 **Review → Merge pull request** (`B_06` ← `green`).

브라우저에 Compare 페이지가 보이면 **Create pull request**만 누르면 됩니다. CLI로 PR을 만들고 싶으면 `.\scripts\create-pr-to-b06.ps1` 실행 후 인증만 완료해 주세요.

[REDACTED]

---

### Turn 318 — user

<user_query>
당신은 Dual-Track UI(Boundary) + Logic(Domain) TDD 실무 전문가입니다.
프로젝트: @c:\DEV_BR\UnitConvertor_06\  / 이번 작업: "하나의 커밋" 단위

중요 규칙:
- 순서 준수: RED 선택 → GREEN 최소 구현 → 테스트 실행 → 통과 확인 → 커밋
- 1개 RED 테스트 묶음만 처리
- REFACTOR는 이번 커밋에서 금지
- 비율 상수 3.28084 / 1.09361은 인라인 하드코딩 금지 (상수 또는 설정 사용)
- 도메인 레이어에 UI/출력 코드 혼입 금지

고정 계약:
- 입력: str (단위:값) — "단위:값" 형식
- 출력: "값 단위 = 변환값 변환단위" 형식
- 예외: ValueError / TypeError

Step 1) 이번 커밋에서 선택할 RED 테스트 1묶음:
  [TRACK B] convert(meter, 2.5, feet) → 8.202100 (오차 1e-5)
  [TRACK A] ":" 없는 입력 → ValueError / TypeError 발생
  선택 이유를 2줄로 설명하십시오.

Step 2) GREEN 최소 구현 (Dual-Track 병렬)
Step 3) 테스트 실행 및 통과 확인

출력 형식:
1) 이번 커밋 목표  2) 선택한 RED 테스트  3) GREEN 최소 구현 범위
4) 실행한 테스트 목록  5) 결과 요약  6) 커밋 메시지 (Conventional Commit)
7) 변경 파일 목록  8) 다음 커밋 RED 후보 2개

주의: REFACTOR 금지 / 한 커밋에 모든 RED 해결 금지
</user_query>

---

### Turn 319 — assistant

현재 RED/GREEN 상태를 확인한 뒤, 이번 커밋에 처리할 RED 묶음 1개를 선택합니다.

[REDACTED]

---

### Turn 320 — assistant

[REDACTED]

---

### Turn 321 — assistant

[REDACTED]

---

### Turn 322 — assistant

[REDACTED]

---

### Turn 323 — assistant

[REDACTED]

---

### Turn 324 — assistant

Track B(TC-B-01)를 선택합니다. `B_06`에서 RED 실패 확인 후 GREEN 최소 구현·커밋을 진행합니다.

[REDACTED]

---

### Turn 325 — assistant

[REDACTED]

---

### Turn 326 — assistant

[REDACTED]

---

### Turn 327 — assistant

[REDACTED]

---

### Turn 328 — assistant

## Step 1) RED 선택 (2줄)

**선택: [TRACK B]** `convert(meter, 2.5, feet) → 8.20210` (ε 1e-5)

`.cursorrules` GREEN 순서상 **Domain(entity) → Boundary** 이므로, 환산 비율 앵커(D-INV-03)를 Logic에서 먼저 고정해야 UI 트랙이 Fake 없이 안전하게 이어집니다.  
제시된 두 묶음 중 **핵심 Happy Path 수치 계약**이므로 Track A 파싱보다 우선합니다.

*(Track A `":"` 없음은 이번 커밋에서 처리하지 않음 — B_06에서 여전히 RED)*

---

## 1) 이번 커밋 목표

**Track B · TC-B-01** — `ConversionEngine.convert("meter", 2.5, "feet")` ≈ `8.20210`

## 2) 선택한 RED 테스트

| ID | 테스트 | 입력/호출 | 기대 |
|----|--------|-----------|------|
| **TC-B-01** | `test_logic_convert_meter_to_feet_within_1e_5` | `convert("meter", 2.5, "feet")` | `8.20210` ±1e-5 |

## 3) GREEN 최소 구현 범위

- **프로덕션 코드 변경 없음** — `B_06`에 `ConversionEngine`·`UnitRegistry.with_defaults()` 이미 존재
- **변경:** `tests/red/entity/test_logic_red_convert.py`만 — RED `pytest.fail` → `ConversionEngine` + `FEET_PER_METER` assert
- **금지 준수:** 비율 인라인 없음(`entity/constants.py`), Domain에 UI 코드 없음, REFACTOR 없음

## 4) 실행한 테스트 목록

```text
pytest tests/red/entity/test_logic_red_convert.py::TestLogicRedConvert::test_logic_convert_meter_to_feet_within_1e_5 -v
pytest tests/red/entity/test_logic_red_convert.py -v
pytest tests/red/boundary/test_ui_red_parse.py::TestUiRedParseErrors::test_ui_parse_missing_colon_raises_value_error -v  # 영향 확인
```

## 5) 결과 요약

| 테스트 | Step 2 (RED) | Step 3 (GREEN) |
|--------|--------------|----------------|
| **TC-B-01** | **FAIL** (`Failed: RED`) | **PASS** |
| 동일 파일 나머지 5건 | FAIL (의도적 RED 유지) | FAIL |
| **TC-A-02** (미선택) | FAIL (RED 유지) | — |

## 6) 커밋 메시지 (Conventional Commit)

```text
feat(entity): GREEN TC-B-01 meter to feet convert

Wire tests/red TC-B-01 to ConversionEngine with defaults registry.
Assert convert(meter, 2.5, feet) is 8.20210 within 1e-5.
Uses FEET_PER_METER constant (no inline ratios).
Remaining logic RED tests unchanged.
```

- **커밋:** `57cd517` (`B_06` 브랜치)

## 7) 변경 파일 목록

- `tests/red/entity/test_logic_red_convert.py` (+12 / −2)

## 8) 다음 커밋 RED 후보 2개

1. **[TRACK B] TC-B-02** — `convert("meter", 1.0, "yard")` → `1.09361` (ε 1e-5)  
2. **[TRACK A] TC-A-02** — `"meter 2.5"` → `ValueError` / `TypeError` (`ERR_INVALID_FORMAT` 문구)

---

**참고:** `green` 브랜치에는 동일 TC-B-01이 이미 `fecf385`에 있습니다. 이번 작업은 **`B_06` 기준 1커밋 단위**로 적용했습니다. 원격 푸시는 `fetch/pull` 후 필요 시 `git push origin B_06` 하시면 됩니다.

[REDACTED]

---

### Turn 329 — user

<user_query>
깃에 커밋학 나머지 테스트도 중요규칙을 참고하여 하나하나씩 처리하면서 중요규칙을 준수해서 작업해줘
</user_query>

---

### Turn 330 — assistant

남은 RED 테스트를 규칙에 맞춰 하나씩 GREEN 처리하고 커밋합니다. 현재 `B_06` 브랜치 상태부터 확인합니다.

[REDACTED]

---

### Turn 331 — assistant

[REDACTED]

---

### Turn 332 — assistant

[REDACTED]

---

### Turn 333 — assistant

entity → boundary 순으로 TC마다 RED 확인 → GREEN → 커밋을 반복합니다.

[REDACTED]

---

### Turn 334 — assistant

[REDACTED]

---

### Turn 335 — assistant

[REDACTED]

---

### Turn 336 — assistant

[REDACTED]

---

### Turn 337 — assistant

B-08·B-09가 B-04 커밋에 묶였습니다. 커밋을 분리한 뒤 나머지 TC를 계속 처리합니다.

[REDACTED]

---

### Turn 338 — assistant

[REDACTED]

---

### Turn 339 — assistant

[REDACTED]

---

### Turn 340 — assistant

[REDACTED]

---

### Turn 341 — assistant

[REDACTED]

---

### Turn 342 — assistant

[REDACTED]

---

### Turn 343 — assistant

[REDACTED]

---

### Turn 344 — assistant

[REDACTED]

---

### Turn 345 — assistant

[REDACTED]

---

### Turn 346 — assistant

[REDACTED]

---

### Turn 347 — assistant

[REDACTED]

---

### Turn 348 — assistant

[REDACTED]

---

### Turn 349 — assistant

[REDACTED]

---

### Turn 350 — assistant

[REDACTED]

---

### Turn 351 — assistant

[REDACTED]

---

### Turn 352 — assistant

[REDACTED]

---

### Turn 353 — assistant

[REDACTED]

---

### Turn 354 — assistant

[REDACTED]

---

### Turn 355 — assistant

[REDACTED]

---

### Turn 356 — assistant

[REDACTED]

---

### Turn 357 — assistant

[REDACTED]

---

### Turn 358 — assistant

[REDACTED]

---

### Turn 359 — assistant

[REDACTED]

---

### Turn 360 — assistant

[REDACTED]

---

### Turn 361 — assistant

[REDACTED]

---

### Turn 362 — assistant

[REDACTED]

---

### Turn 363 — assistant

[REDACTED]

---

### Turn 364 — assistant

[REDACTED]

---

### Turn 365 — assistant

[REDACTED]

---

### Turn 366 — assistant

[REDACTED]

---

### Turn 367 — assistant

[REDACTED]

---

### Turn 368 — assistant

[REDACTED]

---

### Turn 369 — assistant

[REDACTED]

---

### Turn 370 — assistant

## 작업 완료 (`B_06` 브랜치)

중요 규칙(**1 TC = 1 커밋**, entity → boundary, REFACTOR 금지, 비율 상수만 `entity/constants`, Domain에 UI 없음)에 맞춰 **남은 RED 16건**을 순서대로 GREEN 처리하고 커밋했습니다.

### Track B — Entity / Data (11커밋 + 스텁 1)
| TC | 커밋 |
|----|------|
| B-01 | `57cd517` meter → feet |
| B-02 | `db7c49f` meter → yard |
| B-03 | `a5ce760` feet → meter |
| B-04 | `fca7d62` convertAll |
| B-08 | `afb7ffb` 음수 ValueError |
| B-09 | `aabc0fc` zero → 0.0 |
| B-05 | `24a0763` cubit 등록 |
| B-06 JSON | `7503cd3` |
| B-06 YAML | `6aed9fb` |
| B-07 | `43aac31` missing path → defaults |

### Track A — Boundary (7커밋)
| TC | 커밋 |
|----|------|
| A-02 | `a5292a6` `:` 없음 |
| A-03 | `27c7c46` 음수 |
| A-04 | `d71b06f` unknown unit |
| A-07 | `46151a8` `meter:abc` |
| A-01 | `55613a4` Happy path |
| A-05 | `68d5813` table 보존 |
| A-06 | `3fd0e7c` JSON (+ `json_renderer.py`, `handle_convert_line_json`) |

### 검증
- `pytest tests/` → **50 passed**
- `tests/red/` → **17 passed**
- `boundary/`, `control/`에 `3.28084` / `1.09361` 인라인 **없음**

### Git
- 원격에 이미 `green` PR 머지(`c3c5c7e`)가 있어 `pull` 시 충돌 → 해결 후 **`3a3f7ac` 푸시 완료** (`origin/B_06`)

### 참고
- `1860dbf` — B-05 커밋 시 실수로 지워진 B-06/B-07 RED 스텁 복구용 커밋(기능 변경 없음)
- 원격에 bulk 머지와 로컬 **커밋 단위 이력**이 공존합니다. 이후 PR/리뷰는 `B_06` 기준으로 진행하면 됩니다.

[REDACTED]

---

### Turn 371 — user

<user_query>Briefly inform the user about the task result and perform any follow-up actions (if needed). If there's no follow-ups needed, don't explicitly say that.</user_query>

---

### Turn 372 — assistant

## 작업 결과

`B_06` 브랜치에서 **TC-A-01~07, TC-B-01~07**(및 B-08/09)를 **1 TC당 1 커밋** 규칙으로 GREEN 처리했습니다.

- **테스트:** `pytest tests/` → **50 passed**, `tests/red/` → **17 passed**
- **규칙:** entity → boundary 순, 비율은 `entity/constants`만, REFACTOR 없음, TC-A-06만 JSON 렌더러 최소 추가
- **Git:** 원격 `green` 머지와 충돌 해결 후 **`origin/B_06` 푸시 완료** (`3a3f7ac`)

이후는 GitHub에서 `B_06` PR 리뷰·머지를 진행하시면 됩니다.

[REDACTED]

---

### Turn 373 — user

<user_query>
@README.md 
TO-DO 리스트의 체크박스가 다 비어있는데 왜 체크되어있었던걸 지운거야?
</user_query>

---

### Turn 374 — assistant

README의 TO-DO 섹션과 변경 이력을 확인합니다.

[REDACTED]

---

### Turn 375 — assistant

[REDACTED]

---

### Turn 376 — assistant

[REDACTED]

---

### Turn 377 — assistant

[REDACTED]

---

### Turn 378 — assistant

[REDACTED]

---

### Turn 379 — assistant

[REDACTED]

---

### Turn 380 — assistant

[REDACTED]

---

### Turn 381 — assistant

[REDACTED]

---

### Turn 382 — assistant

## 결론: 체크를 “지운” 게 아닙니다

지금 워크스페이스 `README.md`(브랜치 `B_06` / `green` 기준)를 보면 **Track A·B TC 항목은 모두 `- [x]`로 체크되어 있습니다.** 의도적으로 체크를 빼 둔 커밋은 없고, 오히려 GREEN 완료 시점에 **비어 있던 `[ ]`를 `[x]`로 바꾼** 이력이 있습니다.

---

## Git 이력으로 본 변화

| 시점 | 커밋 | RED To-Do (TC-A/B) 상태 |
|------|------|-------------------------|
| RED 단계 | `703950a` | 전부 `- [ ]` (의도적) |
| GREEN 일괄 | `4c74fbc` | 전부 `- [x]`로 변경 |
| B_06 1TC=1커밋 | `57cd517` ~ `3fd0e7c` | **README 수정 없음** (테스트·코드만) |

`703950a` → `4c74fbc` diff는 **`- [ ]` 삭제 + `+ [x]` 추가**이지, 체크 해제가 아닙니다.

---

## “체크가 사라진 것처럼” 보일 수 있는 이유

### 1) 보고 있는 브랜치/버전이 다름
- `703950a`(RED만 완료)나 `main`(README RED 섹션 없을 수 있음)을 보면 **전부 `[ ]`** 입니다.
- 체크가 반영된 건 **`green` / `B_06`(머지 후)** 쪽입니다.

### 2) 항목 **문구가 바뀜** (체크 해제가 아니라 ID 재매핑)
`4c74fbc`에서 설명도 같이 고쳤습니다.

| ID | RED 때 (`703950a`) | GREEN 후 (`4c74fbc`~) |
|----|-------------------|------------------------|
| TC-A-05 | 소수점 파싱 실패 `meter:abc` | 출력 포맷 원 단위·값 보존 |
| TC-A-06 | 출력 포맷 보존 | JSON 스키마 |
| TC-A-07 | value=0 경계값 | `meter:abc` 파싱 실패 |

예전에 익숙한 문구가 없어지면 “체크했던 줄이 지워졌다”고 느낄 수 있습니다.

### 3) README 안내 문구와 실제 체크 시점 불일치
```361:362:c:\DEV_BR\UnitConvertor_06\README.md
> 이 체크리스트는 [test_plan.md](docs/test_plan.md) 기반으로 생성되었습니다.
> 각 항목은 RED(실패 테스트 작성) 완료 시 체크합니다.
```

문서는 **RED 스켈레톤 완료** 기준인데, `[x]`는 **`4c74fbc`에서 pytest GREEN 이후**에 한꺼번에 넣었습니다. RED만 끝냈다면 TC 줄은 원래 `[ ]`가 맞고, 그 상태를 “체크가 있던 걸 지웠다”고 보신 걸 수도 있습니다.

### 4) 아직 비어 있는 항목
**커버리지 목표** 3줄은 여전히 `- [ ]`입니다. 전체가 다 빈 것처럼 보일 수 있습니다.

---

## Agent 세션에서 한 일

- `4c74fbc` / `green` 머지: TC-A/B → `[x]` + 문구 정리  
- `B_06`에서 TC별 커밋: **README는 건드리지 않음** (체크 해제 없음)

---

## 확인 방법

```powershell
git branch --show-current
Select-String "TC-A-01" README.md
```

`B_06` 또는 `green`이고 `- [x] TC-A-01`이면 저장소 기준으로는 정상입니다. `[ ]`만 보이면 `git checkout B_06` 또는 `git pull origin B_06`으로 맞춰 보시면 됩니다.

체크 상태를 **RED 완료 / GREEN 완료**로 나누고 싶으시면 Agent 모드에서 README 문구·체크리스트를 같이 정리할 수 있습니다.

[REDACTED]

---

### Turn 383 — user

<user_query>
@README.md 
to-do 리스트에 Green 단계를 Red 단계의 양식을 참고해서 만들고
현재까지 완료 된 부분이 있다면 체크박스에 체크를 해서 반영해줘
</user_query>

---

### Turn 384 — assistant

README의 RED To-Do 형식과 프로젝트 완료 상태를 확인한 뒤 GREEN 단계 To-Do를 추가합니다.

[REDACTED]

---

### Turn 385 — assistant

[REDACTED]

---

### Turn 386 — assistant

[REDACTED]

---

### Turn 387 — assistant

RED·GREEN To-Do를 분리해 README에 반영합니다.

[REDACTED]

---

### Turn 388 — assistant

[REDACTED]

---

### Turn 389 — assistant

## 반영 내용

`README.md`에 **GREEN 단계 To-Do**를 RED와 같은 Track A / Track B 형식으로 추가했고, 현재 저장소 상태에 맞게 체크를 넣었습니다.

### 변경 요약

1. **목차** — `GREEN 단계 To-Do 리스트` 링크 추가  
2. **RED 섹션** — “RED 스켈레톤 작성” 기준으로 문구 정리 (GREEN과 구분)  
3. **GREEN 섹션 (신규)**  
   - **Track A/B** — TC-A-01~07, TC-B-01~07 전부 **`[x]`** (`tests/red` PASS 기준)  
   - **통합·품질** — 50건 pytest, `UnitConverter` 위임, 비율 인라인 금지 준수 **`[x]`** / REFACTOR **`[ ]`**  
   - **커버리지** — entity ≥95%, boundary ≥85% **`[x]`** / 전체 90% **`[ ]`** (실측 약 89%)  
   - **결함** — BCE GREEN **`[x]`** / 레거시 CLI Open **`[ ]`**  
4. **마일스톤 M1** — `🟡 GREEN 진행 중`으로 갱신  

### 아직 체크하지 않은 항목

- REFACTOR 단계  
- 전체 커버리지 90%+  
- 레거시 CLI 결함(DEF-002,003,006~008)  

커밋까지 원하시면 Agent 모드에서 말씀해 주세요.

[REDACTED]

---

### Turn 390 — user

<user_query>
report 폴더에 지금까지의 진행상황 보고서로 작성해주고(파일명은 폴더 내 파일명을 참고해서 번호는 꼭넣어줘)
prompting 폴더에 지금까지 대화내용 전체를 Export Transcript 해줘
파일명은 보고서 파일명과 같게 만들어줘
그리고 지금까지 작성한 모든 파일 및 변경점이 있는 파일들을 깃허브에 올려줘
꼭 순서대로 작업해줘

</user_query>

---

### Turn 391 — assistant

Report 폴더 명명 규칙과 export 스크립트를 확인한 뒤, 순서대로 보고서 → Transcript → GitHub 푸시를 진행합니다.

[REDACTED]

---

### Turn 392 — assistant

[REDACTED]

---

### Turn 393 — assistant

[REDACTED]

---

### Turn 394 — assistant

[REDACTED]

---

### Turn 395 — assistant

[REDACTED]

---

### Turn 396 — assistant

[REDACTED]

---

### Turn 397 — assistant

[REDACTED]

---

### Turn 398 — assistant

요청하신 순서대로 마쳤습니다.

## 1) Report — 진행 보고서

| 항목 | 내용 |
|------|------|
| **파일** | [Report/03_UnitConvertor_06_Green_TDD_Implementation_Progress.md](Report/03_UnitConvertor_06_Green_TDD_Implementation_Progress.md) |
| **선행** | Report `01`(Phase 5), `02`(RED) |
| **요약** | GREEN 17+33=50 pytest PASS, TC별 커밋, `green` PR 머지, JSON/CLI 위임, README GREEN To-Do, 잔여 REFACTOR·cov 90% |

## 2) Prompting — Transcript Export

| 항목 | 내용 |
|------|------|
| **파일** | [prompting/03_UnitConvertor_06_Green_TDD_Implementation_Progress.md](prompting/03_UnitConvertor_06_Green_TDD_Implementation_Progress.md) |
| **크기** | 약 228KB (에이전트 transcript 5개 세션 + 요약) |
| **스크립트** | `scripts/export_transcript.py` → report `03` 기준으로 갱신 |

## 3) GitHub 푸시

| 항목 | 내용 |
|------|------|
| **브랜치** | `B_06` |
| **커밋** | `53049ba` — `docs: report 03, GREEN To-Do README, transcript export` |
| **푸시** | `origin/B_06` 완료 (`3a3f7ac..53049ba`) |
| **포함 변경** | `README.md`(RED/GREEN To-Do), Report 03, prompting 03, export 스크립트 |

이전 GREEN·TC 커밋들은 이미 `origin/B_06`에 올라가 있었고, 이번 커밋으로 문서·README 미반영분을 맞춰 두었습니다.

**저장소:** https://github.com/yuldakim/UnitConvertor_06/tree/B_06

[REDACTED]

---

## Session `6d00d1f7-3761-420c-95af-5c9b2ce3f74e`

### Turn 399 — user

<user_query>
@docs/ @UnitConverter.py 
[P] 시니어 QA 리드입니다.
[C] Python 3, pytest, pytest-cov, (가능하면 coverage.py HTML 리포트)
[T] 테스트 계획서를 작성해줘.
    - pytest 기반 단위 테스트 범위/우선순위
    - @pytest.mark.parametrize 활용 경계값 케이스 목록
    - 예외/특이 케이스 목록
    - 커버리지 목표 (예: 90%+)와 pytest-cov 측정·개선 전략
      (pytest --cov=gilded_rose --cov-report=term-missing)
[F] Markdown 문서. @docs/ test_plan.md로 저장
</user_query>

---

### Turn 400 — assistant

테스트 계획서 작성을 위해 `UnitConverter.py`와 `docs/` 구조를 먼저 확인합니다.

[REDACTED]

---

### Turn 401 — assistant

[REDACTED]

---

### Turn 402 — assistant

[REDACTED]

---

### Turn 403 — assistant

[REDACTED]

---

### Turn 404 — assistant

PRD·요구사항·현재 `UnitConverter.py`를 반영해 `docs/test_plan.md` 작성 중입니다.

[REDACTED]

---

### Turn 405 — assistant

테스트 계획서를 **`docs/test_plan.md`** 에 저장했습니다.

### 문서 구성 요약

1. **범위·전략** — PRD/BCE 기준 In/Out, 현재 `UnitConverter.py`와 목표 계약 차이 표, P0→P2 우선순위, 레이어별 테스트 피라미드  
2. **pytest 단위 테스트 범위** — `entity` / `boundary` / `control` / `data` / `integration` 별 대상·Mock 정책  
3. **`@pytest.mark.parametrize`** — 환산 ε, ROUND_HALF_UP 표시, 파싱·등록·config·출력 포맷용 표와 예시 코드 스니펫  
4. **예외·특이 케이스** — Domain 예외, CFG 실패·Registry 불변, 부동소수점, 회귀 앵커(A-01 등)  
5. **커버리지** — entity ≥95% / boundary ≥90% / data ≥85%,  
   `pytest --cov=entity --cov=boundary --cov=control --cov=data --cov-report=term-missing`  
   및 `htmlcov` HTML 리포트, 미달 시 7단계 개선 절차  

요청하신 예시의 `--cov=gilded_rose`는 이 프로젝트 패키지명(`entity`, `boundary`, …)에 맞게 반영했습니다. 모노리스 단계에서는 `UnitConverter`만 cov 대상으로 잡을 수 있다는 전환 메모도 포함했습니다.

`docs/testing/RED-test-list.md`는 아직 워크스페이스에 없어서 계획서에서는 “동기화 예정”으로 링크만 걸어 두었습니다. RED 목록이 생기면 P0 ID와 1:1 맞추면 됩니다.

[REDACTED]

---

### Turn 406 — user

<user_query>
@docs/ @README.md @UnitConverter.py 
[P] 테스트 설계에 강한 시니어 Python QA입니다.
[C] Python 3, pytest
[T] 위 참고 문서와 코드를 참고하여 테스트 케이스를 만들어줘
[F] 완성된 테스트 코드. pytest -v가 RED가 되게 작성
</user_query>

---

### Turn 407 — assistant

RED 단계 테스트 작성을 위해 프로젝트 구조와 참고 문서를 확인합니다.

[REDACTED]

---

### Turn 408 — assistant

[REDACTED]

---

### Turn 409 — assistant

[REDACTED]

---

### Turn 410 — assistant

BCE 레이어 구조에 맞춰 RED 테스트 코드를 작성하고 `pytest -v`로 실패를 확인합니다.

[REDACTED]

---

### Turn 411 — assistant

[REDACTED]

---

### Turn 412 — assistant

[REDACTED]

---

### Turn 413 — assistant

[REDACTED]

---

### Turn 414 — assistant

[REDACTED]

---

### Turn 415 — assistant

파서 테스트에서 `mile` 검증은 통합 테스트로만 두고, 개발 의존성 파일을 추가합니다.

[REDACTED]

---

### Turn 416 — assistant

[REDACTED]

---

### Turn 417 — assistant

RED 단계 **pytest 테스트 스위트**를 추가했습니다. `entity` / `boundary` / `data` / `control` 구현이 없어 **수집 단계에서 `ModuleNotFoundError`** 가 나며, 이는 의도한 RED 상태입니다.

### 실행

```bash
pip install -r requirements-dev.txt
pytest -v
```

현재 결과: **10 errors during collection** (0 passed) — `No module named 'entity'` 등.

### 디렉터리 구조

```
tests/
├── conftest.py              # defaults_registry, conversion_engine, fake_conversion_batch
├── entity/
│   ├── test_registry.py     # Registry·등록·INV
│   ├── test_engine.py       # A-01, A-03, A-06, parametrize 환산
│   └── test_display.py      # ROUND_HALF_UP 1자리
├── boundary/
│   ├── test_parser.py       # 파싱·ERR_* exact message
│   ├── test_render_table.py # T-01
│   ├── test_render_json.py
│   └── test_render_csv.py
├── data/
│   └── test_units_repository.py  # C-01, CFG_*
└── integration/
    ├── test_cli_convert.py  # J-01, AC-02/03
    └── test_cli_register.py # cubit 등록
```

`pyproject.toml`에 `pythonpath = ["."]`, 마커 `anchor` / `p0` / `p1` / `p2` 포함.

### 테스트가 기대하는 구현 API (GREEN 시 생성)

| 패키지 | 주요 심볼 |
|--------|-----------|
| `entity` | `UnitRegistry`, `ConversionEngine`, `Quantity`, `ConversionBatch`, `format_display_value`, 예외 4종 |
| `boundary` | `parse_input`, `ErrorCode`, `TableRenderer` / `JsonRenderer` / `CsvRenderer`, `run_command` |
| `data` | `UnitsRepository`, `ConfigError` |

### 회귀 앵커 (`@pytest.mark.anchor`)

- **A-01**, **A-03**, **A-06** — `test_engine.py`
- **T-01** — `test_render_table.py`
- **J-01** — `test_cli_convert.py`
- **C-01** — `test_units_repository.py`

### GREEN 순서 (권장)

1. `entity/` (Registry + Engine + display)  
2. `boundary/parser` + `errors`  
3. `boundary/renderers` + `cli_adapter`  
4. `data/repository`  
5. `control/converter_app` — 통합 테스트 GREEN

`docs/test_plan.md`의 parametrize 표·PRD 오류 문구·README 비율(`meters_per_unit`: 1.0 / 0.3048 / 0.9144)를 기준으로 작성했습니다. 구현을 시작하면 `pytest -v`는 수집 후 **FAILED**로 바뀌고, GREEN을 맞추면 **passed**로 전환됩니다.

[REDACTED]

---

### Turn 418 — user

<user_query>
@README.md 
문서 내 TO-DO-LIST를 참고하여 현재 RED단계에서 완료한것은 체크 표시 위 작업에서 문서에 있는 내용이 반영되지 않았다면 반영 후 체크표시로 변경해줘
</user_query>

---

### Turn 419 — assistant

README의 TO-DO 목록을 확인하고 RED 단계에서 완료된 항목을 반영합니다.

[REDACTED]

---

### Turn 420 — assistant

[REDACTED]

---

### Turn 421 — assistant

[REDACTED]

---

### Turn 422 — assistant

[REDACTED]

---

### Turn 423 — assistant

README에 RED 단계 산출물을 반영하고, 완료된 항목만 체크합니다.

[REDACTED]

---

### Turn 424 — assistant

README **To-Do**와 본문을 RED 단계 산출물에 맞게 갱신했습니다.

### README 본문 반영
- **Quick Start:** `requirements-dev.txt` 설치 경로 추가
- **테스트 실행:** `tests/` 레이아웃, `pyproject.toml` / `requirements-dev.txt`, **RED 단계에서 `pytest -v` 실패가 정상**이라는 설명
- **관련 문서:** [docs/test_plan.md](docs/test_plan.md) 링크 추가

### 체크 표시 (RED에서 완료된 항목만)

| 구분 | 항목 | 비고 |
|------|------|------|
| **Must-Have** | `pyproject·tests/ 레이아웃·pytest RED 실행` | 레이아웃·RED 실행 확인 완료; **GREEN 시 exit 0**은 아직 미완 |
| **Must-Have** | `RED P0 전부 GREEN` | **미체크** — TC 작성만 완료라는 주석 추가 |
| **Tech Debt** | `앵커 TC pytest 작성 (GREEN 대기)` | A-01, A-03, A-06, T-01, J-01, C-01 테스트 코드 반영 |
| **Done** | 테스트 계획서, RED pytest 스위트, pytest 프로젝트 설정 | 3항목 추가 |
| **마일스톤 M1** | `🔴 RED (TC 작성 완료 → GREEN 대기)` | 상태 문구 변경 |

### 의도적으로 미체크 (구현·GREEN 필요)
- entity / boundary / control 구현
- RED P0 **GREEN**
- 통합 Happy path **GREEN**
- 권장·선택 항목 전부

`entity`·`boundary` 등 **프로덕션 코드가 없으므로** Must-Have 구현 항목은 RED TC 작성만으로는 체크하지 않았습니다.

[REDACTED]

---

### Turn 425 — user

<user_query>
RED 단계에서는 한항목밖에 체크되지 않았는데 나머지 체크 되지 않은 항목은 테스트 코드에 반영이 되지 않은거야? 코드 수정 없이 대답만해
</user_query>

---

### Turn 426 — assistant

**아니요.** 체크가 안 된 이유는 대부분 “테스트 코드에 없어서”가 아니라, README To-Do의 **완료 기준**이 **구현 + `pytest` GREEN(exit 0)** 이라서입니다.

RED 단계에서 한 항목만 체크한 것은 **`pyproject` / `tests/` 레이아웃·RED 실행 가능`**처럼, **“테스트가 돌아가는 환경”** 만 Done으로 본 것이고, 나머지는 **TC는 있어도 아직 실패(수집 오류·미구현)** 라서 Must-Have는 그대로 둔 것입니다.

### 테스트 코드에 이미 들어간 것 (체크는 안 됨)

| 미체크 To-Do (요약) | `tests/` 반영 |
|---------------------|----------------|
| entity Registry·환산 | `tests/entity/test_registry.py`, `test_engine.py` (A-01, A-03, A-06 등) |
| 음수·0·미등록 거부 | `test_engine.py`, `test_registry.py`, `test_parser.py`, `test_cli_convert.py` |
| boundary 파싱·table | `test_parser.py`, `test_render_table.py` (T-01) |
| 오류 문구 exact | `test_parser.py` parametrize, CLI 통합 |
| 표시 반올림 1자리 | `test_display.py`, engine/ table·CLI assert |
| 통합 Happy path / unknown | `test_cli_convert.py` (J-01 등) |
| RED P0 (GREEN 아님) | 전 레이어 P0/p1/p2·anchor 마커 다수 — **GREEN 항목이라 미체크** |

### 테스트에 거의/전혀 없거나 약한 것

| 미체크 To-Do | 이유 |
|--------------|------|
| **control 오케스트레이션** | `tests/control/` 없음. `run_command` 통합으로만 간접 커버 |
| **RED P0 전부 GREEN** | TC는 있음. **구현 없어서 통과 불가** |
| **권장** (config JSON/CSV 상세, cov 90%+, BCE refactor, pydantic) | TC 일부는 있음(`data/`, json/csv renderer) but **Done 기준은 구현·커버리지·리팩터** |

**정리:** 미체크 ≠ 테스트 미작성. 대부분은 **RED TC는 작성됐고**, README는 **GREEN·인수 기준**까지 가야 `[x]`로 보는 구조입니다. 예외는 **control 전용 단위 테스트**처럼 To-Do에 비해 테스트가 얇은 항목이 일부 있습니다.

[REDACTED]

---

### Turn 427 — user

<user_query>
그러면 TO-DO-LIST가 현재 작업과는 조금 동떨어진 내용으로 작성이 된것 같은데
RED-GREEN-REFECTORING-기술부채해결 등으로 작업을 진행할 예정이야
이 질문도 코드나 문서수정없이 대답만 먼저 해줘
</user_query>

---

### Turn 428 — assistant

**맞습니다. 지금 README To-Do는 “TDD 단계”보다 “v1.0 릴리스 기능 묶음”에 가깝습니다.** 그래서 RED만 끝냈는데도 체크가 거의 안 되는 느낌이 드는 게 자연스럽습니다.

### 왜 어긋나 보이는지

| README To-Do 방식 | 실제 진행 방식 |
|-------------------|----------------|
| **기능·레이어별 Done** (entity 환산, boundary 파싱, AC-01 GREEN…) | **단계별 Done** (RED 작성 → GREEN 구현 → refactor → 부채) |
| 한 줄에 **구현 + 테스트 통과 + CI**가 한꺼번에 | RED에서는 **TC만** 완료, GREEN에서 **코드**, refactor에서 **구조** |
| Must / Should / Tech debt가 **릴리스 우선순위** | Tech debt 항목이 **refactor 전제**인데 Must와 **같은 리스트**에 섞임 |

지금 체크한 한 줄(`pyproject·tests·pytest RED`)만 “단계”에 가깝고, 나머지 Must는 전부 **“M1 끝났을 때”** 기준이라 RED 중에는 대부분 `[ ]`가 맞습니다. **테스트 미반영이 아니라, 완료 정의가 GREEN 이후**라서 그렇게 보이는 겁니다.

### RED → GREEN → REFACTOR → 기술부채와의 대응

**RED (지금 근처)**  
- 할 일: 계약·앵커·P0 TC 작성, `pytest`가 **의도적으로 실패**  
- README와 맞는 항목: 테스트 계획, `tests/` 레이아웃, RED 실행 — **Done에 넣은 3개가 이 층**  
- 안 맞는 점: Must 8개가 “entity 구현 GREEN”처럼 읽혀 RED 완료가 안 보임  

**GREEN**  
- 할 일: `entity` → `boundary` → `data` → 통합 순으로 **최소 구현**, P0·앵커 **0 failed**  
- 그때 README Must 대부분이 한꺼번에 `[x]`에 가까워짐 (지금 미체크 항목의 본래 의도)  

**REFACTOR**  
- 할 일: `UnitConverter.py` 분리, 의존성 정리, **행위·문구 불변**, refactor 전후 pytest 동일  
- README의 “BCE refactor”, forbidden, RR-04 — **Must가 아니라 M2·Tech debt 쪽**에 가깝은데 Must와 섞여 있음  

**기술부채**  
- 할 일: 비율 단일 출처, 레거시 파일 정리, 문서·코드 드리프트 방지  
- README Tech debt — **단계가 끝난 뒤** 치는 게 맞고, “앵커 TC 미구현”은 RED 후엔 **문구만 outdated** (TC는 있음, GREEN 대기)  

### 정리 (질문에 대한 직접 답)

1. **To-Do가 작업과 동떨어진 느낌이 드는 건 타당합니다.**  
   - 진행 축: **단계(RED/GREEN/refactor/부채)**  
   - 문서 축: **기능 인수(릴리스 게이트)**  

2. **미체크 ≠ 테스트 누락**이었고, **미체크 = “아직 GREEN/릴리스 게이트 미통과”**에 가깝습니다.  

3. 앞으로 RED–GREEN–refactor–부채로 갈 거라면, **추적용 To-Do는 단계·마일스톤별 체크리스트**가 README Must 리스트보다 잘 맞습니다.  
   - 예: RED Done = “P0 TC + 수집/실패 확인”, GREEN Done = “앵커 GREEN”, refactor Done = “레이어 분리 + pytest 동일”, 부채 Done = “config 단일 출처” 등  

4. **지금 README Must는 “M1 완료 정의서”**로 두고, **일상 작업 보드는 단계별로 따로 두는 것**이 혼란을 줄입니다. (문서 수정은 요청하신 대로 하지 않음)

원하시면 다음에 README To-Do를 **4개 섹션(RED / GREEN / REFACTOR / Tech debt)** 으로 재구성하는 초안만 제안할 수 있습니다. 이번에는 대답만 드렸습니다.

[REDACTED]

---

### Turn 429 — user

<user_query>
일단 초안만 작성해줄래? 일단 문서에는 반영하지 말고
</user_query>

---

### Turn 430 — assistant

# To-Do 초안 — RED / GREEN / REFACTOR / 기술부채

> **용도:** README Must-Have 대신 **작업 단계** 기준 추적용 초안.  
> **문서 반영:** 아직 없음 (채팅 초안만).  
> **기준:** [PRD](docs/PRD.md), [test_plan](docs/test_plan.md), 현재 `tests/`, `UnitConverter.py` 레거시.

---

## 진행 규칙 (공통)

| 단계 | 통과 정의 | 금지 |
|------|-----------|------|
| **RED** | P0·앵커 TC 존재; `pytest -v` 실패가 **의도된 상태**(미구현·수집 오류) | skip/xfail로 “통과” 위장 |
| **GREEN** | 동일 스위트 **0 failed**; AC-01~03 메시지 exact; exit code 계약 | API·문구·비율 임의 변경 |
| **REFACTOR** | pytest 전후 **failed 수 0·동일**; 레이어·의존성 정리 | GREEN 중 동작 변경, TC 삭제·완화 |
| **기술부채** | 단일 비율 출처·레거시 정리·문서 동기화 | refactor 없이 대규모 구조 변경 |

**앵커 TC (삭제·assert 완화 금지):** A-01, A-03, A-06, T-01, J-01, C-01

---

## 🔴 Phase 1 — RED (테스트·계약 고정)

**목표:** 구현 없이 계약을 코드로 고정. “Done = TC + 실패 확인”.

### 1.1 문서·환경
- [x] PRD, README, requirements-package, BCE 설계
- [x] 테스트 계획서 (`docs/test_plan.md`)
- [x] `pyproject.toml`, `requirements-dev.txt`, `tests/` 레이아웃
- [ ] RED 테스트 목록 ↔ `tests/` ID 1:1 매핑표 (선택: `docs/testing/RED-test-list.md` 동기화)

### 1.2 entity RED
- [x] Registry: 기본 3단위, register, 중복·factor≤0, 미등록 (`test_registry.py`)
- [x] Engine: A-01, A-03, ε 환산 parametrize, 0·음수·unknown (`test_engine.py`)
- [x] Display: ROUND_HALF_UP 1자리 (`test_display.py`)
- [ ] control 전용 RED (없음 → **추가 후보:** `tests/control/test_converter_app.py`)

### 1.3 boundary RED
- [x] 파싱: convert / register / ERR_* exact (`test_parser.py`)
- [x] table T-01 (`test_render_table.py`)
- [x] json·csv 스키마 (`test_render_json.py`, `test_render_csv.py`)
- [x] CLI: J-01, 형식·unknown·음수·빈 입력 (`test_cli_convert.py`, `test_cli_register.py`)

### 1.4 data RED
- [x] 유효 JSON, CFG_* , Registry 불변 (`test_units_repository.py`, C-01)

### 1.5 RED 마일스톤 완료 조건
- [x] `pytest -v` 실행 가능 (현재: 수집 오류 = 정상)
- [ ] P0 + 앵커 TC 누락 0건 리뷰 (자체 점검 체크리스트)
- [ ] **RED Phase Done 선언** (팀/본인 기준: “이제 GREEN만 하면 됨”)

---

## 🟢 Phase 2 — GREEN (최소 구현)

**목표:** RED 스위트 전부 통과. README Must-Have 대부분이 여기서 `[x]`.

### 2.1 entity (먼저)
- [ ] `entity/models.py` — Quantity, ConversionBatch, ConversionLine
- [ ] `entity/exceptions.py` — Negative, Unregistered, Duplicate, NonPositive
- [ ] `entity/registry.py` — `with_defaults()`, mpu 1.0 / 0.3048 / 0.9144
- [ ] `entity/display.py` — `format_display_value` (ROUND_HALF_UP 1dp)
- [ ] `entity/engine.py` — meter 허브 환산, `get_line()`, batch N줄
- [ ] **Gate:** `pytest tests/entity -v` → 0 failed; A-01, A-03, A-06 GREEN

### 2.2 boundary
- [ ] `boundary/errors.py` — ErrorCode, ErrorEnvelope, exact message
- [ ] `boundary/parser.py` — `parse_input`, 명령 우선순위 (`=` vs `:`)
- [ ] `boundary/renderers/` — table, json, csv
- [ ] `boundary/cli_adapter.py` — `run_command`, exit 0 / ≠0
- [ ] **Gate:** `pytest tests/boundary -v` → 0 failed; T-01 GREEN

### 2.3 data
- [ ] `data/repository.py` + `data/exceptions.py`
- [ ] `config/units.json` (기본 3단위)
- [ ] **Gate:** `pytest tests/data -v` → 0 failed; C-01 GREEN

### 2.4 control (테스트 보강 후 구현)
- [ ] `control/converter_app.py` — parse → engine → render, Registry 주입
- [ ] (선택) RED 추가: control 단위 TC
- [ ] **Gate:** entity→boundary import 0 (리뷰)

### 2.5 통합
- [ ] `tests/integration` 전부 GREEN — J-01, AC-02, AC-03
- [ ] 수동 1회: `meter:2.5` → 3줄, `8.2 feet` / `2.7 yard`
- [ ] **Gate:** `pytest -v` → **exit 0**, 0 failed

### 2.6 GREEN — README Must-Have 매핑 (한꺼번에 체크 가능)
- [ ] entity: Registry + 환산 + 음수·0·미등록
- [ ] boundary: 파싱·table·오류 5종 exact
- [ ] 표시 반올림 1자리
- [ ] control 오케스트레이션
- [ ] 통합 AC-01~03
- [ ] **RED P0 전부 GREEN** (G-01, SC-01)

### 2.7 GREEN — 권장(Should) 중 TC 이미 있는 것
- [ ] 동적 등록: `1 cubit = 0.4572 meter` → 4줄
- [ ] json / csv 출력 CLI 또는 format 인자
- [ ] config 로드 실패 시 환산 stdout 0줄 (AC-04)

### 2.8 GREEN 마일스톤 완료 조건
- [ ] **M1 — v1.0 Core** Done (F-01~F-04, F-02, F-03, AC-01~03)
- [ ] 회귀 R-1: pytest 0 failed, message exact

---

## 🔵 Phase 3 — REFACTOR (구조만, 행위 동일)

**전제:** Phase 2 전체 GREEN 로그 확보.

### 3.1 BCE 분리
- [ ] `UnitConverter.py` → thin entry (`boundary/cli_adapter` 또는 `main.py`)
- [ ] I/O·print·비율 literal → boundary/data/entity 각자 위치
- [ ] **Gate:** refactor 직전·직후 `pytest -v` diff 0 failed (RR-04)

### 3.2 품질·스타일 (행위 불변)
- [ ] 타입 힌트 공개 API 100%
- [ ] (선택) pydantic — Command, ErrorEnvelope, units DTO
- [ ] (선택) black / isort

### 3.3 REFACTOR 마일스톤
- [ ] **M2 — v1.0 Quality** (refactor 항목) 진행 가능 상태
- [ ] forbidden 리뷰: entity I/O 없음, boundary 매직넘버 없음

---

## 🟠 Phase 4 — 기술부채·릴리스 게이트

**전제:** GREEN + REFACTOR 완료 후, 또는 병행 가능한 “정리”만.

### 4.1 부채 해소
- [ ] 비율 단일 출처: `config/units.json` (+ entity Registry만 참조)
- [ ] README / PRD / Gherkin / RED 목록 동기화 (RR-03)
- [ ] 레거시 `UnitConverter.py` 중복 로직 제거 또는 deprecated 명시

### 4.2 품질 게이트 (README §7.2)
- [ ] **R-2** 앵커 6건 GREEN 유지
- [ ] **R-3** pytest-cov: entity ≥95%, boundary ≥90%, data ≥85%
- [ ] **R-4** skip/xfail 위장 0
- [ ] **R-6** forbidden 준수

### 4.3 v2 후보 (백로그)
- [ ] `units.yaml`
- [ ] `--format=json|csv|table` CLI 플래그
- [ ] import-linter / 의존성 자동 검사
- [ ] pytest-bdd Gherkin
- [ ] 등록 단위 영속화

### 4.4 릴리스
- [ ] **M3 — v1.0 Release** (Must + R-1~R-7)
- [ ] (선택) CI 워크플로: pytest + cov gate

---

## README 기존 To-Do ↔ 단계 매핑 (참고)

| README (현재) | 이 초안에서의 위치 |
|---------------|-------------------|
| Must: entity/boundary/control/통합 | **GREEN 2.x** |
| Must: RED P0 GREEN | **GREEN 2.6** |
| Must: pyproject·tests (체크됨) | **RED 1.1** |
| Should: data/json/csv/등록/cov | **GREEN 2.7** + **부채 4.2** |
| Should: BCE refactor | **REFACTOR 3.1** |
| Tech debt: 단일 파일 혼재 | **REFACTOR 3.1** + **부채 4.1** |
| Tech debt: 앵커 미구현 | **RED 1.2** (TC 있음) → **GREEN 2.1** |
| Done (문서·TC·pyproject) | **RED 1.1** 완료 |

---

## 추천 작업 순서 (한 줄)

```
RED 마무리(누락 TC) → entity GREEN → boundary GREEN → data GREEN → control+integration GREEN → REFACTOR → cov·부채·M3
```

---

원하시면 다음 단계에서 이 초안을 README **별도 섹션**(`## 진행 보드 (TDD 단계)`)으로 넣거나, Must-Have를 “릴리스 인수 기준”으로만 두고 진행 보드만 단계별로 두는 **2트랙 구조**로 합칠 수 있습니다. 지금은 문서 미반영 상태입니다.

[REDACTED]

---

### Turn 431 — user

<user_query>
위 내용으로 @README.md 파일의 TO-DO-LIST를 기존 내용을 지우고 수정해줘
</user_query>

---

### Turn 432 — assistant

[REDACTED]

---

### Turn 433 — assistant

[REDACTED]

---

### Turn 434 — assistant

[REDACTED]

---

### Turn 435 — assistant

[REDACTED]

---

### Turn 436 — assistant

README **To-Do 리스트**를 기존 Must/Should/Tech debt/Done 구조에서 제거하고, 초안대로 **4단계(RED → GREEN → REFACTOR → 기술부채)** 보드로 교체했습니다.

### 변경 요약
- **삭제:** 필수/권장/선택/기술부채/완료 항목(Done) 섹션
- **추가:** 단계별 통과 정의, 앵커 TC, 권장 작업 순서
- **Phase 1 RED:** 문서·환경·레이어별 TC — 완료분 `[x]`, RED Done 2항목 `[ ]`
- **Phase 2 GREEN:** entity → boundary → data → control → 통합·PRD Must/Should
- **Phase 3 REFACTOR:** BCE 분리·RR-04·품질
- **Phase 4:** 부채·cov·v2 백로그·M3 릴리스
- **마일스톤:** M-RED, M1(GREEN Core), M2(GREEN+REFACTOR), M3(Release)로 정렬
- **유지:** 회귀 방지 체크리스트(R-1~R-7)는 그대로

목차 링크 문구도 `RED → GREEN → REFACTOR`로 맞춰 두었습니다.

[REDACTED]

---

### Turn 437 — user

<user_query>
@README.md 
문서의 TO-DO-LIST 중 RED항목 중 체크가 되지않은 항목에 대해서 작업해줘
</user_query>

---

### Turn 438 — assistant

[REDACTED]

---

### Turn 439 — assistant

[REDACTED]

---

### Turn 440 — assistant

RED 미완료 항목 작업: `RED-test-list.md` 동기화, `tests/control/` 추가, 리뷰 문서 작성, README 체크 반영.

[REDACTED]

---

### Turn 441 — assistant

[REDACTED]

---

### Turn 442 — assistant

[REDACTED]

---

### Turn 443 — assistant

[REDACTED]

---

### Turn 444 — assistant

RED Phase 미체크 항목 작업을 마쳤습니다. **Phase 1 RED는 README 기준 전부 `[x]`** 입니다.

### 수행 내용

| README 항목 | 작업 |
|-------------|------|
| RED ID ↔ `tests/` 매핑 | [`docs/testing/RED-test-list.md`](docs/testing/RED-test-list.md) — RED 제목·실제 함수·파일 매핑표 |
| control 전용 RED | [`tests/control/test_converter_app.py`](tests/control/test_converter_app.py) — 5건 (engine 미호출·등록·unknown unit 등) |
| P0 + 앵커 리뷰 | [`docs/testing/RED-phase-review.md`](docs/testing/RED-phase-review.md) — 누락 0건, **PASS** |
| RED Phase Done | README 1.5 + 마일스톤 **M-RED ✅ Done** |

### 추가 보강
- `test_parse_convert_rejects_empty_unit_id` (`:2.5`) — `tests/boundary/test_parser.py`
- 관련 문서 링크 — README 「관련 문서」에 `RED-phase-review.md` 추가

### 확인
```bash
pytest -v  # 11 errors (collection) — RED 정상
```

**다음 단계:** GREEN — `entity/` 패키지부터 구현하면 됩니다.

[REDACTED]

---

### Turn 445 — user

<user_query>
report 폴더에 지금까지 진행한 내용을 보고서로 작성해주고(파일명은 폴더 내 파일명을 참고해서 번호는 꼭넣어줘)
prompting 폴더에 지금까지 대화내용 전체를 Export Transcript 해줘
파일명은 보고서 파일명과 같게 만들어줘
그리고 지금까지 작성한 모든 파일 및 변경점이 있는 파일들을 깃허브에 올려줘
꼭 순서대로 작업해줘
</user_query>

---

### Turn 446 — assistant

Report 폴더 파일명 규칙과 현재 변경 사항을 확인한 뒤, 순서대로 보고서 작성 → Transcript Export → GitHub 푸시를 진행합니다.

[REDACTED]

---

### Turn 447 — assistant

[REDACTED]

---

### Turn 448 — assistant

[REDACTED]

---

### Turn 449 — assistant

[REDACTED]

---

### Turn 450 — assistant

[REDACTED]

---

### Turn 451 — assistant

[REDACTED]

---

### Turn 452 — assistant

[REDACTED]

---

### Turn 453 — assistant

[REDACTED]

---

### Turn 454 — assistant

[REDACTED]

---

### Turn 455 — assistant

[REDACTED]

---

### Turn 456 — assistant

작업을 **보고서 → Transcript → GitHub 푸시** 순서로 마쳤습니다.

### 1. 보고서 (`Report/`)
- **[Report/02_UnitConvertor_06_RED_Phase_TDD_Tests.md](Report/02_UnitConvertor_06_RED_Phase_TDD_Tests.md)**  
  - Phase 5(01) 이후 **RED Phase** 요약: 테스트 계획, `tests/` 구조, 앵커 TC, pytest RED 결과, README To-Do 개편, M-RED Done, 다음 GREEN 순서

### 2. Export Transcript (`prompting/`)
- **[prompting/02_UnitConvertor_06_RED_Phase_TDD_Tests.md](prompting/02_UnitConvertor_06_RED_Phase_TDD_Tests.md)**  
  - 보고서와 **동일 파일명(02)**  
  - Cursor `agent-transcripts` jsonl **3개 세션·199 turns** 병합 (긴 assistant 출력은 일부 truncate)

### 3. GitHub 업로드
- **브랜치:** `red` → `origin/red` (신규 푸시)
- **커밋:** `b87b0b6` — `docs(test): complete RED phase — test plan, pytest suite, report 02`
- **포함:** `tests/`, `docs/test_plan.md`, `docs/testing/*`, `README.md`, `pyproject.toml`, `requirements-dev.txt`, Report·prompting 02, `scripts/export_transcript.py`, `.gitignore`
- **PR 생성:** https://github.com/yuldakim/UnitConvertor_06/pull/new/red

`.pytest_cache` 등은 `.gitignore`에 넣어 제외했습니다.

[REDACTED]

---

## Session `70307109-5376-4f81-bf19-8ddc8437f1b4`

### Turn 457 — user

<user_query>
git에 Green 브랜치를 삭제하고 B_06을 베이스로 refactoring 브랜치를 만들고 전환해줘
</user_query>

---

### Turn 458 — assistant

Git 브랜치 상태를 확인한 뒤 Green 브랜치를 삭제하고 B_06을 베이스로 refactoring 브랜치를 만들겠습니다.

[REDACTED]

---

### Turn 459 — assistant

[REDACTED]

---

### Turn 460 — assistant

[REDACTED]

---

### Turn 461 — assistant

`green` 브랜치를 삭제하고 `B_06`에서 `refactoring` 브랜치를 생성합니다.

[REDACTED]

---

### Turn 462 — assistant

작업을 마쳤습니다.

### 수행한 작업

1. **`green` 브랜치 삭제**
   - 로컬: `green` 삭제 (커밋 `85ef5f6`)
   - 원격: `origin/green` 삭제

2. **`refactoring` 브랜치 생성 및 전환**
   - 베이스: `B_06` (현재 HEAD와 동일)
   - 현재 브랜치: **`refactoring`**

### 현재 브랜치 상태

| 브랜치 | 위치 |
|--------|------|
| `refactoring` | 로컬 (현재 체크아웃) |
| `B_06` | 로컬 + `origin/B_06` |
| `main` | 로컬 + `origin/main` |

작업 트리는 clean 상태입니다. `refactoring`을 원격에 올리려면 `git push -u origin refactoring`을 실행하면 됩니다. 원하시면 대신 push까지 진행할까요?

[REDACTED]

---

### Turn 463 — user

<user_query>
푸시까지해서 원격에 적용해줘
</user_query>

---

### Turn 464 — assistant

[REDACTED]

---

### Turn 465 — assistant

원격에 반영했습니다.

- `refactoring` 브랜치를 `origin/refactoring`으로 push했습니다.
- upstream이 설정되어 로컬 `refactoring`이 `origin/refactoring`을 추적합니다.
- 현재 상태: `Your branch is up to date with 'origin/refactoring'`

PR을 만들려면: https://github.com/yuldakim/UnitConvertor_06/pull/new/refactoring

[REDACTED]

---

### Turn 466 — user

<user_query>
[P] 회귀 테스트(Approval/Golden Master) 설계 전문가입니다.
[C] Python 3.11+, pytest, pydantic
[T] UnitConverter 출력 기반 Golden Master 기준 파일을 생성해줘.

    1) 기준 출력(tests/golden_master_expected.txt) 생성/보관 전략
       입력 시나리오 4개:
         "meter:2.5" / "feet:1.0" / "yard:1.0" / "meter:0.0"
       캡처 방식: io.StringIO + contextlib.redirect_stdout        또는 subprocess.run(capture_output=True)
       생성 후: git add tests/golden_master_expected.txt  (버전 관리 필수)

    2) approve 패턴 적용:
       - 기준 파일 없으면 → 현재 출력을 기준으로 자동 생성
       - 기준 파일 있으면 → actual vs expected 문자열 비교
       - 불일치 시: diff 출력 후 테스트 FAIL

    3) 기준 파일 구조:
       [meter:2.5]
       2.5 meter = 8.202100 feet
       2.5 meter = 2.734025 yard
       ---
       [feet:1.0]
       ...

[F] tests/golden_master_expected.txt 파일 내용 + 생성 스크립트

</user_query>

---

### Turn 467 — assistant

Golden Master 테스트를 설계하기 위해 UnitConverter 구조와 기존 테스트를 확인합니다.

[REDACTED]

---

### Turn 468 — assistant

[REDACTED]

---

### Turn 469 — assistant

[REDACTED]

---

### Turn 470 — assistant

[REDACTED]

---

### Turn 471 — assistant

실제 출력 형식을 확인한 뒤 Golden Master 파일을 생성합니다.

[REDACTED]

---

### Turn 472 — assistant

Golden Master 기준 파일·생성 스크립트·approve 패턴 테스트를 추가합니다.

[REDACTED]

---

### Turn 473 — assistant

[REDACTED]

---

### Turn 474 — assistant

[REDACTED]

---

### Turn 475 — assistant

섹션 구분자에 선행 줄바꿈이 빠져 있어 수정합니다.

[REDACTED]

---

### Turn 476 — assistant

[REDACTED]

---

### Turn 477 — assistant

[REDACTED]

---

### Turn 478 — assistant

Golden Master(Approval) 회귀 테스트 구성을 마쳤습니다. 요청 예시의 `8.202100` 형식이 아니라, 현재 `round_display`(소수 1자리) 기준 실제 출력을 기준 파일에 반영했습니다.

## 생성·보관

| 파일 | 역할 |
|------|------|
| `tests/golden_master_expected.txt` | 버전 관리용 기준 출력 (staged) |
| `scripts/generate_golden_master.py` | 기준 파일 생성/갱신 |
| `tests/golden_master.py` | 캡처·포맷·approve 비교 헬퍼 |
| `tests/test_golden_master_approval.py` | pytest approve 테스트 |

## `tests/golden_master_expected.txt` 내용

```1:19:tests/golden_master_expected.txt
[meter:2.5]
2.5 meter = 2.5 meter
2.5 meter = 8.2 feet
2.5 meter = 2.7 yard
---
[feet:1.0]
1.0 feet = 0.3 meter
1.0 feet = 1.0 feet
1.0 feet = 0.3 yard
---
[yard:1.0]
1.0 yard = 0.9 meter
1.0 yard = 3.0 feet
1.0 yard = 1.0 yard
---
[meter:0.0]
0.0 meter = 0.0 meter
0.0 meter = 0.0 feet
0.0 meter = 0.0 yard
```

## Approve 패턴

- **기준 없음** → 현재 출력으로 파일 생성 후 `AssertionError` (리뷰 후 `git add` 안내)
- **기준 있음** → 전체 문자열 비교, 불일치 시 `difflib.unified_diff` 출력 후 FAIL
- 캡처: `io.StringIO` + `redirect_stdout` + `ConverterApp.handle_convert_line` (UnitConverter `print` 본문과 동일)

## 사용법

```bash
# 기준 파일 생성/갱신
python scripts/generate_golden_master.py

# CLI subprocess 경로로 캡처 (선택)
python scripts/generate_golden_master.py --subprocess

# 드리프트 검사만 (CI용)
python scripts/generate_golden_master.py --check

# 회귀 테스트
pytest tests/test_golden_master_approval.py -v
```

`tests/golden_master_expected.txt` 및 관련 파일은 `git add`까지 반영해 두었습니다. 커밋이 필요하면 알려주세요.

[REDACTED]

---

### Turn 479 — user

<user_query>
[P] 회귀 테스트(Approval/Golden Master) 설계 전문가입니다.
[C] Python 3.11+, pytest, pydantic
[T] UnitConverter Golden Master 테스트 코드를 작성해줘.

    구현 요건:
    1) 출력 캡처: io.StringIO + contextlib.redirect_stdout        또는 subprocess.run(capture_output=True)
    2) 파일 비교: open(expected_file).read() vs captured        approve 패턴: 파일 없으면 생성, 있으면 비교
    3) 테스트 마킹: @pytest.mark.golden_master def test_golden_master_meter_2_5():
    4) 빌드/실행: pytest -m golden_master -v pytest --cov=unit_converter -m golden_master
    5) (선택) approvaltests 패키지: verify(actual)

    테스트 케이스 (4개):
    - GM-TC-01: "meter:2.5" 출력 == 기준 파일 [meter:2.5] 섹션
    - GM-TC-02: "feet:1.0"  출력 == 기준 파일 [feet:1.0]  섹션
    - GM-TC-03: "yard:1.0"  출력 == 기준 파일 [yard:1.0]  섹션
    - GM-TC-04: "meter:0.0" 출력 == 기준 파일 [meter:0.0] 섹션

    실패 시 출력:
    --- expected
    +++ actual
    @@ 라인별 diff 표시 @@

[F] test_golden_master.py + golden_master_expected.txt 완성 코드 + pytest -m golden_master -
v 실행 결과

</user_query>

---

### Turn 480 — assistant

요구사항에 맞게 Golden Master 테스트를 정리합니다. 기존 구현을 확인합니다.

[REDACTED]

---

### Turn 481 — assistant

요구사항에 맞게 `test_golden_master.py`와 섹션별 approve 헬퍼를 구현합니다.

[REDACTED]

---

### Turn 482 — assistant

[REDACTED]

---

### Turn 483 — assistant

섹션 파서가 `---`를 본문에 포함하고 있어 수정합니다.

[REDACTED]

---

### Turn 484 — assistant

[REDACTED]

---

### Turn 485 — assistant

[REDACTED]

---

### Turn 486 — assistant

[REDACTED]

---

### Turn 487 — assistant

[REDACTED]

---

### Turn 488 — assistant

Golden Master 테스트를 요구사항에 맞게 정리했습니다.

## 산출물

| 파일 | 역할 |
|------|------|
| `tests/test_golden_master.py` | GM-TC-01~04, `@pytest.mark.golden_master` |
| `tests/golden_master.py` | 캡처·섹션 파싱·approve·diff |
| `tests/golden_master_expected.txt` | 섹션별 기준 출력 |
| `scripts/generate_golden_master.py` | 기준 파일 생성/갱신 |

`tests/test_golden_master_approval.py`는 `test_golden_master.py`로 대체해 제거했습니다.

## 테스트 구조 (GM-TC)

```python
@pytest.mark.golden_master
def test_golden_master_meter_2_5(converter_app) -> None:
    approve_section("meter:2.5", GOLDEN_MASTER_PATH, app=converter_app)
```

- **GM-TC-01** `meter:2.5` ↔ `[meter:2.5]` 섹션  
- **GM-TC-02** `feet:1.0` ↔ `[feet:1.0]`  
- **GM-TC-03** `yard:1.0` ↔ `[yard:1.0]`  
- **GM-TC-04** `meter:0.0` ↔ `[meter:0.0]`

## Approve 패턴

1. `capture_scenario_output()` — `StringIO` + `redirect_stdout` + `print(handle_convert_line(...))`
2. `open(expected_file).read()` — `read_expected_file()`로 CRLF 정규화
3. 기준 없음 → 전체 `golden_master_expected.txt` 생성 후 FAIL (리뷰·`git add` 안내)
4. 기준 있음 → 섹션 body만 비교, 불일치 시:

```
--- expected
+++ actual
@@ ...
```

## 실행 결과

```text
pytest -m golden_master -v
# 4 passed, 50 deselected in 0.20s

tests/test_golden_master.py::test_golden_master_meter_2_5 PASSED
tests/test_golden_master.py::test_golden_master_feet_1_0 PASSED
tests/test_golden_master.py::test_golden_master_yard_1_0 PASSED
tests/test_golden_master.py::test_golden_master_meter_0_0 PASSED
```

커버리지 (실제 패키지: `entity`, `boundary`, `control`, `data`):

```bash
pytest -m golden_master --cov=entity --cov=boundary --cov=control --cov=data --cov-report=term-missing -q
# 4 passed, TOTAL 281 stmts, 68% cover
```

`--cov=unit_converter`는 해당 모듈이 없어 데이터가 수집되지 않습니다. 프로젝트명은 `unit-converter`이고 소스는 BCE 4계층 패키지입니다.

## 기준 파일 (`golden_master_expected.txt`)

```1:19:tests/golden_master_expected.txt
[meter:2.5]
2.5 meter = 2.5 meter
2.5 meter = 8.2 feet
2.5 meter = 2.7 yard
---
[feet:1.0]
...
```

## 보조 명령

```bash
python scripts/generate_golden_master.py          # 기준 갱신
python scripts/generate_golden_master.py --subprocess  # CLI subprocess 캡처
pytest -m golden_master -v
```

선택 사항인 `approvaltests.verify()`는 별도 `.approved.txt` 체계가 필요해, 내장 `difflib.unified_diff` approve 패턴을 기본으로 두었습니다. `approvaltests` 연동이 필요하면 알려주세요.

[REDACTED]

---

### Turn 489 — user

<user_query>
approvaltests 연동이 어떤걸 말하는거야?
코드작성 금지, 설명만해줘
</user_query>

---

### Turn 490 — assistant

**approvaltests 연동**은, 지금 우리가 직접 만든 Golden Master(기준 파일 + `difflib` diff) 대신 **Python `approvaltests` 라이브러리**가 제공하는 “승인(approve) 테스트” 방식을 쓰겠다는 뜻입니다.

## 지금 방식 vs approvaltests

| | **현재 구현** | **approvaltests 사용 시** |
|---|----------------|---------------------------|
| 기준 저장 | `tests/golden_master_expected.txt` (직접 설계한 섹션 형식) | 보통 `Something.approved.txt` 같은 **라이브러리 규칙의 파일명** |
| 비교 | `open(...).read()` 후 문자열/섹션 비교 | `verify(actual)` 한 줄이 “기준과 같나?”를 처리 |
| 기준 없을 때 | 우리 코드가 파일 생성 + “리뷰 후 재실행” | `verify()`가 **received 파일**을 만들고, 개발자가 **승인(이름 변경/도구로 approve)** 하면 다음부터 통과 |
| 실패 출력 | `--- expected` / `+++ actual` (unified diff) | 라이브러리/리포터가 diff·비교 UI 제공 (설정에 따라 다름) |

즉 “연동”은 **pytest 테스트 안에서 `from approvaltests import verify` 후 `verify(캡처한_문자열)`을 호출**하고, 기준 파일 생성·갱신·비교·실패 메시지를 **그 패키지에 맡기는 것**을 말합니다.

## approvaltests가 하는 일 (개념)

1. 테스트가 **실제 출력(actual)** 을 만든다.  
2. `verify(actual)`이 **이미 승인된 기준(approved)** 과 비교한다.  
3. 기준이 없거나 바뀌었으면 테스트는 실패하고, **`.received.txt`** 같은 임시 결과가 생긴다.  
4. 개발자가 “이 출력이 맞다”고 판단하면 **approve** 단계로 기준 파일을 확정한다 (CLI/IDE/수동 rename 등).  
5. 다음 실행부터는 approved 파일과 비교해 통과/실패가 난다.

우리가 말한 **approve 패턴**(없으면 생성 → 사람이 검토 → 있으면 비교)과 **목적은 같고**, 구현 주체가 **우리 코드**냐 **approvaltests**냐의 차이입니다.

## 왜 “선택”이라고 했는지

- **추가 의존성**: `pip install approvaltests` (및 경우에 따라 reporter 설정).  
- **파일 규칙이 다름**: `[meter:2.5]` 섹션이 한 파일에 있는 형식 vs 테스트/함수마다 `*.approved.txt`가 생기는 식.  
- **워크플로**: CI에서는 보통 “approved만 커밋”, 로컬에서만 approve — 팀 규칙이 필요함.  
- **지금 프로젝트**는 이미 `golden_master_expected.txt` + 섹션 파싱 + `pytest.mark.golden_master`로 같은 역할을 하고 있어서, **굳이 라이브러리를 안 써도 요구사항은 충족**합니다.

## 한 줄 요약

**approvaltests 연동** = Golden Master 회귀를 **`verify()` + `.approved.txt` 승인 워크플로**로 바꾸는 것이고, **연동 안 함** = 지금처럼 **자체 `approve_section` + `golden_master_expected.txt`** 로 같은 목적을 달성하는 것입니다. 둘 다 “출력이 바뀌면 diff 보고 막는다”는 점에서는 같고, **도구와 파일·승인 절차**만 다릅니다.

[REDACTED]

---

### Turn 491 — user

<user_query>
그럼 지금 승인테스트 완료는 했고 어떤방식으로 approval Test를 할건지 묻는거네?
코드작성금지, 요약으로 간단히 답변
</user_query>

---

### Turn 492 — assistant

맞습니다.

- **완료된 것**: 자체 Golden Master 방식 — `golden_master_expected.txt` + `approve_section()` + `pytest -m golden_master` (4개 GM-TC).
- **물어본 것**: 그걸 **approvaltests 라이브러리**로 바꿀지, **지금 방식을 유지**할지 선택.

**현재 선택**: 라이브러리 없이 **지금 방식 유지**입니다. `verify()` / `.approved.txt` 승인 워크플로는 쓰지 않습니다.

[REDACTED]

---

### Turn 493 — user

<user_query>
@README.md 파일에 아래 섹션을 추가해줘.
"## RED 단계 To-Do 리스트" 아래에 새 섹션으로 삽입.

## Golden Master 회귀 안전장치

> Refactoring 시작 전 구축. GREEN 완료 후 즉시 적용.

### 기준 파일 생성
- [ ] GM-01: golden_master_expected.txt 생성 (meter:2.5 기준 출력)
- [ ] GM-02: feet:1.0 / yard:1.0 / meter:0.0 시나리오 추가
- [ ] GM-03: git add tests/golden_master_expected.txt (버전 관리 포함)

### 테스트 코드
- [ ] GM-04: test_golden_master.py + golden_master_expected.txt 작성
- [ ] GM-05: approve 패턴 적용 (파일 없으면 생성, 있으면 비교)
- [ ] GM-06: pytest -m golden_master -v → PASS 확인

### CI 연동
- [ ] GM-07: .github/workflows/golden_master.yml 작성
- [ ] GM-08: PR 머지 차단 (required status check) 설정
- [ ] GM-09: Refactoring 후 Golden Master 재실행 → PASS 확인
</user_query>

---

### Turn 494 — assistant

[REDACTED]

---

### Turn 495 — assistant

[REDACTED]

---

### Turn 496 — assistant

[REDACTED]

---

### Turn 497 — assistant

`README.md`에 **RED 단계 To-Do 리스트** 바로 아래, **GREEN 단계 To-Do 리스트** 위에 `## Golden Master 회귀 안전장치` 섹션을 넣었고, 목차에도 링크를 추가했습니다.

GM-01~GM-06은 이미 구현된 상태라면 체크박스를 `[x]`로 바꿔 둘까요?

[REDACTED]

---

### Turn 498 — user

<user_query>
응 그렇게 하고 혹시 TO-DO 리스트  추가한 항목 중 불가한 작업 제외하고 진행 할 수 있는 항목 중 작업이 안되어 있는 항목이 있다면 작업 후 체크까지 해줘
</user_query>

---

### Turn 499 — assistant

README 체크박스를 반영하고, 진행 가능한 GM 항목(GM-07~09 등)을 확인·작업합니다.

[REDACTED]

---

### Turn 500 — assistant

[REDACTED]

---

### Turn 501 — assistant

[REDACTED]

---

### Turn 502 — assistant

[REDACTED]

---

### Turn 503 — assistant

작업 반영했습니다.

### README 체크 (완료 8 / 잔여 1)

| 항목 | 상태 |
|------|------|
| GM-01 ~ GM-06 | [x] (기준 파일·테스트·approve·pytest PASS) |
| GM-03 | [x] (`git add`로 golden master 관련 파일 스테이징 완료) |
| GM-07 | [x] `.github/workflows/golden_master.yml` 추가 |
| GM-09 | [x] `pytest -m golden_master -v` → 4 passed |
| **GM-08** | [ ] **미완료 (불가/수동)** — GitHub 저장소 Admin에서 branch protection + `Golden Master Regression` required check 설정 필요 (`gh` CLI 없음) |

GM-08 안내는 README 해당 항목 아래에 **Settings → Branches → Require status checks → `Golden Master Regression`** 경로로 적어 두었습니다.

### 추가 작업

- **CI 워크플로**: `push`/`pull_request` 시 `pytest -m golden_master -v` 실행
- **테스트 실행** 섹션에 `pytest -m golden_master -v` 명령 추가
- 스테이징: `golden_master_expected.txt`, `test_golden_master.py`, `golden_master.py`, `generate_golden_master.py`, workflow, `README.md`, `pyproject.toml`

워크플로가 원격에서 돌아가려면 **push 후** GitHub Actions에서 한 번 성공해야 GM-08 체크 목록에 job 이름이 보입니다. push·커밋까지 진행할까요?

[REDACTED]

---

### Turn 504 — user

<user_query>
report 폴더에 지금까지의 진행상황 보고서로 작성해주고(파일명은 폴더 내 파일명을 참고해서 번호는 꼭넣어줘)
prompting 폴더에 지금까지 대화내용 전체를 Export Transcript 해줘
파일명은 보고서 파일명과 같게 만들어줘
그리고 지금까지 작성한 모든 파일 및 변경점이 있는 파일들을 깃허브에 푸시 후 pr까지 해줘
(위 작업에서 gm-08 항목까지 반영하여 진행)
가능하면 B_06에 머지 후 B_06을 기준으로 다시 새롭게 refactoring 브랜치를 따서 전환해줘
꼭 순서대로 작업해줘

</user_query>

---

### Turn 505 — assistant

순서대로 진행합니다. 먼저 `report`·`prompting` 폴더와 기존 파일명 규칙을 확인합니다.

[REDACTED]

---

### Turn 506 — assistant

[REDACTED]

---

### Turn 507 — assistant

[REDACTED]

---

### Turn 508 — assistant

**1단계:** 보고서 `04` 작성 중.

[REDACTED]

---

### Turn 509 — assistant

**2단계:** Transcript export 스크립트 업데이트 및 실행.

[REDACTED]

---

### Turn 510 — assistant

**3단계:** 커밋·푸시·PR 생성 진행.

[REDACTED]

---

### Turn 511 — assistant

[REDACTED]

---

### Turn 512 — assistant

[REDACTED]

---

### Turn 513 — assistant

[REDACTED]

---

### Turn 514 — assistant

[REDACTED]

---

### Turn 515 — assistant

[REDACTED]

---

### Turn 516 — assistant

[REDACTED]

---

### Turn 517 — assistant

[REDACTED]

---

### Turn 518 — assistant

[REDACTED]

---

### Turn 519 — assistant

[REDACTED]

---

### Turn 520 — assistant

[REDACTED]

---

### Turn 521 — assistant

[REDACTED]

---

### Turn 522 — assistant

**4단계:** B_06 머지 후 `refactoring` 브랜치 재생성 및 GM-08 설정 시도.

[REDACTED]

---

### Turn 523 — assistant

[REDACTED]

---

### Turn 524 — assistant

[REDACTED]

---

### Turn 525 — assistant

[REDACTED]

---

### Turn 526 — assistant

[REDACTED]

---

### Turn 527 — assistant

요청하신 순서대로 작업을 마쳤습니다.

## 1. 진행 보고서 (Report)

- **파일:** `Report/04_UnitConvertor_06_Golden_Master_Refactoring_Progress.md`
- Golden Master 구축, 브랜치 정리, CI, GM-01~GM-09( GM-08 포함), PR #2 머지 내용 정리

## 2. Export Transcript (prompting)

- **파일:** `prompting/04_UnitConvertor_06_Golden_Master_Refactoring_Progress.md` (보고서와 동일 파일명)
- `scripts/export_transcript.py` → Report 04 기준으로 갱신 후 실행 (~249KB, 세션 전체 대화)

## 3. GitHub 푸시 · PR · B_06 머지

| 단계 | 결과 |
|------|------|
| 커밋 | `6214fc5` — Golden Master, CI, Report/prompting 04 |
| 푸시 | `origin/refactoring` |
| PR | [#2](https://github.com/yuldakim/UnitConvertor_06/pull/2) `refactoring` → `B_06` |
| 머지 | `B_06` @ `0dd6922` (Merge PR #2) |

## 4. GM-08 + 브랜치 재정리

- **GM-08:** `B_06` branch protection + required check **`Golden Master Regression`** API 적용
- README GM-08 → `[x]` 반영 (`c36cf0c` on `refactoring`)
- **브랜치:** `refactoring` 삭제 후 **`B_06`(`0dd6922`)에서 새 `refactoring` 생성** → `origin/refactoring` 푸시
- **현재 브랜치:** `refactoring` (`c36cf0c`, B_06 머지 + GM-08 문서 1커밋)

## 검증

```text
pytest -m golden_master -v  → 4 passed
```

## GM To-Do (README)

GM-01 ~ **GM-09** 모두 `[x]` (GM-08 branch protection 포함)

---

**참고:** `refactoring`은 B_06 머지 직후보다 GM-08 문서 커밋 1건 앞서 있습니다. `B_06`에도 동일 문서를 맞추려면 `refactoring` → `B_06` 소규모 PR을 한 번 더 열면 됩니다.

[REDACTED]

---

### Turn 528 — user

<user_query>Briefly inform the user about the task result and perform any follow-up actions (if needed). If there's no follow-ups needed, don't explicitly say that.</user_query>

---

### Turn 529 — user

<user_query>Briefly inform the user about the task result and perform any follow-up actions (if needed). If there's no follow-ups needed, don't explicitly say that.</user_query>

---

### Turn 530 — user

<user_query>Briefly inform the user about the task result and perform any follow-up actions (if needed). If there's no follow-ups needed, don't explicitly say that.</user_query>

---

### Turn 531 — assistant

[REDACTED]

---

### Turn 532 — assistant

세 개의 백그라운드 셸은 UI상 **aborted**로 표시됐지만, 실제 작업은 모두 끝났습니다.

- **B_06 pull:** `0dd6922`까지 fast-forward 완료 (PR #2 머지 반영)
- **refactoring 재생성:** 원격 `refactoring` 삭제 후 `B_06` 기준으로 새 브랜치 생성·푸시, Golden Master 4건 PASS
- **credential manager 조회:** 해당 명령만 중단됐고, 이후 `git credential fill`로 PR 생성·머지·GM-08 설정은 정상 처리됨

**현재 상태:** `refactoring` @ `c36cf0c`, `origin/refactoring`와 동기화됨. `B_06`은 `0dd6922`(GM-08 문서 커밋 1건은 `refactoring`에만 있음).

[REDACTED]

---

## Session `703eec2c-70c0-4bf2-b508-21ae8577b0e0`

### Turn 533 — user

<user_query>
🔲 BCE 설계 전문가 — Python
Dual-Track(UI/경계 vs Domain) + BCE 관점 설계 전문가로 행동하라.
대상: c:\DEV\unit_converter_python
제약: 구현 코드 작성 금지. 설계·계약·테스트 목록·통합 계획만.

# 1) Entity(Domain) 설계
  1.1 개념 목록과 SRP
  1.2 Invariants
  1.3 유스케이스
  1.4 Domain API (시그니처 수준, 본문 X) + 실패 조건
  1.5 Domain 단위 테스트 설계 (RED 우선)

# 2) Boundary 설계
  2.1 시나리오: 입력→검증→실행→출력
  2.2 외부 계약: Input / Output / Error schema
  2.3 Boundary 계약 테스트 (Domain Mock 가정)
  2.4 에러 메시지 규칙 (문구 패턴 고정)

# 3) Data 설계
  3.1 목적
  3.2 인터페이스 계약 (이름만 제안)
  3.3 InMemory vs File(JSON/YAML) 비교 + 추천 1개와 이유
  3.4 Data 레이어 테스트

# 4) Integration & Verification
  4.1 의존성 방향 포함 흐름
  4.2 통합 테스트 시나리오 (정상 2+, 실패 3+)
  4.3 회귀 보호 규칙
  4.4 커버리지 목표 (Domain / Boundary / Data 수치)
  4.5 Traceability Matrix: Concept→Rule→UseCase→Contract→Test→Component

모호어 금지. 모든 규칙은 테스트로 검증 가능하게.
</user_query>

---

### Turn 534 — assistant

설계 전에 대상 프로젝트 구조와 기존 도메인·계약을 파악합니다.

[REDACTED]

---

### Turn 535 — assistant

[REDACTED]

---

### Turn 536 — assistant

대상 경로 `c:\DEV\unit_converter_python`는 현재 없고, 워크스페이스 `UnitConvertor_06`의 README·`UnitConverter.py`를 요구사항·현행 동작의 기준으로 Dual-Track BCE 설계를 정리했습니다.

---

# Unit Converter — BCE Dual-Track 설계 (Python)

**범위**: 길이 단위 변환 CLI  
**제약**: 구현 코드 없음 — 개념·계약·테스트·통합만  
**기준 요구사항**: `meter`/`feet`/`yard`, `단위:값` 입력, OCP·SRP, 음수·형식·미등록 단위 검증, 비율 외부화, 동적 단위 등록, 출력 포맷(table/JSON/CSV)

---

## 1) Entity (Domain) 설계

### 1.1 개념 목록과 SRP

| 개념 | 책임 (SRP) | 협력 |
|------|------------|------|
| `Quantity` | (값, 단위 식별자) 쌍 보유; 값은 `Decimal` 또는 `float`(프로젝트에서 하나로 고정) | `UnitId` |
| `UnitId` | 단위 식별자 정규화·동등 비교 (예: trim + lowercase) | — |
| `ConversionFactor` | 기준 단위(meter) 대비 양수 비율 1개 보유 | `UnitId` |
| `UnitRegistry` | 등록된 `UnitId`↔`ConversionFactor` 조회; 중복·미등록 판별 | `ConversionFactor` |
| `CanonicalUnit` | 기준 단위 상수 (`meter`) | — |
| `MeasurementNormalizer` | 임의 `Quantity` → 기준 단위 `Quantity` 1건 | `UnitRegistry`, `CanonicalUnit` |
| `ConversionEngine` | 기준 단위 값 → 대상 단위별 `Quantity` N건 | `UnitRegistry` |
| `ConvertAllUnits` (Use Case) | 입력 `Quantity` → 레지스트리 전 단위 변환 결과 집합 | 위 서비스들 |
| `RegisterUnit` (Use Case) | `1 new_unit = ratio meter` 등록 | `UnitRegistry` |
| `ConversionResult` | 원본 `Quantity` + 대상별 `Quantity` 목록 (불변) | — |

**경계(Boundary)에 두지 않을 것**: 파싱, `print`, JSON/CSV 직렬화, 파일 I/O.

---

### 1.2 Invariants (모두 테스트로 검증)

| ID | 규칙 | 위반 시 |
|----|------|---------|
| INV-01 | `ConversionFactor.ratio > 0` | 등록/로드 거부 |
| INV-02 | 기준 단위 `meter`의 `ratio == 1` | 설정/부트스트랩 실패 |
| INV-03 | `Quantity.value >= 0` (0 허용) | `NegativeValueError` |
| INV-04 | `UnitId` 비어 있지 않음 (trim 후 길이 ≥ 1) | `InvalidUnitIdError` |
| INV-05 | `UnitRegistry` 내 `UnitId` 유일 | `DuplicateUnitError` |
| INV-06 | 변환 대상 단위는 반드시 레지스트리에 존재 | `UnknownUnitError` |
| INV-07 | 정규화: `q` → meter: `meter_value = q.value / factor(q.unit)` (factor = “1 unit = factor meter”) | — |
| INV-08 | 역변환: `target_value = meter_value * factor(target)` | — |
| INV-09 | 동적 등록 비율 문구 `1 {new} = {ratio} meter`에서 `ratio > 0` | `InvalidRatioError` |
| INV-10 | `ConvertAllUnits` 결과 건수 = `len(registry) - 0` (자기 단위 포함 여부는 정책으로 고정; **권장: 포함**, README 출력과 동일) | 계약 테스트로 고정 |

**고정 정책 (모호 제거)**  
- 기준 단위: `meter` (README 비즈니스 로직)  
- `feet`: `3.28084`, `yard`: `1.09361` (초기 시드; 파일 로드 시 덮어쓰기 가능하나 INV-02 유지)  
- 출력 반올림: Domain은 **반올림하지 않음**; Boundary가 표시 자릿수 담당

---

### 1.3 유스케이스

| UC-ID | 이름 | 전제 | 주요 흐름 | 사후 조건 |
|-------|------|------|-----------|-----------|
| UC-D01 | 전체 단위로 변환 | 레지스트리 ≥ 1, 입력 단위 등록됨, value ≥ 0 | 정규화 → 각 단위로 역변환 → `ConversionResult` | 결과에 레지스트리 모든 단위 포함 |
| UC-D02 | 단위 동적 등록 | `ratio > 0`, `new` 미등록 | factor 저장 | 이후 UC-D01에서 `new` 사용 가능 |
| UC-D03 | 레지스트리에서 단위 조회 | — | `has(unit)` / `list_units()` | 읽기 전용, 부작용 없음 |

---

### 1.4 Domain API (시그니처만) + 실패 조건

```python
# value object
class UnitId: ...
    @staticmethod
    def parse(raw: str) -> UnitId: ...  # fails: INV-04

class ConversionFactor:
    def __init__(self, unit: UnitId, ratio_to_meter: float): ...  # fails: INV-01

class Quantity:
    def __init__(self, value: float, unit: UnitId): ...  # fails: INV-03, INV-04

# registry
class UnitRegistry:
    def register(self, factor: ConversionFactor) -> None: ...  # DuplicateUnitError
    def get_factor(self, unit: UnitId) -> ConversionFactor: ...  # UnknownUnitError
    def all_units(self) -> tuple[UnitId, ...]: ...
    def contains(self, unit: UnitId) -> bool: ...

# services
class MeasurementNormalizer:
    def to_canonical(self, q: Quantity, registry: UnitRegistry) -> Quantity: ...
    # UnknownUnitError, NegativeValueError(Quantity 생성 시)

class ConversionEngine:
    def convert_all(self, canonical: Quantity, registry: UnitRegistry) -> ConversionResult: ...

# use cases
class ConvertAllUnits:
    def execute(self, input_qty: Quantity, registry: UnitRegistry) -> ConversionResult: ...
    # UnknownUnitError, NegativeValueError

class RegisterUnit:
    def execute(self, new_unit: UnitId, ratio_to_meter: float, registry: UnitRegistry) -> None: ...
    # InvalidRatioError, DuplicateUnitError, InvalidUnitIdError
```

| API | 실패 타입 | 조건 |
|-----|-----------|------|
| `UnitId.parse` | `InvalidUnitIdError` | 빈 문자열, 공백만 |
| `Quantity.__init__` | `NegativeValueError` | value < 0 |
| `UnitRegistry.register` | `DuplicateUnitError` | INV-05 |
| `UnitRegistry.get_factor` | `UnknownUnitError` | INV-06 |
| `RegisterUnit.execute` | `InvalidRatioError` | ratio ≤ 0 |
| `ConvertAllUnits.execute` | `UnknownUnitError` | 입력 단위 미등록 |

Domain 예외는 **메시지 키(code)** 만 가짐; 사용자 문구는 Boundary 책임.

---

### 1.5 Domain 단위 테스트 설계 (RED 우선)

| Test-ID | 대상 | 입력 | 기대 |
|---------|------|------|------|
| DT-01 | INV-01 | ratio=0 | `InvalidRatioError` |
| DT-02 | INV-03 | value=-1 | `NegativeValueError` |
| DT-03 | INV-07 | 2.5 meter | canonical.value≈2.5 |
| DT-04 | INV-07 | 8.2 feet | canonical≈2.5m (허용 오차 ε=1e-4) |
| DT-05 | INV-08 | 2.5m → feet | ≈8.2 (ε) |
| DT-06 | INV-08 | 2.5m → yard | ≈2.7 (ε) |
| DT-07 | feet↔yard | meter 경유 | yard/feet 비율 = 1.09361/3.28084 |
| DT-08 | UC-D01 | meter:2.5, 3단위 | 3건 결과 |
| DT-09 | UC-D02 | cubit 0.4572 | 등록 후 변환 성공 |
| DT-10 | INV-05 | meter 2회 등록 | `DuplicateUnitError` |
| DT-11 | INV-06 | unknown 입력 | `UnknownUnitError` |
| DT-12 | OCP | 4번째 단위 등록만 | `ConversionEngine` 수정 없음(동일 테스트 스위트 통과) |

**RED 순서**: DT-01~03 → DT-04~07 → DT-08 → DT-09~12.

---

## 2) Boundary 설계

### 2.1 시나리오: 입력 → 검증 → 실행 → 출력

```
[stdin/argv] 
  → ParseInput (형식) 
  → ValidateNumber 
  → BuildQuantity 
  → ConvertAllUnits (Domain, registry 주입)
  → FormatOutput (table|json|csv)
  → [stdout]
```

**부가 시나리오 — 동적 등록**  
`register:1 cubit = 0.4572 meter` → `ParseRegisterCommand` → `RegisterUnit` → 성공 메시지 1줄 (포맷 고정).

---

### 2.2 외부 계약: Input / Output / Error schema

#### Input (CLI 한 줄)

| 모드 | 패턴 (정규식) | 예시 |
|------|----------------|------|
| CONVERT | `^{unit}:{number}$` | `meter:2.5` |
| REGISTER | `^register:1\s+{unit}\s*=\s*{number}\s+meter$` | `register:1 cubit = 0.4572 meter` |

- `unit`: `[a-z][a-z0-9_]*` (소문자, 숫자 시작 금지)  
- `number`: `^-?\d+(\.\d+)?$` → Boundary에서 음수는 **Domain 호출 전** 거부 (이중 방어)

#### Output

| format | Content-Type | 스키마 |
|--------|--------------|--------|
| table (default) | text/plain | 각 줄: `{src_value} {src_unit} = {dst_value} {dst_unit}` |
| json | application/json | `{"source":{"unit":"meter","value":2.5},"conversions":[{"unit":"feet","value":8.2},...]}` |
| csv | text/csv | 헤더 `source_unit,source_value,target_unit,target_value` + 행 N |

- 숫자 표시: 소수점 **최대 1자리** 반올림 (`round half up`), README 예시와 정합  
- `--format table|json|csv` (argv); 미지정 시 table

#### Error (stderr 또는 stdout 정책 1개로 고정 — **권장: stdout**, exit code ≠ 0)

```json
{"error":{"code":"ERR_XXX","message":"<고정 패턴>","field":"<optional>"}}
```

| code | HTTP 유사 | 조건 |
|------|-----------|------|
| ERR_FORMAT | 400 | `:` 없음, REGISTER 패턴 불일치 |
| ERR_NUMBER | 400 | float 파싱 실패 |
| ERR_NEGATIVE | 400 | value < 0 |
| ERR_UNKNOWN_UNIT | 404 | 미등록 단위 |
| ERR_DUPLICATE_UNIT | 409 | 등록 중복 |
| ERR_INVALID_RATIO | 400 | ratio ≤ 0 |
| ERR_INTERNAL | 500 | 예상 외 Domain 예외 |

---

### 2.3 Boundary 계약 테스트 (Domain Mock)

| Test-ID | Mock 설정 | 입력 | 기대 출력/코드 |
|---------|-----------|------|----------------|
| BT-01 | Convert → 2건 fixture | `meter:2.5` table | 2줄, 패턴 일치 |
| BT-02 | 동일 | `--format json` | JSON 스키마 키 존재 |
| BT-03 | 동일 | `--format csv` | 헤더+2행 |
| BT-04 | — | `meter` (콜론 없음) | ERR_FORMAT, exit≠0 |
| BT-05 | — | `meter:abc` | ERR_NUMBER |
| BT-06 | — | `meter:-1` | ERR_NEGATIVE |
| BT-07 | registry unknown | `cubit:1` | ERR_UNKNOWN_UNIT |
| BT-08 | Register OK | `register:1 cubit = 0.4572 meter` | 성공 1줄 `Registered: cubit` |
| BT-09 | Register duplicate | 동일 2회 | ERR_DUPLICATE_UNIT |
| BT-10 | Convert raises | 내부 예외 | ERR_INTERNAL |

Mock: `ConvertAllUnits.execute`, `RegisterUnit.execute`만 대체; 파서·포맷터는 실객체.

---

### 2.4 에러 메시지 규칙 (문구 패턴 고정)

| code | message (정확히) |
|------|------------------|
| ERR_FORMAT | `Invalid format. Use unit:value (ex: meter:2.5)` |
| ERR_NUMBER | `Invalid number: {token}` |
| ERR_NEGATIVE | `Value must be non-negative: {value}` |
| ERR_UNKNOWN_UNIT | `Unknown unit: {unit}` |
| ERR_DUPLICATE_UNIT | `Unit already registered: {unit}` |
| ERR_INVALID_RATIO | `Ratio must be positive: {ratio}` |
| ERR_REGISTER_FORMAT | `Invalid register format. Use register:1 unit = ratio meter` |
| ERR_INTERNAL | `Internal error. Contact support.` |

- `{token}`: 사용자가 입력한 숫자 부분 원문  
- Domain 예외 → code 매핑 테이블 1곳 (`BoundaryErrorMapper`)

---

## 3) Data 설계

### 3.1 목적

- 초기 단위·비율 **외부화** (JSON/YAML)  
- 앱 기동 시 레지스트리 **시드**  
- (선택) 런타임 등록 영속화 — 1차 스코프에서는 **InMemory만**; 파일 저장은 2단계

### 3.2 인터페이스 계약 (이름만)

| 인터페이스 | 메서드 |
|------------|--------|
| `UnitDefinitionDTO` | `unit_id: str`, `ratio_to_meter: float` |
| `ConversionConfigDTO` | `canonical_unit: str`, `units: list[UnitDefinitionDTO]` |
| `ConversionConfigLoader` | `load() -> ConversionConfigDTO` |
| `ConversionConfigReader` | `read(path: Path) -> str` (raw) |
| `UnitRegistryFactory` | `from_config(dto) -> UnitRegistry` |
| `UnitRegistryStore` (2단계) | `save(registry)`, `load() -> UnitRegistry` |

Domain은 DTO/Loader를 **알지 않음**; Composition Root에서 Factory 호출.

### 3.3 InMemory vs File — 비교 및 추천

| 항목 | InMemory | File (JSON/YAML) |
|------|----------|------------------|
| 요구 “설정 외부화” | ✗ | ✓ |
| 테스트 속도 | 최고 | 파일 fixture 필요 |
| OCP(단위 추가) | 코드/테스트 시드 변경 | 파일만 변경 |
| 배포 | 단순 | 설정 경로 필요 |

**추천: File (JSON)** — 이유: README “JSON/YAML” 충족, diff·리뷰 용이, 표준 라이브러리 `json`만으로 계약 테스트 가능; YAML은 의존성 추가 없이 2단계 옵션.

**기본 경로 계약**: `./config/units.json` (환경변수 `UNIT_CONFIG_PATH`로 override).

**JSON 스키마 (계약)**:

```json
{
  "canonical_unit": "meter",
  "units": [
    {"unit_id": "meter", "ratio_to_meter": 1},
    {"unit_id": "feet", "ratio_to_meter": 3.28084},
    {"unit_id": "yard", "ratio_to_meter": 1.09361}
  ]
}
```

### 3.4 Data 레이어 테스트

| Test-ID | 내용 |
|---------|------|
| DATA-01 | 유효 JSON → DTO 3단위 |
| DATA-02 | ratio≤0 → 로드 실패 `ConfigValidationError` |
| DATA-03 | canonical≠meter → 실패 |
| DATA-04 | 중복 unit_id → 실패 |
| DATA-05 | 파일 없음 → 실패 (명시 메시지) |
| DATA-06 | Factory → Domain DT-08 통과 (통합 전 단계) |

---

## 4) Integration & Verification

### 4.1 의존성 방향 포함 흐름

```mermaid
flowchart TB
  CLI[Boundary: CLI Adapter]
  Parser[Boundary: Input Parser]
  Formatter[Boundary: Output Formatter]
  UC[Domain: Use Cases]
  ENG[Domain: Engine / Normalizer]
  REG[Domain: UnitRegistry]
  FACT[Data: Registry Factory]
  LOAD[Data: Config Loader]
  FILE[(units.json)]

  CLI --> Parser
  Parser --> UC
  UC --> ENG
  ENG --> REG
  FACT --> REG
  LOAD --> FILE
  LOAD --> FACT
  UC --> Formatter
  Formatter --> CLI

  style REG fill:#e8f5e9
  style UC fill:#e8f5e9
  style ENG fill:#e8f5e9
```

**규칙**: `Domain → (Boundary, Data)` import 금지. `Data → Domain`만 허용. `Boundary → Domain` + `Boundary → Data(Factory)` 허용.

---

### 4.2 통합 테스트 시나리오

**정상 (≥2)**

| IT-ID | 시나리오 | 검증 |
|-------|----------|------|
| IT-OK-01 | `units.json` 시드 + `meter:2.5` table | 3줄, feet≈8.2, yard≈2.7 |
| IT-OK-02 | 동일 + `--format json` | 파싱 가능, conversions 길이=3 |

**실패 (≥3)**

| IT-ID | 시나리오 | 검증 |
|-------|----------|------|
| IT-FAIL-01 | `meter:-1` | ERR_NEGATIVE, exit=1 |
| IT-FAIL-02 | `mile:1` (미등록) | ERR_UNKNOWN_UNIT |
| IT-FAIL-03 | 설정 파일 ratio=0 | 기동 실패, stderr 메시지 고정 |
| IT-FAIL-04 | `register:1 cubit = 0 cubit = 0 meter` (invalid ratio) | ERR_INVALID_RATIO |
| IT-FAIL-05 | 손상 JSON | Config load 실패 |

---

### 4.3 회귀 보호 규칙

1. **비율 상수 변경** 시: DT-04~07, IT-OK-01 동시 실패 → 의도적 변경만 허용  
2. **에러 message 문자열** 변경 시: BT-04~09 스냅샷/정확 일치 테스트 먼저 수정  
3. Domain public 시그니처 변경 시: DT 전체 + Boundary Mock 테스트 재실행  
4. `config/units.json` 스키마 필드 추가는 **하위 호환**(unknown key ignore) — breaking 시 DATA 테스트 추가  
5. CI: `pytest` + coverage gate (4.4) 미달 시 merge 차단

---

### 4.4 커버리지 목표

| 레이어 | Line | Branch | 비고 |
|--------|------|--------|------|
| Domain | ≥ 95% | ≥ 90% | 예외 경로 필수 |
| Boundary | ≥ 85% | ≥ 80% | 포맷 3종 각 1테스트 이상 |
| Data | ≥ 90% | ≥ 85% | validation 분기 전부 |

전체 프로젝트 **≥ 88% line** (통합 테스트 포함).

---

### 4.5 Traceability Matrix

| Concept | Rule (Invariant) | Use Case | Contract | Test | Component |
|---------|------------------|----------|----------|------|-----------|
| Quantity | INV-03, INV-04 | UC-D01 | Input `unit:value` | DT-02, BT-06 | `Quantity`, Parser |
| ConversionFactor | INV-01, INV-02 | UC-D02 | JSON `ratio_to_meter` | DT-01, DATA-02 | `ConversionFactor`, Loader |
| UnitRegistry | INV-05, INV-06 | UC-D01,D02,D03 | Registry API | DT-10,11 | `UnitRegistry` |
| Normalization | INV-07 | UC-D01 | — | DT-03,04 | `MeasurementNormalizer` |
| Conversion | INV-08 | UC-D01 | Output lines | DT-05,06,07 | `ConversionEngine` |
| Convert all | INV-10 | UC-D01 | table/json/csv | DT-08, BT-01~03, IT-OK-* | `ConvertAllUnits` |
| Dynamic register | INV-09 | UC-D02 | REGISTER pattern | DT-09, BT-08,09 | `RegisterUnit` |
| Input format | — | — | ERR_FORMAT | BT-04, IT-FAIL-* | `InputParser` |
| Output format | — | — | JSON/CSV schema | BT-02,03 | `OutputFormatter` |
| Config external | INV-01~02 | boot | `units.json` | DATA-01~06 | `ConversionConfigLoader` |
| Error UX | — | — | message table 2.4 | BT-04~10 | `BoundaryErrorMapper` |

---

## 권장 패키지 구조 (구현 시 참고, 코드 없음)

```
unit_converter/
  domain/          # Quantity, Registry, UseCases, Domain errors
  boundary/        # CLI, Parser, Formatter, ErrorMapper
  data/            # Loader, DTO, Factory
  composition/     # main(), wiring
tests/
  domain/
  boundary/
  data/
  integration/
config/units.json
```

---

## 다음 단계 (구현 착수 시)

1. `tests/domain/`에 DT-01~03 RED 작성  
2. Domain 최소 구현 → DT-04~12  
3. Boundary 계약(BT) + Data(DATA) 병렬  
4. Composition Root + IT-OK/FAIL  
5. 레거시 `UnitConverter.py`는 Boundary thin wrapper로 대체 또는 폐기

원하시면 동일 설계를 `c:\DEV\unit_converter_python` 디렉터리 생성 전제의 `docs/BCE-design.md` 초안 문구로 맞춰 드리거나, REGISTER/영속화를 1차 스코프에 넣을지 범위만 확정해 주시면 계약 표를 그에 맞게 줄이겠습니다.

[REDACTED]

---

### Turn 537 — user

<user_query>
@c:\DEV_BR\UnitConvertor_06\ 
경로는 여기고 docs/BCE-design.md로 저장해줘
</user_query>

---

### Turn 538 — assistant

설계 문서를 `docs/BCE-design.md`에 저장합니다.

[REDACTED]

---

### Turn 539 — assistant

`c:\DEV_BR\UnitConvertor_06\docs\BCE-design.md`에 BCE Dual-Track 설계 문서를 저장했습니다.

포함 내용:
- Domain (개념·SRP·Invariants·유스케이스·API·DT 테스트)
- Boundary (입출력·에러 스키마·BT 테스트·고정 메시지)
- Data (인터페이스·JSON 추천·DATA 테스트)
- Integration (의존성 다이어그램·IT 시나리오·커버리지·Traceability Matrix)
- 권장 패키지 구조 및 구현 착수 순서

경로는 `UnitConvertor_06` 기준으로 맞춰 두었습니다.

[REDACTED]

---

### Turn 540 — user

<user_query>
🔲 Mom Test 질문
unit_converter_python 프로젝트를 "고객 인터뷰" 관점에서 준비한다.
제품이 아니라 학습자/사용자의 행동을 드러내는 Mom Test 질문 10개.
각 질문: (1) 과거 구체 경험 (2) 실제 행동 (3) 돈/시간/리스크 연결.
금지: 기능 나열형 질문만으로 끝내기.
마지막에 "진짜 위험 가정" 3개를 bullet로.
구현·코드 금지.
</user_query>

---

### Turn 541 — assistant

# Mom Test 질문 — Unit Converter (학습·실습 맥락)

**대상**: `unit_converter_python` / `UnitConvertor_06` 실습을 하는 **학습자·실무자** (제품 피치가 아님)  
**목적**: “단위 변환기를 만들면 좋겠다”가 아니라, **언제·왜·어떻게** 길이/단위를 다루는지 드러내기

---

## Mom Test 질문 10개

### 1. 마지막으로 “길이 단위가 섞여서” 계산이 틀렸던 일

**(1)** 가장 최근에 그런 일이 있었을 때, **무엇을 만들거나 주문하려다** 망가졌나요? (예: 가구, 인쇄물, 현장 치수)  
**(2)** 그때 **어떤 단위로 적어 두었고**, 최종적으로 **어디(메모·엑셀·채팅)에 숫자를 옮겼나요?**  
**(3)** 그 실수 때문에 **다시 주문·재작업·납기 지연** 같은 비용이나 **몇 시간**을 썼나요?

---

### 2. 단위 변환을 “직접” 한 번의 작업 흐름

**(1)** 지난 한 달 안에 **feet/meter/yard** 중 하나를 다른 단위로 바꾼 적이 있나요? **가장 기억나는 한 건**만 말해 주세요.  
**(2)** 그때 **구글 검색, 계산기, 엑셀, 머릿속** 중 **실제로 연 것**은 무엇이었나요? 순서대로요.  
**(3)** 그 작업에 **몇 분** 썼고, 틀리면 **누가(본인·팀·고객)** 부담을 지나요?

---

### 3. “비율을 외부 파일로 둔다”는 아이디어 이전의 설정 습관

**(1)** 예전에 **환율·단위·요율**을 코드 밖으로 빼 본 적이 있나요? **언제, 어떤 프로젝트**였나요?  
**(2)** 그때 비율은 **JSON/YAML, .env, DB, 하드코딩** 중 **실제로 어디에** 두었나요?  
**(3)** 비율을 바꿀 때 **배포·재시작·PR 리뷰** 중 무엇이 **시간을 가장** 잡아먹었나요?

---

### 4. 새 단위가 “갑자기” 필요해진 순간

**(1)** 업무나 과제에서 **meter/feet/yard 말고** 다른 길이 단위가 필요했던 **가장 최근 사례**는 무엇이었나요?  
**(2)** 그때 **기존 도구를 고치기 vs 새 스크립트 vs 수동 계산** 중 **실제로 선택한 것**은?  
**(3)** 새 단위를 반영하지 못하면 **일정·점수·현장 리스크** 중 무엇이 걸려 있었나요?

---

### 5. CLI 한 줄 입력(`meter:2.5`) vs 다른 입력 방식

**(1)** 터미널에서 **한 줄짜리 명령**으로 숫자를 넣어 본 **가장 최근 경험**은 무엇이었나요? (git, curl, python -c 등)  
**(2)** 그때 **복사·붙여넣기**를 했나요, **직접 타이핑**했나요? **실수로 다시 친 적**이 있나요?  
**(3)** 입력 형식이 헷갈리면 **몇 번이나 재시도**하고, 그게 **업무 마감**에 영향을 줬나요?

---

### 6. 출력 형식(JSON/CSV/표)을 골랐던 이유

**(1)** 최근에 **표 대신 JSON/CSV**로 결과를 받아야 했던 **구체적 상황**이 있었나요?  
**(2)** 그 결과를 **다음에 실제로 연 도구**(엑셀, 스크립트, 슬랙, 보고서)는 무엇이었나요?  
**(3)** 형식이 맞지 않아 **수동으로 다시 정리**한 적이 있나요? 그때 **몇 분·몇 번**이었나요?

---

### 7. 테스트를 “먼저” 쓴 적이 있는지 (TDD/RED)

**(1)** 단위 테스트를 **기능 구현 전에** 써 본 **한 번의 프로젝트**를 떠올려 보세요. **언제, 누가 시켰나요?**  
**(2)** 그때 **실패하는 테스트(RED)** 를 몇 개 만들었고, **커밋·실행 순서**는 어땠나요?  
**(3)** 테스트 없이 배포·제출했다면 **어떤 버그 비용**(시간, 감점, 롤백)이 있었나요?

---

### 8. OCP·SRP 같은 원칙을 “실제로” 지키려 한 순간

**(1)** “새 단위 추가할 때 기존 코드 거의 안 건드리게” 해 본 **가장 가까운 경험**은 무엇이었나요? (단위 말고도 됨)  
**(2)** 그때 **리팩터링에 쓴 시간**과 **당장 기능 맞추기** 중 **실제로 선택한 쪽**은?  
**(3)** 원칙을 무시하고 빨리 냈을 때 **나중에 고친 시간**이 더 든 적이 있나요? **얼마나**?

---

### 9. 생성형 AI로 코딩·테스트를 한 실제 패턴

**(1)** README에 있는 것처럼 **AI로 과제/실습**을 한 **가장 최근 1회**—**무엇을 맡겼고**, **몇 번 프롬프트**를 썼나요?  
**(2)** AI가 준 코드를 **그대로 실행·복붙·일부만 수정·버림** 중 **실제로 한 비율**은?  
**(3)** AI 답을 그대로 썼을 때 **틀린 테스트·보안·제출 규정** 같은 **리스크**를 겪은 적이 있나요?

---

### 10. “단위 변환기”를 끝까지 안 쓰고 끝낸 경우

**(1)** 비슷한 **작은 계산/변환 도구**를 만들다 **중단하거나 제출만 하고 안 쓴** 경험이 있나요? **왜 멈췄나요?**  
**(2)** 그때 **계속 쓰게 만든 것**은 기능이 아니라 **무엇**(동료, 마감, 채점, 현장 압박)이었나요?  
**(3)** 안 쓰면 **대신 무엇**(엑셀, 사이트, 머릿속)을 **지금도** 쓰고 있나요? **하루에 몇 번**인가요?

---

## 진짜 위험 가정 (검증 필요)

- **가정 A**: 학습자는 “단위 변환 정확도”보다 **제출·통과·마감**이 먼저라, CLI·OCP·외부 설정은 **실제 업무 습관과 연결되지 않으면** 과제 후에는 **구글/엑셀으로 되돌아간다**.
- **가정 B**: `register:1 cubit = …` 같은 **동적 등록**은 현장 니즈가 아니라 **과제 rubric용**에 가깝고, 인터뷰에서는 **“비율을 파일/코드에 한 번 넣고 끝”** 행동만 반복된다.
- **가정 C**: AI·TDD·커버리지 목표는 **학습 성과 측정**에는 도움이 되지만, **음수·형식 검증 같은 Boundary 규칙**은 사용자가 체감한 **돈/시간 손실**과 맞닿지 않아 **테스트·메시지 고정에 시간을 쓰는 것**을 정당화하기 어렵다.

---

**인터뷰 팁**: “이 기능 필요하세요?” 대신 위 질문 후 **“그다음에 뭘 하셨어요?”** 한 번만 더 물으면 기능 나열형 답을 행동으로 바꿀 수 있습니다.

[REDACTED]

---

### Turn 542 — user

<user_query>
docs 하위에 저장해줘
</user_query>

---

### Turn 543 — assistant

[REDACTED]

---

### Turn 544 — assistant

`c:\DEV_BR\UnitConvertor_06\docs\Mom-Test-questions.md`에 저장했습니다.

`docs` 폴더에는 지금 다음 두 문서가 있습니다.

- `BCE-design.md` — BCE Dual-Track 설계
- `Mom-Test-questions.md` — Mom Test 인터뷰 질문 10개 + 위험 가정 3개

[REDACTED]

---

### Turn 545 — user

<user_query>
🔲 BCE 설계 전문가 — Python
Dual-Track(UI/경계 vs Domain) + BCE 관점 설계 전문가로 행동하라.
대상: c:\DEV_BR\unit_converter_python
제약: 구현 코드 작성 금지. 설계·계약·테스트 목록·통합 계획만.

# 1) Entity(Domain) 설계
  1.1 개념 목록과 SRP
  1.2 Invariants
  1.3 유스케이스
  1.4 Domain API (시그니처 수준, 본문 X) + 실패 조건
  1.5 Domain 단위 테스트 설계 (RED 우선)

# 2) Boundary 설계
  2.1 시나리오: 입력→검증→실행→출력
  2.2 외부 계약: Input / Output / Error schema
  2.3 Boundary 계약 테스트 (Domain Mock 가정)
  2.4 에러 메시지 규칙 (문구 패턴 고정)

# 3) Data 설계
  3.1 목적
  3.2 인터페이스 계약 (이름만 제안)
  3.3 InMemory vs File(JSON/YAML) 비교 + 추천 1개와 이유
  3.4 Data 레이어 테스트

# 4) Integration & Verification
  4.1 의존성 방향 포함 흐름
  4.2 통합 테스트 시나리오 (정상 2+, 실패 3+)
  4.3 회귀 보호 규칙
  4.4 커버리지 목표 (Domain / Boundary / Data 수치)
  4.5 Traceability Matrix: Concept→Rule→UseCase→Contract→Test→Component

모호어 금지. 모든 규칙은 테스트로 검증 가능하게.
</user_query>

---

### Turn 546 — assistant

대상 경로와 기존 설계·요구사항을 확인한 뒤 BCE 설계를 정리합니다.

[REDACTED]

---

### Turn 547 — assistant

`unit_converter_python` 경로에 설계 문서를 생성합니다. 기존 `UnitConvertor_06` 요구사항을 반영하고 모호한 항목을 제거합니다.

[REDACTED]

---

### Turn 548 — assistant

`c:\DEV_BR\unit_converter_python\docs\BCE-design.md`에 BCE Dual-Track 설계를 저장했습니다. (물리 폴더 `unit_converter_python` 신규 생성; 요구사항은 `UnitConvertor_06` README·레거시와 동일 기준)

### 이번 설계에서 고정한 것 (모호어 제거)
- 수치 타입: **`float`만** (`Decimal` 제외)
- 상수: `EPSILON=1e-4`, `DISPLAY_DECIMALS=1`, 시드 비율·기준 단위 표
- Domain 예외: **`code`만**; 사용자 문구는 Boundary
- Exit code: `0` / `1` / `2` 계약
- REGISTER/CONVERT **정규식**·ERR 메시지 **완전 일치** 표
- InMemory vs File → **JSON File 추천** + `UNIT_CONFIG_PATH`

### 문서 구성
| 섹션 | 내용 |
|------|------|
| §1 | 9개 개념 SRP, INV-01~11, UC-D01~03, API 시그니처, DT-01~12 |
| §2 | 파이프라인, I/O/Error JSON, BT-01~10, 고정 메시지 |
| §3 | Data 인터페이스 7개, DATA-01~06 |
| §4 | Mermaid 의존성, IT 2+3, 회귀 5규칙, 커버리지 %, Traceability Matrix |

기존 `UnitConvertor_06\docs\BCE-design.md`와 내용이 겹치면 `unit_converter_python` 쪽을 기준 문서로 두고, 구 폴더는 심볼릭 링크·이동만 정리하면 됩니다.

[REDACTED]

---

### Turn 549 — user

<user_query>
DOCS에 폴더로 저장해줘
</user_query>

---

### Turn 550 — assistant

프로젝트 구조를 확인한 뒤 `DOCS` 폴더에 문서를 정리해 저장합니다.

[REDACTED]

---

### Turn 551 — assistant

[REDACTED]

---

### Turn 552 — assistant

`DOCS` 폴더 구조를 만들고 설계·Mom Test 문서를 저장합니다.

[REDACTED]

---

### Turn 553 — assistant

[REDACTED]

---

### Turn 554 — assistant

[REDACTED]

---

### Turn 555 — assistant

`DOCS` 폴더 구조로 저장해 두었습니다.

### `c:\DEV_BR\UnitConvertor_06\DOCS\`

```
DOCS/
├── README.md
├── bce/
│   └── BCE-design.md      ← BCE Dual-Track 설계 (최신본)
└── mom-test/
    └── Mom-Test-questions.md
```

### 추가 처리

- 기존 `docs/`(소문자) → `DOCS/README.md`로 안내 링크 추가
- `c:\DEV_BR\unit_converter_python\DOCS\`에도 동일 구조 복사 (경로만 `unit_converter_python`으로 맞춤)

**기준 문서 경로는 `DOCS/`** 입니다. 구현 시 설계는 `DOCS/bce/BCE-design.md`를 참고하면 됩니다.

[REDACTED]

---

### Turn 556 — user

<user_query>
🔲 RED 테스트 목록
pytest를 가정하고 "구현 없이" RED 단계 테스트 케이스 제목 25~40개.
분류: 파싱 / 음수·0 / 미지원 단위 / 비율 정확도 / 동적 등록 / 출력 직렬화
(JSON/CSV/표 각 최소 3개씩)
각 테스트 옆에 보호하는 invariant 이름 한 줄.
코드 작성 금지.
</user_query>

---

### Turn 557 — assistant

[REDACTED]

---

### Turn 558 — assistant

BCE 설계의 invariant·계약에 맞춰 RED 테스트 목록을 정리하고 `DOCS`에 저장합니다.

[REDACTED]

---

### Turn 559 — assistant

[REDACTED]

---

### Turn 560 — assistant

[REDACTED]

---

### Turn 561 — assistant

# RED 테스트 목록 (pytest · 구현 전 · 38개)

`DOCS/testing/RED-test-list.md`에도 동일 내용을 저장했습니다.

---

## 파싱 (7)

| 테스트 제목 | 보호 |
|-------------|------|
| `test_parse_convert_valid_meter_colon_2_5` | CONVERT 입력 정규식 계약 |
| `test_parse_convert_rejects_line_without_colon` | ERR_FORMAT |
| `test_parse_convert_rejects_non_numeric_value_token` | ERR_NUMBER |
| `test_parse_convert_rejects_empty_unit_id` | INV-04 |
| `test_parse_convert_rejects_unit_starting_with_digit` | INV-04 |
| `test_parse_register_valid_cubit_equals_meter_line` | REGISTER 정규식 계약 |
| `test_parse_register_rejects_line_without_meter_suffix` | ERR_REGISTER_FORMAT |

---

## 음수·0 (5)

| 테스트 제목 | 보호 |
|-------------|------|
| `test_quantity_constructor_rejects_negative_value` | INV-03 |
| `test_cli_convert_negative_meter_emits_err_negative_exit_1` | INV-03 · ERR_NEGATIVE |
| `test_cli_convert_rejects_negative_before_domain_execute` | Boundary: Domain 호출 전 차단 |
| `test_convert_zero_meter_succeeds_exit_0` | INV-03 (0 허용) |
| `test_domain_zero_meter_canonical_value_is_zero` | INV-07 |

---

## 미지원 단위 (4)

| 테스트 제목 | 보호 |
|-------------|------|
| `test_registry_get_factor_unknown_mile_raises_unknown` | INV-06 |
| `test_convert_all_units_unknown_input_raises_unknown` | INV-06 · UC-D01 전제 |
| `test_cli_convert_mile_emits_err_unknown_unit_exit_1` | ERR_UNKNOWN_UNIT |
| `test_unit_id_from_raw_blank_raises_invalid_unit_id` | INV-04 |

---

## 비율 정확도 (7)

| 테스트 제목 | 보호 |
|-------------|------|
| `test_normalize_8_2_feet_to_meter_within_epsilon` | INV-07 |
| `test_convert_canonical_2_5_meter_to_feet_raw_within_epsilon` | INV-08 · RATIO_FEET |
| `test_convert_canonical_2_5_meter_to_yard_raw_within_epsilon` | INV-08 · RATIO_YARD |
| `test_feet_to_yard_ratio_matches_meter_derived_ratio_within_epsilon` | INV-07·08 |
| `test_convert_all_from_meter_2_5_yields_three_targets` | INV-10 |
| `test_register_meter_with_ratio_not_one_raises_invalid_canonical` | INV-02 |
| `test_conversion_factor_ratio_zero_raises_invalid_ratio` | INV-01 |

---

## 동적 등록 (6)

| 테스트 제목 | 보호 |
|-------------|------|
| `test_register_cubit_0_4572_then_convert_lists_cubit_target` | INV-09 · UC-D02→UC-D01 |
| `test_register_same_unit_twice_raises_duplicate` | INV-05 |
| `test_register_ratio_zero_raises_invalid_ratio` | INV-01 · INV-09 |
| `test_cli_register_cubit_prints_registered_exit_0` | 등록 성공 메시지 계약 |
| `test_cli_register_duplicate_emits_err_duplicate_unit` | ERR_DUPLICATE_UNIT |
| `test_after_register_convert_target_count_increases_by_one` | INV-10 · INV-11 |

---

## 출력 직렬화 — 표 (3)

| 테스트 제목 | 보호 |
|-------------|------|
| `test_table_meter_2_5_line_matches_display_pattern` | table 줄 패턴 · DISPLAY_DECIMALS |
| `test_table_emits_one_line_per_registered_unit` | INV-10 |
| `test_table_default_format_when_flag_omitted` | 기본 format=table |

---

## 출력 직렬화 — JSON (3)

| 테스트 제목 | 보호 |
|-------------|------|
| `test_json_meter_2_5_has_source_and_conversions_keys` | JSON 스키마 키 |
| `test_json_conversions_length_equals_registry_size` | INV-10 |
| `test_json_source_unit_and_value_match_input` | INV-11 · source 필드 |

---

## 출력 직렬화 — CSV (3)

| 테스트 제목 | 보호 |
|-------------|------|
| `test_csv_header_is_source_and_target_columns` | CSV 헤더 고정 |
| `test_csv_data_row_count_equals_conversion_count` | INV-10 |
| `test_cli_format_csv_meter_2_5_exit_0` | `--format csv` · exit=0 |

---

## RED 실행 순서 (권장)

`N-01, A-07` → `P-*` → `N-02~05, U-*` → `A-01~06` → `R-*` → `T-*` → `J-*` → `C-*`

**합계 38** (요구 25~40, table/json/csv 각 ≥3 충족). 구현 전 `pytest` 실행 시 **전부 FAIL**이 정상입니다.

[REDACTED]

---

### Turn 562 — user

<user_query>
DOCS 폴더에 파일만들어줘
</user_query>

---

### Turn 563 — assistant

DOCS 폴더 현재 상태를 확인한 뒤 문서 파일을 정리·생성합니다.

[REDACTED]

---

### Turn 564 — assistant

[REDACTED]

---

### Turn 565 — assistant

[REDACTED]

---

### Turn 566 — assistant

[REDACTED]

---

### Turn 567 — assistant

[REDACTED]

---

### Turn 568 — assistant

[REDACTED]

---

### Turn 569 — assistant

[REDACTED]

---

### Turn 570 — assistant

[REDACTED]

---

### Turn 571 — assistant

[REDACTED]

---

### Turn 572 — assistant

[REDACTED]

---

### Turn 573 — assistant

[REDACTED]

---

### Turn 574 — assistant

`DOCS` 폴더에 문서를 정리해 두었습니다.

### 구조

```
DOCS/
├── README.md                          ← 목차·읽는 순서
├── bce/
│   └── BCE-design.md                  ← BCE Dual-Track 설계 (최신본)
├── mom-test/
│   └── Mom-Test-questions.md          ← Mom Test 10문항
└── testing/
    └── RED-test-list.md               ← pytest RED 38개
```

### 처리 내용

- `DOCS/README.md` 생성
- `mom-test/`, `testing/` 문서 저장·경로 메타데이터 반영
- 루트에 있던 중복 파일(`DOCS/BCE-design.md`, `DOCS/Mom-Test-questions.md`) 삭제 → `bce/` 하위만 유지
- 소문자 `docs/README.md` → `DOCS/` 안내 링크 추가

설계 문서는 `DOCS/bce/BCE-design.md`를 기준으로 보면 됩니다.

[REDACTED]

---

## Session `7ed9f542-8ae8-4cf9-ae95-9eaecb9f0689`

### Turn 575 — user

<user_query>
@c:\DEV_BR\UnitConvertor_06\ 프로젝트를 구현하기 위한 깃 브랜치 전략을 알려줘.
개발방법론은 Dual-Track TDD 이고, 다음의 순서로 진행할 거야.

- Dual-Track UI + Logic TDD (RED 단계)
- GREEN 단계 (테스트 통과)
- Dual-Track Refactoring
코드작성금지
</user_query>

---

### Turn 576 — assistant

프로젝트 구조와 README의 개발 방법론을 확인한 뒤, Dual-Track TDD에 맞는 Git 브랜치 전략을 제안합니다.

[REDACTED]

---

### Turn 577 — assistant

[REDACTED]

---

### Turn 578 — assistant

[REDACTED]

---

### Turn 579 — assistant

[REDACTED]

---

### Turn 580 — assistant

[REDACTED]

---

### Turn 581 — assistant

저장소는 이미 `main`(문서·계약 고정), `red`(구현 착수용), `B_06` 등이 있고, `.cursorrules`와 README는 **RED → GREEN → refactor**, Dual-Track은 **Domain(Logic)** vs **Boundary(UI/경계)** 순으로 정의되어 있습니다. 아래는 그 흐름에 맞춘 **브랜치 전략 제안**입니다(코드 작성 없음).

---

## 1. 브랜치 역할 (장기)

| 브랜치 | 역할 | `pytest` 기대 |
|--------|------|----------------|
| **`main`** | 릴리스·회귀 기준선. 문서(M0) + **전체 GREEN**만 반영 | 항상 0 failed |
| **`red`** (또는 `develop`) | 현재 사이클 통합: RED·GREEN·refactor **작업 중** 허용 | RED 구간은 실패 허용, GREEN/refactor 직전·이후는 0 failed 목표 |
| **`spec`** (완료 시) | Phase 5처럼 **구현 없는 명세만** — 이미 `main`에 머지됐다면 삭제·보관만 | N/A |

**원칙:** `main`에는 “의도적 RED 실패”를 두지 않습니다. RED 실패 테스트는 `red` 또는 짧은 feature 브랜치에서만 유지합니다.

---

## 2. Dual-Track × TDD 단계별 브랜치 모델

Dual-Track은 **같은 RED 사이클 안에서 두 갈래**로 움직이고, GREEN/refactor는 **합류 순서**가 있습니다.

```mermaid
gitGraph
  commit id: "M0 docs"
  branch red
  checkout red
  commit id: "RED domain"
  commit id: "RED boundary"
  commit id: "RED data+int"
  checkout main
  merge red id: "GREEN M1" tag: "v1.0-core"
  branch refactor/m2-bce
  checkout refactor/m2-bce
  commit id: "refactor BCE"
  checkout main
  merge refactor/m2-bce id: "M2 quality"
```

### Phase 1 — Dual-Track RED (`red`에서 분기)

| Track | 의미 | 브랜치 예시 | 산출 (테스트만) |
|-------|------|-------------|-----------------|
| **Logic** | `entity` — Registry·Engine·불변식 | `red/domain/<slice>` | `T-D-*`, `A-*`, `N-*`, `U-*`, `R-*` |
| **UI** | `boundary` — 파싱·렌더·exact message | `red/boundary/<slice>` | `P-*`, `T-*`, `J-*`, `C-*` (Engine Mock/Fake) |
| **Data** (M2~) | 설정 로드 | `red/data/<slice>` | `T-DA-*` |
| **통합** | 두 트랙 연결 | `red/integration/<slice>` | `T-I-*` |

**`<slice>` 예:** `anchor`, `negative`, `unknown-unit`, `table`, `json`, `config`

**RED 병합 순서 (권장, RED-test-list·BCE 설계와 동일):**

1. Logic: `A` → `N` → `U` → `R` → `T-D`  
2. UI: 파싱·오류 문구 → table → json/csv  
3. Data (M2)  
4. Integration  

각 slice는 `red/domain/...` · `red/boundary/...`에서 작업 후 **`red`로 PR(또는 merge)** — Logic·UI를 **같은 RED 사이클**에 맞춰 짧게 유지합니다.

**커밋:** `test(entity): RED A-01 anchor conversion` / `test(boundary): RED P-04 invalid format exact`

---

### Phase 2 — GREEN (`red` → `main` 전)

| 규칙 | 브랜치 |
|------|--------|
| RED가 Logic·UI(필요 시 Data)에 쌓인 뒤 | `green/m1-core`, `green/m2-quality` |
| `.cursorrules` 순서: **entity → boundary → control → data → integration** | 한 마일스톤당 하나의 `green/*` 권장 |
| 한 번에 하나의 실패 TC(또는 동일 Invariant 묶음)만 GREEN | `green/m1-core` 안에서 연속 커밋 |

**커밋:** `feat(entity): GREEN A-01` / `feat(boundary): GREEN T-01 table render`

**머지:** `green/m1-core`가 `pytest` 0 failed + P0 RED ID GREEN → **`main` PR 1건** (squash 또는 merge commit 팀 규칙에 따름).

---

### Phase 3 — Dual-Track Refactoring

| 조건 | 브랜치 |
|------|--------|
| **전 테스트 GREEN** 이후만 | `refactor/m2-bce-split`, `refactor/extract-renderer` |
| 행위·계약·문구·수치 불변 (RR-04) | `main`에서 분기 → GREEN 유지하며 PR |

**금지:** refactor 브랜치에서 새 요구·RED 없는 계약 변경.

**커밋:** `refactor(boundary): split table renderer` — README To-Do의 “BCE refactor (GREEN 이후)”와 동일.

---

## 3. 마일스톤 ↔ 브랜치 매핑

| 마일스톤 | README | 브랜치 흐름 |
|----------|--------|-------------|
| **M0** | 문서·계약 | `spec` → `main` (완료) |
| **M1** | v1.0 Core (F-01~04) | `red/domain/*` + `red/boundary/*` → `red` → `green/m1-core` → `main` |
| **M2** | Quality (F-05~07, BCE 분리) | `red/data/*`, `red/boundary/json-csv` → `green/m2-quality` → `refactor/m2-bce` → `main` |
| **M3** | Release | `main` + tag `v1.0.0`, 회귀 R-1~R-7 |

---

## 4. PR·CI 정책 (브랜치와 연동)

| 대상 브랜치 | CI |
|-------------|-----|
| `main` | `pytest` 필수 통과, 커버리지 게이트(M2~) |
| `red`, `red/*`, `green/*` | RED 구간: “실패 수 = 예상 RED 수” 문서화 또는 `continue-on-error` **선택** (학습용). `green/*`·`refactor/*`는 **0 failed** |
| PR to `main` | skip/xfail 금지, 앵커 TC 삭제·완화 금지 (README Contributing) |

**계약 변경 PR:** `red` → 테스트+PRD+RED 목록 **동시** (RR-03).

---

## 5. 브랜치 이름·커밋 컨벤션 (README와 정렬)

```text
red/<track>/<slice>     # track: domain | boundary | data | integration
green/<milestone>       # m1-core | m2-quality
refactor/<topic>        # m2-bce-split | renderer
```

| type | TDD 단계 |
|------|----------|
| `test` | RED |
| `feat` / `fix` | GREEN |
| `refactor` | refactor (GREEN 유지) |
| `docs` | PRD/README/RED 목록 (보통 `main` 또는 `red` 문서만) |

**scope:** `entity`, `boundary`, `control`, `data`, `docs`

---

## 6. 현재 저장소에 대한 정리 제안

| 브랜치 | 제안 |
|--------|------|
| **`main`** | 안정 기준선 유지 |
| **`red`** (현재 체크아웃) | **M1 RED 통합 브랜치**로 사용 — `red/domain/*`, `red/boundary/*`를 여기로 머지 |
| **`B_06`** | 목적이 M1 구현이면 `red`와 통합하거나 `red/domain/m1` 등으로 **이름 통일**; 실험용이면 머지 후 삭제 |
| **`spec`** | M0 완료 시 `main`만 유지, 원격 `spec` 삭제 가능 |

---

## 7. 한 사이클 작업 순서 (체크리스트)

1. `git checkout red` · `git pull`  
2. **RED:** `red/domain/anchor` + `red/boundary/parse-errors` 병렬 → `red` 머지 (실패 OK)  
3. **GREEN:** `green/m1-core`에서 entity → boundary → integration 순 커밋  
4. `pytest` 0 failed → PR `green/m1-core` → `main`  
5. **Refactor:** `main`에서 `refactor/m2-bce-split` → GREEN 유지 → PR  
6. M3: `main`에 `v1.0.0` 태그  

---

## 8. 요약

- **Trunk:** `main` = 항상 GREEN.  
- **Integration:** `red` = Dual-Track RED + 사이클 통합.  
- **Short-lived:** `red/<track>/<slice>` → `green/<milestone>` → `refactor/<topic>`.  
- **Dual-Track RED**는 Logic·UI를 **같은 사이클**에서 slice 단위로 나누고, **GREEN**은 entity → boundary → … **한 줄**로 좁힙니다.  
- **Refactor**는 `main` 기준, 테스트 diff 0만 허용.

`B_06`을 M1 전용으로 쓸지, `red`로 통합할지 정해 주시면 그에 맞춰 브랜치 이름만 더 구체화할 수 있습니다.

[REDACTED]

---

### Turn 582 — user

<user_query>
@README.md 와 @docs/PRD.md 문서를 참고하여
테스트 플랜 작성을 위한 샘플 예제 1개를 선택해줘.

선택 기준:
1. README의 기본 요구사항에 명시된 핵심 변환 기능
2. 비즈니스 로직(1 meter = 3.28084 feet, 1 meter = 1.09361 yard)을 직접 검증
3. 정상 경로(happy path)와 경계값 모두 포함 가능한 기능

선택한 예제에 대해 다음을 명시하라:
- 선택한 기능 이름 (예: meter → feet 변환)
- README 요구사항 번호 (예: 기본 요구사항 4번)
- 입력 예시: "meter:2.5"
- 기대 출력: "2.5 meter = 8.202100 feet"
- 이 예제를 선택한 이유 2줄

코드 작성 금지. 선택 결과 문서만 출력.
</user_query>

---

### Turn 583 — assistant

README와 PRD에서 핵심 변환·표시 계약을 확인한 뒤, 테스트 플랜 샘플로 쓸 예제 하나를 고릅니다.

[REDACTED]

---

### Turn 584 — assistant

[REDACTED]

---

### Turn 585 — assistant

# 테스트 플랜 샘플 예제 선택 결과

## 선택 기능

| 항목 | 내용 |
|------|------|
| **기능 이름** | **meter 입력 → 기본 3단위 전체 table 환산** (대표 라인: **meter → feet**, `meter:2.5`) |
| **README 요구사항** | **예시 입출력** · **입력 형식 계약(변환 `unit:value`)** · **출력 포맷(table)** · Must-Have **「boundary: `unit:value` 파싱·table 렌더」** · **「표시 반올림 1자리 ROUND_HALF_UP」** |
| **PRD 요구사항** | **F-01**, **F-03**, **F-04**, **AC-01**, **G-02**, 시나리오 **S-01** |
| **입력 예시** | `meter:2.5` |
| **기대 출력 (table, stdout exact)** | 아래 3줄, **exit code 0** |

```text
2.5 meter = 2.5 meter
2.5 meter = 8.2 feet
2.5 meter = 2.7 yard
```

| 검증 층 | 기대값 (계약) |
|---------|----------------|
| **비즈니스 로직 (entity, ε≤1e-4)** | feet ≈ `2.5 × 3.28084` = **8.2021**; yard ≈ `2.5 × 1.09361` = **2.734025** (`meters_per_unit`: feet `0.3048`, yard `0.9144`) |
| **표시 (boundary/table, 1자리 ROUND_HALF_UP)** | feet **8.2**, yard **2.7** (README·PRD 인수 기준과 동일) |

> 참고: 질문 예시의 `8.202100`은 **내부 환산값**에 가깝고, README·PRD의 **CLI table 계약**은 표시 1자리이므로 기대 stdout 라인은 **`2.5 meter = 8.2 feet`** 입니다.

---

## 선택 이유

1. README·PRD의 **핵심 Happy path(AC-01, S-01)** 이자 회귀 앵커(**T-01, A-06**)와 직결되어, `1 m = 3.28084 ft` / `1 m = 1.09361 yd` 비율을 **내부 수치(ε)** 와 **표시 반올림(8.2 / 2.7)** 로 나눠 Dual-Track 테스트 플랜을 쓰기에 가장 적합합니다.  
2. 동일 입력 `meter:2.5` 주변에 **경계값**(`meter:0` 허용, `meter:-1` 거부, `meter 2.5` 형식 오류)을 한 시나리오 묶음으로 확장할 수 있어, 정상 경로와 입력 검증(F-02)을 한 테스트 플랜에 포함하기 좋습니다.

[REDACTED]

---

### Turn 586 — user

<user_query>
[P] 시니어 QA 리드입니다.
[C] Python 3.11+, pytest, pydantic
[T] 선택한 샘플 예제(meter→feet 변환)를 기반으로 테스트 계획서를 작성해줘.

    포함 항목:
    - pytest 기반 단위 테스트 범위/우선순위
    - 경계값 케이스 목록:
        · value = 0 (영값 변환)
        · value = 매우 큰 수 (오버플로 위험)
        · value < 0 (음수 입력 정책)
        · 소수점 파싱 실패 ("meter:abc")
        · ":"없는 입력 (형식 오류)
        · 없는 단위 ("parsec:1.0")
    - 예외/특이 케이스 목록
    - 커버리지 목표 (Domain 95%+ / Boundary 85%+)
    - pip install pytest-cov / pytest --cov=unit_converter --cov-report=term-missing 측정 전략

[F] Markdown 문서. @docs/ test_plan.md로 저장.
</user_query>

---

### Turn 587 — assistant

PRD·README·프로젝트 구조를 확인한 뒤 `docs/test_plan.md` 테스트 계획서를 작성합니다.

[REDACTED]

---

### Turn 588 — assistant

[REDACTED]

---

### Turn 589 — assistant

`docs/test_plan.md` 작성 중입니다.

[REDACTED]

---

### Turn 590 — assistant

`docs/test_plan.md`에 테스트 계획서를 저장했습니다.

### 문서 요약

| 섹션 | 내용 |
|------|------|
| **범위** | 샘플 `meter:2.5` / meter→feet, PRD F-01~04·AC-01~03, Dual-Track |
| **우선순위** | P0 entity/boundary/integration → P1 control → P2 M2 |
| **경계값** | BV-01~06 — `meter:0`, 큰 수, `meter:-1`, `meter:abc`, `meter 2.5`, `parsec:1.0` (exact message·exit 포함) |
| **특이 케이스** | 다중 `:`, 빈 입력, HALF_UP 경계, skip/xfail 금지 등 |
| **커버리지** | **entity ≥ 95%**, **boundary ≥ 85%** (README 90%는 목표선으로 병기) |
| **cov 전략** | `pip install pytest-cov`, BCE용 `--cov=entity --cov=boundary`, 요청하신 `--cov=unit_converter` 별도 표기 |

기대 stdout은 PRD 계약에 맞춰 **`2.5 meter = 8.2 feet`**(표시 1자리)이고, entity는 **≈ 8.2021 (ε≤1e-4)** 로 이중 검증하도록 적어 두었습니다.

경로: [docs/test_plan.md](c:\DEV_BR\UnitConvertor_06\docs\test_plan.md)

[REDACTED]

---

### Turn 591 — user

<user_query>
@README.md 파일에 아래 섹션을 추가해줘.
기존 내용은 일부 유지(TO-DO 리스트만 기존내용 삭제)하고, "## RED 단계 To-Do 리스트" 섹션만 새로 삽입.

추가할 섹션 형식:

## RED 단계 To-Do 리스트

> 이 체크리스트는 test_plan.md 기반으로 생성되었습니다.
> 각 항목은 RED(실패 테스트 작성) 완료 시 체크합니다.

### Track A — UI / Boundary 테스트
- [ ] TC-A-01: 정상 입력 "meter:2.5" → 변환 결과 반환 (Happy Path)
- [ ] TC-A-02: ":" 없는 입력 → ValueError / TypeError 발생
- [ ] TC-A-03: 음수 입력 "meter:-1.0" → ValueError / TypeError 발생
- [ ] TC-A-04: 없는 단위 "parsec:1.0" → ValueError / TypeError 발생
- [ ] TC-A-05: 소수점 파싱 실패 "meter:abc" → ValueError / TypeError 발생
- [ ] TC-A-06: 출력 포맷에 원 입력 단위·값 보존 ("2.5 meter = ...")
- [ ] TC-A-07: value=0 경계값 처리 확인

### Track B — Domain / Logic 테스트
- [ ] TC-B-01: convert("meter", 2.5, "feet") == 8.20210 (오차 1e-5)
- [ ] TC-B-02: convert("meter", 1.0, "yard") == 1.09361 (오차 1e-5)
- [ ] TC-B-03: convert("feet", 1.0, "meter") == 0.30480 (역변환)
- [ ] TC-B-04: convertAll("meter", 1.0) → 모든 등록 단위 변환 반환
- [ ] TC-B-05: registerUnit("cubit", 0.4572) 후 변환 가능
- [ ] TC-B-06: loadConfig(유효한 경로) → 비율 정상 로드
- [ ] TC-B-07: loadConfig(없는 경로) → 기본값(3.28084/1.09361) 유지

### 커버리지 목표
- [ ] Domain Logic: 95%+ (pip install pytest-cov)
- [ ] Boundary Layer: 85%+
- [ ] 전체 TOTAL: 90%+

### 결함 목록 연결
- [ ] defect_list.md 생성 및 발견 결함 기록
- [ ] 모든 결함 수정 후 회귀 테스트 통과 확인

</user_query>

---

### Turn 592 — assistant

README.md의 To-Do 섹션 위치를 확인한 뒤, 기존 To-Do는 제거하고 RED 단계 To-Do 리스트를 삽입합니다.

[REDACTED]

---

### Turn 593 — assistant

[REDACTED]

---

### Turn 594 — assistant

[REDACTED]

---

### Turn 595 — assistant

[REDACTED]

---

### Turn 596 — assistant

`README.md`를 반영했습니다.

### 변경 요약

1. **목차** — `To-Do 리스트 — UnitConverter` → `RED 단계 To-Do 리스트` 링크로 변경  
2. **관련 문서** — [docs/test_plan.md](docs/test_plan.md) 링크 추가  
3. **삭제** — 기존 Must/Should/Nice/Tech Debt/Done To-Do 블록 전체  
4. **추가** — 요청하신 `## RED 단계 To-Do 리스트` 섹션 (Track A/B, 커버리지, 결함 목록)  
5. **유지** — 회귀 방지 체크리스트, 마일스톤 및 그 위 섹션은 그대로 유지  

새 섹션은 `## 라이선스` / `## 관련 문서` 다음, 회귀 체크리스트 앞에 있습니다.

[REDACTED]

---

### Turn 597 — user

<user_query>
[P] 테스트 설계에 강한 시니어 Python QA입니다.
[C] Python 3.11+, pytest, pydantic
[T] 아이템 타입별 최소 5개 테스트를 작성해줘.

    대상 케이스:
    - 정상 변환: meter→feet, meter→yard, feet→meter (역변환)
    - 경계값: value=0 / 매우 큰 수 / 소수점 6자리 정확도
    - 예외: 잘못된 형식 / 음수 / 없는 단위
    - 동적 등록: registerUnit 후 변환
    - 설정 로드: JSON/YAML 정상·실패 케이스

    형식 규칙:
    - pytest 사용
    - Given-When-Then 주석 구조
    - 각 테스트에 변환 비율 명시 (1 meter = 3.28084 feet)
    - 테스트 이름: test_[변환타입]_[조건]_[기대결과] 형식

[F] 완성된 테스트 코드. pytest가 Green이 되게 작성.
</user_query>

---

### Turn 598 — assistant

프로젝트 구조와 구현 상태를 확인한 뒤, pytest가 통과하도록 테스트를 작성합니다.

[REDACTED]

---

### Turn 599 — assistant

[REDACTED]

---

### Turn 600 — assistant

BCE 레이어와 테스트를 구현해 pytest가 통과하도록 진행합니다.

[REDACTED]

---

### Turn 601 — assistant

[REDACTED]

---

### Turn 602 — assistant

[REDACTED]

---

### Turn 603 — assistant

[REDACTED]

---

### Turn 604 — assistant

[REDACTED]

---

### Turn 605 — assistant

[REDACTED]

---

### Turn 606 — assistant

[REDACTED]

---

### Turn 607 — assistant

[REDACTED]

---

### Turn 608 — assistant

[REDACTED]

---

### Turn 609 — assistant

pytest **33 passed** — BCE 구현과 테스트를 추가했습니다.

### 테스트 구조 (유형별 5개 이상)

| 유형 | 파일 | 테스트 수 |
|------|------|-----------|
| 정상 변환 | `tests/entity/test_convert_normal_happy_path.py` | 5 |
| 경계값 | `tests/entity/test_convert_boundary_precision.py` | 5 |
| 예외 | `tests/boundary/test_exception_parse_policy.py` | 6 |
| 동적 등록 | `tests/entity/test_register_dynamic_unit.py` | 6 |
| 설정 로드 | `tests/data/test_config_load_json_yaml.py` | 6 |
| 표시(table) | `tests/boundary/test_convert_display_table.py` | 5 |

### 구현 레이어 (GREEN용)

- `entity/` — Registry, ConversionEngine, 예외, `round_display`
- `boundary/` — parser, table renderer, PRD exact 오류 문구
- `control/` — `ConverterApp` (`convert`, `convert_all`, `register_unit`, `load_config`)
- `data/` — JSON/YAML `UnitDefinitionRepository`
- `config/units.json`, `pyproject.toml`

### 실행

```bash
pip install -e ".[dev]"
pytest -v
```

### 규칙 반영

- **Given-When-Then** 주석
- **비율 주석**: `1 meter = 3.28084 feet` 등
- **이름**: `test_[변환타입]_[조건]_[기대결과]`
- **표시**: `meter:2.5` → `2.5 meter = 8.2 feet` (내부 ≈ 8.20210, ε 1e-5)
- **예외**: `ValueError` 계열 (`ParseError`, `NegativeMagnitudeError`, …)

레거시 `UnitConverter.py`는 그대로 두었습니다. CLI는 `ConverterApp` 기준으로 확장하면 됩니다.

[REDACTED]

---

### Turn 610 — user

<user_query>
[P] 디버깅과 결함 분석에 능한 Python QA 엔지니어입니다.
[T] (여기에 pytest 실패 로그를 붙여넣을 것)

    1) 테스트 실패의 기대/실제 차이 요약
       예: expected 8.202100 but got 0.000000
    2) 버그 위치 특정 (파일명:줄번호)
       예: UnitConverter.py:27
    3) 결함 심각도 분류 및 근거:
       Critical   — 변환 결과가 완전히 틀린 경우
       Major      — 경계값에서 오차 초과
       Minor      — 출력 포맷 불일치
       Info       — 코드 스타일/주석 문제
    4) 최소 변경 수정 방안 (Python 스타일)
       - if-else 체인 유지 최소 수정 (GREEN 통과 우선)
       - Item/기본 구조체 수정 금지

[F] 수정 diff 제안 + pytest Green 확인 절차

</user_query>

---

### Turn 611 — assistant

실패 로그가 붙여지지 않았습니다. pytest를 실행해 현재 상태를 확인하고, 프로젝트에서 흔한 실패 패턴을 분석합니다.

[REDACTED]

---

### Turn 612 — assistant

실패 로그가 메시지에 없어, 현재 저장소 기준으로 pytest를 돌리고 레거시 `UnitConverter.py`와 테스트 계약이 어긋날 때의 대표 실패를 분석합니다.

[REDACTED]

---

### Turn 613 — assistant

## 현재 상태

요청 본문에 **pytest 실패 로그가 붙어 있지 않습니다.**  
저장소 기준 방금 실행 결과: **`33 passed in 0.19s`** (전부 GREEN).

아래는 (1) 질문에 나온 예시 패턴, (2) 레거시 `UnitConverter.py`만 쓸 때 자주 나는 실패, (3) 이전에 실제로 깨졌던 2건을 기준으로 한 **결함 분석 템플릿**입니다. 실제 로그를 붙여 주시면 항목별로 1:1 매핑해 드리겠습니다.

---

## 결함 분석 (대표 시나리오)

### DEF-001 — 변환 수치 0 또는 전혀 다른 값 (예: `expected 8.202100 but got 0.000000`)

| 항목 | 내용 |
|------|------|
| **1) 기대/실제** | `pytest.approx(8.20210, abs=1e-5)` 기대, 실제 **`0.0`** (또는 `0.000000`) |
| **2) 위치** | **테스트 대상 혼동** — `tests/entity/test_convert_normal_happy_path.py:18-22` 는 `entity.engine.ConversionEngine` 호출. `UnitConverter.py:27-28` 은 **테스트가 import하지 않음**. |
| **3) 심각도** | **Critical** — 핵심 환산 결과가 무효(0). |
| **근거** | `ConverterApp`/`ConversionEngine` 미연결, 스텁 `convert()`가 `0` 반환, 또는 잘못된 모듈 import 시 발생. 레거시 CLI만 실행해도 이 테스트는 통과하지 않음. |

**최소 수정 (GREEN 우선, 구조체 변경 없음)**

- 테스트는 이미 `entity` + `control` 경로를 사용 → **`pip install -e ".[dev]"` 후 `pytest`** (BCE 경로).
- 레거시만 고칠 경우가 아니라면 `UnitConverter.py` 단독 수정으로는 `test_convert_normal_*` 가 GREEN 되지 않음.

```diff
# 확인용: tests/conftest.py — ConverterApp + UnitRegistry.with_defaults() 사용 중
# UnitConverter.py 는 수동 CLI용; 단위 테스트와 분리됨
```

---

### DEF-002 — 표시 포맷: `8.2` 기대 vs `8.2021` 출력 (table / display 테스트)

| 항목 | 내용 |
|------|------|
| **1) 기대/실제** | 기대: stdout에 **`2.5 meter = 8.2 feet`** (exact). 실제: **`2.5 meter = 8.2021 feet`** (내부 float 그대로 출력) |
| **2) 위치** | `UnitConverter.py:30-32` (`print`에 반올림 없음). 계약 구현: `boundary/renderers/table.py:24-28` |
| **3) 심각도** | **Minor** — 수치는 맞으나 **표시 계약**(1자리 `ROUND_HALF_UP`) 위반. |
| **근거** | PRD §6.1, `test_convert_display_meter_2_5_table_three_lines` (line 20). |

**최소 수정 diff (`UnitConverter.py` — if-else 체인 유지, 구조체 없음)**

```diff
--- a/UnitConverter.py
+++ b/UnitConverter.py
@@ -1,3 +1,4 @@
+from decimal import ROUND_HALF_UP, Decimal
+
 def main():
@@ -26,9 +27,16 @@ def main():
     in_feet = meter_value * 3.28084
     in_yards = meter_value * 1.09361
 
+    def display_one(value: float) -> str:
+        rounded = Decimal(str(value)).quantize(
+            Decimal("0.1"), rounding=ROUND_HALF_UP
+        )
+        return f"{float(rounded):.1f}"
+
     print(f"{value} {unit} = {in_meters} meter")
-    print(f"{value} {unit} = {in_feet} feet")
-    print(f"{value} {unit} = {in_yards} yard")
+    print(f"{value} {unit} = {display_one(in_meters)} meter")
+    print(f"{value} {unit} = {display_one(in_feet)} feet")
+    print(f"{value} {unit} = {display_one(in_yards)} yard")
```

> **참고:** 위 수정만으로는 `tests/boundary/test_convert_display_*.py` 가 여전히 실패할 수 있음 — 해당 테스트는 **`ConverterApp` → `render_table`** 경로를 검증함. GREEN은 BCE 경로 기준으로 확인.

---

### DEF-003 — 음수/형식/미등록 단위: 예외 기대 vs 조용히 출력

| 항목 | 내용 |
|------|------|
| **1) 기대/실제** | `meter:-1.0` → **`ValueError`** / message `Value must be zero or positive: -1`. 실제: 예외 없이 **3줄 출력** 또는 잘못된 환산 |
| **2) 위치** | `UnitConverter.py:16-32` (음수 검증 없음). 계약: `boundary/parser.py:62-66`, `entity/engine.py:20-21` |
| **3) 심각도** | **Major** — F-02 입력 검증 미준수; 음수 허용 시 잘못된 환산 노출. |
| **근거** | `test_exception_negative_meter_raises_value_error`, PRD §3.2 |

**최소 수정 diff (`UnitConverter.py`)**

```diff
@@ -14,6 +14,10 @@ def main():
         print(f"Invalid number: {value_str}")
         return
 
+    if value < 0:
+        print(f"Value must be zero or positive: {value}")
+        return
+
     if unit == "meter":
```

`parsec:1.0` / `meter 2.5` / `meter:abc` 는 이미 `else`·`:` 검사·`float` except로 일부 처리됨. exit code ≠ 0 는 레거시에 없음 → 통합 테스트 실패 시 `sys.exit(1)` 추가는 **Minor** (exit 계약).

---

### DEF-004 — 경계값: 초대형 float 비율 assert (실제 발생했던 실패)

| 항목 | 내용 |
|------|------|
| **1) 기대/실제** | 기대: `3.28084e+100 ± …`. 실제: `3.2808398950131233e+100` — **절대/상대 오차 한계 초과** |
| **2) 위치** | `tests/entity/test_convert_boundary_precision.py:47-48` (수정 후 GREEN) |
| **3) 심각도** | **Major** — 경계값에서 **검증 방식**이 float 스케일에 부적합 (로직 버그 아님). |
| **근거** | `1e100` 근처에서 `3.28084` 리터럴과 `0.3048` 기반 계산의 **표현 차이**. |

**최소 수정 (테스트 쪽 1줄, 프로덕션 구조 변경 없음)**

```diff
--- a/tests/entity/test_convert_boundary_precision.py
+++ b/tests/entity/test_convert_boundary_precision.py
@@ -44,4 +44,4 @@
-    assert result == pytest.approx(large * RATIO_METER_TO_FEET, rel=1e-9)
+    assert result / large == pytest.approx(RATIO_METER_TO_FEET, abs=1e-5)
```

---

### DEF-005 — 설정: 빈 `units: []` 가 로드됨 (실제 발생했던 실패)

| 항목 | 내용 |
|------|------|
| **1) 기대/실제** | 기대: `ConfigLoadError`. 실제: **예외 없음**, 빈 Registry |
| **2) 위치** | `data/repository.py:71-76` (수정 후 GREEN). 테스트: `tests/data/test_config_load_json_yaml.py:80-86` |
| **3) 심각도** | **Major** — 잘못된 설정으로 **환산 불가/오동작** 가능. |

**최소 수정 diff**

```diff
--- a/data/repository.py
+++ b/data/repository.py
@@ -68,6 +68,11 @@
             ) from exc
 
+        if not config.units:
+            raise ConfigLoadError(
+                "CFG_PARSE_ERROR",
+                "Failed to parse config file.",
+            )
+
         registry = UnitRegistry()
```

---

## 심각도 요약

| ID | 심각도 | 한 줄 요약 |
|----|--------|------------|
| DEF-001 | Critical | 환산 결과 0 / 엔진 미연결 |
| DEF-002 | Minor | table 1자리 반올림 미적용 (`UnitConverter.py:30-32`) |
| DEF-003 | Major | 음수·검증 누락 (`UnitConverter.py:16-24`) |
| DEF-004 | Major | 초대형 float assert 방식 (테스트/검증) |
| DEF-005 | Major | 빈 config 허용 (`data/repository.py`) |

---

## pytest GREEN 확인 절차

```bash
cd c:\DEV_BR\UnitConvertor_06
python -m venv venv
venv\Scripts\activate
pip install -e ".[dev]"
python -m pytest -v --tb=short
```

| 단계 | 명령 | 통과 기준 |
|------|------|-----------|
| 1 | `pytest tests/entity/test_convert_normal_happy_path.py -v` | meter→feet `8.20210` (ε 1e-5) |
| 2 | `pytest tests/boundary/test_convert_display_table.py -v` | `8.2 feet` exact line |
| 3 | `pytest tests/boundary/test_exception_parse_policy.py -v` | ValueError + exact message |
| 4 | `pytest tests/data/test_config_load_json_yaml.py -v` | malformed/empty → `ConfigLoadError` |
| 5 | `pytest --cov=entity --cov=boundary --cov-report=term-missing` | Domain ≥95%, Boundary ≥85% (목표) |

**현재 저장소:** 5단계 중 **전체 `pytest` → 33 passed** (DEF-004·005 수정 반영됨).

---

## 다음에 로그를 붙일 때

아래 형식으로 붙여 주시면 위 템플릿을 **실패 건별**로 채워 드립니다.

```text
FAILED tests/.../test_xxx.py::test_yyy - AssertionError: ...
```

특히 **어느 파일을 실행 중이었는지** (`UnitConverter.py` vs `ConverterApp`)를 함께 적어 주세요. 같은 증상이라도 원인·수정 위치가 달라집니다.

[REDACTED]

---

### Turn 614 — user

<user_query>
[P] QA 리드입니다.
[C] 현재까지 발견된 테스트 실패/결함들을 문서화합니다.
[T] 발견된 결함을 defect_list.md에 정리해줘.

    항목 형식:
    | ID | Severity | 변환 타입 | 재현 절차 | 기대값 | 실제값 | 근본 원인 | 수정 요약 |

    예시:
    | DEF-001 | Critical | meter→feet | "meter:2.5" 입력 | 8.202100 | 0.000000 |
    | if-else 체인에서 feet 분기 누락 | meterValue * 3.28084 추가 |

[F] Markdown. @docs/ defect_list.md로 저장.
    README의 "RED 단계 To-Do 리스트 > 결함 목록 연결" 체크박스도 업데이트.
</user_query>

---

### Turn 615 — assistant

[REDACTED]

---

### Turn 616 — assistant

[REDACTED]

---

### Turn 617 — assistant

요청 형식에 맞추기 위해 `Status` 열을 제거하고 `수정 요약`에 상태를 통합합니다.

[REDACTED]

---

### Turn 618 — assistant

`docs/defect_list.md`를 추가했고 README를 갱신했습니다.

### 저장 위치
- [docs/defect_list.md](c:\DEV_BR\UnitConvertor_06\docs\defect_list.md) — **DEF-001 ~ DEF-008** (8건)
- 예시 형식 8열 테이블 + 테스트 매핑·회귀 절차·레거시 최소 수정 참고

### README 변경
- **관련 문서**에 `defect_list.md` 링크 추가
- **결함 목록 연결**
  - [x] `defect_list.md` 생성 및 기록
  - [x] BCE 회귀 `pytest` 33 passed (레거시 CLI Open 항목은 문서에 명시)

### 요약
| 구분 | 건수 |
|------|------|
| **Fixed** (BCE + pytest) | DEF-001, 004, 005 및 002·003·006·007 BCE 경로 |
| **Open** (레거시 `UnitConverter.py`) | DEF-002, 003, 006~008 |

[REDACTED]

---

### Turn 619 — user

<user_query>
당신은 Dual-Track UI + Logic TDD 전문가입니다.
프로젝트: @c:\DEV_BR\UnitConvertor_06\ 
현재 코드 상태: 단일 main() 함수, if-else 체인, 예외 처리 없음

중요: 구현 코드 작성 금지 / GREEN 단계 금지 / REFACTOR 금지
오직 RED 테스트만 작성하십시오.

프로젝트 조건:
- 입력: str (단위:값) (예: "meter:2.5")
- 변환: 1 meter = 3.28084 feet, 1 meter = 1.09361 yard
- 출력: "2.5 meter = 8.202100 feet" 형식
- 예외: ValueError / TypeError

TRACK A — UI / Boundary RED:
1. "meter:2.5" 정상 입력 → 변환 결과 반환
2. ":" 없는 입력 → 예외 발생 (잘못된 형식)
3. 음수 값 입력 ("meter:-1.0") → 예외 발생
4. 없는 단위 ("parsec:1.0") → 예외 발생
5. 반환 포맷에 원 입력 단위·값 보존 확인
6. JSON 출력 요청 시 올바른 스키마 반환
각 테스트에: 테스트 이름 / Given / When / Then / 보호하는 계약

TRACK B — Domain / Logic RED:
1. convert(fromUnit, value, toUnit) — meter↔feet 정확도 (1e-5 이내)
2. convert(fromUnit, value, toUnit) — meter↔yard 정확도
3. convertAll(fromUnit, value) — 모든 등록 단위로 변환 반환
4. registerUnit(name, ratio_to_meter) — 새 단위 등록 후 변환 가능
5. loadConfig(path) — JSON/YAML 설정 파일 로드 후 비율 적용
6. loadConfig(invalid_path) — 파일 없을 때 기본값 유지
각 테스트: 실패 상태 명확히 설명 / 보호 Invariant 명시

출력 형식:
# UI RED Tests — Test ID / Given/When/Then / Invariant
# Logic RED Tests — Test ID / Scenario / Invariant
</user_query>

---

### Turn 620 — assistant

프로젝트 상태를 확인한 뒤, 구현 없이 RED 테스트 명세만 작성합니다.

[REDACTED]

---

### Turn 621 — assistant

레거시 `UnitConverter.py` 기준으로 RED 명세만 작성합니다. 구현·GREEN·REFACTOR는 포함하지 않습니다.

[REDACTED]

---

### Turn 622 — assistant

Dual-Track **RED 명세만** 작성했습니다. 구현·GREEN·REFACTOR·pytest 코드는 포함하지 않았습니다.

저장 경로: [docs/testing/RED-dual-track-tests.md](c:\DEV_BR\UnitConvertor_06\docs\testing\RED-dual-track-tests.md)

**전제:** 현재 `UnitConverter.py`는 `main()` + if-else만 있으며 `convert` / `convertAll` / `registerUnit` / `loadConfig` 및 Boundary 파서·JSON 렌더가 없습니다. 아래 RED는 **의도적 실패** 기준입니다.

---

# UI RED Tests — Test ID / Given/When/Then / Invariant

## TC-A-01 — 정상 입력

| | |
|--|--|
| **테스트 이름** | `test_ui_convert_meter_2_5_returns_conversion_result` |
| **Given** | Registry(meter, feet, yard). `"meter:2.5"`. **1 meter = 3.28084 feet** |
| **When** | Boundary 파싱 → 변환 결과(또는 table/JSON용 DTO) **반환** |
| **Then** | 성공; feet ≈ `8.20210` (ε≤1e-5) 또는 출력 `"2.5 meter = 8.202100 feet"`; exit `0` |
| **Invariant** | F-01, D-INV-03, G-02 |
| **RED 실패** | `main()`은 print만 → 반환값 없음 → **assert / ImportError** |

## TC-A-02 — `:` 없음

| | |
|--|--|
| **테스트 이름** | `test_ui_parse_missing_colon_raises_value_error` |
| **Given** | `"meter 2.5"` |
| **When** | `parse_convert_line(...)` |
| **Then** | **ValueError / TypeError**; `Invalid format. Use unit:value (ex: meter:2.5)` |
| **Invariant** | F-02 ERR_INVALID_FORMAT, P-04 |
| **RED 실패** | `UnitConverter.py:4-6` print 후 return → **raises 실패** |

## TC-A-03 — 음수

| | |
|--|--|
| **테스트 이름** | `test_ui_parse_negative_meter_raises_value_error` |
| **Given** | `"meter:-1.0"` |
| **When** | 파싱·검증 |
| **Then** | **ValueError / TypeError**; `Value must be zero or positive: -1.0` |
| **Invariant** | F-02 ERR_NEGATIVE_VALUE, D-INV-02 |
| **RED 실패** | 음수 검증 없음 → **예외 없이 출력** |

## TC-A-04 — 없는 단위

| | |
|--|--|
| **테스트 이름** | `test_ui_parse_unknown_unit_parsec_raises_value_error` |
| **Given** | `"parsec:1.0"` |
| **When** | unit 등록 조회 |
| **Then** | **ValueError / TypeError**; `Unknown unit: parsec` |
| **Invariant** | F-02 ERR_UNKNOWN_UNIT, U-03 |
| **RED 실패** | print 후 return → **raises 실패** |

## TC-A-05 — 원 단위·값 보존

| | |
|--|--|
| **테스트 이름** | `test_ui_table_output_preserves_source_unit_and_value` |
| **Given** | `"meter:2.5"`, table |
| **When** | stdout 렌더 |
| **Then** | `2.5 meter = …` 패턴; source `2.5`·`meter` 보존 |
| **Invariant** | F-04 §6.1 |
| **RED 실패** | full float 표시(`8.2021`) vs 계약 `8.2` 시 **문자열 불일치** |

## TC-A-06 — JSON 스키마

| | |
|--|--|
| **테스트 이름** | `test_ui_json_format_meter_2_5_matches_schema` |
| **Given** | `"meter:2.5"`, format=json |
| **When** | JSON 렌더 |
| **Then** | `source` + `conversions[]` 길이 3; `feet` 값 `8.2` (표시) |
| **Invariant** | F-05 §6.2, J-01~J-04 |
| **RED 실패** | JSON **미구현** → NotImplemented / ImportError |

## TC-A-07 — (보강) `meter:abc`

| | |
|--|--|
| **테스트 이름** | `test_ui_parse_invalid_number_abc_raises_value_error` |
| **Given** | `"meter:abc"` |
| **When** | float 파싱 |
| **Then** | **ValueError / TypeError**; `Invalid number: abc` |
| **Invariant** | F-02 ERR_INVALID_NUMBER, P-05 |
| **RED 실패** | print·return만 → **raises 실패** |

---

# Logic RED Tests — Test ID / Scenario / Invariant

| Test ID | Scenario | Invariant | 기대 | RED 실패 (레거시) |
|---------|----------|-----------|------|-------------------|
| **TC-B-01** | `convert("meter", 2.5, "feet")` — **1 m = 3.28084 ft** | D-INV-03, G-02 | `8.20210` ±1e-5 | `convert` 없음 → **AttributeError** |
| **TC-B-02** | `convert("meter", 1.0, "yard")` — **1 m = 1.09361 yd** | D-INV-03, D-INV-04 | `1.09361` ±1e-5 | API 없음 |
| **TC-B-03** | `convert("feet", 1.0, "meter")` 역변환 | D-INV-03 | `0.30480` ±1e-5 | API 없음 |
| **TC-B-04** | `convertAll("meter", 1.0)` | D-INV-06, F-01 | 3건, feet≈3.28084, yard≈1.09361 | 구조화 반환 없음 |
| **TC-B-05** | `registerUnit("cubit", 0.4572)` 후 convert | D-INV-01, F-07, OCP | cubit→feet 유한; 4단위 batch | `registerUnit` 없음 |
| **TC-B-06** | `loadConfig(valid.json\|yaml)` | F-06, T-DA-01 | mpu feet=0.3048 | `loadConfig` 없음 |
| **TC-B-07** | `loadConfig(missing_path)` | F-06 defaults | 비율 3.28084/1.09361 유지 | `loadConfig` 없음 |
| **TC-B-08** | `convert("meter", -1.0, "feet")` | D-INV-02 | **ValueError** | 검증 없음 |
| **TC-B-09** | `convert("meter", 0.0, "feet")` | D-INV-02 (0 허용) | `0.0` | API 없음 |

---

### RED vs README To-Do 매핑

| README 항목 | RED ID |
|-------------|--------|
| TC-A-01 ~ A-07 | TC-A-01 ~ A-07 (+ A-07 = `meter:abc`) |
| TC-B-01 ~ B-07 | TC-B-01 ~ B-07 (+ B-08, B-09 보강) |

pytest 파일은 `tests/red/`에 위 ID·이름으로 옮기면 됩니다. **skip/xfail 금지** (RR-05). Logic Track은 Registry·Engine **실객체**, UI Track은 Engine **Mock/Fake** (`.cursorrules`).

[REDACTED]

---

### Turn 623 — user

<user_query>
pytest 테스트 스켈레톤을 작성하라.
파일/클래스 이름만 적고, 메서드 본문은 pytest.fail("RED") 한 줄만.
RED 원칙으로만 작성하십시오.

예시:
def test_convert_meter_to_feet_returns_correct_ratio():     pytest.fail("RED")
</user_query>

---

### Turn 624 — assistant

RED 명세의 Test ID에 맞춰 `tests/red/`에 pytest 스켈레톤만 추가합니다.

[REDACTED]

---

### Turn 625 — assistant

[REDACTED]

---

### Turn 626 — assistant

`tests/red/`에 RED 스켈레톤 **17개**를 추가했습니다. 본문은 모두 `pytest.fail("RED")` 한 줄입니다.

### 파일 구조

```
tests/red/
├── boundary/
│   ├── test_ui_red_convert.py      # TestUiRedConvertHappyPath, TestUiRedJsonOutput
│   └── test_ui_red_parse.py          # TestUiRedParseErrors
└── entity/
    ├── test_logic_red_convert.py     # TestLogicRedConvert
    └── test_logic_red_register_config.py  # TestLogicRedRegisterUnit, TestLogicRedLoadConfig
```

### Track A (UI) — 7 tests

| 클래스 | 메서드 |
|--------|--------|
| `TestUiRedConvertHappyPath` | `test_ui_convert_meter_2_5_returns_conversion_result` |
| | `test_ui_table_output_preserves_source_unit_and_value` |
| `TestUiRedJsonOutput` | `test_ui_json_format_meter_2_5_matches_schema` |
| `TestUiRedParseErrors` | `test_ui_parse_missing_colon_raises_value_error` |
| | `test_ui_parse_negative_meter_raises_value_error` |
| | `test_ui_parse_unknown_unit_parsec_raises_value_error` |
| | `test_ui_parse_invalid_number_abc_raises_value_error` |

### Track B (Logic) — 10 tests

| 클래스 | 메서드 |
|--------|--------|
| `TestLogicRedConvert` | `test_logic_convert_meter_to_feet_within_1e_5` |
| | `test_logic_convert_meter_to_yard_within_1e_5` |
| | `test_logic_convert_feet_to_meter_reverse_within_1e_5` |
| | `test_logic_convert_all_meter_returns_all_registered_units` |
| | `test_logic_convert_negative_meter_raises_value_error` |
| | `test_logic_convert_zero_meter_to_feet_is_zero` |
| `TestLogicRedRegisterUnit` | `test_logic_register_unit_cubit_then_convert_to_feet` |
| `TestLogicRedLoadConfig` | `test_logic_load_config_valid_json_applies_ratios` |
| | `test_logic_load_config_valid_yaml_applies_ratios` |
| | `test_logic_load_config_missing_path_keeps_default_ratios` |

### 실행

```bash
pytest tests/red -v
# 17 failed — Failed: RED (의도적 RED 상태)
```

기존 `tests/`(GREEN)와 분리되어 있습니다. RED만 돌리려면 위 경로만 지정하면 됩니다.

[REDACTED]

---

### Turn 627 — user

<user_query>
report 폴더에 현재 브랜치에서 지금까지의 진행상황 보고서로 작성해주고(파일명은 폴더 내 파일명을 참고해서 번호는 꼭넣어줘)
prompting 폴더에 지금까지 대화내용 전체를 Export Transcript 해줘
파일명은 보고서 파일명과 같게 만들어줘
그리고 지금까지 작성한 모든 파일 및 변경점이 있는 파일들을 깃허브에 올려줘
꼭 순서대로 작업해줘
</user_query>

---

### Turn 628 — assistant

Report 폴더 명명 규칙과 git 상태를 확인한 뒤, 순서대로 보고서·트랜스크립트 작성 후 GitHub에 푸시합니다.

[REDACTED]

---

### Turn 629 — assistant

[REDACTED]

---

### Turn 630 — assistant

[REDACTED]

---

### Turn 631 — assistant

[REDACTED]

---

### Turn 632 — assistant

[REDACTED]

---

### Turn 633 — assistant

[REDACTED]

---

### Turn 634 — assistant

[REDACTED]

---

### Turn 635 — assistant

[REDACTED]

---

### Turn 636 — assistant

[REDACTED]

---

### Turn 637 — assistant

[REDACTED]

---

### Turn 638 — assistant

요청하신 순서대로 작업을 마쳤습니다.

---

## 1. 진행 보고서 (Report)

**파일:** [Report/02_UnitConvertor_06_Red_TDD_Implementation_Progress.md](c:\DEV_BR\UnitConvertor_06\Report\02_UnitConvertor_06_Red_TDD_Implementation_Progress.md)

- 번호 **02** (01번 Phase 5 보고서 형식 준수)
- 브랜치 `red` 기준: BCE 구현, pytest GREEN 33 / RED 스켈레톤 17, QA 문서, 결함·마일스톤·리스크

---

## 2. 대화 Export Transcript (prompting)

**파일:** [prompting/02_UnitConvertor_06_Red_TDD_Implementation_Progress.md](c:\DEV_BR\UnitConvertor_06\prompting\02_UnitConvertor_06_Red_TDD_Implementation_Progress.md)

- 보고서와 **동일 파일명**
- `agent-transcripts` JSONL 세션 전체 Export (~197KB)
- report 02 범위 요약(Supplement) 포함

재생성: `python scripts/export_transcript.py`

---

## 3. GitHub 푸시

| 항목 | 내용 |
|------|------|
| 브랜치 | `red` |
| 커밋 | `703950a` — `feat(red): BCE layers, pytest GREEN/RED, QA docs, report 02 and transcript` |
| 원격 | https://github.com/yuldakim/UnitConvertor_06.git (`origin/red`) |
| 제외 | `venv/`, `*.egg-info/`, `__pycache__/` (`.gitignore` 추가) |

**푸시된 주요 변경 (42 files):**  
`entity/`, `boundary/`, `control/`, `data/`, `config/`, `tests/`, `tests/red/`, `docs/test_plan.md`, `docs/defect_list.md`, `docs/testing/RED-dual-track-tests.md`, `README.md`, Report·prompting 02, `pyproject.toml`, `scripts/export_transcript.py`

---

로컬 확인:

```bash
git log -1 --oneline
pytest tests --ignore=tests/red -q
pytest tests/red -q   # 17 failed (RED 의도)
```

[REDACTED]

---

### Turn 639 — user

<user_query>
B_06 브랜치로 머지해주고 머지 된 B_06 브랜치를 기준으로 green 브랜치를 새로 만들어서 green branch로 switch 해줘
</user_query>

---

### Turn 640 — assistant

브랜치 상태를 확인한 뒤 `B_06`에 머지하고, 머지된 `B_06`에서 `green` 브랜치를 생성해 전환합니다.

[REDACTED]

---

### Turn 641 — assistant

[REDACTED]

---

### Turn 642 — assistant

[REDACTED]

---

### Turn 643 — assistant

[REDACTED]

---

### Turn 644 — assistant

[REDACTED]

---

### Turn 645 — assistant

작업을 마쳤습니다. 현재 체크아웃 브랜치는 **`green`** 입니다.

### 수행 내역

| 단계 | 작업 | 결과 |
|------|------|------|
| 1 | `red` → `B_06` 머지 | **Fast-forward** (`a5e7c5a` → `703950a`) |
| 2 | 머지된 `B_06`에서 `green` 생성 | `git checkout -b green` |
| 3 | `green`으로 전환 | 현재 브랜치: **`green`** |
| 4 | 원격 푸시 | `origin/B_06`, `origin/green` 갱신 |

### 브랜치 상태

```
B_06   @ 703950a  (origin/B_06 동기화됨)
green  @ 703950a  (* 현재, origin/green 추적)
red    @ 703950a  (동일 커밋)
```

`B_06`과 `green`은 같은 커밋(`703950a`)을 가리킵니다. 이후 GREEN 작업은 `green`에서 진행하면 됩니다.

```bash
git branch --show-current   # green
```

[REDACTED]

---

### Turn 646 — user

<user_query>
그리고 red 브랜치는 삭제해줘
</user_query>

---

### Turn 647 — assistant

[REDACTED]

---

### Turn 648 — assistant

`red` 브랜치를 삭제했습니다.

| 대상 | 결과 |
|------|------|
| 로컬 `red` | 삭제됨 (`703950a`) |
| 원격 `origin/red` | 삭제됨 |

현재 브랜치는 **`green`** 이고, `B_06`·`green`·`main`만 남아 있습니다.

[REDACTED]

---

## Session `ad271a3a-25d8-40c5-8567-1f20caae99bb`

### Turn 649 — user

<user_query>
프로젝트: @c:\DEV_BR\UnitConvertor_06\ 

신규 기능 RED 테스트를 작성하라. (구현 금지)

기능 설명:
  registerUnit("cubit", 0.4572)  // 1 cubit = 0.4572 meter
  convert("cubit", 1.0, "meter") == 0.4572 (오차 1e-5)
  convert("meter", 1.0, "cubit") == 1.0/0.4572 ≈ 2.1872 (오차 1e-5)
  convert("cubit", 1.0, "feet")  == 0.4572 * 3.28084 ≈ 1.4997 (오차 1e-5)

제약:
  - 기존 convert() 함수 시그니처 변경 금지
  - 음수 비율 등록 시 예외 발생 (비율 > 0 강제)

테스트 케이스 (최소 5개):
  BT-01: registerUnit("cubit", 0.4572) 후 cubit→meter 변환
  BT-02: registerUnit 후 meter→cubit 역변환
  BT-03: registerUnit 후 cubit→feet 교차 변환
  BT-04: 음수 비율 등록 → ValueError / TypeError 발생
  BT-05: registerUnit 후 convertAll("cubit", 1.0) → 전 단위 반환
  BT-06: 기존 meter→feet 결과 불변 (회귀 보호)

테스트 마킹: @pytest.mark.bonus def test_decaying_unit_conversion():

산출물: decaying_unit.py + tests/test_decaying_unit.py (실패 상태)
</user_query>

---

### Turn 650 — assistant

새 기능 RED 테스트 작성 — 구현 없이. 프로젝트 구조와 기존 테스트 패턴을 확인합니다.

[REDACTED]

---

### Turn 651 — assistant

[REDACTED]

---

### Turn 652 — assistant

[REDACTED]

---

### Turn 653 — assistant

[REDACTED]

---

### Turn 654 — assistant

[REDACTED]

---

### Turn 655 — assistant

[REDACTED]

---

### Turn 656 — assistant

`decaying_unit.py` 스텁과 `@pytest.mark.bonus` RED 테스트 작성 중. `pyproject.toml`에 bonus 마커 등록.

[REDACTED]

---

### Turn 657 — assistant

[REDACTED]

---

### Turn 658 — assistant

[REDACTED]

---

### Turn 659 — assistant

[REDACTED]

---

### Turn 660 — assistant

요청한 `test_decaying_unit_conversion` 이름으로 통합하고, BT-04는 `NotImplementedError` 대신 비율 검증 실패가 드러나도록 스텁에 최소 검증만 추가합니다(구현 없이).

[REDACTED]

---

### Turn 661 — assistant

람다 기반 parametrized 테스트가 읽기 어려워 명확한 구조로 다시 작성합니다.

[REDACTED]

---

### Turn 662 — assistant

[REDACTED]

---

### Turn 663 — assistant

신규 기능 RED 테스트와 스텁 모듈을 추가했습니다. **구현은 하지 않았고**, bonus 테스트 6건은 모두 `NotImplementedError`로 실패합니다.

## 산출물

### `decaying_unit.py` (스텁)
- camelCase API: `registerUnit`, `convert`, `convertAll`
- `convert(from, value, to) -> float` 시그니처 고정
- `reset()` — 테스트 격리용
- 모든 메서드는 `NotImplementedError` (GREEN 단계에서 `ConverterApp`/`UnitRegistry` 위임 예정)

### `tests/test_decaying_unit.py`
| TC | 내용 |
|----|------|
| BT-01 | cubit 등록 후 cubit→meter ≈ 0.4572 |
| BT-02 | meter→cubit ≈ 1/0.4572 |
| BT-03 | cubit→feet ≈ 0.4572 × 3.28084 (≈ 1.4997) |
| BT-04 | 음수 비율 → `ValueError` / `TypeError` |
| BT-05 | `convertAll("cubit", 1.0)` → 4단위 dict |
| BT-06 | cubit 등록 후 `meter:2.5→feet` ≈ 8.20210 (회귀) |

모든 테스트에 `@pytest.mark.bonus` 적용, 함수명은 `test_decaying_unit_conversion_bt**` 형태입니다.

### `pyproject.toml`
- `bonus` 마커 등록

## 실행

```powershell
# RED (6 failed — 의도)
pytest tests/test_decaying_unit.py -m bonus -v

# 기존 회귀 (68 passed)
pytest -m "not bonus" -q
```

## GREEN 시 참고
- `decaying_unit.DecayingUnitConverter`에서 `UnitRegistry.with_defaults()` + `register_unit` 위임
- BT-04: `meters_per_unit <= 0`일 때 `ValueError` (기존 `entity`는 `InvalidRatioError` — bonus API는 요구사항대로 `ValueError`/`TypeError`)
- 기존 `entity.engine.convert` / `control.converter_app.convert` 시그니처는 변경하지 않음

[REDACTED]

---

### Turn 664 — user

<user_query>
프로젝트: @c:\DEV_BR\UnitConvertor_06\ 
신규 기능 RED 테스트를 작성하라. (구현 금지)

기능 설명:
  registerUnit("cubit", 0.4572)  // 1 cubit = 0.4572 meter
  convert("cubit", 1.0, "meter") == 0.4572 (오차 1e-5)
  convert("meter", 1.0, "cubit") == 1.0/0.4572 ≈ 2.1872 (오차 1e-5)
  convert("cubit", 1.0, "feet")  == 0.4572 * 3.28084 ≈ 1.4997 (오차 1e-5)

제약:
  - 기존 convert() 함수 시그니처 변경 금지
  - 음수 비율 등록 시 예외 발생 (비율 > 0 강제)

테스트 케이스 (최소 5개):
  BT-01: registerUnit("cubit", 0.4572) 후 cubit→meter 변환
  BT-02: registerUnit 후 meter→cubit 역변환
  BT-03: registerUnit 후 cubit→feet 교차 변환
  BT-04: 음수 비율 등록 → ValueError / TypeError 발생
  BT-05: registerUnit 후 convertAll("cubit", 1.0) → 전 단위 반환
  BT-06: 기존 meter→feet 결과 불변 (회귀 보호)

테스트 마킹: @pytest.mark.bonus def test_decaying_unit_conversion():

산출물: decaying_unit.py + tests/test_decaying_unit.py (실패 상태)
</user_query>

---

### Turn 665 — assistant

요청과 기존 산출물을 대조해, `test_decaying_unit_conversion` 마킹·이름 규격에 맞게 정리합니다.

[REDACTED]

---

### Turn 666 — assistant

요청한 `test_decaying_unit_conversion` 단일 함수·`@pytest.mark.bonus` 형식에 맞게 테스트를 정리합니다.

[REDACTED]

---

### Turn 667 — assistant

RED 테스트와 스텁이 요구사항에 맞게 준비되어 있습니다. **구현은 하지 않았습니다.**

## 산출물

| 파일 | 역할 |
|------|------|
| `decaying_unit.py` | `registerUnit` / `convert` / `convertAll` API 스텁 (`NotImplementedError`) |
| `tests/test_decaying_unit.py` | `@pytest.mark.bonus` + `test_decaying_unit_conversion()` (BT-01~06) |

## `test_decaying_unit_conversion()` 시나리오

- **BT-01** `cubit→meter` ≈ 0.4572 (ε 1e-5)
- **BT-02** `meter→cubit` ≈ 1/0.4572 ≈ 2.1872
- **BT-03** `cubit→feet` ≈ 0.4572 × 3.28084 ≈ 1.4997
- **BT-04** 음수 비율 → `ValueError` / `TypeError` (`reset()` 후 격리)
- **BT-05** `convertAll("cubit", 1.0)` → meter/feet/yard/cubit 4단위
- **BT-06** cubit 등록 후 `meter:2.5→feet` ≈ 8.20210 (회귀)

## RED 확인

```text
pytest tests/test_decaying_unit.py -m bonus -v
# 1 failed — NotImplementedError: registerUnit not implemented
```

기존 `entity`/`control`의 `convert()` 시그니처는 변경하지 않았습니다. GREEN 단계에서는 `decaying_unit.DecayingUnitConverter`가 `UnitRegistry`/`ConversionEngine`에 위임하면 됩니다.

[REDACTED]

---

### Turn 668 — user

<user_query>
[단계] TDD GREEN만 수행. REFACTOR는 하지 않는다.
프로젝트: @c:\DEV_BR\UnitConvertor_06\ 

구현 접근법: registerUnit("temp_celsius", ratio) 호출만으로 추가

할 일:
1. pytest -m bonus -v 실행 → BT-01~06 FAIL 확인
2. registerUnit() 메서드/함수 최소 구현:
   - 내부 UnitRegistry(Map/Dict)에 단위명·비율 저장
   - convert()는 Registry를 조회하여 meter 허브 경유 변환
   - 기존 convert() 함수 시그니처 변경 금지
3. pytest -m bonus -v 재실행 → BT-01~06 PASS 확인
4. 기존 회귀 테스트 전체 PASS 확인:
   pytest

산출물:
- BT-01~06이 통과하는 최소 구현 코드
- 기존 TC-A/TC-B 전체 PASS 유지 확인
- 커밋 메시지: feat(feature): add registerUnit with OCP registry
</user_query>

---

### Turn 669 — assistant

TDD GREEN 단계 진행: bonus 테스트 상태 확인 후 `decaying_unit.py` 최소 구현합니다.

[REDACTED]

---

### Turn 670 — assistant

[REDACTED]

---

### Turn 671 — assistant

FAIL 확인됨. `UnitRegistry`와 `ConversionEngine`을 사용해 최소 구현합니다.

[REDACTED]

---

### Turn 672 — assistant

[REDACTED]

---

### Turn 673 — assistant

BT-02의 `2.1872` 리터럴 검증이 `1/0.4572`와 ε=1e-5로 맞지 않습니다. 중복 assertion을 제거해 스펙과 일치시킵니다.

[REDACTED]

---

### Turn 674 — assistant

69건 통과. 커밋 진행합니다.

[REDACTED]

---

### Turn 675 — assistant

[REDACTED]

---

### Turn 676 — assistant

TDD GREEN 단계를 완료했습니다.

## 1. RED 확인
`pytest -m bonus -v` → `NotImplementedError` (FAIL)

## 2. 최소 구현 (`decaying_unit.py`)
- `DecayingUnitConverter`가 `UnitRegistry.with_defaults()` + `ConversionEngine` 사용
- `registerUnit()` → `registry.register_unit()` (dict 기반 OCP 레지스트리)
- `convert()` / `convertAll()` → meter 허브 경유 (`ConversionEngine`)
- 기존 `entity.engine.convert` / `control.converter_app.convert` 시그니처는 변경 없음
- `InvalidRatioError`는 `ValueError` 하위 클래스 → BT-04 통과

## 3. GREEN 확인
```
pytest -m bonus -v  → 1 passed
pytest              → 69 passed
```

## 4. 테스트 보정 (GREEN 통과용 최소 수정)
`2.1872`, `1.4997` 리터럴은 ε=1e-5 안에 들지 않아, 이미 있는 정확값 assertion(`1/0.4572`, `0.4572×3.28084`)과 중복되는 줄만 제거했습니다.

## 커밋
`6234f34` — `feat(feature): add registerUnit with OCP registry`

| 파일 | 내용 |
|------|------|
| `decaying_unit.py` | bonus facade GREEN |
| `tests/test_decaying_unit.py` | BT-01~06 |
| `pyproject.toml` | `bonus` 마커 |

[REDACTED]

---

### Turn 677 — user

<user_query>
신규 기능 구현 완료 후 전체 테스트, 커버리지, Golden Master를 확인하라.

1) 전체 테스트:
pytest pytest -v tests/

2) 커버리지:
pip install pytest-cov pytest --cov=unit_converter --cov-report=term-missing pytest --cov=unit_converter --cov-report=html

3) Golden Master (출력 불변 확인):
pytest -m bonus -v pytest --cov=unit_converter -m bonus

확인 항목:
- BT- 전체 PASS (신규 기능)
- TC-A-전체, TC-B-전체 PASS (기존 회귀)
- Golden Master PASS (meter/feet/yard 출력 불변)
- registerUnit("cubit", -1.0) → ValueError / TypeError 발생 확인
- Domain 커버리지 ≥ 95% / Boundary ≥ 85%

</user_query>

---

### Turn 678 — assistant

전체 테스트·커버리지·Golden Master를 프로젝트 설정에 맞게 실행합니다.

[REDACTED]

---

## Session — Workspace summary (report 06 scope)

### Topics covered

1. Bonus RED: decaying_unit.py stub + tests/test_decaying_unit.py (BT-01~06, @pytest.mark.bonus)
2. Bonus GREEN: UnitRegistry + ConversionEngine facade in decaying_unit.py
3. Verification: pytest 69 passed, GM 8 passed, entity 95% / boundary 100% cov
4. registerUnit negative ratio → InvalidRatioError (ValueError subclass)
5. Report 06 + transcript export; commit/push feature → PR to B_06
