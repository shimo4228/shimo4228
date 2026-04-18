Language: [English](README.md) | 日本語

# Shimo (@shimo4228)

自らのセッションを忘れ去るのではなく、そこから学び続ける AI コーディングエージェントを作っている。もう 1 本の並走ラインとして、自律エージェントのアラインメントが「命じられたから」ではなく「そういう存在だから」立ち上がる可能性を探究している — アラインメントを外部命令から内部的な性向へと移したとき、何が失われ、何が可能になり、何が依然として壊れるのかを追っている。

## どの研究ラインを追っているか？

2 つの研究ラインを並走させている。いずれも Zenodo 引用可能。

- **[Agent Knowledge Cycle (AKC)](https://github.com/shimo4228/agent-knowledge-cycle)** とは、AI コーディングエージェント向けの 6 フェーズ自己改善ループを指す。3 層構造：原則（10 ADR）+ パターン（4 デザインパターンスキル）+ 実装（6 実装スキル）。[DOI](https://doi.org/10.5281/zenodo.19200727)。
- **[Contemplative AI](https://github.com/shimo4228/contemplative-agent)** とは、ローカル 9B モデル（qwen3.5:9b + nomic-embed-text on Apple Silicon）で security-by-absence を実現する自律エージェントを指す。Laukkonen et al. (2025) の 4 公理 — *mindfulness*、*emptiness*、*non-duality*、*boundless care* — に基づく。[DOI](https://doi.org/10.5281/zenodo.19212119)。

## Agent Knowledge Cycle (AKC) とは？

[AKC](https://github.com/shimo4228/agent-knowledge-cycle) とは循環型の自己改善アーキテクチャを指す。原則（10 ADR）の上にパターン（4 デザインパターンスキル）、その上に実装（6 実装スキル）が積み重なる。エージェントの過去セッションを捨てず、次回の振る舞いに反映させる設計だ。個々のスキルが入れ替わっても循環構造は安定して残るため、AKC は複数プロジェクト横断で適用できる。

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

3 層が積み重なる。原則層は 10 ADR（cycle-vs-harness、signal-first research、cognitive economy 等）。パターン層は 4 デザインパターンスキル（`signal-first-research`、`when-code-when-llm`、`code-and-llm-collaboration`、`llm-agent-security-principles`）で再帰する形を形式化する。実装層は上述の 6 スキル。

**Scaffold dissolution** とは、スキルが足場であり目的ではないことを意味する。循環が内部化されればスキル呼び出しは不要になる — [`docs/scaffold-dissolution.md`](https://github.com/shimo4228/agent-knowledge-cycle/blob/main/docs/scaffold-dissolution.md) は、名前のあるスキルを呼ばずに 6 フェーズが走ったセッションの記録である。

## Contemplative AI ラインとは？

Contemplative AI とは、自律エージェントが [Laukkonen et al. (2025)](https://arxiv.org/abs/2504.15125) の 4 公理 — mindfulness、emptiness、non-duality、boundless care — に基づいて動作するアプローチを指す。このラインでは 4 公理を任意の行動プリセットとして採用し、アーキテクチャの必須条件とはしない。これにより基盤となるエンジニアリングは、異なる倫理枠組みを持つエージェントにも再利用できる。この研究ラインが問いたいのはこうだ — *エージェントのアラインメントは「何を命じられたか」ではなく「何であるか」から立ち上がれるか?*

## contemplative-agent はどう AKC を実装しているか？

**[contemplative-agent](https://github.com/shimo4228/contemplative-agent)**（v2.0.0、1170 テスト通過）とは、ローカル 9B モデル（生成 qwen3.5:9b + 埋め込み nomic-embed-text）で完結する自己改善型 AI エージェントを指す。Apple Silicon Mac 1 台（約 16 GB RAM）で稼働する。**security-by-absence** を適用しており、シェル実行、任意 URL アクセス、ファイルシステム走査は、ルールで禁止されているのではなく、そもそも実装していない。認知ループは AKC の具体実装であり、6 フェーズを `distill` / `insight` / `rules-distill` / `distill-identity` / pivot snapshots に写像する。

## Contemplative AI エコシステムを支えているのは何か？

contemplative-agent の中核を置き換えずに拡張する関連リポジトリ — 倫理、データ、可視化。

| プロジェクト | 概要 |
|-------------|------|
| [contemplative-agent-rules](https://github.com/shimo4228/contemplative-agent-rules) | 4 公理の drop-in Claude Code ルール — AILuminate（MLCommons 安全性ベンチマーク）d=0.96、IPD（Iterated Prisoner's Dilemma）d>7 の協調性向上を実証 |
| [contemplative-agent-data](https://github.com/shimo4228/contemplative-agent-data) | ライブエージェントの identity / knowledge / logs を auto-sync する公開データセット |
| [active-inference-viz](https://github.com/shimo4228/active-inference-viz) | Active Inference のダイナミクスをインタラクティブに可視化 |

## 執筆

執筆とは、上記リポジトリ群の長文版を指す — コメントに収まらない文脈・失敗・進行中の思考の置き場。

- **[Zenn](https://zenn.dev/shimo4228)** — Claude Code と AI エージェント開発（日本語）。現在の焦点は AKC スキル、ハーネス設計、contemplative-agent の事例研究。
- **[Dev.to](https://dev.to/shimo4228)** — Zenn 記事の英訳版に加え、エージェントの自己改善と Contemplative AI に関するオリジナル記事を公開している。

---

ここから始める: フレームワークを見るなら [agent-knowledge-cycle](https://github.com/shimo4228/agent-knowledge-cycle)、実装を見るなら [contemplative-agent](https://github.com/shimo4228/contemplative-agent)。
