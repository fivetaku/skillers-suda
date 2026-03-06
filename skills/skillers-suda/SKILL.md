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
| 기획자 | `general-purpose` | `haiku` | "기획자 관점 분석" |
| 사용자 | `general-purpose` | `haiku` | "사용자 관점 분석" |
| 전문가 | `general-purpose` | `haiku` | "전문가 관점 분석" |
| 검수자 | `general-purpose` | `haiku` | "검수자 관점 분석" |

**각 에이전트의 프롬프트 템플릿:**

아래 템플릿의 `{아이디어}`를 사용자가 말한 아이디어로 교체한다. `{추가정보}`는 Phase A에서 수집한 추가 정보가 있으면 넣고, 없으면 생략한다.

**기획자 에이전트 프롬프트:**
```
너는 스킬 기획 전문가야. 아래 스킬 아이디어를 기획자 관점에서 분석해줘.

아이디어: {아이디어}
{추가정보}

분석 항목 (한국어로, 각 항목 2-3줄):
1. 목적: 이 스킬이 해결하는 핵심 문제
2. 대상: 누가 쓸 건지 (나만/팀/불특정 다수)
3. 범위: MVP로 먼저 만들 핵심 기능 vs 나중에 추가할 기능
4. 트리거 키워드: 이 스킬을 부를 때 자연스러운 키워드 5개 제안
5. 우려사항: 기획 관점에서 주의할 점

출력 형식: 각 항목을 번호와 함께 작성. 마지막에 "기획자 한줄 요약: {요약}" 추가.
```

**사용자 에이전트 프롬프트:**
```
너는 바이브코더(비개발자) 사용자야. 아래 스킬 아이디어를 실제 사용자 관점에서 분석해줘.

아이디어: {아이디어}
{추가정보}

분석 항목 (한국어로, 각 항목 2-3줄):
1. 사용 시나리오: 실제로 이 스킬을 어떤 상황에서 쓸지
2. 입력 방식: 사용자가 뭘 제공해야 하는지 (텍스트/파일/URL 등), 가장 편한 방식
3. 출력 기대: 결과물이 어떤 형태면 좋겠는지 (텍스트 요약/파일/보고서)
4. 사용성: 처음 쓰는 사람도 바로 이해할 수 있는지, 불편할 수 있는 점
5. 실망 포인트: 이 스킬이 기대에 못 미칠 수 있는 부분

출력 형식: 각 항목을 번호와 함께 작성. 마지막에 "사용자 한줄 요약: {요약}" 추가.
```

**전문가 에이전트 프롬프트:**
```
너는 Claude Code 플러그인/스킬 개발 전문가야. 아래 스킬 아이디어를 기술 구현 관점에서 분석해줘.

아이디어: {아이디어}
{추가정보}

분석 항목 (한국어로, 각 항목 2-3줄):
1. 워크플로우 제안: 단계별 실행 흐름 (3-5단계)
2. 단계 타입: 각 단계가 prompt/script/api_mcp/rag/review/generate 중 어떤 타입인지
   - prompt: Claude가 생각하는 단계 (분석, 요약, 판단)
   - script: Python/Bash 스크립트 (반복/일관성/API 작업)
   - api_mcp: 외부 도구 연동 (웹 검색, 노션 등)
   - rag: 참조 파일 검색 (도메인 지식)
   - review: 검토 단계 (AI 또는 사용자 확인)
   - generate: 최종 출력 (파일 생성, 보고서)
3. 필요한 도구: 외부 API, MCP, 스크립트 등
4. 컴포넌트 타입: 스킬/에이전트/커맨드 중 적합한 것과 이유
5. 기술적 리스크: 구현 시 까다로운 부분

출력 형식: 각 항목을 번호와 함께 작성. 마지막에 "전문가 한줄 요약: {요약}" 추가.
```

**검수자 에이전트 프롬프트:**
```
너는 QA/품질 검수 전문가야. 아래 스킬 아이디어를 품질과 안정성 관점에서 분석해줘.

아이디어: {아이디어}
{추가정보}

분석 항목 (한국어로, 각 항목 2-3줄):
1. 엣지 케이스: 정상 경로 외에 발생할 수 있는 예외 상황 3개 이상
2. 에러 핸들링: 각 엣지 케이스에 대한 대응 방안
3. 입력 검증: 잘못된 입력이 들어올 때 어떻게 처리할지
4. 테스트 시나리오: 정상/비정상 테스트 케이스 각 2개
5. 실패 시 복구: 중간에 실패했을 때 사용자 경험

출력 형식: 각 항목을 번호와 함께 작성. 마지막에 "검수자 한줄 요약: {요약}" 추가.
```

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

