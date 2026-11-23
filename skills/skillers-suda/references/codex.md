# Codex에서 실행할 때 (skillers-suda)

SKILL.md 절차는 그대로 따르고, 아래 차이만 적용한다.

## 선택지 질문 = 질문 도구 (이번 세션 도구 목록으로 판단)

1. `request_user_input_async`가 있으면 선택지 질문 1콜 = 이 도구 1콜. 문항 ≤4개.
   - 형식: `{"questions":[{"title":"헤더 — 한 줄 질문","options":["라벨 (추천) — 뭔지, 장점, 단점","대안 — 뭔지, 트레이드오프"]}]}`
   - 문항에는 `title`·`options`만. `question`·`header`·`id`를 넣으면 파싱 오류가 난다.
   - 추천안을 맨 앞에. "기타·직접 적기" 옵션은 넣지 않는다(자유 입력 칸이 자동으로 붙는다).
   - 부른 뒤 "위 질문에 답해 주시면 이어서 진행합니다" 한 줄만 쓰고 **턴을 끝낸다.** 답에 달린 결정을 추측으로 진행하지 않는다.
2. Plan 모드라 `request_user_input`만 있으면: 1콜 3문항까지. `header`(12자 이내)·`id`(snake_case)·`question`, 선택지 2~3개(`label`·`description`), 추천 라벨 끝에 `(Recommended)`.
3. 둘 다 없으면 채팅에 번호 블록으로 낸다(답은 "Q1-1, Q2-2"처럼, 모르면 1번으로 진행):

```text
Q1. <한 줄 질문>
  1. <추천안> (추천) — 무엇인지, 왜 좋은지, 트레이드오프
  2. <대안> — 무엇인지, 트레이드오프
  3. 문장으로 직접 적기
```

4. `codex exec`처럼 사람이 답할 수 없는 실행이면 묻지 않고 추천안으로 진행하고 가정을 기록한다.

**멈춤 지점:** Phase B Step 4 방향 확인(Q2/Q3)과 Phase D 워크플로우 확인(Q6)은 Codex에서도 생략하지 않는다. `request_user_input_async`는 바로 반환되지만 답이 온 것이 아니다 — 부른 뒤 턴을 끝내고, 답 없이 다음 Phase로 진행하지 않는다.

Phase A 첫 질문(아이디어 발굴)은 열린 채팅 질문이다. `question-templates.md`의 `preview`는 질문 도구 호출 직전 채팅에 짧게 먼저 보여준다.

## 도구 차이

- 서브에이전트(Phase B 4명 병렬 분석, eval 채점·비교): Claude의 `Agent` 대신 `spawn_agent`로 한 턴에 함께 띄운다. 스폰 도구가 없으면 메인 스레드에서 4관점을 순서대로 독립 섹션으로 작성한다(존재하지 않는 도구를 가정하지 않는다).
- 프롬프트 안의 `${CLAUDE_PLUGIN_ROOT}`는 이 플러그인 루트(SKILL.md에서 두 단계 위)의 실제 절대경로로 바꿔 넘긴다.
- `scripts/run_eval.py`·`run_loop.py`·`improve_description.py`는 `claude -p`를 서브프로세스로 쓴다 — Codex에서는 쓰지 않는다. eval은 스폰한 서브에이전트(없으면 메인 스레드 순차)로 with/without 실행을 대신하고 같은 디렉터리 구조로 저장한다. description 최적화는 수동으로 문구를 비교한다.
- 첫 실행 설정(`setup/setup.sh`)은 Claude Code 전용이다. Codex에서는 실행하지 않는다.

## 만든 스킬의 저장 위치·형식

- Claude Code는 `~/.claude/skills/<이름>/`(개인) 또는 프로젝트 `.claude/skills/<이름>/`이고, 에이전트는 `.claude/agents/`, 명령은 `commands/`다.
- Codex는 `$CODEX_HOME/skills/<이름>/`(개인, 기본 `~/.codex/skills`) 또는 프로젝트 `.agents/skills/<이름>/`에 둔다. SKILL.md frontmatter는 `name`·`description` 두 필드, 선택적으로 `references/`·`scripts/`·`assets/`.
- Codex에는 슬래시 커맨드 폴더와 에이전트 로스터 폴더가 없다. 진입은 description 트리거로, 자율 역할은 스킬의 `references/agents/<이름>.md`에 프롬프트로 두고 SKILL.md에서 "이 파일을 프롬프트로 서브에이전트를 스폰한다"고 적는다. `commands/*.md`·`.claude/agents/*.md`는 만들지 않는다.
- 플러그인 패키지로 묶으면 Claude 형식(`.claude-plugin/plugin.json` + `skills/`)을 쓴다. Codex도 이 형식을 읽는다.
- 기존 에이전트 확인(`.claude/agents/*.md` 스캔)은 Codex에서는 건너뛴다. 분석 모드의 에이전트 파일은 서브에이전트 프롬프트 파일(`references/agents/*.md`)로 읽는다.
