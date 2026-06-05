# Writing Style 가이드

생성되는 SKILL.md의 품질을 높이기 위한 작성 규칙.
Anthropic의 skill-creator, Codex의 skill-creator, plugin-dev의 skill-development 베스트 프랙티스를 통합.

## 1. Imperative Form (명령형)

SKILL.md 본문은 **imperative/infinitive form**(동사 시작 지시문)으로 작성한다.
Second person ("You should...") 금지.

### 올바른 예시
```
Read the configuration file.
Parse the frontmatter using sed.
Validate the input before processing.
To accomplish X, do Y.
```

### 잘못된 예시
```
You should read the configuration file.
You need to parse the frontmatter.
You can use the grep tool to search.
Claude should extract fields...
```

## 2. Description (Frontmatter)

### 형식
```yaml
---
name: skill-name
description: This skill should be used when the user asks to "trigger1", "trigger2", "trigger3".
---
```

### 규칙
- **Third-person** 필수: "This skill should be used when..."
- **구체적 trigger phrase** 3-5개 포함 — 사용자가 실제로 말할 문장
- 한국어 트리거와 영어 트리거 모두 포함
- "무엇을 하는지"와 "언제 사용하는지" 모두 포함

### 좋은 예시
```yaml
description: This skill should be used when the user asks to "번역해줘", "translate this document", "문서 번역", "영어로 바꿔줘". Translates documents with glossary support and quality review.
```

### 나쁜 예시
```yaml
description: Use this skill when translating.  # Wrong person, vague
description: Provides translation guidance.     # No trigger phrases
description: 번역 스킬입니다.                    # Not third person, no triggers
```

## 3. Concise 원칙

### 컨텍스트 윈도우는 공공재
스킬은 시스템 프롬프트, 대화 기록, 다른 스킬 메타데이터와 컨텍스트를 공유한다.
각 문장이 토큰 비용만큼의 가치가 있는지 자문한다.

### 기본 가정: Claude는 이미 똑똑하다
Claude가 이미 아는 정보는 반복하지 않는다. 비자명한(non-obvious) 절차적 지식만 포함.

### 단어 수 기준

| 파일 | 목표 | 최대 |
|------|------|------|
| SKILL.md 본문 | 1,500-2,000 단어 | 3,000 단어 (500줄) |
| references/ 개별 파일 | 2,000-5,000 단어 | 제한 없음 |
| description | 1-2문장 | 100 단어 |

### Progressive Disclosure (3단계 로딩)
1. **메타데이터** (name + description) — 항상 컨텍스트에 (~100 단어)
2. **SKILL.md 본문** — 스킬 트리거 시 (<5k 단어)
3. **references/scripts/assets** — 필요 시만 (무제한)

### 분리 기준
SKILL.md에 남겨야 할 것:
- 핵심 워크플로우
- 빠른 참조 테이블
- references/scripts/assets 포인터

references/로 옮겨야 할 것:
- 상세 패턴, 고급 기법
- API 문서, 스키마
- 엣지 케이스, 트러블슈팅
- 긴 예시, 워크스루

## 4. 파일 구조 규칙

### assets/ 폴더
출력물에 사용되는 파일. 컨텍스트에 로드하지 않음.

- 템플릿 (HTML, React 보일러플레이트)
- 이미지, 아이콘, 폰트
- 샘플 데이터, 설정 파일 프리셋

### scripts/ vs references/ vs assets/ 판단

| 질문 | Yes → |
|------|-------|
| 같은 코드를 반복 작성하나? | scripts/ |
| Claude가 참고해야 하는 문서인가? | references/ |
| 출력에 직접 사용하는 파일인가? | assets/ |

### 불필요한 파일 금지
- README.md, INSTALLATION_GUIDE.md, CHANGELOG.md 등 보조 문서 생성 금지
- AI가 작업하는 데 필요한 파일만 포함

## 5. 검증 체크리스트

생성된 스킬이 이 기준을 충족하는지 확인:

**구조:**
- [ ] SKILL.md에 유효한 YAML frontmatter 존재
- [ ] name, description 필드 존재
- [ ] 참조된 파일이 실제로 존재

**Description 품질:**
- [ ] Third-person ("This skill should be used when...")
- [ ] 구체적 trigger phrase 3-5개 포함
- [ ] 한국어 + 영어 트리거 모두 포함

**Content 품질:**
- [ ] Imperative form 사용 (second person 없음)
- [ ] 본문 1,500-2,000 단어 이내
- [ ] 상세 내용은 references/로 분리
- [ ] references/scripts/assets 참조 명시