각 시나리오 형식:
```
시나리오: {이름}
입력: {사용자가 제공할 입력}
기대 행동: {스킬이 해야 할 것}
성공 기준: {무엇이 되어야 "성공"인지}
```

정상 시나리오 2-3개 + 엣지 케이스 1-2개를 정의한다. 상세 가이드: `references/eval-guide.md` 참조.

**워크플로우 + Eval 확인:**

워크플로우 설계 결과와 eval 시나리오를 AskUserQuestion의 markdown 프리뷰로 보여준다.

**EXECUTE:** 아래 JSON의 markdown 필드를 워크플로우 설계 결과(단계별 흐름 + eval 시나리오)로 채운 후 AskUserQuestion 도구를 즉시 호출한다:

```json
{
  "questions": [
    {
      "question": "워크플로우와 테스트 기준을 확인해주세요.",
      "header": "워크플로우 + Eval",
      "options": [
        {
          "label": "이대로 진행 (추천)",
          "description": "이 워크플로우대로 파일을 만들고 자동 검증까지 해드릴게요.",
          "markdown": "(동적: 단계별 흐름 + eval 시나리오 목록)"
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
- `.claude/agents/{agent-name}.md` — 에이전트 파일

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

**Description 최적화 (SKILL.md 생성 후 반드시 수행):**

description은 스킬 검색과 트리거의 핵심이다. 생성 후 아래 절차로 최적화한다:

1. **후보 생성** — description 2-3개를 서로 다른 관점으로 작성:
   - A: 기능 중심 ("This skill should be used when the user asks to '번역해줘', 'translate'...")
   - B: 상황 중심 ("This skill should be used when the user needs to translate documents...")
   - C: 혼합형 (기능 + 상황)
2. **평가 기준** — 각 후보를 아래 기준으로 비교:
   - 트리거 커버리지: 다양한 표현을 포괄하는가? (한/영 모두)
   - 구체성: 다른 스킬과 구분되는가?
   - 간결성: 1-2문장 이내인가?
3. **최적 선택** — 가장 높은 점수의 후보를 채택. 동점이면 혼합형 우선.

이 과정은 내부적으로 수행하고, 최종 description만 SKILL.md에 반영한다.

**Writing Style 규칙 (SKILL.md 생성 시 반드시 적용):**

1. **Imperative form 사용** — "To accomplish X, do Y" 형식. "You should do X" 금지.
   - O: "Read the configuration file. Validate the input."
   - X: "You should read the configuration file."
2. **Description은 third-person** — "This skill should be used when..." 형식.
   - O: `description: This skill should be used when the user asks to "번역해줘", "translate this".`
   - X: `description: Use this skill when you want to translate.`
3. **구체적 trigger phrase 포함** — description에 사용자가 실제로 말할 문장을 3-5개 넣는다.
4. **Concise 원칙** — SKILL.md 본문은 1,500-2,000 단어 이내. 상세 내용은 references/로 분리.
   - 컨텍스트 윈도우는 공공재. Claude가 이미 아는 정보는 반복하지 않는다.
   - "이 문단이 토큰 비용만큼의 가치가 있는가?" 자문한다.
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

### Phase F: Eval 테스트 + 고도화

**목표:** Phase D에서 정의한 eval 시나리오 기반으로 스킬을 테스트하고 개선합니다.

**검증 결과 + 테스트 안내:**

Phase E-verify 결과와 eval 시나리오를 함께 보여준다:

```
자동 검증 통과! ({pass}개 PASS, {warn}개 WARN)

이제 실제 테스트를 해볼까요? Phase D에서 정의한 시나리오에요:

정상 시나리오:
1. "{시나리오1 이름}" — 이렇게 말해보세요: "{트리거 예시}"
2. "{시나리오2 이름}" — 이렇게 말해보세요: "{트리거 예시}"

