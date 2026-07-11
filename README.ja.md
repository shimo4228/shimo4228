Language: [English](README.md) | 日本語

# Tatsuya Shimomoto (@shimo4228)

[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/shimo4228/shimo4228) [![GitMCP](https://img.shields.io/endpoint?url=https://gitmcp.io/badge/shimo4228/shimo4228)](https://gitmcp.io/shimo4228/shimo4228)

> 下本竜也による 5 本の独立引用可能な実践ラインの hub repository。主題は AI エージェント設計、AI 仲介時代の著者性、計算論的現象学。3 本の agent-design line はひとつの主張を共有する — [Through-line](#through-line) 参照。

下本竜也。AI エージェントを一人で作っている — Apple Silicon Mac 1 台、ラボも所属もなしで。やっているのは、AI 時代の「良いやり方」を実地で探ることだ。論文や DOI はその探究の道具であって、肩書きではない — 仕事を引用可能で永続的、追跡可能に保つためのものだ。この repo は地図であり、各プロジェクトの現在状態の source of truth ではない — 各実践ラインはそれぞれの repository と Zenodo concept DOI を持ち、この hub は安定した関係と引用ポインタを 1 か所にまとめる。

## 早見表

| Line | 役割 | 安定した概念 | 正準 record |
|---|---|---|---|
| [Contemplative Agent](https://github.com/shimo4228/contemplative-agent) | エージェントの disposition と実装 | 価値層を Constitution という明示的なハーネス artifact として持つ local agent — agent は自らの経験からこの Constitution を改訂していき、その改訂は human-gated review を通る。 | [DOI 10.5281/zenodo.19212118](https://doi.org/10.5281/zenodo.19212118) |
| [Agent Knowledge Cycle](https://github.com/shimo4228/agent-knowledge-cycle) | エージェント設計の mechanism | エージェントと操作者の意図 alignment を、振る舞いと判断の変化に合わせて保つ 6 フェーズ loop。 | [DOI 10.5281/zenodo.19200726](https://doi.org/10.5281/zenodo.19200726) |
| [Agent Attribution Practice](https://github.com/shimo4228/agent-attribution-practice) | accountability practice | 何を禁止するか、制御をどこに置くか、agent が壊れたとき誰が答えるかを扱う harness-neutral な ADR 群。 | [DOI 10.5281/zenodo.19652013](https://doi.org/10.5281/zenodo.19652013) |
| [Authorship Strategy](https://github.com/shimo4228/authorship-strategy) | AI 時代の著者性 methodology | LLM が発見と引用を仲介する時代に、known author であるための framework。 | [DOI 10.5281/zenodo.20263316](https://doi.org/10.5281/zenodo.20263316) |
| [Attention, Not Self](https://github.com/shimo4228/attention-not-self) | 認知と仏教の inquiry | Abhidharma の cognitive-process model と computational phenomenology の比較。 | [DOI 10.5281/zenodo.20262112](https://doi.org/10.5281/zenodo.20262112) |

5 本のラインは sibling であり、依存関係ではない — どれ 1 本でも単独で採用できる。

## Through-line

3 本の agent-design line（Contemplative Agent / AKC / AAP）を貫く主張が一つある: **[value-layer harness engineering（価値層ハーネス工学）](https://shimo4228.github.io/shimo4228/concepts/value-layer-harness-engineering.html)** だ。エージェントハーネスに普通置かれるのはタスクの規則 — コーディング規約・セキュリティ方針・執筆スタイルだ。このプログラムは同じ層に価値規範（contemplative axioms、authorship-strategy の判断スタック）を書き、下位層と同じ human-gated サイクルで統治する（[claude-harness](https://github.com/shimo4228/claude-harness) がその公開 snapshot）。その価値層の contemplative な中身は著者の meditation 実践に由来し、5 本のうち 2 本のラインの源流でもある。Authorship Strategy はプログラム全体が公開され引用されるための方法論だ。

## Papers

各実践ラインから独立した Zenodo record として deposit した position paper。正準は concept DOI で、SSRN mirror は維持している行に併記する。

| Paper | Line | Links |
|---|---|---|
| *Harness Alignment and Harness Drift: Why Intent, Unlike Correctness, Resists Automation* | AKC | [DOI 10.5281/zenodo.20578272](https://doi.org/10.5281/zenodo.20578272) · [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6892740) |
| *Distributing Accountability, Not Capability: Phase Separation and the LLM Workflow Quadrant in Autonomous AI Agent Architectures* | AAP | [DOI 10.5281/zenodo.20353789](https://doi.org/10.5281/zenodo.20353789) · [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6817598) |
| *The Two-Layer Black Box: Operator Visibility, Commercial Secrecy, and a Minimum Disclosure Set for Accountable Autonomous AI Agents* | AAP | [DOI 10.5281/zenodo.20355907](https://doi.org/10.5281/zenodo.20355907) · [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6823878) |

## データと執筆

長文記事: [Zenn](https://zenn.dev/shimo4228) · [Dev.to](https://dev.to/shimo4228) · [Substack](https://substack.com/@shimo4228)（source は [zenn-content](https://github.com/shimo4228/zenn-content)）。公開 GitHub Traffic [dashboard](https://shimo4228.github.io/shimo4228/traffic/dashboard/) と [raw data](traffic/)、CC0。source は [Software Heritage](https://archive.softwareheritage.org/browse/origin/?origin_url=https://github.com/shimo4228/shimo4228) に content-addressed でアーカイブされている。

## 機械読解

機械はまず [`graph.jsonld`](graph.jsonld)、次に [`llms.txt`](llms.txt)、最後に [`llms-full.txt`](llms-full.txt)。網羅的な ecosystem inventory — supporting repositories・datasets・probe surfaces — はこれらと [concept index](https://shimo4228.github.io/shimo4228/concepts/) にあり、この README には置かない。

## 引用と識別子

著者: 下本竜也 (Tatsuya Shimomoto) — [ORCID 0009-0002-6168-4162](https://orcid.org/0009-0002-6168-4162) · [Wikidata Q140090100](https://www.wikidata.org/wiki/Q140090100) · [Hugging Face @Shimo4228](https://huggingface.co/Shimo4228)

この hub は CC0 licensed。実践ラインの内容を使う場合は、個別 line の concept DOI を引用する。この hub 自体は、aggregate index、knowledge graph、traffic snapshots、probe dataset を参照する場合だけ引用する。
