# 02 — UnitConvertor_06 RED·TDD 구현·테스트 진행 보고서

| 항목 | 내용 |
|------|------|
| 문서 번호 | 02 |
| 프로젝트 | UnitConvertor_06 (Python 길이 단위 변환 학습 시스템) |
| 작업 기간 | 2026-05-20 ~ 2026-05-21 |
| 기준 PRD | [docs/PRD.md](../docs/PRD.md) (PRD-UC-06-001) |
| **현재 브랜치** | `red` |
| 선행 보고서 | [01_UnitConvertor_06_Phase5_Spec_Documentation.md](01_UnitConvertor_06_Phase5_Spec_Documentation.md) |
| 작성 | AI 보조 세션 (Dual-Track TDD · pytest) |

---

## 1. Executive Summary

`red` 브랜치에서 Phase 5(문서·계약) 이후 **Dual-Track TDD** 착수 단계를 진행했다. **BCE 레이어**(entity / boundary / control / data)와 **GREEN pytest 33건**, **RED 스켈레톤 17건**, QA 문서(test_plan, defect_list, RED 명세)를 추가했으며 README는 **RED 단계 To-Do**로 갱신했다.

레거시 `UnitConverter.py`(단일 `main()`, if-else)는 유지·미연동 상태이며, 결함 목록에 **Open** 항목으로 추적 중이다.

**다음 단계:** `tests/red/` RED 스켈레톤에 실제 assert 채우기 → 전 RED GREEN → refactor(M2).

---

## 2. 브랜치·Git 상태

| 항목 | 값 |
|------|-----|
| 브랜치 | `red` (원격 `origin/red` 존재) |
| 기준 커밋 | `a5e7c5a` — Phase 5 문서·README·cursorrules |
| 미커밋 산출물 | BCE 패키지, tests/, docs/, pyproject.toml, Report 02, prompting 02 |

### 권장 브랜치 전략 (세션 산출)

| 브랜치 | 역할 |
|--------|------|
| `main` | 문서 + **전체 pytest GREEN** 만 |
| `red` | RED 스켈레톤·통합 작업 |
| `red/domain/*`, `red/boundary/*` | Dual-Track slice (선택) |
| `green/m1-core` | entity→boundary→integration GREEN |

---

## 3. 작업 범위 및 산출물

### 3.1 문서

| 산출물 | 경로 | 설명 |
|--------|------|------|
| 테스트 계획서 | `docs/test_plan.md` | meter→feet 샘플, 경계값·cov 전략 |
| 결함 목록 | `docs/defect_list.md` | DEF-001~008 |
| RED Dual-Track 명세 | `docs/testing/RED-dual-track-tests.md` | TC-A/B, Given-When-Then |
| README 갱신 | `README.md` | RED To-Do, defect_list 링크 |
| 진행 보고서 | `Report/02_...` (본 문서) | |
| 대화 Export | `prompting/02_...` | Transcript |

### 3.2 구현 (BCE — GREEN 기준)

| 레이어 | 경로 | 핵심 |
|--------|------|------|
| entity | `entity/` | `UnitRegistry`, `ConversionEngine`, 예외, `round_display` |
| boundary | `boundary/` | `parse_convert_line`, table renderer, PRD exact errors |
| control | `control/converter_app.py` | `ConverterApp` 오케스트레이션 |
| data | `data/repository.py` | JSON/YAML load, defaults |
| config | `config/units.json` | 3단위 시드 |

### 3.3 테스트

| 구분 | 경로 | 건수 | 상태 |
|------|------|------|------|
| GREEN (BCE) | `tests/entity`, `boundary`, `data` | 33 | **passed** |
| RED 스켈레톤 | `tests/red/` | 17 | **failed (의도적 `pytest.fail("RED")`)** |
| 레거시 | `UnitConverter.py` | — | 테스트 미연결 |

```bash
pytest tests --ignore=tests/red   # 33 passed
pytest tests/red                  # 17 failed: RED
```

---

## 4. Dual-Track 진행 현황

### 4.1 Track A — UI / Boundary

| RED ID | README To-Do | 스켈레톤 | BCE GREEN 테스트 |
|--------|--------------|----------|------------------|
| TC-A-01 | TC-A-01 | `test_ui_convert_meter_2_5_*` | `test_convert_display_*` |
| TC-A-02~05,07 | TC-A-02~05 | `test_ui_red_parse.py` | `test_exception_parse_*` |
| TC-A-06 | — | `test_ui_json_*` | (JSON renderer M2) |

### 4.2 Track B — Domain / Logic

| RED ID | README To-Do | 스켈레톤 | BCE GREEN 테스트 |
|--------|--------------|----------|------------------|
| TC-B-01~04 | TC-B-01~04 | `test_logic_red_convert.py` | `test_convert_normal_*`, `boundary` |
| TC-B-05 | TC-B-05 | `test_logic_register_*` | `test_register_dynamic_*` |
| TC-B-06~07 | TC-B-06~07 | `test_logic_load_config_*` | `test_config_load_*` |

---

## 5. 결함·품질

| 문서 | 요약 |
|------|------|
| [defect_list.md](../docs/defect_list.md) | DEF-001~005 BCE **Fixed**; DEF-002,003,006~008 레거시 **Open** |
| 커버리지 목표 | entity ≥95%, boundary ≥85% (test_plan) |

---

## 6. PRD / 마일스톤 대비

| 마일스톤 | 상태 | 비고 |
|----------|------|------|
| M0 문서·계약 | ✅ Done | Report 01 |
| M1 v1.0 Core | 🟡 진행 중 | BCE GREEN 33; RED 스켈레톤 17; 레거시 CLI 분리 |
| M2 Quality | ⏳ | JSON/CSV, refactor |
| M3 Release | ⏳ | 회귀 R-1~R7 |

| PRD 항목 | 문서화 | BCE 구현 | 레거시 CLI |
|----------|--------|----------|------------|
| F-01~04 | ✅ | ✅ (table) | 부분 |
| F-02 검증 | ✅ | ✅ | ❌ 음수 등 |
| F-05 JSON | ✅ | ⏳ | ❌ |
| F-06~07 config/등록 | ✅ | ✅ | ❌ |

---

## 7. 리스크·이슈

| # | 리스크 | 완화 |
|---|--------|------|
| R-1 | GREEN(`tests/`) vs RED(`tests/red/`) 이중 트랙 혼선 | CI에서 경로 분리 실행 |
| R-2 | 레거시·BCE 동시 존재 | Quick Start를 `ConverterApp`으로 통일(M2) |
| R-3 | RED 스켈레톤이 `pytest.fail`만 포함 | RED 명세대로 assert 단계적 이관 |

---

## 8. 다음 작업 체크리스트

- [ ] `tests/red/` 각 TC에 Given-When-Then assert 구현 (RED→GREEN)
- [ ] README RED To-Do Track A/B 체크
- [ ] `UnitConverter.py` → boundary adapter 또는 폐기
- [ ] `pytest --cov=entity --cov=boundary` 게이트 CI
- [ ] `main` 머지 전 회귀 R-1~R7

---

## 9. 승인·검토

- [ ] QA: RED 17건 의도적 실패 로그 보관
- [ ] 학습자: GREEN 33건 로컬 재현
- [ ] 리뷰어: defect_list Open 항목 처리 계획

---

*문서 끝.*