엣지 케이스:
1. "{엣지 시나리오}" — {어떤 상황인지 설명}
```

**고도화 루프:**

테스트 후 **EXECUTE:** 아래 JSON으로 AskUserQuestion 도구를 즉시 호출한다:

```json
{
  "questions": [
    {
      "question": "방금 결과 어때요?",
      "header": "피드백",
      "options": [
        {"label": "좋아요, 완성!", "description": "이대로 최종 완성할게요."},
        {"label": "톤 수정", "description": "너무 딱딱하거나 너무 캐주얼해요."},
        {"label": "내용 수정", "description": "용어나 내용이 틀렸어요."},
        {"label": "단계 변경", "description": "단계를 추가하거나 바꾸고 싶어요."}
      ],
      "multiSelect": false
    }
  ]
}
```

사용자가 "완성"을 선택할 때까지 반복합니다.

---

## AI 행동 규칙

### 반드시 지킬 것

- 인터뷰 없이 파일을 만들지 않습니다
- **Phase B에서 반드시 4개 에이전트를 병렬 스폰합니다** (시뮬레이션 금지)
- 4개 에이전트는 반드시 하나의 메시지에서 동시에 스폰합니다 (순차 스폰 금지)
- 워크플로우 확인 없이 생성하지 않습니다
- 스크립트는 반복성/일관성/API가 필요한 작업에만 생성합니다
- API > MCP > 직접 구현 우선순위를 지킵니다
- api_mcp/rag 단계 이후에는 반드시 review 또는 prompt 단계를 추가합니다
- **SKILL.md 본문은 1,500-2,000 단어 이내로 유지합니다** (컨텍스트 윈도우 효율)
- 상세 내용은 `references/`로 분리합니다 (progressive disclosure)
- **Writing Style 규칙을 반드시 적용합니다** (imperative form, third-person description)
- **assets/ 폴더를 적절히 활용합니다** (템플릿, 이미지 등 출력용 파일)
- **Phase D에서 eval 시나리오를 반드시 정의합니다** (정상 2-3개 + 엣지 1-2개)
- **Phase D에서 자유도(고정/가변 요소)를 반드시 식별합니다**
- **Phase E에서 description 후보 2-3개를 생성하고 최적을 선택합니다**
- **Phase E 후 verify-skill.py를 반드시 실행합니다** (FAIL 시 자동 수정 → 재검증)
- 생성된 스킬은 반드시 eval 시나리오 기반으로 테스트를 제안합니다
- 가변 요소가 있으면 Settings 섹션에 기본값 + 변경 방법을 명시합니다
- AskUserQuestion으로 고도화 기회를 제공합니다
- 전문 용어는 항상 쉬운 설명을 함께 붙입니다

### 절대 하지 말 것

- **4명의 대화를 텍스트로 시뮬레이션하기** (반드시 Agent 도구로 실제 스폰)
- 전문 용어를 설명 없이 사용하기
- 인터뷰 질문 5개 초과하기 (Phase A 1-2개 + Phase C 1-2개 = 최대 4개)
- 한 번에 모든 것을 물어보기
- 스크립트 없이 API 호출을 프롬프트에 넣기
- api_mcp/rag 결과를 검토 없이 최종 출력으로 사용하기
- 사용자 동의 없이 파일 덮어쓰기
- 코딩 지식을 전제로 설명하기

---

## References

상세 내용은 아래 파일에서 확인하세요 (progressive disclosure):

- **`references/writing-style-guide.md`** — SKILL.md 작성 규칙 (imperative form, description 품질, concise 원칙, 검증 체크리스트)
- **`references/eval-guide.md`** — Eval 방법론 (시나리오 정의, 자동 검증, 수동 검증, 자동 수정 규칙)
- **`scripts/verify-skill.py`** — 생성된 SKILL.md 자동 검증 스크립트 (frontmatter, writing style, word count, references)
- **`references/interview-guide.md`** — 인터뷰 방법론 + 페르소나 에이전트 설계
- **`references/workflow-step-types.md`** — 6가지 단계 타입 상세 설명과 선택 기준
- **`references/component-type-decision.md`** — 스킬/에이전트/커맨드 판단 기준 트리
- **`references/script-templates.md`** — Python/Bash 스크립트 템플릿 모음
- **`references/api-mcp-integration.md`** — API/MCP 연동 가이드와 예시
