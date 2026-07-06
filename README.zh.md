[English](README.md) | [한국어](README.ko.md) | 中文 | [日本語](README.ja.md) | [Español](README.es.md)

# skillers-suda

<p align="center">
  <img src="assets/skillers-suda-hero-01.png" alt="skillers-suda" width="320">
</p>

> **四位专家代理边聊边辩，把你模糊的想法变成能用的 Claude Code 技能。**

你只需描述一个想法。规划师、用户、专家、评审员四个角色会以真正的并行代理身份启动，先内部讨论一番，再引导你完成一场结构化访谈。最终产出是一个完整脚手架的技能、代理或命令——自动通过 9 项质量标准验证、经 A/B eval 基准测试，并完成触发优化，让 Claude 真正知道何时该调用它。

[快速开始](#快速开始) • [为什么选择 skillers-suda？](#为什么选择-skillers-suda) • [工作原理](#工作原理) • [功能](#功能) • [四位专家](#四位专家) • [环境要求](#环境要求)

---

## 快速开始

### 1. 添加市场（仅需一次）

```
/plugin marketplace add https://github.com/fivetaku/gptaku_plugins.git
```

### 2. 安装插件

```
/plugin install skillers-suda
```

### 3. 重启 Claude Code

### 4. 创建你的第一个技能

```
/skillers-suda make a translation skill
```

或者直接用自然语言表达你的需求：

```
make me a skill
create an agent
build a command
```

---

## 为什么选择 skillers-suda？

- **无需编程知识** —— 每个问题都附带说明和取舍分析；拿不准就选标有 (recommended) 的选项
- **真正的代理，而非角色扮演** —— 四个 Claude 子代理并行运行，在访谈开始前就从各自角度分析你的想法
- **多步骤工作流设计** —— 不是单一提示词技能；六种步骤类型（prompt / script / api_mcp / rag / review / generate）会根据你的回答自动组合
- **内置质量关卡** —— 生成后立即运行 9 项结构检查；FAIL 项在你看到结果之前就已自动修复
- **A/B eval 开箱即用** —— 自动对比启用技能与基线的结果，让你确认技能真的有效
- **切实有效的触发优化** —— 通过 train/test 分割防止过拟合，对 description 进行最多 5 轮迭代打磨
- **附带分析模式** —— 指向任何现有的技能或代理文件，即可获得四视角评审和可落地的改进建议

---

## 工作原理

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

## 功能

### 技能创建工作流（9 个阶段）

| 阶段 | 内容 |
|-------|-------------|
| A — 收集想法 | 通过 AskUserQuestion 收集你的想法；若对话上下文中已有工作流则直接提取 |
| B — 组建专家团队 | 四个代理并行运行，各自从自己的角色视角分析想法 |
| C — 访谈 | 3–5 个结构化问题，附带选项、说明和推荐默认值 |
| D — 确认工作流 | 在写入任何文件之前确认步骤类型和顺序 |
| E — 生成文件 | 自动写出 SKILL.md + scripts/ + references/ 脚手架 |
| F — Eval | 对比 with_skill 与 without_skill 场景；评分代理逐项打分，结果输出到 eval_review.html |
| G — 质量验证 | verify-skill.py 检查 9 项结构指标；自动修复 FAIL 并重新验证 |
| H — Description 优化 | run_loop.py 生成约 20 条触发/非触发查询，最多迭代 5 轮以找出最佳 description |
| I — 测试与打磨 | 交互式打磨循环 —— 调整语气、添加 API 步骤、优化脚本 |

### 质量验证（9 项检查）

| 检查项 | 验证内容 |
|-------|-----------------|
| frontmatter | YAML 头格式是否正确 |
| name | 是否有技能名称 |
| description | 是否有触发描述 |
| third_person | description 是否使用第三人称 |
| trigger_phrases | 触发短语是否足够 |
| word_count | 内容是否过于单薄 |
| imperative_form | 指令是否使用祈使句 |
| references_exist | references/ 中引用的文件是否存在 |
| progressive_disclosure | 是否采用渐进式披露结构 |

每项检查判定为 PASS / WARN / FAIL。FAIL 项会在技能交付给你之前自动修正。

### 工作流步骤类型

| 类型 | 说明 | 示例 |
|------|-------------|---------|
| prompt | 由 Claude 推理处理 | 文本分析、摘要、翻译 |
| script | 重复性 / 一致性 / API 工作 → Python 或 Bash | API 调用、数据解析 |
| api_mcp | 外部工具集成（API 优先于 MCP） | 发送 Slack、查询数据库 |
| rag | 从 references/ 检索知识 | 术语表、风格指南 |
| review | 质量检查（AI 或用户） | 翻译准确度、代码质量 |
| generate | 产出最终结果 | 生成文件、输出报告 |

### 分析模式

对任何现有的技能或代理文件运行 `/skillers-suda analyze <path>`。四位专家各自从自己的视角评审，并产出一份汇总的改进报告。

```
/skillers-suda analyze skills/my-skill/SKILL.md
/skillers-suda analyze .claude/agents/my-agent.md
```

### 组件自动判定

访谈结束后，技能会自动判断你的用例更适合技能、代理还是命令——并生成相应的文件结构。

---

## 四位专家

| 专家 | 角色 | 会问的问题 |
|--------|------|------|
| 规划师 | 方向与范围 | "谁来用？解决什么问题？" |
| 用户 | UX 验证 | "换成我，实际会怎么用？" |
| 专家 | 技术可行性 | "这个领域要注意这些坑" |
| 评审员 | 边界情况检测 | "这种情况下还能用吗？" |

四位专家全部以真正的并行 Claude 子代理身份启动——不是角色扮演式的模拟。

---

## 命令

| 命令 | 说明 |
|---------|-------------|
| `/skillers-suda` | 交互式菜单（新建技能 / 分析 / 使用说明） |
| `/skillers-suda [description]` | 带着想法直接开始访谈 |
| `/skillers-suda analyze [path]` | 分析现有的技能或代理文件 |

### 自然语言触发

- "make me a skill"
- "create an agent"
- "build a command"
- "skillers-suda"
- "skill builder"

---

## 环境要求

- [Claude Code](https://docs.anthropic.com/claude-code) CLI
- Claude Max/Pro 订阅，或受支持的 Claude API 密钥

没有其他依赖。无需 npm install。无需构建步骤。

---

## 许可证

MIT

---

<div align="center">

**说一句话，得到一个能用的技能。**

</div>
