# Changelog

## [1.0.0] - 2026-03-06

### Added
- Anthropic skill-creator 통합 — eval/benchmark/description 최적화 기능 원스톱 제공
- Phase A: 대화 컨텍스트 추출 — 기존 대화에서 워크플로우 자동 추출
- Phase B: MCP 추천 — 전문가 에이전트가 `references/mcp-catalog.md` 기반으로 적합한 MCP 서버 추천
- Phase F: 자동 eval 실행 + 벤치마크 — subagent 병렬 실행, baseline 비교, grading, aggregate_benchmark, eval-viewer
- Phase G: 반복 개선 — 피드백 기반 수정 + 일반화 원칙 + 반복 코드 번들 + blind comparison
- Phase H: Description 최적화 — eval 쿼리 20개 → eval_review.html 리뷰 → run_loop.py (train/test 분할) → best_description 적용
- Phase I: 패키징 — package_skill.py로 .skill 파일 생성
- Scripts 9개 (skill-creator에서 복사): run_eval.py, run_loop.py, utils.py, aggregate_benchmark.py, generate_report.py, improve_description.py, package_skill.py, quick_validate.py
- Agents 3개: grader.md, comparator.md, analyzer.md (eval 채점/비교/분석)
- Eval-viewer: generate_review.py + viewer.html (브라우저 기반 eval 결과 리뷰)
- Assets: eval_review.html (description 최적화용 eval 쿼리 리뷰 템플릿)
- References: schemas.md (JSON 스키마), mcp-catalog.md (MCP 서버 카탈로그), improvement-principles.md (개선 원칙), trigger-mechanism.md (트리거 메커니즘)
- THIRD_PARTY_LICENSES (Apache 2.0, Anthropic skill-creator)

### Changed
- Phase D: eval 시나리오를 evals.json 형식으로 강화 (should-trigger / should-not-trigger, 현실적 프롬프트)
- Phase E: Description 작성을 Pushy 전략으로 변경 (undertrigger 방지), Why 설명 우선 원칙
- AI 행동 규칙: eval 자동 실행, description 최적화, 일반화 원칙, 반복 코드 번들 추가

### Removed
- Phase E의 description 후보 2-3개 비교 방식 (run_loop.py 자동 최적화로 대체)

## [0.7.0] - 2026-03-06

### Added
- Description 최적화 — SKILL.md 생성 후 description 후보 2-3개 생성 → 평가 기준(커버리지, 구체성, 간결성)으로 비교 → 최적 선택
- Degrees of Freedom — Phase D에서 고정/가변 요소 식별, 가변 요소는 Settings 섹션에 기본값 + 변경 방법 명시
- SKILL.md 템플릿에 Settings 섹션 추가 (가변 요소 있을 때만)

### Changed
- Phase D: 자유도 식별 단계 추가
- Phase E: description 최적화 절차 추가
- AI 행동 규칙에 description 최적화, 자유도 식별 필수 규칙 추가

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