**Progressive Disclosure:**
- [ ] SKILL.md에 핵심만
- [ ] 상세 문서는 references/
- [ ] 유틸리티는 scripts/
- [ ] 출력용 파일은 assets/

**규율형(Discipline) 스킬일 때만 (§6 참조):**
- [ ] Iron Law 1줄 (스킬 상단)
- [ ] 합리화 차단표 (Excuse → Reality)
- [ ] Red Flags 자기점검 리스트
- [ ] Spirit vs Letter 한 줄

## 6. 규율형(Discipline) 스킬의 합리화 차단 장치

> 출처: obra/superpowers `writing-skills` — "Bulletproofing Skills Against Rationalization".
> LLM은 압박을 받으면 규칙의 루프홀을 찾는다. 규칙을 **말하는 것**과 **지켜지게 만드는 것**은 다르다.

### 6-1. 먼저 판별 — 이 스킬은 규율형인가?

스킬은 두 부류로 나뉜다:

| 부류 | 정의 | 예시 | 차단 장치 |
|------|------|------|----------|
| **규율형(Discipline)** | AI가 압박받으면 건너뛰고 싶어하는 규칙을 강제 | "테스트 먼저", "근본원인 먼저", "완료 전 검증", "직접 코딩 금지" | **필수 (아래 4종)** |
| **기법형(Technique/Pattern)** | 방법·패턴·워크플로우를 안내 | 번역, 회의록 정리, 데이터 포맷팅 | 불필요 (넣지 마라 — 토큰 낭비) |

**판별 기준 (하나라도 Yes → 규율형):**
- "X 하기 전에 반드시 Y"를 강제하는가?
- AI가 시간 압박·단순함을 핑계로 건너뛸 유인이 있는가?
- 건너뛰면 **조용히** 실패(나중에 발견)하는가?

기법형이면 6-2~6-5를 **생략**한다. 규율형에만 적용한다.

### 6-2. Iron Law (절대 규칙 한 줄)

규율의 핵심을 한 줄 대문자 규칙으로. SKILL.md **상단**(소개 직후)에 배치.

```
**Iron Law: NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE.**
```

형식: `NO {행동} WITHOUT {선행조건} FIRST`. 한국어 병기 가능 — 단 규칙은 한 줄, 모호어("적절히", "가능하면") 금지.

### 6-3. 합리화 차단표 (Excuse → Reality)

AI가 규칙을 건너뛸 때 만들 변명을 **미리** 표로 반박한다. 규칙만 적지 말고 *특정 우회로*를 명시해 봉쇄.

```markdown
## 합리화 차단표
| 이런 변명이 떠오르면 | 현실 |
|---------------------|------|
| "이건 너무 간단해서 안 거쳐도 됨" | 간단한 게 사고 난다. 절차는 30초면 끝난다 |
| "급하니까 그냥 넘어가자" | 절차가 추측-수정 반복보다 빠르다 |
| "나중에 한꺼번에 검증하지" | '나중'은 안 온다. 지금 안 하면 영영 안 한다 |
```

작성법: "이 규칙을 건너뛴다면 나는 뭐라고 변명할까?"를 3-5개 상상 → 각각 한 줄로 반박.

### 6-4. Red Flags 자기점검 리스트

규칙 위반 **직전의 생각 신호**를 나열한다. AI가 합리화 중인 자신을 잡아내게 한다.

```markdown
## Red Flags — STOP
이 생각이 들면 멈추고 규칙으로 복귀하라:
- "그냥 이번 한 번만..."
- "확인 안 해도 될 것 같은데"
- "거의 다 됐으니 됐다고 하자"
→ 전부 같은 의미다: 규칙을 건너뛰는 중. 멈춰라.
```

### 6-5. Spirit vs Letter (루프홀 봉쇄)

규칙 끝에 한 줄 고정 문구. 문자만 지키고 의도를 무력화하는 우회를 차단.

```
**규칙의 문구(letter)를 어기는 것은 규칙의 의도(spirit)를 어기는 것이다.**
```

### 작성 절차 (규율형 스킬 생성 시)

1. 이 스킬이 강제하는 핵심 규칙 1개 → **Iron Law** (6-2)
2. 그 규칙을 건너뛸 변명 3-5개 상상 → **합리화 차단표** (6-3)
3. 위반 직전 신호 3-5개 → **Red Flags** (6-4)
4. **Spirit vs Letter** 한 줄 추가 (6-5)

> 주의: 이 4종은 *규율형 스킬에만*. 기법형(번역·포맷팅 등)에 넣으면 불필요한 압박 + 토큰 낭비다. 6-1 판별을 먼저 통과한 경우만 적용한다.
