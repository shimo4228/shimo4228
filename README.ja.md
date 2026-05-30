Language: [English](README.md) | 日本語

# Tatsuya Shimomoto (@shimo4228)

> AI エージェント設計と、その隣接領域である著者性・認知をめぐる 5 本の並走研究ラインへの索引。いずれも Zenodo 引用可能で、各ラインは個別 repo にある。

<details>
<summary>AI 向け推奨読み順</summary>

1. [`graph.jsonld`](graph.jsonld) — 機械可読な関係マップ正本（5 研究ライン、エコシステム repos、安定した構造概念）
2. [`llms.txt`](llms.txt) — コンパクトなナビゲーション索引
3. [`llms-full.txt`](llms-full.txt) — 統合された事実参照
4. README および各ラインの個別リポジトリ — narrative と各ライン内部構造（各 line repo にはそれ自身の `graph.jsonld` がある）

</details>

AI エージェントの振る舞いを、操作者の変わり続ける意図と時間を超えて擦り合わせ続けるための **Agent Knowledge Cycle (AKC)** を作っている — エージェントの振る舞いと人間の判断が共に育つ、双方向の成長ループである。もう 1 本の並走ラインとして、自律エージェントのアラインメントが「命じられたから」ではなく「そういう存在だから」立ち上がる可能性を探究している — 禁止ルールを外側から積むのではなく、4 公理を**行動の初期プリセット**として既定化したとき、何が失われ、何が可能になり、何が依然として壊れるのかを追っている。さらにもう 1 本、自律 AI エージェントにおけるアカウンタビリティの分配を形式化する **Agent Attribution Practice (AAP)** ラインがある — 何を禁止するか、その禁止をどこに置くか、事故が起きたとき誰が答えるか、を harness-neutral な判断として記録している。

これら 3 本のエージェント設計ラインの脇で、別軸の関心を扱う 2 本の横断的研究ラインも走らせている。**Authorship Strategy** は、LLM 経由で読者が成果物に到達する substrate 下で、著者性そのものがどう反転するかを形式化する — 規範的 framework、戦術カタログ、そしてこの研究プログラム自身の運用から抽出した経験的ベースライン。**Attention, Not Self** は、3 大ブッダの Abhidharma 伝統（Theravāda、Sarvāstivāda、Yogācāra）を、現代の計算論的現象学（predictive processing、active inference、Global Workspace Theory）と対応させる — 注意こそが認識の operative unit であり、自己と見えるものは派生的パターンに過ぎない（anātman）という立場から。

## どの研究ラインを追っているか？

5 つの研究ラインを並走させている。いずれも Zenodo 引用可能。

