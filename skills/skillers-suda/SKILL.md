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

## 소개

이 스킬은 코딩을 몰라도 됩니다. 아이디어만 있으면 돼요.

4명의 전문가 에이전트를 **실제로 소집**해서 여러분의 아이디어를 분석합니다. 시뮬레이션이 아니라 진짜 4개의 에이전트가 병렬로 동시에 분석하고, 그 결과를 종합해서 동작하는 스킬/에이전트/커맨드를 만들어드립니다.

**4명의 전문가:**
- **기획자** — 방향을 잡아줘요. "누가 쓸 건데? 뭘 해결하는 거야?"
- **사용자** — UX를 검증해요. "나라면 이걸 어떻게 쓸까?"
- **전문가** — 기술적 가능성을 따져요. "이 분야는 이런 점을 조심해야 해"
- **검수자** — 엣지 케이스를 잡아요. "이거 이 경우에도 돼?"

---

## 워크플로우

### Phase A: 아이디어 수집

**목표:** 만들고 싶은 스킬의 핵심 아이디어를 파악합니다.

**대화 컨텍스트 추출:** 현재 대화에 이미 워크플로우가 있는 경우 (예: "이걸 스킬로 만들어줘"), 대화 히스토리에서 답을 먼저 추출한다 — 사용된 도구, 단계별 순서, 사용자가 한 수정, 입출력 형식. 사용자가 빈 부분을 채우고, 다음 단계로 넘어가기 전에 확인받는다.

슬래시 커맨드 인수로 아이디어가 제공되었으면 그대로 사용합니다. 없으면 AskUserQuestion으로 물어봅니다.

**EXECUTE:** 아래 JSON으로 AskUserQuestion 도구를 즉시 호출한다:

```json
{
  "questions": [
    {
      "question": "어떤 스킬을 만들고 싶으세요? 한 문장으로 말해주세요.",
      "header": "아이디어",
      "options": [
        {"label": "번역 스킬 (예시)", "description": "문서를 다른 언어로 번역하는 스킬이에요."},
        {"label": "회의록 정리 (예시)", "description": "회의 내용을 요약하고 액션 아이템을 뽑아요."},
        {"label": "코드 리뷰 (예시)", "description": "코드를 분석해서 개선점을 찾아요."}
      ],
      "multiSelect": false
    }
  ]
}
```

사용자가 "Other"로 자유 입력하면 그것을 아이디어로 사용합니다. 예시 옵션을 선택해도 됩니다.

아이디어가 너무 모호하면 (예: "좋은 스킬") 1개 추가 질문으로 구체화합니다. 명확하면 바로 Phase B로 진행합니다.

---

### Phase B: 전문가 팀 소집 + 토론

**목표:** 4명의 전문가 에이전트를 병렬로 스폰하여 아이디어를 다각도로 분석합니다.

#### Step 1: 팀 소집 안내

사용자에게 알립니다:

```
4명의 전문가를 소집할게요. 잠시만 기다려주세요...

소집 중: 기획자 / 사용자 / 전문가 / 검수자
```

#### Step 2: 4개 에이전트 병렬 스폰

**반드시 Agent 도구를 사용하여 4개 에이전트를 동시에 (하나의 메시지에서) 스폰한다.**

각 에이전트의 설정:

| 에이전트 | subagent_type | model | description |
|----------|---------------|-------|-------------|
| 기획자 | `general-purpose` | `sonnet` | "기획자 관점 분석" |
| 사용자 | `general-purpose` | `sonnet` | "사용자 관점 분석" |
| 전문가 | `general-purpose` | `sonnet` | "전문가 관점 분석" |
| 검수자 | `general-purpose` | `sonnet` | "검수자 관점 분석" |

**에이전트 프롬프트:** `references/interview-guide.md` 섹션 2-1의 템플릿을 사용한다. `{아이디어}`를 사용자 아이디어로, `{추가정보}`를 Phase A 추가 정보로 교체.

#### Step 3: 토론 결과 종합

4개 에이전트의 응답을 수집한 뒤, **자연스러운 대화 형식**으로 종합하여 사용자에게 보여준다.

**종합 출력 형식:**

```
전문가 4명이 분석을 마쳤어요! 토론 결과를 정리할게요:

🎯 기획자: "{기획자 한줄 요약}"
→ {핵심 분석 1-2줄}

👤 사용자: "{사용자 한줄 요약}"
→ {핵심 분석 1-2줄}

🔧 전문가: "{전문가 한줄 요약}"
→ {핵심 분석 1-2줄}

🔍 검수자: "{검수자 한줄 요약}"
→ {핵심 분석 1-2줄}

💬 종합: {4명의 분석을 통합한 방향 제안 2-3줄}
```

