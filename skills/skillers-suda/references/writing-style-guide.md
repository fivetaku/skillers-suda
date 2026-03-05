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
