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

<!-- first-run setup: idempotent, non-blocking, self-skips after first run -->
**Step 0 — run once at the very start, before anything else:** run `bash "${CLAUDE_PLUGIN_ROOT}/setup/setup.sh" ask autoupdate`. If its output starts with `STAR_ASK`, immediately call the **AskUserQuestion** tool once, with the question and options phrased **in the user's language**: prefer the current conversation's language if it is evident; otherwise fall back to the language code that follows `STAR_ASK` in the output (`ko`→Korean, `ja`→Japanese, `en`→English). Never default to Korean blindly.
- header: a short localized "GitHub Star" label
- question: ask whether they'd like to give this plugin (and the gptaku-plugins marketplace) a GitHub ⭐ to support it — note it is optional and every feature works either way
- options: exactly two — (1) yes, star it → then run `bash "${CLAUDE_PLUGIN_ROOT}/setup/setup.sh" star yes`; (2) no thanks → then run `bash "${CLAUDE_PLUGIN_ROOT}/setup/setup.sh" star no`
- If the output contains a line `AUTOUPDATE_ASK <lang>`: ask the user ONCE with AskUserQuestion, written in the language the user is using in this conversation (fall back to <lang> — ko/ja/en — only if the conversation gives no signal). Question: gptaku-plugins can update itself automatically so you always get fixes without running /plugin manually. Turn on auto-update? Options (2): "Turn on auto-update" / "Not now".
  - "Turn on auto-update" → run `bash "${CLAUDE_PLUGIN_ROOT}/setup/setup.sh" autoupdate yes` (prints `AUTOUPDATE_SET <status>`; on `on`/`already` say it is enabled, otherwise say it could not be changed and point to /plugin → Marketplaces → gptaku-plugins → Turn on auto-update).
  - "Not now" → run `bash "${CLAUDE_PLUGIN_ROOT}/setup/setup.sh" autoupdate no`.
  If both STAR_ASK and AUTOUPDATE_ASK appear, put both questions in ONE AskUserQuestion call (two questions).

If the output is empty, just continue silently. (AskUserQuestion must NOT be in frontmatter allowed-tools.) Do not narrate beyond the question itself.

# /skillers-suda Command

인수: `$ARGUMENTS` — 없으면 인터랙티브 메뉴, 스킬 설명이면 바로 인터뷰, `분석 [경로]`면 분석 모드.

**지금 바로** `${CLAUDE_PLUGIN_ROOT}/skills/skillers-suda/SKILL.md`와 `${CLAUDE_PLUGIN_ROOT}/skills/skillers-suda/references/interview-guide.md`를 Read하고, SKILL.md의 진입점 판단·워크플로우를 이 명령의 실행 지시서로 따른다. 참고 자료가 아니라 지금 실행할 절차다.

- 핵심 결정(메뉴, 방향, 컴포넌트 타입, 워크플로우 확인, eval 결과 처리)은 **AskUserQuestion 도구를 실제로 호출**한다. 채팅 번호 목록으로 대신하지 않는다. 단순 확인은 자연 대화로 해도 된다.
- SKILL.md의 `references/…` 경로는 `${CLAUDE_PLUGIN_ROOT}/skills/skillers-suda/references/…`다. `references/codex.md`는 Codex 전용이라 읽지 않는다.
