# Traffic Data

[@shimo4228](https://github.com/shimo4228) の公開研究 repo 6 件に対する GitHub Traffic API の daily snapshot。

**Dashboard**: [shimo4228.github.io/shimo4228/traffic/dashboard/](https://shimo4228.github.io/shimo4228/traffic/dashboard/) で 6 repo を 1 ページに可視化 (合算 timeline / repo 別 small multiples / clones:views 比 / 生データ table)。

## 何のデータか

`data/` 配下に append-only JSONL の time series を repo ごと 1 ファイルで保存:

- [contemplative-agent](https://github.com/shimo4228/contemplative-agent)
- [agent-knowledge-cycle](https://github.com/shimo4228/agent-knowledge-cycle)
- [agent-attribution-practice](https://github.com/shimo4228/agent-attribution-practice)
- [contemplative-agent-data](https://github.com/shimo4228/contemplative-agent-data)
- [zenn-content](https://github.com/shimo4228/zenn-content)
- [shimo4228](https://github.com/shimo4228/shimo4228) (この profile repo)

GitHub Traffic API は直近 14 日しか返さない。daily snapshot を取り続けることで、後追い不可能な long-term record を蓄積する。

## なぜ public か

これらのプロジェクトの AI 時代オーセンシティ姿勢の 1 軸が openness (希少性 → 拡散、排他性 → 派生、**囲い込み → 開放**)。観察ログを公開することは、観察対象の作品を公開していることと整合する。また、AI 経由の discovery (LLM / RAG indexer / AI coding assistant) が idea-rescue 系研究 repo にどう interaction するかを研究する人にとって、具体的なデータ点になる。

## どう読まないか

短期 (1-2 週) の変動には人間 signal がほとんど含まれない。既存の分析で観察された pattern:

- clone:view 比率 30:1 〜 215:1 — access の大半は非人間
- 記事公開日に cross-repo crawler wave が発生する (単 repo イベントではない)
- README のキーワード編集は数値を動かさない (observable scale で)

長期観察ログとして扱い、marketing dashboard として読まない。

## Schema

1 行 = 1 つの JSON object:

```json
{"date":"2026-05-05","clones":{"count":130,"uniques":42},"views":{"count":7,"uniques":5},"fetched_at":"2026-05-06T00:30:12Z"}
```

| Field | Source | 意味 |
|---|---|---|
| `date` | API `timestamp` (UTC midnight) | 集計対象日 |
| `clones.count` | `/traffic/clones` `count` | 当日 total clone (重複含む) |
| `clones.uniques` | `/traffic/clones` `uniques` | 当日 unique cloner 数 |
| `views.count` | `/traffic/views` `count` | 当日 total view |
| `views.uniques` | `/traffic/views` `uniques` | 当日 unique visitor 数 |
| `fetched_at` | Workflow runtime (ISO 8601) | snapshot 取得時刻 |

Repo の identity はファイル名に encode する (line 内に repo フィールドは持たない)。

## 更新頻度

UTC 00:30 daily、[`.github/workflows/traffic-daily.yml`](../.github/workflows/traffic-daily.yml) より。

## ライセンス

CC0 1.0 — public domain dedication。データ自体と同じ openness。
