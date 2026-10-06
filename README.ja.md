Language: [English](README.md) | 日本語

![カバーアート: 一筆の墨から五色の糸がほどけ、円相へ流れ込む](assets/readme-cover.jpg)

# Tatsuya Shimomoto

> AI エージェント・著者性・注意をめぐる 5 本の長期プロジェクト（それぞれ単独で引用できます）の hub であり、Claude Code と TypeSafe Jev 向けに公開している道具の入口でもあります。

こんにちは、Tatsuya Shimomoto（shimo4228）です。ラボにも組織にも属さず、AI エージェントを一人で作っています。そのひとつは M1 Mac 上のローカル LLM で動き、5 本のうち 1 本は瞑想で見えたことをそのまま書き留めたものです。エージェントのハーネス（エージェントに渡す規則とツール一式）を作っている人、自律エージェントの説明責任を考えている人、AI 時代の著者性に関心がある人に向けています。このリポジトリは地図であって正本ではありません。各プロジェクトと各道具の最新情報はそれぞれのリポジトリにあり、ここには変わらない関係と引用先だけを置いています。

## どこから来たかで選ぶ

- **TypeSafe Jev のプロジェクトから:** [jev-skill-router](https://github.com/shimo4228/jev-skill-router)（prompt ごとに Jev へ「どの skill が合うか」を聞く Claude Code の hook）と [jev-research-pipeline](https://github.com/shimo4228/jev-research-pipeline)（code がループを持ち、Jev が判定し、Qwen が書く、毎日の研究監視）。その次は [claude-harness](https://github.com/shimo4228/claude-harness) の `jev-judgment-design` skill へ。
- **Claude の plugin directory から:** [harness-scope](https://github.com/shimo4228/harness-scope)（global harness は 1 つのまま、repo ごとに Claude に見せるものを選ぶ）と [akc-cycle](https://github.com/shimo4228/akc-cycle)（Agent Knowledge Cycle を 1 つの rules file と plugin にしたもの）。どちらも Anthropic の Claude plugin directory に掲載されています。その次は、両方の出どころである [claude-harness](https://github.com/shimo4228/claude-harness) へ。
- **記事・DOI・用語の検索から:** 下の表へ。

## 早見表

| プロジェクト | 何か | 代表的な引用先 |
|---|---|---|
| [Contemplative Agent](https://github.com/shimo4228/contemplative-agent) | 価値観の層を Constitution（憲法）という明示的なファイルとして持ち、経験からの改訂を人間のレビューで通すローカルエージェント。 | [DOI 10.5281/zenodo.19212118](https://doi.org/10.5281/zenodo.19212118) |
| [Agent Knowledge Cycle (AKC)](https://github.com/shimo4228/agent-knowledge-cycle) | エージェントと操作者の両方が変わり続ける中で、意図のずれを直し続ける 6 フェーズのループ。 | [DOI 10.5281/zenodo.19200726](https://doi.org/10.5281/zenodo.19200726) |
| [Agent Attribution Practice (AAP)](https://github.com/shimo4228/agent-attribution-practice) | 何を禁止するか、制御をどこに置くか、壊れたとき誰が責任を持つかを、特定ツールに依存しない形で記録した設計判断集。 | [DOI 10.5281/zenodo.19652013](https://doi.org/10.5281/zenodo.19652013) |
| [Authorship Strategy](https://github.com/shimo4228/authorship-strategy) | 読者が LLM 越しに考えに出会う時代に著者が見つかり続ける方法。囲い込むのではなく開くことで、広まること自体に出どころを運ばせる。 | [DOI 10.5281/zenodo.20263316](https://doi.org/10.5281/zenodo.20263316) |
| [Attention, Not Self](https://github.com/shimo4228/attention-not-self) | 瞑想で気づいたことを、古典仏教の心の地図（アビダルマ）で言い表し、計算論的現象学と並べたエッセイ集と知識グラフ。 | [DOI 10.5281/zenodo.20262112](https://doi.org/10.5281/zenodo.20262112) |

5 本は兄弟プロジェクトで、互いに依存していません。関心に近いところから開いてください。表の DOI は Zenodo の concept DOI（常に最新版へつながる代表 DOI）です。

## Through-line

私自身の瞑想が Contemplative Agent と Attention, Not Self の源流にあります。エージェント設計の 3 本は 1 つの主張、[value-layer harness engineering（価値層ハーネス工学）](https://shimo4228.github.io/shimo4228/concepts/value-layer-harness-engineering.html)を共有しています。ハーネスにはコーディング規約と同じ場所に価値の規範も書き込め、それも同じ人間レビューで改訂され続ける、という主張です。Contemplative Agent は「そんな層を持ったエージェントが本当に動くのか」を、AKC は「双方が変わり続ける中でその層を操作者の意図に沿わせ続けられるか」を、AAP は「壊れたとき誰が責任を持つのか」を問います。[claude-harness](https://github.com/shimo4228/claude-harness) はこの主張の実働形で、私のエージェントたちが日々動いているハーネスの公開版です。Authorship Strategy は、他の 4 本と自分自身を外に開いて引用できるようにする方法です。

## ほかの場所

- 執筆: [Zenn](https://zenn.dev/shimo4228) · [Dev.to](https://dev.to/shimo4228) · [note](https://note.com/shimo4228) · [Substack](https://substack.com/@shimo4228)。原稿は [zenn-content](https://github.com/shimo4228/zenn-content)
- データ: このリポジトリの GitHub Traffic を [dashboard](https://shimo4228.github.io/shimo4228/traffic/dashboard/) と[生データ](traffic/)で公開（どちらも CC0）。ソース一式は [Software Heritage](https://archive.softwareheritage.org/browse/origin/?origin_url=https://github.com/shimo4228/shimo4228) にもアーカイブ
- 機械向け: [`graph.jsonld`](graph.jsonld) → [`llms.txt`](llms.txt) → [`llms-full.txt`](llms-full.txt) の順に。関連リポジトリやデータセットの全体目録はそこと [concept index](https://shimo4228.github.io/shimo4228/concepts/) にあります。対話形式で聞くなら [DeepWiki](https://deepwiki.com/shimo4228/shimo4228)
- 識別子: [ORCID 0009-0002-6168-4162](https://orcid.org/0009-0002-6168-4162) · [Hugging Face @Shimo4228](https://huggingface.co/Shimo4228) · [`CITATION.cff`](CITATION.cff)。この hub は CC0 です。各プロジェクトはその concept DOI で引用してください
