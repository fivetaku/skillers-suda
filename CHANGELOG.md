# Changelog

## [0.6.0] - 2026-03-05

### Added
- Eval 기준 정의 — Phase D에서 워크플로우와 함께 eval 시나리오(정상 2-3개 + 엣지 1-2개) 정의
- 자동 검증 스크립트 (`scripts/verify-skill.py`) — frontmatter, writing style, word count, references 자동 체크
- Phase E-verify 단계 신설 — 파일 생성 직후 자동 검증, FAIL 시 자동 수정 후 재검증
- `references/eval-guide.md` — Eval 방법론 레퍼런스 (시나리오 정의, 검증 항목, 자동 수정 규칙)

### Changed
- Phase D: 워크플로우 확인에 eval 시나리오 포함
- Phase F: eval 시나리오 기반 구조적 테스트로 개선
- AI 행동 규칙에 eval 정의 필수, verify-skill.py 실행 필수 추가

## [0.5.0] - 2026-03-05

### Added
- Writing Style 가이드 통합 — SKILL.md 생성 시 imperative form, third-person description 강제
- Concise 원칙 적용 — 본문 1,500-2,000 단어 기준 (기존 2,000-3,000에서 조정)
- assets/ 폴더 지원 — 템플릿, 이미지, 폰트 등 출력용 파일 분리
- references/writing-style-guide.md — 작성 규칙 + 검증 체크리스트 레퍼런스
- Description 품질 기준 — trigger phrase 3-5개, 한/영 혼합, third-person 형식

### Changed
- Phase E 파일 구조에 assets/ 추가
- SKILL.md 생성 템플릿에 Writing Style 규칙 + Assets 섹션 추가
- AI 행동 규칙에 writing style, assets 활용, concise 원칙 명시

## [0.2.3] - 2026-03-02

### Fixed
- AskUserQuestion 도구 호출 보장을 위한 SKILL.md 전면 개선 (7가지 근본 원인 해결)
  - 실행 앵커 강화: "WHEN TRIGGERED" 섹션을 구체적 실행 지시서로 교체
  - 모든 AskUserQuestion 블록에 "EXECUTE:" 명령형 키워드 적용 (Phase A/B/C/D/F)
  - Phase C "예시 JSON" 표현 제거 → "EXECUTE:" 패턴으로 교체
  - Phase D "먼저 텍스트로 보여줍니다" 제거 → markdown 프리뷰로 대체
  - 질문 규칙 테이블의 부정형 지시 → 긍정형 "EXECUTE:" 참조로 변경

## [0.2.2] - 2026-03-02

### Fixed
- Command file 실행 섹션: "스킬 위치:" 정보 제공 → 명시적 Read 지시로 변경
  - SKILL.md + interview-guide.md 파일을 반드시 Read하도록 번호 리스트 추가
  - AskUserQuestion 도구 호출 필수 규칙 명시
  - 이 변경으로 SKILL.md가 로드되지 않아 AskUserQuestion이 텍스트로 출력되던 문제 해결

## [0.2.1] - 2026-03-02

### Fixed
- AskUserQuestion pseudo-code 5개를 JSON 형식으로 전환 — 도구 호출 보장

## [0.2.0] - 2026-03-02

### Changed
- 4명 페르소나 시뮬레이션 → Agent Team 아키텍처로 전면 재설계
- Phase B에서 4개 에이전트를 Agent 도구로 실제 병렬 스폰
- interview-guide.md를 Agent Team 방식으로 재작성

## [0.1.0] - 2026-03-01

### Added
- Phase 1 MVP 구현
- 4명 페르소나 인터뷰 시스템 (기획자/사용자/전문가/검수자)
- 6가지 워크플로우 단계 타입 (prompt/script/api_mcp/rag/review/generate)
- 컴포넌트 타입 자동 판단 (스킬/에이전트/커맨드)
- SKILL.md + scripts/ + references/ 자동 생성
- AskUserQuestion 반복 고도화
- 테스트 설계 + 피드백 루프
- /skillers-suda 슬래시 커맨드
- validate-skill.sh 검증 스크립트
- 5개 레퍼런스 문서 (progressive disclosure)
