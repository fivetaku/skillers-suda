# Phase 실행 상세 — AskUserQuestion 템플릿 & 출력 포맷

## Phase A: 아이디어 수집 AskUserQuestion

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

사용자가 "Other"로 자유 입력하면 그것을 아이디어로 사용. 예시 옵션 선택도 가능.
아이디어가 너무 모호하면 (예: "좋은 스킬") 1개 추가 질문으로 구체화.

---

## Phase B: 팀 소집 안내 텍스트

```
4명의 전문가를 소집할게요. 잠시만 기다려주세요...

소집 중: 기획자 / 사용자 / 전문가 / 검수자
```

### 에이전트 스폰 설정

| 에이전트 | subagent_type | model | description |
|----------|---------------|-------|-------------|
| 기획자 | `general-purpose` | `haiku` | "기획자 관점 분석" |
| 사용자 | `general-purpose` | `haiku` | "사용자 관점 분석" |
| 전문가 | `general-purpose` | `haiku` | "전문가 관점 분석" |
| 검수자 | `general-purpose` | `haiku` | "검수자 관점 분석" |

에이전트 프롬프트: `references/interview-guide.md` 섹션 2-1의 템플릿 사용. `{아이디어}`와 `{추가정보}` 교체.

### 토론 결과 종합 출력 포맷

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

### 의견 충돌 처리

```
⚡ 의견이 갈렸어요:
- 기획자는 "{A}"를 제안했지만, 사용자는 "{B}"가 더 낫다고 했어요.
- 어떤 방향이 좋을까요?
```

### 방향 확인 AskUserQuestion

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

---

## Phase C: 상세 인터뷰 AskUserQuestion (예시)

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

팀 토론에서 충분히 파악되었으면 이 Phase를 스킵하고 Phase D로 바로 진행.

---

## Phase D: 워크플로우 + Eval 확인 AskUserQuestion

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

### Eval 기준 정의 (evals.json 형식)

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

### 현실적 프롬프트 철학

eval 프롬프트는 실제 사용자가 입력할 법한 구체적 문장으로 작성. 파일 경로, 개인 상황, 약어, 오타, 캐주얼한 표현을 자연스럽게 섞는다.
- BAD: `"이 데이터를 포맷해줘"`, `"PDF에서 텍스트 추출"`
- GOOD: `"다운로드 폴더에 'Q4 매출 최종_v2.xlsx' 있는데 C열이 매출이고 D열이 비용이야. 이익률 퍼센트 컬럼 추가해줘"`

### should-trigger / should-not-trigger 구분

| 유형 | 개수 | 설명 |
|------|------|------|
| should-trigger | 2-3개 | 스킬이 반드시 트리거되어야 하는 쿼리. 다양한 표현 |
| should-not-trigger | 1-2개 | 키워드는 겹치지만 실제로는 다른 작업 |

---

## Phase E: 파일 생성 템플릿

### 디렉토리 구조

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

### SKILL.md 생성 템플릿

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

### 스크립트 생성 규칙

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

경로는 `${CLAUDE_PLUGIN_ROOT}`를 기준.

---

## Phase F: Eval 결과 AskUserQuestion

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

---

## Phase H: Description 최적화 상세

### Step 1: 트리거 eval 쿼리 생성
should-trigger 8-10개 + should-not-trigger 8-10개 = 약 20개 eval 쿼리.
현실적이고 구체적인 프롬프트로 작성.

### Step 2: 사용자 리뷰
`assets/eval_review.html` 템플릿으로 eval 세트를 사용자에게 보여준다:
1. `__EVAL_DATA_PLACEHOLDER__`를 eval JSON으로 교체
2. `__SKILL_NAME_PLACEHOLDER__`를 스킬 이름으로 교체
3. `__SKILL_DESCRIPTION_PLACEHOLDER__`를 현재 description으로 교체
4. `/tmp/eval_review_{skill-name}.html`에 저장 후 열기
5. 사용자가 수정 후 "Export Eval Set" → `eval_set.json` 다운로드

### Step 3: 최적화 루프 실행

```bash
python -m scripts.run_loop \
  --eval-set {eval_set.json 경로} \
  --skill-path {스킬 경로} \
  --model {현재 세션 모델 ID} \
  --max-iterations 5 --verbose
```

60% train / 40% test 분할. 각 description을 3회 반복 테스트. test score 기준 best_description 선택.

### Step 4: 결과 적용
`best_description`을 SKILL.md frontmatter에 적용. 사용자에게 before/after + 점수 제시.