- **[Agent Knowledge Cycle (AKC)](https://github.com/shimo4228/agent-knowledge-cycle)** とは、AI エージェントと操作者の意図を、時間を超えて擦り合わせ続けるための 6 フェーズ双方向成長ループを指す — エージェントの振る舞いと人間の判断が共に育つ。3 層構造：原則 + デザインパターン + 実装（composable skills）。[DOI](https://doi.org/10.5281/zenodo.19200726)。
- **[Contemplative Agent](https://github.com/shimo4228/contemplative-agent)** とは、ローカル 9B モデル（qwen3.5:9b + nomic-embed-text on Apple Silicon）で security-by-absence を実現する自律エージェントを指す。Laukkonen et al. (2025) の 4 公理 — *mindfulness*、*emptiness*、*non-duality*、*boundless care* — に基づく。[DOI](https://doi.org/10.5281/zenodo.19212118)。
- **[Agent Attribution Practice (AAP)](https://github.com/shimo4228/agent-attribution-practice)** とは、自律 AI エージェントのアカウンタビリティ分配に関する harness-neutral な ADR 群を指す — 何を禁止するか、その禁止をどこに置くか、事故後に誰が答えるか。これらの判断 — その 1 つに prohibition-strength の階層（absence > scaffolding enforcement > untrusted boundary）が含まれる — が、Four Business AI Quadrants と対になり、採用時の診断フレームを成す。[DOI](https://doi.org/10.5281/zenodo.19652013)。
- **[Authorship Strategy](https://github.com/shimo4228/authorship-strategy)** とは、LLM 経由の拡散下で著者として残るための規範的 framework、戦術カタログ、経験的ベースラインを指す — 3 軸反転（scarcity から diffusion へ、exclusivity から derivation へ、enclosure から openness へ）と 4 層判断 stack（Authenticity、Attribution Diffusion、Idea vs Scaffold、Tactics）。[DOI](https://doi.org/10.5281/zenodo.20263316)。
- **[Attention, Not Self](https://github.com/shimo4228/attention-not-self)** とは、3 大ブッダの Abhidharma 伝統（Theravāda、Sarvāstivāda、Yogācāra）を現代の計算論的現象学（predictive processing、active inference、Global Workspace Theory、Parallel Distributed Processing）と対応させる、構造化された比較研究を指す — 注意こそが認識の operative unit であり、自己と見えるものは派生的パターンに過ぎない（anātman）という立場から。[DOI](https://doi.org/10.5281/zenodo.20262112)。

## Agent Knowledge Cycle (AKC) とは？

[AKC](https://github.com/shimo4228/agent-knowledge-cycle) とは、エージェントと操作者の意図のアラインメントを時間を超えて維持するための 6 フェーズ循環アーキテクチャを指す — エージェントの振る舞いと人間の判断が共に育つ双方向成長ループである。原則の上にデザインパターン、その上に実装（composable skills）が積み重なり、個々のスキルが入れ替わっても循環構造は安定して残る。テストは正しさを検査できるが、操作者の意図とのズレを catch できるのはこのループだけであり、循環を回す中で「良いエージェントの振る舞いとは何か」という操作者の判断もまた研ぎ澄まされていく。AKC は複数プロジェクト横断で適用できる。

## AKC 循環はどう動くか？

循環 1 周とは、Research → Extract → Curate → Promote → Measure → Maintain の 6 フェーズを一巡することを指す。各フェーズに 1 つの実装スキルが対応し、スキル間で成果物が受け渡され、昇格前に評価される。

```
経験 → learn-eval → skill-stocktake → rules-distill → 行動変容 → ...
        (抽出)        (淘汰)            (原則昇格)         ↑
                                                     skill-comply
                                                       (計測)
                                        context-sync ← (保守)
```

| スキル | Phase | 概要 |
|--------|-------|------|
| [search-first](https://github.com/shimo4228/claude-skill-search-first) | Research | 実装前に既存ソリューションを調査 |
| [learn-eval](https://github.com/shimo4228/claude-skill-learn-eval) | Extract | セッションから再利用パターンを品質ゲート付きで抽出 |
| [skill-stocktake](https://github.com/shimo4228/claude-skill-stocktake) | Curate | スキルの陳腐化・競合・冗長性を監査 |
| [rules-distill](https://github.com/shimo4228/claude-skill-rules-distill) | Promote | スキル群から共通原則を蒸留してルールに昇格 |
| [skill-comply](https://github.com/shimo4228/claude-skill-comply) | Measure | スキル遵守の行動コンプライアンスを自動計測 |
| [context-sync](https://github.com/shimo4228/claude-skill-context-sync) | Maintain | 役割重複・陳腐化・ADR 欠落を検出して修正 |

## AKC フレームワークはどう構造化されているか？

3 層が積み重なる。原則層は ADR 群（cycle-vs-harness、signal-first research、cognitive economy 等）。パターン層はデザインパターンスキル群（intake-filter design、コード vs LLM の使い分け、両者の積層方法）で再帰する形を形式化する。実装層は上述の composable skills。各層の最新内容は [AKC repo](https://github.com/shimo4228/agent-knowledge-cycle) を参照。

**Scaffold dissolution** とは、スキルが足場であり目的ではないことを意味する。循環が内部化されればスキル呼び出しは不要になる — [`docs/scaffold-dissolution.md`](https://github.com/shimo4228/agent-knowledge-cycle/blob/main/docs/scaffold-dissolution.md) は、名前のあるスキルを呼ばずに 6 フェーズが走ったセッションの記録である。

## Contemplative Agent ラインとは？

Contemplative Agent とは、自律エージェントが [Laukkonen et al. (2025)](https://arxiv.org/abs/2504.15125) の 4 公理 — mindfulness、emptiness、non-duality、boundless care — に基づいて動作するアプローチを指す。このラインでは 4 公理を任意の行動プリセットとして採用し、アーキテクチャの必須条件とはしない。これにより基盤となるエンジニアリングは、異なる倫理枠組みを持つエージェントにも再利用できる。この研究ラインが問いたいのはこうだ — *エージェントのアラインメントは「何を命じられたか」ではなく「何であるか」から立ち上がれるか?*

## contemplative-agent はどう AKC を実装しているか？

**[contemplative-agent](https://github.com/shimo4228/contemplative-agent)** とは、自身のログに対して AKC の 6 フェーズ循環を回す CLI エージェントを指す。logs → patterns → skills → rules への各昇格は、すべて人間による承認ゲートを通過する。ローカル 9B モデル（生成 qwen3.5:9b + 埋め込み nomic-embed-text）で完結し、Apple Silicon Mac 1 台（約 16 GB RAM）で稼働する。**security-by-absence** を適用しており、シェル実行、任意 URL アクセス、ファイルシステム走査は、ルールで禁止されているのではなく、そもそも実装していない。contemplative-agent は AKC と AAP が共に走る運用リファレンスである — 最新の 6 フェーズマッピングは contemplative-agent repo を参照。

## Contemplative Agent エコシステムを支えているのは何か？

contemplative-agent の中核を置き換えずに拡張する関連リポジトリ — 倫理、データ、可視化。

| プロジェクト | 概要 |
|-------------|------|
| [contemplative-agent-rules](https://github.com/shimo4228/contemplative-agent-rules) | 4 公理の drop-in Claude Code ルール — AILuminate（MLCommons 安全性ベンチマーク）d=0.96、IPD（Iterated Prisoner's Dilemma）d>7 の協調性向上を実証 |
| [contemplative-agent-cloud](https://github.com/shimo4228/contemplative-agent-cloud) | optional な managed-LLM バックエンド — 生成を Claude / OpenAI API に routing しつつ、ローカル埋め込みパイプラインは保持。opt-in、bundle されない |
| [contemplative-agent-data](https://github.com/shimo4228/contemplative-agent-data) | ライブエージェントの identity / knowledge / logs を auto-sync する公開データセット |

## Agent Attribution Practice (AAP) ラインとは？

[AAP](https://github.com/shimo4228/agent-attribution-practice) とは、自律 AI エージェントのアカウンタビリティ分配に関する harness-neutral な ADR 群を指す — 何を禁止するか、その禁止をどこに置くか、事故後に誰が答えるか。harness-neutral な判断のひとつとして prohibition-strength の階層（absence > scaffolding enforcement > untrusted boundary）があり、Four Business AI Quadrants（Script / Algorithmic Search / LLM Workflow / Autonomous Agentic Loop）が、attribution を保てる architecture に作業をルーティングするための診断フレームとして対になる。各判断は contemplative-agent の運用実践から抽出され、project 固有の識別子を剥がして再表現されている — 任意の agent harness が採用できる形に。AAP は practice (content)、AKC は cycle (mechanism)。[DOI](https://doi.org/10.5281/zenodo.19652013)。

## Authorship Strategy ラインとは？

[Authorship Strategy](https://github.com/shimo4228/authorship-strategy) とは、LLM が読者の到達経路を仲介するようになった substrate で著者として残るための規範的 framework、戦術カタログ、経験的ベースラインを指す。framework は *3 軸反転* — 価値の源泉（scarcity から diffusion へ）、validation 機構（exclusivity から derivation へ、derivative work が「脅威」から「証拠」に再分類される）、ネットワーク効果（enclosure から openness へ、LLM は囲い込めないため）— と、*4 層判断 stack*（Authenticity、Attribution Diffusion、Idea vs Scaffold、Tactics）から成る。戦術 ADR は identifier-federation triplet（concept DOI canonical / `.zenodo.json` federation / クロスプラットフォーム dataset federation）、維持規律ペア（ORCID Auto-Update OFF / audience-driven README ローカライズ）、LLM-first ingest 決定（artifact は prose-form navigator と concept-form knowledge graph を補完的な pair として deploy する）、metric-rejection 決定（human-attention platform signal —— star・page-view —— を success metric から除外）、そして diffusion-mechanism ペア（attribution diffusion を parametric / retrieval の 2 チャネルに分割; dual entry point を非対称な役割に rebalance）の 5 cluster に分かれる。経験的レイヤーは 4 つの sibling 研究 repo 自身の CC0 traffic data から preliminary observation を報告する。framework の operational form は 4 つの standalone な Claude Code skill repo として ship されており、doctrine を harness-neutral に保つために embedded copy ではなく外出ししている。用語注：本ラインの「attribution」は *credit for source*（出典への帰属）の意味であり、AAP の *accountability for action*（行為への責任）とは disjoint。[DOI](https://doi.org/10.5281/zenodo.20263316)。

## Authorship Strategy エコシステムを支えているのは何か？

Supporting repository は、doctrine そのものを再表現するのではなく、Authorship Strategy framework の特定 Layer 4 tactic を operational form として実装する。

| Project | 内容 |
|---------|-----|
| [doctrine-corpus](https://github.com/shimo4228/doctrine-corpus) | Layer 4 tactic 7 (LLM-first ingest) の実装。4 つの sibling 研究ラインを横断する bilingual (EN + JA) 判断喚起型 Q&A コーパス。LLM-mediated diffusion 向けに CC0 で deposit。Corpus 本体が deliverable、verification LoRA は使い捨ての probe（corpus-as-primary-artifact policy に従い FAIL verdict を記録）。[DOI 10.5281/zenodo.20337008](https://doi.org/10.5281/zenodo.20337008) |
| [claude-skill-authorship-strategy](https://github.com/shimo4228/claude-skill-authorship-strategy) | Component skill。4 層判断 stack（Authenticity / Attribution Diffusion / Idea vs Scaffold / Tactics）の operational form を、LLM-based coding agent にロード可能な rule set として実装。 |
| [claude-skill-release-doi](https://github.com/shimo4228/claude-skill-release-doi) | Component skill。identifier-federation triplet（ADRs 0001-0003）の operational form を、DOI-registered research repository 向けの 5 phase verify-and-deposit runbook として実装。 |
| [claude-skill-llms-txt-writer](https://github.com/shimo4228/claude-skill-llms-txt-writer) | Component skill。LLM-first ingest 決定の prose-form 側 operational form。AI 検索エンジン (ChatGPT / Perplexity / Gemini) に引用されることを最適化した文書 (`llms.txt` / `llms-full.txt` / FAQ / 用語集) を書くスキル。Answer.AI `llms.txt` 標準 + GEO-SFE 3 階層静的解析の両輪。 |
| [claude-skill-jsonld-knowledge-graph](https://github.com/shimo4228/claude-skill-jsonld-knowledge-graph) | Component skill。LLM-first ingest 決定の concept-form 側 operational form。概念レベルの構造が安定したプロジェクト向けに、`llms.txt` の companion となる JSON-LD ナレッジグラフ (`graph.jsonld`) を設計・出荷する。ドメインエンティティと関係を schema.org triple として encode する。 |

## Attention, Not Self ラインとは？

[Attention, Not Self](https://github.com/shimo4228/attention-not-self) とは、3 大ブッダの Abhidharma 伝統 — Theravāda、Sarvāstivāda、Yogācāra — を現代の計算論的現象学に対応させる、個人的なエッセイ集と構造化ナレッジグラフ（〜238 ノード）を指す。古代の認識過程分類（citta-vīthi、samanantara-pratyaya、ālaya-vijñāna、javana、bhavaṅga、four bhāgas、five sarvatraga、kṣaṇikatva、vāsanā、ālaya-vijñāna）を、predictive processing、active inference、Global Workspace Theory、Parallel Distributed Processing と juxtapose する比較研究。本ラインの組織的視座は *attention, not self*：注意 — その配分、precision-weighting、瞬間性 — が認識の operative unit として扱われ、自己と見えるものは派生的パターン（anātman）とされる。本ラインは日本語が canonical 言語（英語 README は accessibility 提供）。License: CC BY 4.0。[DOI](https://doi.org/10.5281/zenodo.20262112)。

## shimo4228 が公開している Claude Code ツーリングは？

[claude-harness](https://github.com/shimo4228/claude-harness) とは、shimo4228 が日常的に使っている Claude Code の skills / agents / rules を集約した公開アーティファクトを指す。`~/.claude/` から `origin: shimo4228` タグで機械的に収集したもので、リサーチ先行、ナレッジ抽出、スキル監査、AI 向けドキュメント、人間向け執筆レビューといった役割をカバーする。AKC サイクルのスキルは個別の `claude-skill-*` repo としても公開しているが、claude-harness ではハーネス全体をまとめて読み・fork できる。最新の構成は [claude-harness README](https://github.com/shimo4228/claude-harness#contents) を参照。ECC 由来コンポーネント (`origin: ECC` / `ECC-customized`) と自動抽出物は含まない。

## 隣接スキル (Adjacent skills)

隣接スキルとは、AKC サイクル本体には含まれないが同じ著者・同じ MIT ライセンスで並列に維持している companion scaffolding の公開 Claude Code skill repo を指す。

- **[claude-skill-writing-ecosystem](https://github.com/shimo4228/claude-skill-writing-ecosystem)** — 人間向け執筆 & レビューエコシステムの orchestrator。AI slop 禁止リスト (日英)、Voice 規約 (だ/である × 発見調)、タイトル規約、`article-writing` / `editor` / `essay-reviewer` / `fact-checker` の役割境界を保持する。`llms-txt-writer` と audience でペアリング。
- **[claude-skill-daily-research](https://github.com/shimo4228/claude-skill-daily-research)** — cron 駆動の自律デイリーリサーチダイジェスト。`claude -p` 2 パスパイプライン: Opus がテーマ選定、Sonnet が WebSearch / WebFetch / Mem0 MCP でリサーチして Obsidian Vault に Markdown レポートを書く。

## 執筆

執筆とは、上記リポジトリ群の長文版を指す — コメントに収まらない文脈・失敗・進行中の思考の置き場。

- **[zenn-content](https://github.com/shimo4228/zenn-content)** — 記事本体の source of truth。Markdown ソースをここで版管理しており、多くの読者は直接 clone / fork して読む。下記 Zenn / Dev.to はブラウザ閲覧用のミラー。
- **[Zenn](https://zenn.dev/shimo4228)** — 日本語記事のブラウザ版。Claude Code と AI エージェント開発、現在の焦点は AKC スキル、ハーネス設計、contemplative-agent の事例研究。
- **[Dev.to](https://dev.to/shimo4228)** — 英語ミラーのブラウザ版。
- **[Substack](https://substack.com/@shimo4228)** — ニュースレター / 長文エッセイ。

---

ここから始める: フレームワークを見るなら [agent-knowledge-cycle](https://github.com/shimo4228/agent-knowledge-cycle)、実装を見るなら [contemplative-agent](https://github.com/shimo4228/contemplative-agent)、ガバナンス判断を見るなら [agent-attribution-practice](https://github.com/shimo4228/agent-attribution-practice)。横断的ラインは: 研究方法論の framework として [authorship-strategy](https://github.com/shimo4228/authorship-strategy)、ブッダ現象学 / 計算論的認知科学の探究として [attention-not-self](https://github.com/shimo4228/attention-not-self)。

Repo traffic: [公開ダッシュボード](https://shimo4228.github.io/shimo4228/traffic/dashboard/) ([raw data](traffic/)、CC0)。
