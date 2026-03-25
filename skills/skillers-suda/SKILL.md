---
name: skillers-suda
description: This skill should be used when the user asks to "스킬 만들어줘", "에이전트 만들어줘", "커맨드 만들어줘", "스킬러들의 수다", "수다", "skill builder", "make a skill", "create a skill", "build a skill".
---

# 스킬러들의 수다

> 4명의 전문가 에이전트를 실제로 소집하여 토론시키고, 그 결과로 바이브코더의 아이디어를 동작하는 스킬로 변환합니다.

---

## WHEN TRIGGERED - EXECUTE IMMEDIATELY

**이 문서는 참고 문서가 아니라 실행 지시서다.**
- 첫 번째 action: 아래 워크플로우의 첫 AskUserQuestion 도구를 즉시 호출
- 텍스트 출력 후 질문하지 않는다. 도구를 먼저 호출한다.
- 모든 질문은 AskUserQuestion 도구 호출로만 진행한다.

---

## 워크플로우 개요

```
Phase A → B → C → D → E → E-verify → F → G(반복) → H → I
아이디어  토론  인터뷰  설계   생성    검증    eval  개선   최적화  패키징
```

### 질문 규칙 (모든 AskUserQuestion 호출 시 준수)

| 규칙 | 설명 |
|------|------|
| AskUserQuestion 필수 | 모든 질문은 반드시 AskUserQuestion 도구를 즉시 호출 |
| 설명 필수 | 모든 옵션의 description에 "뭔지 + 장단점" 포함 |
| 추천 표시 | 가장 적합한 옵션 label에 "(추천)" 붙이고 첫 번째 배치 |
| 쉬운 말 | 전문 용어 대신 일상 비유 사용 |
| 한 번에 하나 | 질문은 1개씩 |
| 기타 옵션 불필요 | AskUserQuestion이 자동으로 "Other" 제공 |

---

### Phase A: 아이디어 수집

대화 컨텍스트에 워크플로우가 있으면 (예: "이걸 스킬로 만들어줘") 히스토리에서 답을 먼저 추출.
슬래시 커맨드 인수로 아이디어가 제공되었으면 그대로 사용. 없으면 AskUserQuestion 호출.

**EXECUTE:** `references/phase-execution.md` Phase A 섹션의 JSON으로 AskUserQuestion 즉시 호출.

아이디어가 모호하면 1개 추가 질문으로 구체화. 명확하면 바로 Phase B.

---

### Phase B: 전문가 팀 소집 + 토론

**반드시 Agent 도구를 사용하여 4개 에이전트를 동시에 (하나의 메시지에서) 스폰한다.**

1. 팀 소집 안내 출력 (`references/phase-execution.md` 참조)
2. 4개 에이전트 병렬 스폰 — 설정은 `references/phase-execution.md`, 프롬프트는 `references/interview-guide.md` 섹션 2-1 참조
3. 응답을 자연스러운 대화 형식으로 종합 — 출력 포맷은 `references/phase-execution.md` 참조
4. 의견 충돌이 있으면 반드시 보여준다
5. 방향 확인 AskUserQuestion 호출 — "다시 토론해줘" 선택 시 Step 2부터 재실행

---

### Phase C: 상세 인터뷰 (0-2개 추가 질문)

팀 토론에서 자동 판단한 내용: purpose, input/output type, trigger keywords, domain, constraints.
불확실한 항목에 대해서만 AskUserQuestion 호출 (최대 2개). 충분하면 스킵.

**EXECUTE:** `references/phase-execution.md` Phase C 섹션 참조.

---

### Phase D: 워크플로우 설계

팀 토론 결과 + 사용자 답변을 바탕으로 워크플로우를 설계한다.

1. **단계 타입 선택** — 6가지 타입 상세: `references/workflow-step-types.md`
2. **컴포넌트 타입 결정** — 스킬/에이전트/커맨드 판단: `references/component-type-decision.md`
3. **자유도 식별** — 고정 요소(워크플로우 구조, 필수 검증)와 가변 요소(사용자 변경 가능 파라미터) 구분. 가변 요소가 있으면 SKILL.md에 Settings 섹션으로 명시.
4. **Eval 기준 정의** — evals.json 형식으로 should-trigger/should-not-trigger 시나리오 정의. 스키마: `references/schemas.md`, 상세: `references/eval-guide.md`
5. **사용자 확인** — 워크플로우 + eval을 AskUserQuestion markdown 프리뷰로 확인

**EXECUTE:** `references/phase-execution.md` Phase D 섹션의 JSON으로 AskUserQuestion 호출.

---

### Phase E: 파일 생성

확인된 워크플로우를 실제 파일로 만든다. 파일 구조/템플릿: `references/phase-execution.md` Phase E 섹션 참조.

**Description 작성 (Pushy 전략):**
- 스킬이 하는 것 + 구체적 트리거 상황을 함께 기술 (undertrigger 방지)
- 한/영 혼합 트리거 포함
- Phase H에서 `scripts/run_loop.py`로 자동 최적화
- 상세: `references/trigger-mechanism.md`

**Writing Style:** imperative form, third-person description, why 설명 우선, 1,500-2,000 단어 이내. 상세: `references/writing-style-guide.md`

**파일 덮어쓰기 규칙:** 같은 이름의 파일이 있으면 반드시 사용자에게 확인. 동의 없이 덮어쓰지 않는다.