**의견 충돌 처리:**

에이전트 간 의견이 다른 부분이 있으면 반드시 보여줍니다:

```
⚡ 의견이 갈렸어요:
- 기획자는 "{A}"를 제안했지만, 사용자는 "{B}"가 더 낫다고 했어요.
- 어떤 방향이 좋을까요?
```

#### Step 4: 방향 확인

**EXECUTE:** 아래 JSON으로 AskUserQuestion 도구를 즉시 호출한다:

```json
{
  "questions": [
    {
      "question": "전문가들의 분석을 봤는데, 어떻게 할까요?",
      "header": "방향",
      "options": [
        {"label": "이 방향 좋아요 (추천)", "description": "전문가들이 제안한 대로 워크플로우를 설계할게요."},
        {"label": "수정할 부분 있어요", "description": "어떤 부분을 바꾸고 싶은지 알려주세요."},
        {"label": "다시 토론해줘", "description": "추가 정보를 주면 전문가들이 다시 분석해요."}
      ],
      "multiSelect": false
    }
  ]
}
```

"다시 토론해줘" 선택 시: 사용자의 추가 정보를 받고 Step 2부터 다시 실행합니다.

---

### Phase C: 상세 인터뷰 (1-2개 추가 질문)

**목표:** 팀 토론에서 결정하지 못한 사항을 사용자에게 직접 물어봅니다.

팀 토론 결과에서 자동으로 판단한 내용:
- `purpose` — 기획자가 분석
- `input_type` / `output_type` — 사용자가 분석
- `trigger_keywords` — 기획자가 제안
- `domain` — 전문가가 판단
- `constraints` — 검수자가 식별

**추가로 확인이 필요한 경우만 질문합니다:**

자동 판단이 불확실한 항목에 대해서만 AskUserQuestion을 호출합니다. 최대 2개까지.

**EXECUTE:** 아래 JSON의 옵션을 토론 결과에 맞게 동적으로 채운 후 AskUserQuestion 도구를 즉시 호출한다:

```json
{
  "questions": [
    {
      "question": "결과물은 어떤 형태가 좋을까요?",
      "header": "출력",
      "options": [
        {"label": "텍스트 요약 (추천)", "description": "바로 대화창에 보여드려요."},
        {"label": "파일 생성", "description": ".md/.txt/.csv 등 파일로 저장해요."},
        {"label": "여러 파일 세트", "description": "프로젝트 구조처럼 여러 파일을 만들어요."}
      ],
      "multiSelect": false
    }
  ]
}
```

팀 토론에서 충분히 파악되었으면 이 Phase를 스킵하고 Phase D로 바로 진행합니다.

**질문 규칙 (모든 AskUserQuestion 호출 시 준수):**

| 규칙 | 설명 |
|------|------|
| AskUserQuestion 필수 | 모든 질문은 반드시 AskUserQuestion 도구를 즉시 호출한다. 각 JSON 블록의 "EXECUTE:" 지시를 따른다. |
| 설명 필수 | 모든 옵션의 description에 "뭔지 + 장단점" 포함 |
| 추천 표시 | 가장 적합한 옵션 label에 "(추천)" 붙이고 첫 번째 배치 |
| 쉬운 말 | 전문 용어 대신 일상 비유 사용 |
| 한 번에 하나 | 질문은 1개씩 |
| 기타 옵션 불필요 | AskUserQuestion이 자동으로 "Other" 제공 |

---

### Phase D: 워크플로우 설계

**목표:** 팀 토론 결과 + 사용자 답변을 바탕으로 워크플로우를 설계합니다.

**6가지 단계 타입:**

1. **prompt** — Claude가 생각하는 단계 (분석, 요약, 판단, 창작)
2. **script** — 반복/일관성/API 작업을 위한 Python/Bash
3. **api_mcp** — 외부 도구 연동 (API > MCP > 직접 구현 우선순위)
4. **rag** — 참조 파일 검색 (`references/` 폴더)
5. **review** — 검토 단계 (api_mcp/rag 뒤에 반드시 포함)
6. **generate** — 최종 출력 (파일 생성, 보고서)

**단계 타입 선택 기준:**

