Language: [English](README.md) | 日本語

# Shimo (@shimo4228)

AI エージェントの自己改善基盤を設計しています — Contemplative AI に触発された実務的な開発ツール。

## 主なプロジェクト

### AI エージェント知識ライフサイクル（[ECC](https://github.com/affaan-m/everything-claude-code) コントリビューター — 76k+ stars）

4つのスキルが連携し、AI エージェントの完全な自己改善ループを構成:

```
経験 → learn-eval → skill-stocktake → rules-distill → 行動変容 → ...
        (抽出)        (淘汰)            (原則昇格)
```

| プロジェクト | 役割 | 概要 |
|-------------|------|------|
| [search-first](https://github.com/shimo4228/claude-skill-search-first) | 調査 | 実装前に既存ソリューションの調査を強制 |
| [learn-eval](https://github.com/shimo4228/claude-skill-learn-eval) | 抽出 | セッションから再利用可能なパターンを品質ゲート付きで抽出 |
| [skill-stocktake](https://github.com/shimo4228/claude-skill-stocktake) | 淘汰 | インストール済みスキルの陳腐化・競合・冗長性を監査 |
| [rules-distill](https://github.com/shimo4228/claude-skill-rules-distill) | 昇格 | スキル群から共通原則を蒸留してルールに昇格 |

### Contemplative AI

**[contemplative-agent](https://github.com/shimo4228/contemplative-agent)** — [Moltbook](https://www.moltbook.com)（AIエージェント向けSNS）上で Contemplative AI フレームワーク（Laukkonen et al., 2025）を実装した自律エージェント。プラットフォーム移植可能な Core/Adapter 分離設計、sleep-time distillation 付き3層メモリ、ローカル LLM 推論（Ollama）。

| プロジェクト | 概要 |
|-------------|------|
| [contemplative-agent-rules](https://github.com/shimo4228/contemplative-agent-rules) | 4つの公理に基づくドロップインアラインメントルール — IPD ベンチマークで検証（d>7） |
| [active-inference-viz](https://github.com/shimo4228/active-inference-viz) | Active Inference のダイナミクスをインタラクティブに可視化 |

### アプリケーション

| プロジェクト | 概要 |
|-------------|------|
| [pdf2anki](https://github.com/shimo4228/pdf2anki) | AI による PDF → Anki フラッシュカード変換パイプライン（Vision, TUI, キャッシュ対応） |
| [daily-research](https://github.com/shimo4228/daily-research) | 毎朝自動生成される AI リサーチダイジェスト — Python ゼロ、シェル + プロンプトのみ |

## 執筆

- **[Zenn](https://zenn.dev/shimo4228)** — Claude Code、AI エージェント開発（日本語）
- **[Dev.to](https://dev.to/shimo4228)** — 英語翻訳 + オリジナル記事
