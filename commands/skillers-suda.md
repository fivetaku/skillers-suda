---
name: skillers-suda
description: "스킬러들의 수다 — 4명의 전문가가 수다 떨면서 바이브코더의 아이디어를 동작하는 스킬로 변환"
argument-hint: "[스킬 설명|분석 <스킬경로>]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - Agent
---

# /skillers-suda Command

인수(argument)를 파싱해서 동작을 결정합니다:

| 인수 패턴 | 동작 |
|-----------|------|
| (인수 없음) | 인터랙티브 메뉴 표시 |
| [스킬 설명] | 바로 인터뷰 시작 |
| `분석 [경로]` | 기존 스킬 또는 에이전트 분석 |

**경로 판별:**
- 경로가 `.claude/agents/*.md` 패턴이거나 에이전트 파일이면 → **에이전트 분석 모드** (SKILL.md의 "에이전트 분석 모드" 섹션 실행)
- 경로가 스킬 디렉토리 (SKILL.md 포함) 또는 SKILL.md 파일이면 → **기존 스킬 분석 모드** (아래 "분석 모드" 섹션 실행)

---

## 인수 없음 — 인터랙티브 메뉴

**EXECUTE:** 아래 JSON으로 AskUserQuestion 도구를 즉시 호출한다:

```json
{
  "questions": [
    {
      "question": "어떤 걸 도와드릴까요?",
      "header": "스킬러",
      "options": [
        {
          "label": "새 스킬 만들기 (추천)",
          "description": "아이디어 하나만 말해주세요. 4명의 전문가가 인터뷰로 동작하는 스킬을 만들어드려요."
        },
        {
          "label": "기존 스킬 분석",
          "description": "만들어둔 스킬을 분석해서 개선점을 제안해드려요."
        },
        {
          "label": "사용법 안내",
          "description": "스킬러들의 수다가 뭔지, 어떻게 쓰는지 알려드려요."
        }
      ],
      "multiSelect": false
    }
  ]
}
```

After user selection:
- **새 스킬 만들기** → Ask for one-sentence idea if not provided, then execute skillers-suda skill workflow
- **기존 스킬 분석** → Ask for skill path, then execute analysis mode
- **사용법 안내** → Explain in plain Korean:
  1. 한 문장으로 아이디어를 말하면 4명의 전문가가 수다를 떨며 인터뷰 시작
  2. 3-5개 질문에 답하면 동작하는 스킬 파일이 완성
  3. 모든 질문에 설명과 장단점이 있으니 읽고 고르면 됨
  4. 모르겠으면 (추천) 표시된 걸 고르면 됨

---

## 인수 있음 — 바로 인터뷰 시작

인수를 스킬 아이디어로 받아서 인터뷰(Phase A)를 바로 시작합니다.

예: `/skillers-suda 유튜브 댓글을 분석해서 인사이트를 뽑아주는 스킬`

→ 해당 아이디어로 4명의 전문가 내부 의논 후 인터뷰 시작.

---

## 분석 모드 — "분석 [경로]"

예: `/skillers-suda 분석 skills/my-skill/SKILL.md`

주어진 경로의 스킬 파일을 읽고 4명의 전문가 관점에서 분석합니다.

**분석 항목:**
- **기획자 관점**: 목적이 명확한가? 트리거 키워드가 충분한가?
- **사용자 관점**: 바이브코더가 쓰기 쉬운가? 설명이 이해하기 쉬운가?
- **전문가 관점**: 워크플로우가 기술적으로 올바른가? 스크립트/API 활용이 적절한가?
- **검수자 관점**: 엣지 케이스가 처리되는가? 에러 핸들링이 있는가?

**결과 형식:**

```
분석 결과를 알려드릴게요!

기획자: "{평가}"
사용자: "{평가}"
전문가: "{평가}"
검수자: "{평가}"

개선 제안:
1. {제안 1}
2. {제안 2}
3. {제안 3}

개선해드릴까요?

A. [개선] 제안대로 수정해줘
B. [선택] 일부만 수정하고 싶어
C. [유지] 지금 이대로 괜찮아
```

---

## 실행

스킬 파일을 읽고 워크플로우를 따른다:

1. Read `${CLAUDE_PLUGIN_ROOT}/skills/skillers-suda/SKILL.md`
2. Read `${CLAUDE_PLUGIN_ROOT}/skills/skillers-suda/references/interview-guide.md`
3. SKILL.md의 워크플로우를 따라 실행: `$ARGUMENTS`
4. 모든 질문은 반드시 AskUserQuestion 도구를 호출한다 — 텍스트로 출력하면 안 된다