1. 외부 서비스가 필요한가? → **api_mcp** (뒤에 review 추가)
2. 참조 문서/도메인 지식이 필요한가? → **rag** (뒤에 review/prompt 추가)
3. 반복 작업/정확한 형식이 필요한가? → **script**
4. Claude의 판단/창작이 필요한가? → **prompt**
5. 결과 확인이 필요한가? → **review**
6. 파일/보고서를 만들어야 하는가? → **generate**

**기존 에이전트 확인 (컴포넌트 타입 판단 전):**

에이전트 컴포넌트가 후보일 때, `.claude/agents/` 디렉토리를 Glob으로 스캔하여 기존 에이전트를 확인한다:

1. `.claude/agents/*.md` 파일이 있으면 파일명과 description만 빠르게 스캔 (Read로 frontmatter만)
2. 새로 만들려는 에이전트와 역할이 겹치는 기존 에이전트가 있으면 사용자에게 안내:
   ```
   비슷한 역할의 전문가가 이미 있어요: [에이전트명] — [description]
   새로 만들까요, 기존 걸 개선할까요?
   ```
   **EXECUTE:** AskUserQuestion으로 선택 받기:
   ```json
   {
     "questions": [
       {
         "question": "비슷한 역할의 에이전트가 이미 있어요. 어떻게 할까요?",
         "header": "기존 에이전트 발견",
         "options": [
           {"label": "기존 걸 개선 (추천)", "description": "기존 에이전트를 읽고 개선 버전으로 업데이트해드려요."},
           {"label": "새로 만들기", "description": "기존 에이전트와 별개로 새 에이전트를 만들어요."}
         ],
         "multiSelect": false
       }
     ]
   }
   ```
3. "기존 걸 개선" 선택 시 → 기존 에이전트 파일을 Read로 읽고, Phase E에서 개선 버전으로 덮어쓰기 (덮어쓰기 전 사용자 확인 필수)
4. "새로 만들기" 선택 시 → 기존 워크플로우 계속
5. 기존 에이전트가 없으면 → 조용히 기존 워크플로우 계속 (사용자에게 불필요한 안내 없음)

**컴포넌트 타입 (전문가 에이전트의 분석을 참고하여 결정):**

| 타입 | 특징 | 언제 |
|------|------|------|
| **스킬** | 대화에 자연스럽게 녹아들어요. 단일 작업. | 기본값 |
| **에이전트** | 독립적으로 실행. 자체 컨텍스트. 다단계 자율 실행. | 복잡한 자율 작업 |
| **커맨드** | 사용자가 명시적으로 트리거. 인수 기반 분기. | 명확한 진입점 필요 시 |

**Degrees of Freedom (자유도) 식별:**

워크플로우 설계 시 **고정 요소**와 **가변 요소**를 구분한다:

| 구분 | 설명 | 예시 |
|------|------|------|
| 고정 | 워크플로우 구조, 단계 순서, 필수 검증 | "항상 3단계로 실행" |
| 가변 | 사용자가 바꿀 수 있는 파라미터 | 출력 언어, 상세도, 포맷 |

가변 요소가 있으면 SKILL.md에 **기본값 + 변경 방법**을 명시한다. 워크플로우 내 AskUserQuestion으로 처리하거나, SKILL.md 상단에 설정 가능 항목으로 문서화한다.

**Eval 기준 정의:**

워크플로우 설계와 함께 eval 시나리오를 정의한다. 검수자 에이전트의 분석(엣지 케이스, 테스트 시나리오)을 활용.

evals.json 형식으로 저장:
```json
{
  "skill_name": "{skill-name}",
  "evals": [
    {
      "id": 1,
      "prompt": "현실적이고 구체적인 사용자 프롬프트",
      "expected_output": "기대 결과 설명",
      "should_trigger": true,
      "files": []
    }
  ]
}
```

**품질 메트릭 정의 (선택):**
expectations 외에, 출력 품질을 연속 점수로 평가할 quality_metrics를 정의할 수 있다. 스킬 유형에 맞는 메트릭을 `references/eval-guide.md` 섹션 6의 템플릿에서 선택한다. 각 메트릭에 criteria, evaluation_steps(3-5개), threshold를 정의한다.

**현실적 프롬프트 철학:** eval 프롬프트는 실제 사용자가 입력할 법한 구체적 문장으로 작성한다. 파일 경로, 개인 상황, 약어, 오타, 캐주얼한 표현을 자연스럽게 섞는다.
- BAD: `"이 데이터를 포맷해줘"`, `"PDF에서 텍스트 추출"`
- GOOD: `"다운로드 폴더에 'Q4 매출 최종_v2.xlsx' 있는데 C열이 매출이고 D열이 비용이야. 이익률 퍼센트 컬럼 추가해줘"`

