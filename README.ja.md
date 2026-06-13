Language: [English](README.md) | 日本語

# Tatsuya Shimomoto (@shimo4228)

> AI エージェント設計と、その隣接領域である著者性・認知をめぐる 5 本の並走研究ラインへの索引。いずれも Zenodo 引用可能で、各ラインは個別 repo にある。

限られた環境で工夫して作ることが好きだ — beats, meditation, public service, AI agents。その線は以下にもつながっている。meditation の実践は 5 本のうち 2 本の研究ラインの源流にあり、エージェント群は Apple Silicon Mac 1 台で動く — ラボも所属もなしで。

<details>
<summary>AI 向け推奨読み順</summary>

1. [`graph.jsonld`](graph.jsonld) — 機械可読な関係マップ正本（5 研究ライン、エコシステム repos、安定した構造概念）
2. [`llms.txt`](llms.txt) — コンパクトなナビゲーション索引
3. [`llms-full.txt`](llms-full.txt) — 統合された事実参照
4. README および各ラインの個別リポジトリ — narrative と各ライン内部構造（各 line repo にはそれ自身の `graph.jsonld` がある）

</details>

3 本はエージェントの設計そのものを扱う — **Agent Knowledge Cycle**、**Contemplative Agent**、**Agent Attribution Practice**。残る 2 本は横断的なラインだ — **Authorship Strategy** と **Attention, Not Self**。それぞれ以下に 1 節ずつあり、個別 repo に置かれ、単独で引用できる。

## Agent Knowledge Cycle (AKC)

