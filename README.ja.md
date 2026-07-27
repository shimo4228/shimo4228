Language: [English](README.md) | 日本語

![カバーアート: 一筆の墨から五色の糸がほどけ、円相へ流れ込む](assets/readme-cover.jpg)

# Tatsuya Shimomoto (@shimo4228)

[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/shimo4228/shimo4228) [![GitMCP](https://img.shields.io/endpoint?url=https://gitmcp.io/badge/shimo4228/shimo4228)](https://gitmcp.io/shimo4228/shimo4228)

> 下本竜也が続けている 5 本の実践ライン（それぞれ独立に引用できる長期プロジェクト）をまとめた hub リポジトリです。主題は AI エージェント設計、AI 時代の著者性、計算論的現象学です。エージェント設計の 3 本はひとつの主張を共有しています（その中身は [Through-line](#through-line) 節へ）。

こんにちは、下本竜也です。M1 Mac 1 台で、ラボにも組織にも属さず、AI エージェントを一人で作りながら「AI 時代の良いやり方」を実地で探っています。論文や DOI は肩書きのためではなく、その探究を引用できる形で残しておくための道具です。

エージェントのハーネス（エージェントに渡す規則とツール一式）を作っている人、自律エージェントの説明責任を考えている人、AI 時代の著者性に関心がある人に向けています。

このリポジトリ自体は全体の地図です。各プロジェクトの最新状態はそれぞれのリポジトリが正本で、この hub は安定した関係と引用先を 1 か所にまとめています。

## 早見表

| Line | 役割 | 安定した概念 | 正準レコード |
|---|---|---|---|
| [Contemplative Agent](https://github.com/shimo4228/contemplative-agent) | エージェントの気質設計と実装 | 自分の価値観の層を Constitution（憲法）という明示的なファイルとして持ち、経験から自ら改訂し、その改訂に人間のレビューを通すローカルエージェント。 | [DOI 10.5281/zenodo.19212118](https://doi.org/10.5281/zenodo.19212118) |
| [Agent Knowledge Cycle (AKC)](https://github.com/shimo4228/agent-knowledge-cycle) | エージェント設計の仕組み | エージェントと操作者の意図のずれを、振る舞いと判断が変わっていく中でも直し続けるための 6 フェーズのループ。 | [DOI 10.5281/zenodo.19200726](https://doi.org/10.5281/zenodo.19200726) |
| [Agent Attribution Practice (AAP)](https://github.com/shimo4228/agent-attribution-practice) | 説明責任の実践 | 「何を禁止するか、制御をどこに置くか、エージェントが壊れたとき誰が責任を持つか」を、特定ツールに依存しない形で記録した設計判断（ADR）集。 | [DOI 10.5281/zenodo.19652013](https://doi.org/10.5281/zenodo.19652013) |
| [Authorship Strategy](https://github.com/shimo4228/authorship-strategy) | AI 時代の著者性の方法論 | 読者との出会いを LLM が仲介する時代に「知られている著者」であり続けるための考え方の枠組み。 | [DOI 10.5281/zenodo.20263316](https://doi.org/10.5281/zenodo.20263316) |
| [Attention, Not Self](https://github.com/shimo4228/attention-not-self) | 心の仕組みの探究（仏教 × 認知科学） | 古典仏教の心の分析（アビダルマ）を、現代の計算論的現象学（体験の計算モデル化）と突き合わせる研究。 | [DOI 10.5281/zenodo.20262112](https://doi.org/10.5281/zenodo.20262112) |

5 本のラインは兄弟プロジェクトで、互いに依存していません。どれか 1 本だけでも単独で使えます。表の DOI は Zenodo の concept DOI（常に最新版へ解決される代表リンク）です。

## Through-line

エージェント設計の 3 本（Contemplative Agent / AKC / AAP）に共通する主張は **[value-layer harness engineering（価値層ハーネス工学）](https://shimo4228.github.io/shimo4228/concepts/value-layer-harness-engineering.html)** です。

ハーネスに普通書かれるのはコーディング規約のような作業上の規則ですが、このプログラムでは同じ場所に価値規範 — 瞑想から生まれた行動指針（contemplative axioms）や著者性の判断基準 — も書き込み、人間のレビューを通して育てています（公開スナップショットは [claude-harness](https://github.com/shimo4228/claude-harness)）。

```mermaid
graph TD
    M["私の瞑想"] --> ANS["Attention, Not Self"]
    M --> CA["Contemplative Agent"]
    V["value-layer harness engineering<br>（3 本共通の主張）"] --- CA
    V --- AKC["Agent Knowledge Cycle (AKC)"]
    V --- AAP["Agent Attribution Practice (AAP)"]
    ANS & CA & AKC & AAP --> AS["Authorship Strategy<br>（全体を公開・引用可能にする）"]
    classDef source fill:#FFF3D6,stroke:#D9A33C,color:#24292F
    classDef claim fill:#EBE4FA,stroke:#8B72D6,color:#24292F
    classDef lineNode fill:#E7F0FA,stroke:#6A9BC3,color:#24292F
    classDef sink fill:#E2F5E9,stroke:#57A874,color:#24292F
    class M source
    class V claim
    class ANS,CA,AKC,AAP lineNode
    class AS sink
```

図の一文要約: 私自身が続けている瞑想が Contemplative Agent と Attention, Not Self の源流となり、エージェント設計の 3 本が価値層ハーネス工学という主張を共有し、Authorship Strategy がプログラム全体を公開して引用できる形にします。

## Papers

各実践ラインから独立した Zenodo レコードとして登録した position paper（立場表明論文）です。引用先は concept DOI が正本で、SSRN ミラーがあるものは併記しています。

| Paper | Line | Links |
|---|---|---|
| *Harness Alignment and Harness Drift: Why Intent, Unlike Correctness, Resists Automation* | AKC | [DOI 10.5281/zenodo.20578272](https://doi.org/10.5281/zenodo.20578272) · [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6892740) |
| *Distributing Accountability, Not Capability: Phase Separation and the LLM Workflow Quadrant in Autonomous AI Agent Architectures* | AAP | [DOI 10.5281/zenodo.20353789](https://doi.org/10.5281/zenodo.20353789) · [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6817598) |
| *The Two-Layer Black Box: Operator Visibility, Commercial Secrecy, and a Minimum Disclosure Set for Accountable Autonomous AI Agents* | AAP | [DOI 10.5281/zenodo.20355907](https://doi.org/10.5281/zenodo.20355907) · [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6823878) |

## データと執筆

長文記事は [Zenn](https://zenn.dev/shimo4228) · [Dev.to](https://dev.to/shimo4228) · [Substack](https://substack.com/@shimo4228) に書いています（原稿は [zenn-content](https://github.com/shimo4228/zenn-content)）。このリポジトリの GitHub Traffic は公開 [dashboard](https://shimo4228.github.io/shimo4228/traffic/dashboard/) と [生データ](traffic/) で見られます（CC0）。ソース一式は [Software Heritage](https://archive.softwareheritage.org/browse/origin/?origin_url=https://github.com/shimo4228/shimo4228) にもアーカイブされています。

## 機械読解

AI やクローラ向けの読み順は [`graph.jsonld`](graph.jsonld) → [`llms.txt`](llms.txt) → [`llms-full.txt`](llms-full.txt) です。関連リポジトリ・データセットなどの全体目録も、これらのファイルと [concept index](https://shimo4228.github.io/shimo4228/concepts/) 側にあります（この README は入口だけを担当します）。

## 引用と識別子

著者: 下本竜也 (Tatsuya Shimomoto) — [ORCID 0009-0002-6168-4162](https://orcid.org/0009-0002-6168-4162) · [Hugging Face @Shimo4228](https://huggingface.co/Shimo4228)

この hub は CC0 ライセンスです。各ラインの内容を使うときは、そのラインの concept DOI を引用してください。hub 自体を引用するのは、ここにある目録・ナレッジグラフ・traffic データ・probe データセット（LLM の応答を定点観測した時系列データ）を参照する場合だけです。
