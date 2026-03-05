# Eval 가이드

생성된 스킬의 품질을 체계적으로 검증하기 위한 방법론.
Anthropic의 skill-creator eval 패턴을 skillers-suda 워크플로우에 맞게 적용.

## 1. Eval 기준 정의

스킬 생성 전(Phase D)에 성공 기준을 먼저 정의한다.

### 필수 기준

| 기준 | 설명 | 측정 방법 |
|------|------|-----------|
| 트리거 정확도 | 의도한 입력에 스킬이 활성화되는가 | 3-5개 트리거 문장으로 테스트 |
| 워크플로우 완결성 | 모든 단계가 정상 실행되는가 | 시나리오별 end-to-end 실행 |
| 출력 품질 | 결과물이 기대에 부합하는가 | 사용자 확인 |
| 엣지 케이스 | 예외 상황에서 graceful하게 처리하는가 | 검수자 시나리오 실행 |

### Eval 시나리오 템플릿

각 시나리오는 아래 형식으로 정의:

```
시나리오: {시나리오 이름}
입력: {사용자가 제공할 입력}
기대 행동: {스킬이 해야 할 것}
성공 기준: {무엇이 되어야 "성공"인지}
```

### 시나리오 수

| 스킬 복잡도 | 정상 시나리오 | 엣지 케이스 |
|-------------|-------------|------------|
| 단순 (1-3 단계) | 2개 | 1개 |
| 보통 (4-6 단계) | 3개 | 2개 |
| 복잡 (7+ 단계) | 3-5개 | 3개 |

## 2. 자동 검증 (verify-skill.py)

스킬 생성 직후 `scripts/verify-skill.py`로 구조적 품질을 자동 검증한다.

### 검증 항목

| 항목 | 기준 | 상태 |
|------|------|------|
| frontmatter_exists | YAML frontmatter 존재 | PASS/FAIL |
| name_field | name 필드 존재 | PASS/FAIL |
| description_field | description 필드 존재 | PASS/FAIL |
| third_person | "This skill should be used when..." 형식 | PASS/FAIL |
| trigger_phrases | 3-5개 quoted 트리거 포함 | PASS/WARN/FAIL |
| word_count | 본문 1,500-2,000 단어 (최대 3,000) | PASS/WARN/FAIL |
| imperative_form | second-person 미사용 | PASS/FAIL |
| references_exist | 참조된 파일이 실제 존재 | PASS/FAIL |
| progressive_disclosure | References 섹션 존재 | PASS/WARN |

### 실행 방법

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/skillers-suda/scripts/verify-skill.py" path/to/SKILL.md
```

### 결과 해석

| 상태 | 의미 | 조치 |
|------|------|------|
| PASS | 기준 충족 | 다음 단계 진행 |
| WARN | 권장사항 미충족 | 사용자에게 안내, 선택적 수정 |
| FAIL | 필수 기준 미달 | 반드시 수정 후 재검증 |

## 3. 자동 수정 규칙

FAIL 항목에 대한 자동 수정:

| FAIL 항목 | 자동 수정 |
|-----------|-----------|
| third_person | description을 "This skill should be used when..." 형식으로 변환 |
| trigger_phrases | 워크플로우에서 트리거 키워드 추출하여 추가 |
| imperative_form | second-person 표현을 imperative로 변환 |
| references_exist | 누락 파일 생성 또는 참조 제거 |

word_count FAIL은 자동 수정하지 않음 — 내용 판단이 필요하므로 사용자에게 안내.

## 4. 수동 검증

자동 검증으로 잡을 수 없는 항목:

- **의미적 정확성** — 워크플로우가 논리적으로 올바른가
- **도메인 적합성** — 해당 분야의 용어/관행이 정확한가
- **사용자 경험** — 실제 사용 시 자연스러운가
- **엣지 케이스 대응** — 예외 상황 처리가 적절한가

이 항목들은 Phase F의 테스트 실행으로 검증한다.

## 5. Eval 워크플로우 요약

```
Phase D: 워크플로우 설계 + Eval 기준 정의
  |  워크플로우 + eval 시나리오 확정
  v
Phase E: 파일 생성
  |  스킬 파일 생성
  v
Phase E-verify: 자동 검증
  |  verify-skill.py 실행
  |  FAIL -> 자동 수정 -> 재검증
  |  PASS -> Phase F 진행
  v
Phase F: 수동 검증 (테스트)
  |  eval 시나리오 기반 테스트
  |  사용자 피드백 -> 반복
  v
완성
```