**should-trigger / should-not-trigger 구분:**

| 유형 | 개수 | 설명 |
|------|------|------|
| should-trigger | 2-3개 | 스킬이 반드시 트리거되어야 하는 쿼리. 다양한 표현(격식/캐주얼)으로 커버리지 확보 |
| should-not-trigger | 1-2개 | 키워드는 겹치지만 실제로는 다른 작업. 명백히 무관한 쿼리는 피한다 |

정상 시나리오 2-3개 + 엣지 케이스 1-2개를 정의한다. 상세 가이드: `references/eval-guide.md` 참조. 스키마 상세: `references/schemas.md` 참조.

**워크플로우 + Eval 확인:**

워크플로우 설계 결과와 eval 시나리오를 **일반 텍스트로 먼저 출력**한 후, AskUserQuestion으로 간결한 확인만 받는다.

> **절대 금지:** AskUserQuestion의 `markdown` 필드에 워크플로우/테이블/흐름도를 넣지 마. Claude Code에서 접혀서 안 보인다.

**Step D-1: 워크플로우 + Eval을 일반 텍스트로 출력**

단계별 흐름과 eval 시나리오 목록을 일반 텍스트로 출력한다. 예시:
```
워크플로우 설계 결과:

1단계: [설명]
2단계: [설명]
...

Eval 시나리오:
- should-trigger: [시나리오 1], [시나리오 2]
- should-not-trigger: [시나리오 1]
```

**Step D-2: AskUserQuestion으로 확인**

**EXECUTE:** 텍스트 출력 직후 AskUserQuestion 도구를 즉시 호출한다:

```json
{
  "questions": [
    {
      "question": "워크플로우와 테스트 기준을 확인해주세요.",
      "header": "워크플로우 + Eval",
      "options": [
        {
          "label": "이대로 진행 (추천)",
          "description": "이 워크플로우대로 파일을 만들고 자동 검증까지 해드릴게요."
        },
        {"label": "수정할 부분 있어", "description": "워크플로우나 테스트 기준을 바꾸고 싶은지 알려주세요."},
        {"label": "나중에 할게", "description": "여기서 멈출게요. 나중에 다시 시작할 수 있어요."}
      ],
      "multiSelect": false
    }
  ]
}
```

---

### Phase E: 파일 생성

**목표:** 확인된 워크플로우를 실제 파일로 만듭니다.

**생성할 파일 구조:**

```
skills/{skill-name}/
├── SKILL.md              # 워크플로우 (1,500-2,000 단어)
├── scripts/              # script 타입 단계용
│   └── {script}.py
├── references/           # rag 타입 단계용
│   └── {reference}.md
└── assets/               # 출력에 사용되는 파일 (컨텍스트에 로드하지 않음)
    └── {template/image/font/etc.}
```

**assets/ 폴더 용도:**
- 템플릿 파일 (HTML, React 보일러플레이트 등)
- 이미지, 아이콘, 폰트
- 샘플 데이터, 설정 파일
- scripts/references와 달리 **컨텍스트에 로드하지 않고** 출력물에 직접 사용

필요 시 추가 생성:
- `commands/{skill-name}.md` — 슬래시 커맨드
- `.claude/agents/{agent-name}.md` — 에이전트 파일 (생성 시 `references/agent-templates.md`를 참조하여 표준 구조와 품질 기준을 적용한다)

**SKILL.md 생성 템플릿:**

```markdown
---
name: {skill-name}
description: This skill should be used when the user asks to "{trigger1}", "{trigger2}", "{trigger3}".
---

# {Display Name}

> {한 줄 설명}

## 워크플로우

### Step 1: {단계 이름}
**타입**: {prompt/script/api_mcp/rag/review/generate}
{실행 지침}

### Step 2: ...

## References
- **`references/{file}.md`** — {설명}

## Scripts
- **`scripts/{file}.py`** — {설명}

## Assets
- **`assets/{file}`** — {설명}

## Settings (가변 요소가 있을 때만)
| 설정 | 기본값 | 변경 방법 |
|------|--------|-----------|
| {파라미터} | {기본값} | {AskUserQuestion 또는 인수로 변경} |
```

**Description 작성 (Pushy 전략):**

