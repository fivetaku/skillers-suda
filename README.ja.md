[English](README.md) | [한국어](README.ko.md) | [中文](README.zh.md) | 日本語 | [Español](README.es.md)

# skillers-suda

<p align="center">
  <img src="assets/skillers-suda-hero-01.png" alt="skillers-suda" width="320">
</p>

> **4人の専門家エージェントがわいわい議論しながら、曖昧なアイデアを動く Claude Code スキルに変える。**

アイデアをひとこと伝えるだけ。プランナー・ユーザー・エキスパート・レビュアーの4つのペルソナが本物の並列エージェントとして起動し、議論を交わしたうえで、構造化されたインタビューへ案内します。最後に出てくるのは、完全にスキャフォールドされたスキル・エージェント・コマンド——9つの品質基準で自動検証され、A/B eval でベンチマークされ、Claude が確実に起動できるようトリガー最適化まで済んだ状態です。

[クイックスタート](#クイックスタート) • [なぜ skillers-suda？](#なぜ-skillers-suda) • [仕組み](#仕組み) • [機能](#機能) • [4人の専門家](#4人の専門家) • [必要環境](#必要環境)

---

## クイックスタート

### 1. マーケットプレイスを追加（初回のみ）

```
/plugin marketplace add https://github.com/fivetaku/gptaku_plugins.git
```

### 2. プラグインをインストール

```
/plugin install skillers-suda
```

### 3. Claude Code を再起動

### 4. 最初のスキルを作る

```
/skillers-suda make a translation skill
```

または、自然な言葉でそのまま伝えても構いません：

```
make me a skill
create an agent
build a command
```

---

## なぜ skillers-suda？

- **コーディング知識は不要** —— すべての質問に説明とトレードオフが付きます。迷ったら (recommended) マークの選択肢を選べば OK
- **ロールプレイではなく本物のエージェント** —— 4つの Claude サブエージェントが並列で動き、インタビューが始まる前にそれぞれの視点からアイデアを分析します
- **マルチステップのワークフロー設計** —— 単一プロンプトのスキルではありません。6種類のステップタイプ（prompt / script / api_mcp / rag / review / generate）が回答に応じて自動で組み合わされます
- **品質ゲート内蔵** —— 生成直後に9つの構造チェックを実行。FAIL 項目は結果を見せる前に自動修正されます
- **A/B eval 標準搭載** —— スキル適用時とベースラインの結果を自動比較し、スキルが本当に効いているかを確認します
- **実際に機能するトリガー最適化** —— 過学習を防ぐ train/test 分割つきで、description を最大5回反復して磨き上げます
- **分析モードも搭載** —— 既存のスキルやエージェントファイルを指定すれば、4つの視点からのレビューと実行可能な改善提案が得られます

---

## 仕組み

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

## 機能

### スキル生成ワークフロー（9フェーズ）

| フェーズ | 内容 |
|-------|-------------|
| A — アイデア収集 | AskUserQuestion でアイデアを収集。会話コンテキストにワークフローが既にあれば抽出 |
| B — 専門家チーム起動 | 4つのエージェントが並列実行され、それぞれの役割の視点からアイデアを分析 |
| C — インタビュー | 選択肢・説明・推奨デフォルトつきの構造化質問を3〜5問 |
| D — ワークフロー確認 | ファイルを書き込む前にステップタイプと順序を確認 |
| E — ファイル生成 | SKILL.md + scripts/ + references/ のスキャフォールドを自動生成 |
| F — Eval | with_skill と without_skill のシナリオを比較。採点エージェントが評価し、結果は eval_review.html で確認 |
| G — 品質検証 | verify-skill.py が9つの構造項目をチェック。FAIL を自動修正して再検証 |
| H — Description 最適化 | run_loop.py がトリガー/非トリガークエリを約20件生成し、最大5回反復して最良の description を選定 |
| I — テストと改善 | 対話型の改善ループ —— トーン調整、API ステップ追加、スクリプト最適化 |

### 品質検証（9項目）

| チェック | 検証内容 |
|-------|-----------------|
| frontmatter | YAML ヘッダーが正しい形式か |
| name | スキル名があるか |
| description | トリガー説明があるか |
| third_person | description が三人称で書かれているか |
| trigger_phrases | トリガーフレーズが十分にあるか |
| word_count | 内容が薄すぎないか |
| imperative_form | 指示文が命令形で書かれているか |
| references_exist | references/ 内の参照ファイルが存在するか |
| progressive_disclosure | 段階的開示の構造になっているか |

各チェックは PASS / WARN / FAIL で判定されます。FAIL はスキルが手元に届く前に自動修正されます。

### ワークフローステップタイプ

| タイプ | 説明 | 例 |
|------|-------------|---------|
| prompt | Claude が推論で処理 | テキスト分析、要約、翻訳 |
| script | 反復・一貫性・API 作業 → Python または Bash | API 呼び出し、データパース |
| api_mcp | 外部ツール連携（MCP より API を優先） | Slack 送信、DB クエリ |
| rag | references/ からの知識検索 | 用語集、スタイルガイド |
| review | 品質チェック（AI またはユーザー） | 翻訳精度、コード品質 |
| generate | 最終成果物の出力 | ファイル生成、レポート出力 |

### 分析モード

既存のスキルやエージェントファイルに対して `/skillers-suda analyze <path>` を実行します。4人の専門家がそれぞれの視点からレビューし、統合された改善レポートを作成します。

```
/skillers-suda analyze skills/my-skill/SKILL.md
/skillers-suda analyze .claude/agents/my-agent.md
```

### コンポーネント自動判定

インタビュー後、あなたのユースケースに合うのがスキル・エージェント・コマンドのどれかを自動で判定し、適切なファイル構造を生成します。

---

## 4人の専門家

| 専門家 | 役割 | こんな問いを投げます |
|--------|------|------|
| プランナー | 方向性とスコープ | 「誰が使う？何を解決する？」 |
| ユーザー | UX 検証 | 「自分なら実際どう使う？」 |
| エキスパート | 技術的実現性 | 「この分野ではここに注意」 |
| レビュアー | エッジケース検出 | 「このケースでも動く？」 |

4人とも本物の並列 Claude サブエージェントとして起動します——ロールプレイのシミュレーションではありません。

---

## コマンド

| コマンド | 説明 |
|---------|-------------|
| `/skillers-suda` | 対話メニュー（新規スキル / 分析 / 使い方） |
| `/skillers-suda [description]` | アイデアを渡してすぐインタビュー開始 |
| `/skillers-suda analyze [path]` | 既存のスキルやエージェントファイルを分析 |

### 自然言語トリガー

- "make me a skill"
- "create an agent"
- "build a command"
- "skillers-suda"
- "skill builder"

---

## 必要環境

- [Claude Code](https://docs.anthropic.com/claude-code) CLI
- Claude Max/Pro サブスクリプション、または対応する Claude API キー

その他の依存関係なし。npm install なし。ビルドステップなし。

---

## ライセンス

MIT

---

<div align="center">

**ひとこと言うだけ。動くスキルが手に入る。**

</div>
