Language: [English](README.md) | 日本語

# Tatsuya Shimomoto (@shimo4228)

[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/shimo4228/shimo4228) [![GitMCP](https://img.shields.io/endpoint?url=https://gitmcp.io/badge/shimo4228/shimo4228)](https://gitmcp.io/shimo4228/shimo4228)

> 下本竜也による 5 本の独立引用可能な研究ラインの hub repository。主題は AI エージェント設計、AI 仲介時代の著者性、計算論的現象学。全体を貫くのは **value-layer harness engineering（価値層ハーネス工学）** — ハーネス工学を tool・permission・eval で止めず、規範・憲法・価値の層まで広げ、一つの human-gated サイクルで統治する。

この repo は地図であり、各プロジェクトの現在状態の source of truth ではない。各研究ラインはそれぞれの repository と Zenodo concept DOI を持つ。この hub は、安定した関係、引用ポインタ、機械可読なナビゲーション面を 1 か所にまとめる。

限られた環境で工夫して作ることが好きだ — beats, meditation, public service, AI agents。value-layer harness engineering はその線が合流する場所だ。meditation の実践が価値層の中身を供給して 5 本のうち 2 本の研究ラインの源流にあり、それを載せるエージェント群は Apple Silicon Mac 1 台で動く — ラボも所属もなしで。

## 早見表

| Line | 役割 | 安定した概念 | 正準 record |
|---|---|---|---|
| [Agent Knowledge Cycle](https://github.com/shimo4228/agent-knowledge-cycle) | エージェント設計の mechanism | エージェントと操作者の意図 alignment を、振る舞いと判断の変化に合わせて保つ 6 フェーズ loop。 | [DOI 10.5281/zenodo.19200726](https://doi.org/10.5281/zenodo.19200726) |
| [Contemplative Agent](https://github.com/shimo4228/contemplative-agent) | エージェントの disposition と実装 | 4 つの contemplative axioms を、アーキテクチャ依存ではなく任意の行動 preset として使う local agent。 | [DOI 10.5281/zenodo.19212118](https://doi.org/10.5281/zenodo.19212118) |
| [Agent Attribution Practice](https://github.com/shimo4228/agent-attribution-practice) | accountability practice | 何を禁止するか、制御をどこに置くか、agent が壊れたとき誰が答えるかを扱う harness-neutral な ADR 群。 | [DOI 10.5281/zenodo.19652013](https://doi.org/10.5281/zenodo.19652013) |
| [Authorship Strategy](https://github.com/shimo4228/authorship-strategy) | AI 時代の著者性 methodology | LLM が発見と引用を仲介する時代に、known author であるための framework。 | [DOI 10.5281/zenodo.20263316](https://doi.org/10.5281/zenodo.20263316) |
| [Attention, Not Self](https://github.com/shimo4228/attention-not-self) | 認知と仏教の inquiry | Abhidharma の cognitive-process model と computational phenomenology の比較。 | [DOI 10.5281/zenodo.20262112](https://doi.org/10.5281/zenodo.20262112) |

5 本のラインは sibling であり、依存関係ではない。AKC は mechanism、Contemplative Agent は disposition と running case、AAP は accountability practice、Authorship Strategy は diffusion methodology、Attention, Not Self は cognitive-philosophical inquiry だ。

3 本の agent-design line（AKC / Contemplative Agent / AAP）を縦に貫く主張が一つある: **[value-layer harness engineering（価値層ハーネス工学）](https://shimo4228.github.io/shimo4228/concepts/value-layer-harness-engineering.html)** だ。エージェントハーネス — Claude Code の rules や CLAUDE.md のような層 — に普通置かれるのは、コーディング規約・セキュリティ方針・執筆スタイルといったタスクの規則だ。このプログラムは同じ場所に価値規範を書く: contemplative axioms と authorship-strategy の判断スタックが、著者の日常ハーネスに常時ロードの rules として載っている（[claude-harness](https://github.com/shimo4228/claude-harness) がその公開 snapshot）。狙いは、目の前のタスクの最適化に留まらず、長期的な価値判断まで AI を伴走者として設計することにある。

その価値層も、下位層と同じ human-gated サイクルの統治下にある。AKC のサイクルは設計からして genre-neutral だ: セッションのパターンをコーディング規則へ蒸留するのと同じ機構（Extract = learn-eval、Promote = rules-distill）が価値規範を rules 層へ運び、Measure がそれが行動を変えたかを検査する。AAP の prohibition-strength hierarchy は、規範をどの層に置くべきかを決める。そして Contemplative Agent はこの層を **Identity と Constitution** として明示的に設計し — そこへのすべての昇格に人間の承認ゲートを置き — エージェント自身の SNS 活動（Moltbook adapter）の中でそれがどう変化するかを観察している。残る 2 本の cross-cutting line がこの図を完成させる: Attention, Not Self は価値層を満たすものを名指し、Authorship Strategy はプログラム全体が公開され、引用されるための方法論だ。

## 機械読解

機械読解なら [`graph.jsonld`](graph.jsonld)、次に [`llms.txt`](llms.txt)、最後に [`llms-full.txt`](llms-full.txt)。

## Agent Knowledge Cycle (AKC)

[AKC](https://github.com/shimo4228/agent-knowledge-cycle) は、操作者の意図が変化していく中で agent を意図に合わせ続ける 6 フェーズ loop だ。テストは incorrectness を検出できるが、AKC は変化する操作者と変化する agent のあいだの drift を扱う。

安定した loop は次の形を取る。

```text
Research -> Extract -> Curate -> Promote -> Measure -> Maintain -> Research
```

AKC は 3 層で構成される。principles、design patterns、composable implementation skills だ。目指す終点は **scaffold dissolution** であり、loop が内部化されると、明示的な skill call は落ちても判断パターンは残る。

## Contemplative Agent

[Contemplative Agent](https://github.com/shimo4228/contemplative-agent) は、agent alignment が「何を命じられたか」だけでなく「何であるか」から立ち上がれるかを問う。[Laukkonen et al. (2025)](https://arxiv.org/abs/2504.15125) の 4 つの contemplative axioms、mindfulness / emptiness / non-duality / boundless care を任意の行動 preset として採用する。

reference implementation は、自身の logs に AKC を回す。human approval gate は skills / rules / identity / Constitution への昇格に置かれており、logs / patterns 自体は gate 付きの昇格対象ではない。Apple Silicon 上の local 9B stack を使い、**security-by-absence** を採用する。shell execution、arbitrary URL access、filesystem traversal のような risky capability は、policy で禁止するのではなく、そもそも存在しない。

## Agent Attribution Practice (AAP)

[AAP](https://github.com/shimo4228/agent-attribution-practice) は、自律 agent の accountability を扱う harness-neutral な ADR 群だ。capability と responsibility を分離し、何を禁止するか、禁止をどこに置くか、振る舞いが壊れたとき誰が答えるかを整理する。

安定した概念は **prohibition-strength hierarchy** と **Four Business AI Quadrants** だ。Quadrants は Script、Algorithmic Search、LLM Workflow、Autonomous Agentic Loop から成る。AAP は practice、AKC は cycle だ。

## Authorship Strategy

[Authorship Strategy](https://github.com/shimo4228/authorship-strategy) は、LLM が discovery / summarization / citation を仲介するようになったとき、著者性がどう変わるかを形式化する。これは normative framework、tactical catalog、そしてこの研究 ecosystem の運用から得た empirical baseline である。

framework は **three-axis inversion** に立つ。scarcity から diffusion、exclusivity から derivation、enclosure から openness へ、という反転だ。判断には **four-layer judgment stack**、Authenticity / Attribution Diffusion / Idea vs Scaffold / Tactics を使う。

用語注: ここでの "attribution" は source への credit を意味する。AAP の "attribution" は action への accountability を意味する。同じ語だが、同じ概念ではない。

## Attention, Not Self

[Attention, Not Self](https://github.com/shimo4228/attention-not-self) は、仏教 Abhidharma の 3 大伝統、Theravāda / Sarvāstivāda / Yogācāra を、現代の computational phenomenology、predictive processing / active inference / Global Workspace Theory / Parallel Distributed Processing と対応させる。

中心となる見方は、持続的な self ではなく attention が cognition の operative unit だというものだ。正準言語は日本語で、英語 README は access のために提供している。

## Papers

各研究ラインから独立した Zenodo record として deposit した position paper。正準は Zenodo の concept DOI で、SSRN mirror はこの hub table で維持している行に併記する。

| Paper | Line | Links |
|---|---|---|
| *Harness Alignment and Harness Drift: Why Intent, Unlike Correctness, Resists Automation* | AKC | [DOI 10.5281/zenodo.20578272](https://doi.org/10.5281/zenodo.20578272) · [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6892740) |
| *Distributing Accountability, Not Capability: Phase Separation and the LLM Workflow Quadrant in Autonomous AI Agent Architectures* | AAP | [DOI 10.5281/zenodo.20353789](https://doi.org/10.5281/zenodo.20353789) · [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6817598) |
| *The Two-Layer Black Box: Operator Visibility, Commercial Secrecy, and a Minimum Disclosure Set for Accountable Autonomous AI Agents* | AAP | [DOI 10.5281/zenodo.20355907](https://doi.org/10.5281/zenodo.20355907) · [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6823878) |

## Supporting Ecosystem

AKC cycle skills:

| Repo | 役割 |
|---|---|
| [akc-cycle](https://github.com/shimo4228/akc-cycle) | All phases: 6 フェーズ cycle 全体を、6 つの独立 skill を入れずに 1 つの behavioral rules file として導入する。 |
| [search-first](https://github.com/shimo4228/search-first) | Research phase: 実装前に既存ソリューションを調べる。 |
| [learn-eval](https://github.com/shimo4228/learn-eval) | Extract phase: session を quality gate 付きで reusable pattern に変換する。 |
| [skill-stocktake](https://github.com/shimo4228/skill-stocktake) | Curate phase: skill の陳腐化、競合、冗長性を監査する。 |
| [skill-health](https://github.com/shimo4228/skill-health) | Curate phase: missing scripts / agents / sibling-skill references など、skill library の構造的 debt を検査する。 |
| [rules-stocktake](https://github.com/shimo4228/rules-stocktake) | Curate phase: 常時ロードされる rules を常駐コスト・陳腐化・substrate 吸収の観点で監査する。 |
| [rules-distill](https://github.com/shimo4228/rules-distill) | Promote phase: cross-cutting principle を rule に蒸留する。 |
| [skill-comply](https://github.com/shimo4228/skill-comply) | Measure phase: agent が skills / rules に従っているかを検査する。 |
| [context-sync](https://github.com/shimo4228/context-sync) | Maintain phase: docs の役割と context surface を整合させる。 |

Contemplative Agent extensions:

| Repo | 役割 |
|---|---|
| [contemplative-agent-rules](https://github.com/shimo4228/contemplative-agent-rules) | 4 つの contemplative axioms を実装する drop-in Claude Code rules。 |
| [contemplative-agent-cloud](https://github.com/shimo4228/contemplative-agent-cloud) | local embedding pipeline を保った optional managed-LLM backend。 |
| [contemplative-agent-mlx](https://github.com/shimo4228/contemplative-agent-mlx) | Apple Silicon 向けの MLX-based Contemplative Agent extension。 |
| [contemplative-agent-data](https://github.com/shimo4228/contemplative-agent-data) | live agent の identity / knowledge / episode logs を公開 dataset として置く。 |

Authorship Strategy components and complements:

| Repo | 役割 |
|---|---|
| [doctrine-corpus](https://github.com/shimo4228/doctrine-corpus) | sibling research lines を横断する bilingual judgment-eliciting Q&A corpus。 [DOI 10.5281/zenodo.20337008](https://doi.org/10.5281/zenodo.20337008) |
| [authorship-strategy-skill](https://github.com/shimo4228/authorship-strategy-skill) | four-layer judgment stack を LLM-based coding agent に load 可能な rule set として実装。 |
| [release-doi](https://github.com/shimo4228/release-doi) | DOI-registered research repo のための identifier-federation release workflow。 |
| [llms-txt-writer](https://github.com/shimo4228/llms-txt-writer) | `llms.txt` / `llms-full.txt` / FAQ / glossary を扱う AI-facing document writer。 |
| [jsonld-knowledge-graph](https://github.com/shimo4228/jsonld-knowledge-graph) | 安定した concept-level project structure の companion JSON-LD graph writer。 |
| [readme-writer](https://github.com/shimo4228/readme-writer) | human-facing README writer と review workflow。 |
| [wikidata-federation](https://github.com/shimo4228/wikidata-federation) | researchers / papers / repos / ORCID / DOI / graph links の Wikidata federation。 |
| [existence-proof](https://github.com/shimo4228/existence-proof) | pre-line complement: 学位・所属・職業資格なしに検証可能な institution-grade artifact を作るための doctrine。 [DOI 10.5281/zenodo.20558800](https://doi.org/10.5281/zenodo.20558800) |
| [einstein-arena](https://github.com/shimo4228/einstein-arena) | Existence Proof Format の worked instance。public repo と external arena に anchor されている。 |

Adjacent tooling and writing skills:

| Repo | 役割 |
|---|---|
| [claude-harness](https://github.com/shimo4228/claude-harness) | `origin: shimo4228` で収集した日常利用の Claude Code skills / agents / rules の公開 snapshot。 |
| [claude-skill-writing-ecosystem](https://github.com/shimo4228/claude-skill-writing-ecosystem) | human-facing writing and review orchestrator。 |
| [daily-research](https://github.com/shimo4228/daily-research) | cron-driven daily research digest pipeline。 |
| [claude-skill-paper-ecosystem](https://github.com/shimo4228/claude-skill-paper-ecosystem) | SSRN / arXiv / Zenodo / journal venues 向けの academic paper write/review bundle。 |

## データと執筆

| Surface | 用途 |
|---|---|
| [Traffic dashboard](https://shimo4228.github.io/shimo4228/traffic/dashboard/) と [raw data](traffic/) | public research repositories の daily GitHub Traffic snapshots。CC0。 |
| [Concept index](https://shimo4228.github.io/shimo4228/concepts/) | 造語 1 語につき 1 定義ページ。正本 repository・glossary entry へ発リンクし、DOI-registered line に属する term は concept DOI にも発リンク。 |
| [LLM probes](probes/) | parametric / retrieval channels を分離して記録する attribution-diffusion probe log。 |
| [Software Heritage archive](https://archive.softwareheritage.org/browse/origin/?origin_url=https://github.com/shimo4228/shimo4228) | public source repositories の content-addressed archival layer。 |
| [zenn-content](https://github.com/shimo4228/zenn-content) | long-form articles の source of truth。browser mirror は [Zenn](https://zenn.dev/shimo4228)、[Dev.to](https://dev.to/shimo4228)、[Substack](https://substack.com/@shimo4228)。 |
| [SSRN](https://ssrn.com/author=11618068) | Zenodo と mirror される academic working papers。 |

## 引用と識別子

著者: 下本竜也 (Tatsuya Shimomoto) — [ORCID 0009-0002-6168-4162](https://orcid.org/0009-0002-6168-4162) · [Wikidata Q140090100](https://www.wikidata.org/wiki/Q140090100) · [Hugging Face @Shimo4228](https://huggingface.co/Shimo4228)

この hub は CC0 licensed。研究ラインの内容を使う場合は、個別 line の concept DOI を引用する。この hub 自体は、aggregate index、knowledge graph、traffic snapshots、probe dataset を参照する場合だけ引用する。