description은 스킬 트리거의 핵심 메커니즘이다. Claude는 스킬을 트리거하지 않는 쪽으로 편향되어 있으므로 (undertrigger), description을 적극적으로 작성한다.

1. **Pushy description** — 스킬이 하는 것 + 구체적 트리거 상황을 함께 기술한다.
   - BAD: `"코드 리뷰 도구"`
   - GOOD: `"코드 리뷰, 코드 검토, 코드 봐줘, review my code, 버그 찾아줘. Make sure to use this skill whenever the user mentions code review, even if they don't explicitly ask for it."`
2. **Why 설명** — description에 "무엇을 하는가"뿐 아니라 "왜 하는가"를 포함한다.
   - BAD: `"코드를 리뷰합니다"`
   - GOOD: `"코드를 리뷰합니다 — 보안 취약점과 성능 병목을 조기에 발견하여 프로덕션 장애를 예방하기 위해"`
3. **한/영 혼합** — 한국어와 영어 트리거를 모두 포함한다.
4. **복잡한 쿼리만 트리거** — 단순 질문("Python이 뭐야?")이 아닌, 스킬이 필요한 복잡한 요청에 반응하도록 설계한다.

초안 description을 작성하되, Phase H에서 `scripts/run_loop.py`로 자동 최적화한다.
상세 가이드: `references/trigger-mechanism.md` 참조.

**Writing Style 규칙 (SKILL.md 생성 시 반드시 적용):**

1. **Imperative form 사용** — "To accomplish X, do Y" 형식. "You should do X" 금지.
   - O: "Read the configuration file. Validate the input."
   - X: "You should read the configuration file."
2. **Description은 third-person** — "This skill should be used when..." 형식.
3. **Why 설명 우선** — 지시사항에서 ALWAYS/NEVER 대신 이유를 설명한다. LLM은 이유를 이해하면 더 잘 따른다.
4. **Concise 원칙** — SKILL.md 본문은 1,500-2,000 단어 이내. 상세 내용은 references/로 분리.
   - 컨텍스트 윈도우는 공공재. Claude가 이미 아는 정보는 반복하지 않는다.
5. **references 참조 명시** — SKILL.md에서 references/ 파일을 명확히 링크한다.

상세 가이드: `references/writing-style-guide.md` 참조.

**스크립트 생성 규칙:**

Python:
```python
#!/usr/bin/env python3
# {설명}
import sys
import json

def main():
    # 에러는 stderr로
    # 결과는 JSON으로 stdout에
    pass

if __name__ == "__main__":
    main()
```

Bash:
```bash
#!/usr/bin/env bash
set -euo pipefail
# 에러는 stderr로: echo "에러" >&2
```

경로는 `${CLAUDE_PLUGIN_ROOT}`를 기준으로 합니다.

> `${CLAUDE_PLUGIN_ROOT}`는 Claude Code가 플러그인 실행 시 자동으로 설정하는 환경 변수로, 해당 플러그인의 루트 디렉토리를 가리킵니다.

**파일 덮어쓰기 규칙:** 같은 이름의 파일이 있으면 반드시 사용자에게 확인합니다. 동의 없이 덮어쓰지 않습니다.

---

### Phase E-verify: 자동 검증

**목표:** 생성된 SKILL.md의 구조적 품질을 자동 검증하고, FAIL 항목을 수정합니다.

**Step 1: verify-skill.py 실행**