---

### Phase E-verify: 자동 검증

파일 생성 직후 검증 스크립트 실행:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/skillers-suda/scripts/verify-skill.py" <생성된 SKILL.md 경로>
```

| 결과 | 조치 |
|------|------|
| 전체 PASS | Phase F로 진행 |
| WARN 있음 | 사용자에게 안내 후 Phase F 진행 |
| FAIL 있음 | 자동 수정 → 재검증 (상세: `references/eval-guide.md`) |

---

### Phase F: 자동 Eval 실행 + 벤치마크

1. evals.json을 `evals/evals.json`으로 저장
2. 각 eval 케이스마다 **with_skill + without_skill(baseline)** 2개 subagent 병렬 스폰
3. 결과를 `{skill-name}-workspace/iteration-{N}/eval-{ID}/`에 저장
4. 채점 (`references/agents/grader.md`) → 벤치마크 집계 → 분석 (`references/agents/analyzer.md`)
5. 뷰어 실행: `python assets/eval-viewer/generate_review.py ...`
6. 사용자 피드백 수집 후 AskUserQuestion 호출

**EXECUTE:** `references/phase-execution.md` Phase F 섹션의 JSON으로 AskUserQuestion 호출.

---

### Phase G: 반복 개선

피드백 기반으로 스킬을 개선하고 다시 테스트한다. 개선 원칙: `references/improvement-principles.md`

**반복 루프:** 수정 → 새 iteration 디렉토리에 재실행(baseline 포함) → `--previous-workspace`로 비교 뷰어 → 사용자 리뷰 → 만족할 때까지 반복.

블라인드 비교가 필요하면: `references/agents/comparator.md` + `references/agents/analyzer.md`

---

### Phase H: Description 최적화

run_loop.py로 description을 자동 최적화하여 트리거 정확도를 높인다.
상세 실행 절차: `references/phase-execution.md` Phase H 섹션 참조.

---

### Phase I: 패키징

`present_files` 도구가 있을 때만 실행:

```bash
python -m scripts.package_skill {스킬 폴더 경로}
```

---

## AI 행동 규칙

### 반드시 지킬 것

- 인터뷰 없이 파일을 만들지 않는다
- **Phase B에서 반드시 4개 에이전트를 병렬 스폰** (시뮬레이션 금지, 하나의 메시지에서 동시 스폰)
- 워크플로우 확인 없이 생성하지 않는다
- API > MCP > 직접 구현 우선순위
- SKILL.md 본문 1,500-2,000 단어 이내 (상세는 references/로 분리)
- Writing Style 규칙 적용 (imperative form, third-person description, why 설명)
- Phase D에서 eval 시나리오 + 자유도 반드시 정의
- Phase E에서 Pushy description 작성
- Phase E 후 verify-skill.py 반드시 실행 (FAIL 시 자동 수정)
- Phase F에서 eval 자동 실행 (subagent 병렬 + baseline 비교 + 벤치마크)
- Phase H에서 run_loop.py로 description 자동 최적화 (train/test 분할)

### 절대 하지 말 것

- 4명의 대화를 텍스트로 시뮬레이션하기 (반드시 Agent 도구로 실제 스폰)
- 인터뷰 질문 5개 초과 (Phase A 1-2개 + Phase C 1-2개 = 최대 4개)
- api_mcp/rag 결과를 검토 없이 최종 출력으로 사용
- 사용자 동의 없이 파일 덮어쓰기
- eval 케이스를 하드코딩으로 통과시키기 (일반화 원칙 위반)
- 사용자 리뷰 없이 eval 결과를 직접 판단 (뷰어 제공 필수)

---

## References

### Phase 실행 상세
- **`references/phase-execution.md`** — AskUserQuestion JSON 템플릿, 출력 포맷, 파일 생성 템플릿

### 작성 가이드
- **`references/writing-style-guide.md`** — SKILL.md 작성 규칙
- **`references/trigger-mechanism.md`** — 트리거 메커니즘, pushy description 전략
- **`references/improvement-principles.md`** — 반복 개선 원칙

### Eval & 검증
- **`references/eval-guide.md`** — Eval 방법론, 자동 검증, 자동 수정 규칙
- **`references/schemas.md`** — evals.json, grading.json, benchmark.json 스키마
- **`references/agents/grader.md`** — assertion 채점 에이전트
- **`references/agents/comparator.md`** — 블라인드 A/B 비교 에이전트
- **`references/agents/analyzer.md`** — 벤치마크 분석 에이전트

### 설계 가이드
- **`references/interview-guide.md`** — 인터뷰 방법론 + 페르소나 에이전트 설계
- **`references/workflow-step-types.md`** — 6가지 단계 타입 상세
- **`references/component-type-decision.md`** — 스킬/에이전트/커맨드 판단 기준
- **`references/mcp-catalog.md`** — MCP 서버 카탈로그

### 스크립트 & 도구
- **`scripts/`** — verify-skill.py, run_eval.py, run_loop.py, aggregate_benchmark.py, generate_report.py, improve_description.py, package_skill.py, quick_validate.py
- **`assets/eval-viewer/`** — eval 결과 브라우저 뷰어
- **`assets/eval_review.html`** — description 최적화용 eval 리뷰 템플릿
- **`references/script-templates.md`** — Python/Bash 스크립트 템플릿
- **`references/api-mcp-integration.md`** — API/MCP 연동 가이드
