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
description: {무엇을 하는지 한 문장}. Use when {언제 쓰는지}.
---
```

### 규칙
- **두 요소를 담는다**: 무엇을 하는지 + 언제 쓰는지
- 3인칭이면 형식은 자유: "Use when …", "This skill should be used when …", "~할 때 사용한다" 모두 된다
- 1,024자 이하
- 따옴표 트리거 목록은 선택이다. 키워드만 나열하면 "무엇을 하는지"가 빠진다
- 한국어 사용자가 대상이면 한국어·영어 표현을 함께 넣는다
- 최종 문구는 Phase H `run_loop.py`가 측정해 고른 결과가 이 규칙보다 우선한다

### 좋은 예시
```yaml
description: Translates documents with glossary support and a quality review pass. Use when the user wants a document translated (번역해줘, 영어로 바꿔줘) and terminology must stay consistent.
```

### 나쁜 예시
```yaml
description: Provides translation guidance.                          # what만 있고 when 없음
description: This skill should be used when the user asks to "번역", "translate", "번역해줘".  # 키워드 나열, what 없음
description: 번역 스킬입니다.                                          # 둘 다 모호
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
| SKILL.md 본문 | 짧을수록 좋다 | 500줄 이하 (약 5,000 단어) |
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
- [ ] 무엇을 하는지 + 언제 쓰는지 두 요소 포함
- [ ] 1,024자 이하
- [ ] (한국어 사용자 대상이면) 한국어 + 영어 표현

**Content 품질:**
- [ ] Imperative form 사용 (second person 없음)
- [ ] 본문은 짧을수록 좋다, 500줄 이하
- [ ] 상세 내용은 references/로 분리
- [ ] references/scripts/assets 참조 명시

**Progressive Disclosure:**
- [ ] SKILL.md에 핵심만
- [ ] 상세 문서는 references/
- [ ] 유틸리티는 scripts/
- [ ] 출력용 파일은 assets/

**건너뛰기 쉬운 규칙을 담는 스킬 (§6 참조):**
- [ ] 규칙마다 건너뛰면 무엇이 조용히 깨지는지 이유를 적었다
- [ ] 대문자 명령(ALWAYS/NEVER/NO … WITHOUT …)으로 대신하지 않았다

## 6. 건너뛰기 쉬운 규칙 — 명령 대신 이유

"테스트 먼저", "완료 전 검증"처럼 AI가 압박받으면 건너뛰고 싶어지는 규칙을 담는 스킬도 기본 원칙은 같다: **ALWAYS/NEVER 대신 이유를 설명한다.** LLM은 이유를 이해하면 더 잘 따르고, 규칙이 맞지 않는 상황에서도 의도에 맞게 판단한다. 대문자 한 줄 규칙이나 변명 반박표는 규칙의 이유를 가리고, 맞지 않는 상황에서도 기계적으로 적용되게 만든다.

작성법:
1. 규칙을 한 문장으로 쓴다. 대문자·절대어("반드시", "절대") 대신 평서문으로.
2. 바로 뒤에 **건너뛰면 무엇이 깨지는지**를 쓴다. 특히 *조용히* 깨지는 경우(나중에야 발견되는 경우)를 구체적으로.
3. 규칙이 적용되지 않는 예외가 있으면 함께 적는다. 예외가 없다고 우기기보다 경계를 밝히는 편이 잘 지켜진다.
4. 지켜졌는지 확인할 수 있는 흔적(로그, 테스트 출력, 파일)을 요구한다. 말보다 증거가 규칙을 지키게 한다.

예:
```markdown
완료를 보고하기 전에 방금 실행한 검증 출력(테스트 결과, exit code)을 함께 붙인다.
이전 실행 결과나 기억으로 "통과했다"고 쓰면, 그 사이 바뀐 코드가 깨져 있어도 아무도 모른 채 넘어간다.
문서만 고친 변경처럼 실행할 검증이 없으면 "검증 대상 없음"이라고 적는다.
```

기법형 스킬(번역·포맷팅 등)에는 이런 장치 자체가 필요 없다 — 워크플로우만 쓴다.