파일 생성 직후, Bash 도구로 검증 스크립트를 실행한다:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/skillers-suda/scripts/verify-skill.py" <생성된 SKILL.md 경로>
```

**Step 2: 결과 처리**

| 결과 | 조치 |
|------|------|
| 전체 PASS | Phase F로 진행 |
| WARN 있음 | 사용자에게 안내 후 Phase F 진행 |
| FAIL 있음 | 아래 자동 수정 → 재검증 |

**FAIL 자동 수정:**

| FAIL 항목 | 자동 수정 |
|-----------|-----------|
| third_person | description을 "This skill should be used when..." 형식으로 변환 |
| trigger_phrases | 워크플로우에서 트리거 키워드 추출하여 추가 |
| imperative_form | second-person 표현을 imperative로 변환 |
| references_exist | 누락 파일 생성 또는 참조 제거 |

word_count FAIL은 자동 수정 불가 — 사용자에게 어떤 부분을 references/로 분리할지 확인한다.

자동 수정 후 verify-skill.py를 재실행하여 PASS를 확인한다. 상세 가이드: `references/eval-guide.md` 참조.

---

### Phase F: 자동 Eval 실행 + 벤치마크

**목표:** Phase D에서 정의한 eval 시나리오를 자동 실행하고, 정량적/정성적으로 평가합니다.

**Step 1: evals.json 생성**

Phase D에서 정의한 eval 시나리오를 `evals/evals.json`으로 저장한다. 스키마: `references/schemas.md` 참조.

**Step 2: 테스트 실행 (subagent 병렬)**

각 eval 케이스마다 2개 subagent를 동시에 스폰한다:
- **with_skill**: 스킬을 적용하여 eval prompt 실행
- **without_skill (baseline)**: 스킬 없이 동일 prompt 실행

결과를 `{skill-name}-workspace/iteration-{N}/eval-{ID}/` 에 저장한다.

각 eval 디렉토리에 `eval_metadata.json` 생성:
```json
{
  "eval_id": 0,
  "eval_name": "descriptive-name",
  "prompt": "사용자 프롬프트",
  "assertions": []
}
```

**Step 3: assertion 작성 (실행 중)**

테스트 실행 중에 정량적 assertion을 작성한다. 객관적으로 검증 가능한 것만 assertion으로 만들고, 주관적 품질은 사용자 리뷰에 맡긴다.

**Step 4: 채점 + 벤치마크 + 뷰어**

모든 실행 완료 후:

1. **채점** — `references/agents/grader.md` 참조하여 assertion 평가. `grading.json` 저장.
2. **벤치마크 집계**:
   ```bash
   python -m scripts.aggregate_benchmark {workspace}/iteration-N --skill-name {name}
   ```
3. **분석** — `references/agents/analyzer.md` 참조하여 패턴 분석 (비차별 assertion, 고분산 eval 등).
4. **뷰어 실행**:
   ```bash
   python assets/eval-viewer/generate_review.py {workspace}/iteration-N \
     --skill-name "{name}" --benchmark {workspace}/iteration-N/benchmark.json
   ```
   iteration 2+ 에서는 `--previous-workspace` 옵션 추가.

**Step 5: 사용자 피드백 수집**

뷰어에서 사용자가 리뷰 후 "Submit All Reviews" → `feedback.json` 생성. 피드백 읽고 Phase G로 진행.

**EXECUTE:** 아래 JSON으로 AskUserQuestion 도구를 즉시 호출한다:

```json
{
  "questions": [
    {
      "question": "eval 결과를 확인했어요. 어떻게 할까요?",
      "header": "Eval 결과",
      "options": [
        {"label": "좋아요, 다음 단계로!", "description": "결과가 만족스러우면 description 최적화로 넘어갈게요."},
        {"label": "개선이 필요해요", "description": "피드백 기반으로 스킬을 개선하고 다시 테스트할게요."},
        {"label": "eval 케이스 수정", "description": "테스트 시나리오를 바꾸고 싶어요."}
      ],
      "multiSelect": false
    }
  ]
}
```

"개선이 필요해요" 선택 시 Phase G로 진행합니다.

---

### Phase G: 반복 개선

**목표:** 피드백 기반으로 스킬을 개선하고, 다시 테스트합니다.

**개선 원칙** (`references/improvement-principles.md` 참조):

1. **일반화** — 특정 eval 케이스만 통과하도록 하드코딩하지 않는다. 개별 케이스가 아닌 패턴을 해결한다.
2. **Lean 유지** — 효과 없는 지시를 제거한다. 트랜스크립트를 읽고 비생산적인 부분을 파악한다.
3. **Why 설명** — ALWAYS/NEVER 대신 이유를 설명한다. LLM은 이유를 이해하면 더 잘 따른다.
4. **반복 코드 번들** — 테스트 실행에서 subagent들이 독립적으로 같은 스크립트를 작성했다면, 스킬에 번들한다.

**반복 루프:**

1. 피드백 기반으로 스킬 수정
2. 새 `iteration-{N+1}/` 디렉토리에 재실행 (baseline 포함)
3. `--previous-workspace`로 뷰어 실행하여 이전 iteration과 비교
4. 사용자 리뷰 → 피드백 수집
5. 반복 (사용자가 만족하거나 의미 있는 개선이 없을 때까지)

**Blind Comparison (선택사항):**

두 버전 간 엄밀 비교가 필요하면 `references/agents/comparator.md`와 `references/agents/analyzer.md` 참조. 독립 에이전트가 블라인드로 품질을 판단한다.

---

### Phase H: Description 최적화

**목표:** 스킬의 description을 자동 최적화하여 트리거 정확도를 높입니다.

**Step 1: 트리거 eval 쿼리 생성**

should-trigger 8-10개 + should-not-trigger 8-10개 = 약 20개 eval 쿼리를 생성한다.
현실적이고 구체적인 프롬프트로 작성 (Phase D의 현실적 프롬프트 철학 적용).

**Step 2: 사용자 리뷰**

`assets/eval_review.html` 템플릿으로 eval 세트를 사용자에게 보여준다:
1. `__EVAL_DATA_PLACEHOLDER__`를 eval JSON으로 교체
2. `__SKILL_NAME_PLACEHOLDER__`를 스킬 이름으로 교체
3. `__SKILL_DESCRIPTION_PLACEHOLDER__`를 현재 description으로 교체
4. `/tmp/eval_review_{skill-name}.html`에 저장 후 열기
5. 사용자가 수정 후 "Export Eval Set" → `eval_set.json` 다운로드

**Step 3: 최적화 루프 실행**

```bash
python -m scripts.run_loop \
  --eval-set {eval_set.json 경로} \
  --skill-path {스킬 경로} \
  --model {현재 세션 모델 ID} \
  --max-iterations 5 --verbose
