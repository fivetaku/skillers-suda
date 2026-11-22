# 질문·출력 템플릿

SKILL.md 각 Phase에서 쓰는 AskUserQuestion JSON과 대화 출력 형식을 모은 파일이다.
JSON은 출발점이다. 옵션은 그때의 토론 결과·대화에 맞게 채우거나 바꾼다.

공통 규칙:
- 핵심 결정(컴포넌트 타입, 방향, 워크플로우 확인, eval 결과 처리)은 AskUserQuestion으로 묻는다. 선택지가 분명하고, 버튼으로 고르는 편이 바이브코더에게 쉽기 때문이다.
- 단순 확인이나 짧은 추가 질문("혹시 이런 뜻인가요?")은 자연 대화로 해도 된다.
- 옵션마다 description을 쓰고, 추천 옵션은 첫 번째에 "(추천)"을 붙인다. 쉬운 말로 쓴다.
- "Other"(직접 입력)는 자동 제공되므로 따로 넣지 않는다.

---

## Q1. Phase A — 아이디어 수집

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

## Q2. Phase B — 방향 확인 (의견 충돌이 있을 때)

충돌 포인트 자체를 선택지로 만든다.

```json
{
  "questions": [
    {
      "question": "{충돌 내용을 구체적으로 — 예: '커맨드로 만들까요, 스킬로 만들까요?'}",
      "header": "방향",
      "options": [
        {"label": "{선택지A} (추천)", "description": "{왜 이게 나은지 — 전문가 근거 요약}"},
        {"label": "{선택지B}", "description": "{왜 이걸 고를 수 있는지 — 다른 전문가 근거}"},
        {"label": "다시 토론해줘", "description": "추가 정보를 주면 전문가들이 다시 분석해요."}
      ],
      "multiSelect": false
    }
  ]
}
```

## Q3. Phase B — 방향 확인 (충돌이 없을 때)

핵심 결정 사항을 `preview`에 요약한다.

```json
{
  "questions": [
    {
      "question": "전문가들이 합의한 방향이에요. 확인해주세요.",
      "header": "방향",
      "options": [
        {"label": "좋아요, 진행 (추천)", "description": "이 방향대로 워크플로우를 설계할게요.", "preview": "{MVP 범위}\n{핵심 워크플로우 요약}\n{컴포넌트 타입}"},
        {"label": "수정할 부분 있어요", "description": "어떤 부분을 바꾸고 싶은지 알려주세요."},
        {"label": "다시 토론해줘", "description": "추가 정보를 주면 전문가들이 다시 분석해요."}
      ],
      "multiSelect": false
    }
  ]
}
```

## Q4. Phase C — 상세 인터뷰 (예: 출력 형태)

토론에서 결정하지 못한 항목만, 최대 2개.

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

## Q5. Phase D — 비슷한 기존 에이전트 발견

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

## Q6. Phase D — 워크플로우 + Eval 확인

```json
{
  "questions": [
    {
      "question": "워크플로우와 테스트 기준을 확인해주세요.",
      "header": "워크플로우 + Eval",
      "options": [
        {"label": "이대로 진행 (추천)", "description": "이 워크플로우대로 파일을 만들고 자동 검증까지 해드릴게요."},
        {"label": "수정할 부분 있어", "description": "워크플로우나 테스트 기준을 바꾸고 싶은지 알려주세요."},
        {"label": "나중에 할게", "description": "여기서 멈출게요. 나중에 다시 시작할 수 있어요."}
      ],
      "multiSelect": false
    }
  ]
}
```

## Q7. Phase F — Eval 결과 처리

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

## Q8. 에이전트 분석 모드 — 개선안 적용

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

---

## 출력 형식 — Phase B 토론 결과 종합

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

의견이 갈린 부분은 숨기지 않고 보여준다:

```
⚡ 의견이 갈렸어요:
- 기획자는 "{A}"를 제안했지만, 사용자는 "{B}"가 더 낫다고 했어요.
- 어떤 방향이 좋을까요?
```

## 출력 형식 — Phase D 워크플로우 + Eval 미리보기

```
워크플로우 설계 결과:

1단계: [설명]
2단계: [설명]
...

Eval 시나리오:
- should-trigger: [시나리오 1], [시나리오 2]
- should-not-trigger: [시나리오 1]
```
