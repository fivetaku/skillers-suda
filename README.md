English | [한국어](README.ko.md)

# skillers-suda

> **Four expert agents chatter, debate, and turn your vague idea into a working Claude Code skill.**

You describe an idea. Four personas — planner, user, expert, reviewer — spin up as real parallel agents, argue it out, then walk you through a structured interview. What comes out the other end is a fully scaffolded skill, agent, or command, automatically verified against 9 quality criteria, benchmarked with A/B eval, and trigger-optimized so Claude actually knows when to use it.

[Quick Start](#quick-start) • [Why skillers-suda?](#why-skillers-suda) • [How It Works](#how-it-works) • [Features](#features) • [Experts](#the-four-experts) • [Requirements](#requirements)

---

## Quick Start

### 1. Add the marketplace (once)

```
/plugin marketplace add https://github.com/fivetaku/gptaku_plugins.git
```

### 2. Install the plugin

```
/plugin install skillers-suda
```

### 3. Restart Claude Code

### 4. Build your first skill

```
/skillers-suda make a translation skill
```

Or just say what you want in natural language:

```
make me a skill
create an agent
build a command
```

---

## Why skillers-suda?

- **No coding knowledge required** — every question comes with explanations and tradeoffs; pick the one marked (recommended) if unsure
- **Real agents, not simulated personas** — four Claude subagents run in parallel, each analyzing your idea from a different angle before the interview even starts
- **Multi-step workflow design** — not a single-prompt skill; six step types (prompt, script, api_mcp, rag, review, generate) are composed automatically based on your answers
- **Built-in quality gate** — 9 structural checks run immediately after generation; FAIL items are auto-fixed before you ever see the result
- **A/B eval baked in** — skill-applied vs. baseline results are compared automatically so you know the skill actually helps
- **Trigger optimization that works** — description is refined over up to 5 iterations with train/test split to prevent overfitting
- **Analysis mode included** — point it at any existing skill or agent file and get a four-perspective critique with actionable improvement suggestions

---

## How It Works

```
You: "make a translation skill"
         ↓
Four expert agents spawn in parallel (planner / user / expert / reviewer)
         ↓
"We talked it over — here's what we think..."
         ↓
Structured interview (3–5 questions, each with options + explanations)
         ↓
Workflow design (prompt / script / api_mcp / rag / review / generate steps)
         ↓
SKILL.md + scripts/ + references/ generated automatically
         ↓
Quality verification (9 checks) → FAIL items auto-fixed → re-verified
         ↓
Eval runs (with_skill vs. without_skill A/B comparison)
         ↓
Description optimized (up to 5 iterations, 60/40 train/test split)
         ↓
"Want to test it?" → feedback → refinement loop
```

---

## Features

### Skill creation workflow (9 phases)

| Phase | What happens |
|-------|-------------|
| A — Idea collection | Gathers your idea via AskUserQuestion; extracts from conversation context if a workflow is already present |
| B — Expert team spawn | Four agents run in parallel; each analyzes the idea from their role perspective |
| C — Interview | 3–5 structured questions with options, descriptions, and recommended defaults |
| D — Workflow confirmation | Step types and sequence confirmed before any files are written |
| E — File generation | SKILL.md + scripts/ + references/ scaffold written automatically |
| F — Eval | with_skill vs. without_skill scenarios compared; scoring agent grades each; results in eval_review.html |
| G — Quality verification | verify-skill.py checks 9 structural items; auto-fixes FAILs and re-verifies |
| H — Description optimization | run_loop.py generates ~20 trigger/non-trigger queries, iterates up to 5× to find the best description |
| I — Test and refine | Interactive refinement loop — adjust tone, add API steps, optimize scripts |

### Quality verification (9 checks)

| Check | What it validates |
|-------|-----------------|
| frontmatter | YAML header is well-formed |
| name | Skill name is present |
| description | Trigger description is present |
| third_person | Description uses third-person form |
| trigger_phrases | Sufficient trigger phrases exist |
| word_count | Content is not too sparse |
| imperative_form | Instructions use imperative form |
| references_exist | Referenced files in references/ are present |
| progressive_disclosure | Stepwise disclosure structure is used |

Each check reports PASS / WARN / FAIL. FAILs are auto-corrected before the skill is handed to you.

### Workflow step types

| Type | Description | Example |
|------|-------------|---------|
| prompt | Claude handles via reasoning | Text analysis, summarization, translation |
| script | Repeatable / consistent / API work → Python or Bash | API calls, data parsing |
| api_mcp | External tool integration (API preferred over MCP) | Slack send, DB query |
| rag | Knowledge retrieval from references/ | Glossary, style guide |
| review | Quality check (AI or user) | Translation accuracy, code quality |
| generate | Final output production | File creation, report output |

### Analysis mode

Run `/skillers-suda analyze <path>` on any existing skill or agent file. The four experts each review from their own perspective and produce a consolidated improvement report.

```
/skillers-suda analyze skills/my-skill/SKILL.md
/skillers-suda analyze .claude/agents/my-agent.md
```

### Component selection

After the interview, the skill automatically determines whether your use case calls for a skill, agent, or command — and generates the appropriate file structure.

---

## The Four Experts

| Expert | Role | Asks |
|--------|------|------|
| Planner | Direction and scope | "Who uses this? What problem does it solve?" |
| User | UX validation | "How would I actually use this?" |
| Expert | Technical feasibility | "Here's what to watch out for in this domain" |
| Reviewer | Edge case detection | "Does this still work in this case?" |

All four spawn as real parallel Claude subagents — not role-play simulation.

---

## Commands

| Command | Description |
|---------|-------------|
| `/skillers-suda` | Interactive menu (new skill / analyze / how-to) |
| `/skillers-suda [description]` | Start interview immediately with your idea |
| `/skillers-suda analyze [path]` | Analyze an existing skill or agent file |

### Natural language triggers

- "make me a skill"
- "create an agent"
- "build a command"
- "skillers-suda"
- "skill builder"

---

## Requirements

- [Claude Code](https://docs.anthropic.com/claude-code) CLI
- Claude Max/Pro subscription or a supported Claude API key

No other dependencies. No npm install. No build step.

---

## License

MIT

---

<div align="center">

**Say one sentence. Get a working skill.**

</div>