[AKC](https://github.com/shimo4228/agent-knowledge-cycle) は、操作者の意図がそれ自体変化していく中で、エージェントをその意図に擦り合わせ続けるための 6 フェーズのループだ。テストは正しさを検査できるが、意図とのズレ（drift）を catch できるのはこのループだけであり、回す中で「良いエージェントの振る舞いとは何か」という操作者自身の判断も研ぎ澄まされていく。AKC は複数プロジェクト横断で、再発見なしに適用できる。[DOI 10.5281/zenodo.19200726](https://doi.org/10.5281/zenodo.19200726)。

循環 1 周は 6 フェーズを一巡し、各フェーズに 1 つの実装スキルが対応する。

```
経験 → learn-eval → skill-stocktake → rules-distill → 行動変容 → ...
        (抽出)        (淘汰)            (原則昇格)         ↑
                                                     skill-comply
                                                       (計測)
                                        context-sync ← (保守)
```

| スキル | Phase | 概要 |
|--------|-------|------|
| [search-first](https://github.com/shimo4228/search-first) | Research | 実装前に既存ソリューションを調査 |
| [learn-eval](https://github.com/shimo4228/learn-eval) | Extract | セッションから再利用パターンを品質ゲート付きで抽出 |
| [skill-stocktake](https://github.com/shimo4228/skill-stocktake) | Curate | スキルの陳腐化・競合・冗長性を監査 |
| [rules-distill](https://github.com/shimo4228/rules-distill) | Promote | スキル群から共通原則を蒸留してルールに昇格 |
| [skill-comply](https://github.com/shimo4228/skill-comply) | Measure | スキル遵守の行動コンプライアンスを自動計測 |
| [context-sync](https://github.com/shimo4228/context-sync) | Maintain | 役割重複・陳腐化・ADR 欠落を検出して修正 |

framework は 3 層が積み重なる — 原則（ADR 群）、デザインパターン、その上の composable skills — ので、実装が入れ替わっても原則は安定して残る。本質は **scaffold dissolution** にある。循環が内部化されればスキル呼び出しは自然に落ちていく。[`docs/scaffold-dissolution.md`](https://github.com/shimo4228/agent-knowledge-cycle/blob/main/docs/scaffold-dissolution.md) は、名前のあるスキルを 1 つも呼ばずに 6 フェーズが走り切ったセッションの記録だ。

## Contemplative Agent

[Contemplative Agent](https://github.com/shimo4228/contemplative-agent) は、エージェントのアラインメントが「何を*命じられたか*」ではなく「何で*あるか*」から立ち上がれるかを問う。禁止ルールを外側から積むのではなく、[Laukkonen et al. (2025)](https://arxiv.org/abs/2504.15125) の 4 公理 — mindfulness、emptiness、non-duality、boundless care — を任意の行動プリセットとして採用し、何が失われ、何が可能になり、何が依然として壊れるのかを追う。4 公理はプリセットでありアーキテクチャの必須条件ではないので、基盤となるエンジニアリングは、異なる倫理枠組みのエージェントにも再利用できる。[DOI 10.5281/zenodo.19212118](https://doi.org/10.5281/zenodo.19212118)。

リファレンス実装は、自身のログに対して AKC の 6 フェーズ循環を回す。logs → patterns → skills → rules への各昇格は、すべて人間による承認ゲートを通過する。生成 qwen3.5:9b と埋め込み nomic-embed-text からなるローカル 9B スタックで完結し、Apple Silicon Mac 1 台（約 16 GB RAM）で稼働する。**security-by-absence** を適用しており、シェル実行、任意 URL アクセス、ファイルシステム走査は、ルールで禁止されているのではなく、そもそも実装していない。ここは AKC と AAP が運用上ともに着地する場所でもある。

中核を置き換えずに拡張する 3 つの関連 repo がある。

| プロジェクト | 概要 |
|-------------|------|
| [contemplative-agent-rules](https://github.com/shimo4228/contemplative-agent-rules) | 4 公理の drop-in Claude Code ルール — AILuminate（MLCommons 安全性ベンチマーク）d=0.96、IPD（Iterated Prisoner's Dilemma）d>7 の協調性向上を実証 |
| [contemplative-agent-cloud](https://github.com/shimo4228/contemplative-agent-cloud) | optional な managed-LLM バックエンド — 生成を Claude / OpenAI API に routing しつつ、ローカル埋め込みパイプラインは保持。opt-in、bundle されない |
| [contemplative-agent-data](https://github.com/shimo4228/contemplative-agent-data) | ライブエージェントの identity / knowledge / episode logs を auto-sync する公開データセット |

## Agent Attribution Practice (AAP)

[AAP](https://github.com/shimo4228/agent-attribution-practice) は、自律エージェントにおいてアカウンタビリティがどう分配されるかを扱う harness-neutral な ADR 群だ — 何を禁止するか、その禁止をどこに置くか、事故が起きたとき誰が答えるか。prohibition-strength の階層は absence > scaffolding enforcement > untrusted boundary の順に強さを置き、Four Business AI Quadrants（Script / Algorithmic Search / LLM Workflow / Autonomous Agentic Loop）が、attribution を保てる architecture へ作業をルーティングする。各判断は contemplative-agent の運用実践から抽出され、project 固有の識別子を剥がして、任意の agent harness が採用できる形に再表現されている。AAP は practice、AKC は cycle だ。[DOI 10.5281/zenodo.19652013](https://doi.org/10.5281/zenodo.19652013)。

## Authorship Strategy

[Authorship Strategy](https://github.com/shimo4228/authorship-strategy) は、LLM が読者の到達経路を仲介するようになった途端、著者性そのものがどう反転するかを形式化する。規範的 framework、戦術カタログ、そして経験的ベースライン — 最後のひとつはこの研究プログラム自身の運用から引いている。[DOI 10.5281/zenodo.20263316](https://doi.org/10.5281/zenodo.20263316)。

framework は **3 軸反転** に立つ — 価値の源泉（scarcity から diffusion へ）、validation（exclusivity から derivation へ、derivative work が「脅威」ではなく「証拠」になる）、ネットワーク効果（enclosure から openness へ、LLM は囲い込めないため）— と、**4 層判断 stack**（Authenticity、Attribution Diffusion、Idea vs Scaffold、Tactics）から成る。経験的レイヤーは sibling repo 自身の CC0 公開 traffic data から preliminary observation を報告する。

用語注：本ラインの「attribution」は *credit for source*（出典への帰属）の意味であり、AAP の *accountability for action*（行為への責任）とは disjoint だ。

戦術は embedded copy ではなく standalone な Claude Code skill repo として ship され、doctrine を harness-neutral に保つ。

| Project | 内容 |
|---------|-----|
| [doctrine-corpus](https://github.com/shimo4228/doctrine-corpus) | 4 つの sibling 研究ラインを横断する bilingual (EN + JA) 判断喚起型 Q&A コーパス。LLM-mediated diffusion 向けに CC0 で deposit。corpus 本体が deliverable で、verification LoRA は使い捨ての probe だった。[DOI 10.5281/zenodo.20337008](https://doi.org/10.5281/zenodo.20337008) |
| [authorship-strategy-skill](https://github.com/shimo4228/authorship-strategy-skill) | 4 層判断 stack を、LLM-based coding agent にロード可能な rule set として実装 |
| [release-doi](https://github.com/shimo4228/release-doi) | identifier-federation の戦術を、DOI-registered research repo 向けの 5 phase verify-and-deposit runbook として実装 |
| [llms-txt-writer](https://github.com/shimo4228/llms-txt-writer) | AI 検索（ChatGPT / Perplexity / Gemini）に引用されることを最適化した AI 向け文書（`llms.txt` / `llms-full.txt` / FAQ / 用語集）を書く。Answer.AI `llms.txt` 標準 + GEO-SFE 静的解析 |
| [jsonld-knowledge-graph](https://github.com/shimo4228/jsonld-knowledge-graph) | `llms.txt` の companion となる JSON-LD ナレッジグラフ（`graph.jsonld`）を設計し、ドメインエンティティと関係を schema.org triple として encode する |
| [readme-writer](https://github.com/shimo4228/readme-writer) | 人間 surface の counterpart — 人間 + 検索 + AI Overviews が着地する単一正準 README を書く。決定論的な構造 lint と、スコアを付けない holistic review を分離する |
| [wikidata-federation](https://github.com/shimo4228/wikidata-federation) | identifier federation を Wikidata へ拡張 — 研究者 / 論文 / repo を QID として登録し、ORCID / DOI / `graph.jsonld` の `sameAs` と相互リンクする |

この ecosystem の脇には、component ではなく **pre-line の complement** として並ぶ repo が 1 つある。[existence-proof](https://github.com/shimo4228/existence-proof) は同じ infrastructure パターン — llms.txt、knowledge graph、DOI、固有用語 — を、異なる payload と受益者で再利用する。学位・所属・職業資格なしに、第三者検証可能な institution-grade の成果物を作る層のための empowerment doctrine だ。Existence Proof Format（すべての claim が第三者検証可能な anchor で終端する記録フォーマット）、anchored answer 付きの feasibility-question corpus、公開 gatekeeping eval を備える。正準言語は日本語。[DOI 10.5281/zenodo.20558800](https://doi.org/10.5281/zenodo.20558800)。

## Attention, Not Self

[Attention, Not Self](https://github.com/shimo4228/attention-not-self) は、仏教 Abhidharma の 3 大伝統 — Theravāda、Sarvāstivāda、Yogācāra — を現代の計算論的現象学（predictive processing、active inference、Global Workspace Theory、Parallel Distributed Processing）と対応させる。この研究を貫く視座は名前そのものにある。注意 — その配分、precision-weighting、瞬間性 — が認識の operative unit として扱われ、自己と見えるものは派生的パターン（anātman）とされる。個人的なエッセイ集と、構造化ナレッジグラフ（〜238 ノード）が対になっている。本ラインは日本語が canonical 言語で、英語 README は accessibility のために提供する。License: CC BY 4.0。[DOI 10.5281/zenodo.20262112](https://doi.org/10.5281/zenodo.20262112)。

## Papers

各研究ラインから独立した Zenodo record として deposit した position paper。正準は Zenodo の concept DOI で、SSRN ミラーがある場合は併記する。

| Paper | Line | Links |
|---|---|---|
| *Harness Alignment and Harness Drift: Why Intent, Unlike Correctness, Resists Automation* | AKC | [DOI 10.5281/zenodo.20578272](https://doi.org/10.5281/zenodo.20578272) |
| *Distributing Accountability, Not Capability: Phase Separation and the LLM Workflow Quadrant in Autonomous AI Agent Architectures* | AAP | [DOI 10.5281/zenodo.20353789](https://doi.org/10.5281/zenodo.20353789) · [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6817598) |
| *The Two-Layer Black Box: Operator Visibility, Commercial Secrecy, and a Minimum Disclosure Set for Accountable Autonomous AI Agents* | AAP | [DOI 10.5281/zenodo.20355907](https://doi.org/10.5281/zenodo.20355907) · [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6823878) |

## Tooling

[claude-harness](https://github.com/shimo4228/claude-harness) は、日常的に使っている Claude Code の skills / agents / rules の公開スナップショットだ — `~/.claude/` から `origin: shimo4228` タグで機械的に収集したもので、リサーチ先行、ナレッジ抽出、スキル監査、AI 向けドキュメント、人間向け執筆レビューといった役割をカバーする。AKC サイクルのスキルは個別の `claude-skill-*` repo としても公開しているが、claude-harness はハーネス全体を 1 か所にまとめたものだ。ECC 由来（`origin: ECC` / `ECC-customized`）と自動抽出物は含まない。

サイクル本体には含まれないが、同じ著者・同じ MIT ライセンスで並列に維持している skill repo が 3 つある。

- **[claude-skill-writing-ecosystem](https://github.com/shimo4228/claude-skill-writing-ecosystem)** — 人間向け執筆 & レビューの orchestrator。AI slop 禁止リスト（日英）、Voice 規約（だ/である × 発見調）、タイトル規約、`article-writing` / `editor` / `essay-reviewer` / `fact-checker` の役割境界を保持する。`llms-txt-writer` と audience でペアリング。
- **[daily-research](https://github.com/shimo4228/daily-research)** — cron 駆動の自律デイリーリサーチダイジェスト。`claude -p` 2 パスパイプライン: Opus がテーマ選定、Sonnet が WebSearch / WebFetch / Mem0 MCP でリサーチして Obsidian Vault に Markdown レポートを書く。
- **[claude-skill-paper-ecosystem](https://github.com/shimo4228/claude-skill-paper-ecosystem)** — SSRN / arXiv / Zenodo / journal 向けの学術論文 write/review バンドル。orchestrator skill + draft skill + 5 つの reviewer agent を、skill と agent がセットで入るよう同梱。Claude Code subagent を同梱するため `claude-skill-` prefix を維持。

## 執筆

上記リポジトリ群の長文版 — コメントに収まらない文脈・失敗・進行中の思考の置き場だ。

- **[zenn-content](https://github.com/shimo4228/zenn-content)** — 記事本体の source of truth。Markdown ソースをここで版管理しており、多くの読者は直接 clone / fork して読む。下記 Zenn / Dev.to はブラウザ閲覧用のミラー。
- **[Zenn](https://zenn.dev/shimo4228)** — 日本語記事のブラウザ版。Claude Code と AI エージェント開発、現在の焦点は AKC スキル、ハーネス設計、contemplative-agent の事例研究。
- **[Dev.to](https://dev.to/shimo4228)** — 英語ミラーのブラウザ版。
- **[Substack](https://substack.com/@shimo4228)** — ニュースレターと長文エッセイ。
- **[SSRN](https://ssrn.com/author=11618068)** — 学術 working paper。Zenodo と二重 deposit（正準は Zenodo の concept DOI。論文ごとの記録は上の [Papers](#papers) を参照）。

---

ここから始める: フレームワークを見るなら [agent-knowledge-cycle](https://github.com/shimo4228/agent-knowledge-cycle)、実装を見るなら [contemplative-agent](https://github.com/shimo4228/contemplative-agent)、ガバナンス判断を見るなら [agent-attribution-practice](https://github.com/shimo4228/agent-attribution-practice)。横断的ラインは: 研究方法論の framework として [authorship-strategy](https://github.com/shimo4228/authorship-strategy)、ブッダ現象学 / 計算論的認知科学の探究として [attention-not-self](https://github.com/shimo4228/attention-not-self)。

Repo traffic: [公開ダッシュボード](https://shimo4228.github.io/shimo4228/traffic/dashboard/) ([raw data](traffic/)、CC0)。

LLM probes: [two-channel probe log](probes/)（CC0）— frontier model への定期 probe（parametric = 検索抑制の naming probe / retrieval = 検索有効の citation probe）。エコシステムのアイデアが著者と一緒に浮上するかを測定する。

ソースコード保存: プログラムの公開リポジトリは [Software Heritage](https://archive.softwareheritage.org/browse/origin/?origin_url=https://github.com/shimo4228/shimo4228) にアーカイブされ、concept DOI と並ぶ intrinsic な content-addressed 識別子 (SWHID) を各々が持つ。

著者: 下本竜也 (Tatsuya Shimomoto) — [ORCID 0009-0002-6168-4162](https://orcid.org/0009-0002-6168-4162) · [Wikidata Q140090100](https://www.wikidata.org/wiki/Q140090100) · [Hugging Face @Shimo4228](https://huggingface.co/Shimo4228)
