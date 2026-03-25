Language: [English](README.md) | 日本語

# Tatsuya Shimomoto (@shimo4228)

2つの研究ライン: AI コーディングエージェントの**実用的な自己改善ツール**と、自律エージェントの**Contemplative AI**。

## 主なプロジェクト

### [Agent Knowledge Cycle (AKC)](https://github.com/shimo4228/agent-knowledge-cycle)

AI コーディングエージェントの自己改善ループ — 6つのスキルが循環的に連携:

```
経験 → learn-eval → skill-stocktake → rules-distill → 行動変容 → ...
        (抽出)        (淘汰)            (原則昇格)         ↑
                                                     skill-comply
                                                       (計測)
                                        context-sync ← (保守)
```

| スキル | フェーズ | 概要 |
|--------|---------|------|
| [search-first](https://github.com/shimo4228/claude-skill-search-first) | 調査 | 実装前に既存ソリューションを調査 |
| [learn-eval](https://github.com/shimo4228/claude-skill-learn-eval) | 抽出 | セッションから再利用可能なパターンを品質ゲート付きで抽出 |
| [skill-stocktake](https://github.com/shimo4228/claude-skill-stocktake) | 淘汰 | スキルの陳腐化・競合・冗長性を監査 |
| [rules-distill](https://github.com/shimo4228/claude-skill-rules-distill) | 昇格 | スキル群から共通原則を蒸留してルールに昇格 |
| [skill-comply](https://github.com/shimo4228/claude-skill-comply) | 計測 | スキルが実際に遵守されているか行動コンプライアンスを自動計測 |
| [context-sync](https://github.com/shimo4228/claude-skill-context-sync) | 保守 | ドキュメントの役割重複・陳腐化・ADR 欠落を検出して修正 |

### Contemplative AI

**[contemplative-agent](https://github.com/shimo4228/contemplative-agent)** — 自らの経験を知識とスキルに蒸留する自律AIエージェント — 睡眠時記憶統合、アイデンティティ精錬、行動スキル抽出をローカルLLM（Ollama）上で実行。

| プロジェクト | 概要 |
|-------------|------|
| [contemplative-agent-rules](https://github.com/shimo4228/contemplative-agent-rules) | 4つの公理に触発された Claude Code ルール — IPD ベンチマークで検証 |
| [active-inference-viz](https://github.com/shimo4228/active-inference-viz) | Active Inference のダイナミクスをインタラクティブに可視化 |

### アプリケーション

| プロジェクト | 概要 |
|-------------|------|
| [pdf2anki](https://github.com/shimo4228/pdf2anki) | AI による PDF → Anki フラッシュカード変換 |
| [daily-research](https://github.com/shimo4228/daily-research) | 毎朝自動生成される AI リサーチダイジェスト — Python ゼロ、シェル + プロンプトのみ |

## 執筆

- **[Zenn](https://zenn.dev/shimo4228)** — Claude Code、AI エージェント開発（日本語）
- **[Dev.to](https://dev.to/shimo4228)** — 英語翻訳 + オリジナル記事