```

60% train / 40% test 분할로, 각 description을 3회 반복 테스트하여 트리거율을 측정한다. test score 기준으로 best_description을 선택 (과적합 방지).

**Step 4: 결과 적용**

`best_description`을 SKILL.md frontmatter에 적용. 사용자에게 before/after + 점수를 보여준다.

---

### Phase I: 패키징

**목표:** 완성된 스킬을 .skill 파일로 패키징합니다.

`present_files` 도구가 있을 때만 실행:

```bash
python -m scripts.package_skill {스킬 폴더 경로}
```

패키징 후 `.skill` 파일 경로를 사용자에게 안내한다.

---

### 에이전트 분석 모드

`/skillers-suda 분석 .claude/agents/[에이전트].md` 로 실행됩니다.

**Step 1: 에이전트 파일 읽기**

대상 에이전트 파일을 Read로 읽고, frontmatter + 본문을 파싱한다:
- `name`, `description`, `tools` 등 frontmatter 필드 추출
- 본문에서 역할 정의, 워크플로우, 도구 배정 파악

**Step 2: 4명 전문가 분석 (Phase B와 동일)**

4명의 전문가 에이전트를 병렬 스폰하여 에이전트를 분석한다 (반드시 Agent 도구로 실제 스폰, 시뮬레이션 금지):

| 전문가 | 분석 관점 |
|--------|-----------|
| 기획자 | 역할 명확성, 목적 적합성 |
| 사용자 | 트리거 자연스러움, 사용 편의성 |
| 전문가 | 도구 배정 적절성, 프롬프트 품질 |
| 검수자 | R&R 완성도, 엣지 케이스 대응 |

**Step 3: 개선안 제안**

4명의 분석 결과를 종합하여 사용자에게 구체적인 개선안을 제안한다:
- description 개선 (Pushy 전략 적용 — undertrigger 방지)
- 도구 배정 최적화
- R&R 보강
- 프롬프트 정제

**EXECUTE:** 개선안을 정리한 후 AskUserQuestion 도구를 즉시 호출한다:

```json
{
  "questions": [
    {
      "question": "분석 결과를 바탕으로 개선안을 만들었어요. 어떻게 할까요?",
      "header": "에이전트 분석 완료",
      "options": [
        {"label": "개선안 적용 (추천)", "description": "제안된 개선안대로 에이전트 파일을 수정해드려요."},
        {"label": "일부만 수정", "description": "어떤 부분을 바꾸고 싶은지 알려주세요."},
        {"label": "지금은 유지", "description": "분석 결과만 참고하고 파일은 그대로 둘게요."}
      ],
      "multiSelect": false
    }
  ]
}
```

**Step 4: 사용자 확인 후 수정**

"개선안 적용" 또는 "일부만 수정" 선택 시 → Edit 도구로 에이전트 파일을 수정한다. 덮어쓰기 전 수정 내용을 미리 보여주고 확인 받는다.

---

## AI 행동 규칙

### 반드시 지킬 것

- 인터뷰 없이 파일을 만들지 않습니다
- **Phase B에서 반드시 4개 에이전트를 병렬 스폰합니다** (시뮬레이션 금지)
- 4개 에이전트는 반드시 하나의 메시지에서 동시에 스폰합니다 (순차 스폰 금지)
- 워크플로우 확인 없이 생성하지 않습니다
- API > MCP > 직접 구현 우선순위를 지킵니다
- **SKILL.md 본문은 1,500-2,000 단어 이내로 유지합니다** (컨텍스트 윈도우 효율)
- 상세 내용은 `references/`로 분리합니다 (progressive disclosure)
- **Writing Style 규칙을 반드시 적용합니다** (imperative form, third-person description, why 설명)
- **Phase D에서 eval 시나리오를 evals.json 형식으로 정의합니다** (should-trigger / should-not-trigger 구분)
- **Phase D에서 자유도(고정/가변 요소)를 반드시 식별합니다**
- **Phase E에서 Pushy description을 작성합니다** (undertrigger 방지)
- **Phase E 후 verify-skill.py를 반드시 실행합니다** (FAIL 시 자동 수정 → 재검증)
- **Phase F에서 eval을 자동 실행합니다** (subagent 병렬 실행 + baseline 비교 + 벤치마크)
- **Phase G에서 일반화 원칙을 적용합니다** (특정 케이스 하드코딩 금지, 반복 코드 번들)
- **Phase H에서 run_loop.py로 description을 자동 최적화합니다** (train/test 분할, 과적합 방지)
- 가변 요소가 있으면 Settings 섹션에 기본값 + 변경 방법을 명시합니다
- 전문 용어는 항상 쉬운 설명을 함께 붙입니다

### 절대 하지 말 것

- **4명의 대화를 텍스트로 시뮬레이션하기** (반드시 Agent 도구로 실제 스폰)
- 전문 용어를 설명 없이 사용하기
- 인터뷰 질문 5개 초과하기 (Phase A 1-2개 + Phase C 1-2개 = 최대 4개)
- 한 번에 모든 것을 물어보기
- api_mcp/rag 결과를 검토 없이 최종 출력으로 사용하기
- 사용자 동의 없이 파일 덮어쓰기
- 코딩 지식을 전제로 설명하기
- **eval 케이스를 하드코딩으로 통과시키기** (일반화 원칙 위반)
- **사용자 리뷰 없이 eval 결과를 직접 판단하기** (generate_review.py로 뷰어 제공 필수)

---

## References

상세 내용은 아래 파일에서 확인하세요 (progressive disclosure):

### 작성 가이드
- **`references/writing-style-guide.md`** — SKILL.md 작성 규칙 (imperative form, description 품질, concise 원칙)
- **`references/trigger-mechanism.md`** — 스킬 트리거 메커니즘, undertrigger 방지, pushy description 전략
- **`references/improvement-principles.md`** — 반복 개선 원칙 (일반화, lean 유지, why 설명, 반복 코드 번들)

### Eval & 검증
- **`references/eval-guide.md`** — Eval 방법론 (시나리오 정의, 자동 검증, 자동 수정 규칙)
- **`references/schemas.md`** — evals.json, grading.json, benchmark.json 스키마 정의
- **`references/agents/grader.md`** — assertion 채점 에이전트 프롬프트
- **`references/agents/comparator.md`** — 블라인드 A/B 비교 에이전트 프롬프트
- **`references/agents/analyzer.md`** — 벤치마크 분석 에이전트 프롬프트

### 설계 가이드
- **`references/interview-guide.md`** — 인터뷰 방법론 + 페르소나 에이전트 설계
- **`references/workflow-step-types.md`** — 6가지 단계 타입 상세 설명과 선택 기준
- **`references/component-type-decision.md`** — 스킬/에이전트/커맨드 판단 기준 트리
- **`references/mcp-catalog.md`** — MCP 서버 카탈로그 (전문가 에이전트 MCP 추천용)
- **`references/agent-templates.md`** — 에이전트 컴포넌트 생성 시 품질 기준과 표준 구조 가이드

### 스크립트 & 도구
- **`scripts/`** — verify-skill.py (품질 검증), run_eval.py (eval 실행), run_loop.py (description 최적화), aggregate_benchmark.py (벤치마크 집계), generate_report.py (HTML 리포트), improve_description.py (description 개선), package_skill.py (패키징), quick_validate.py (구조 검증)
- **`assets/eval-viewer/`** — eval 결과 브라우저 뷰어 (generate_review.py + viewer.html)
- **`assets/eval_review.html`** — description 최적화용 eval 쿼리 리뷰 템플릿
- **`references/script-templates.md`** — Python/Bash 스크립트 템플릿 모음
- **`references/api-mcp-integration.md`** — API/MCP 연동 가이드와 예시
