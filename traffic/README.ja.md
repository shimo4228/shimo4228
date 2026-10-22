# Traffic Data

[@shimo4228](https://github.com/shimo4228) の公開 repo（下の一覧）に対する GitHub Traffic API の daily snapshot。

**Dashboard**: [shimo4228.github.io/shimo4228/traffic/dashboard/](https://shimo4228.github.io/shimo4228/traffic/dashboard/) で、`REPOS` に載せた repo を 1 ページに表示する（スマホ向け）。4 指標（unique visitors / views / unique cloners / clones）を 30 日・90 日・全期間で切り替え、日次グラフ、全期間のカレンダー、並べ替えられる repo 一覧と repo ごとのグラフ、生データ表、attribution probe を載せる。

## 何のデータか

`data/` 配下に append-only JSONL の time series を repo ごと 1 ファイルで保存:

- [contemplative-agent](https://github.com/shimo4228/contemplative-agent)
- [agent-knowledge-cycle](https://github.com/shimo4228/agent-knowledge-cycle)
- [agent-attribution-practice](https://github.com/shimo4228/agent-attribution-practice)
- [authorship-strategy](https://github.com/shimo4228/authorship-strategy)
- [attention-not-self](https://github.com/shimo4228/attention-not-self)
- [contemplative-agent-data](https://github.com/shimo4228/contemplative-agent-data)
- [zenn-content](https://github.com/shimo4228/zenn-content)
- [claude-harness](https://github.com/shimo4228/claude-harness) (公開 Claude Code harness — skills / agents / rules)
- [shimo4228](https://github.com/shimo4228/shimo4228) (この profile repo)

snapshot のみ（dashboard には載せない。2026-10-06 追加）: claude-harness から export した skill repo と退役台帳 —
[search-first](https://github.com/shimo4228/search-first)、[skill-stocktake](https://github.com/shimo4228/skill-stocktake)、[codex-review](https://github.com/shimo4228/codex-review)、[readme-writer](https://github.com/shimo4228/readme-writer)、[llms-txt-writer](https://github.com/shimo4228/llms-txt-writer)、[harness-pruning](https://github.com/shimo4228/harness-pruning)。

2026-10-07 追加: awesome list などの外部リストに出した repo。うち 4 本（harness-scope、jev-skill-router、jev-research-pipeline、akc-cycle）は dashboard にも載せ、残りは snapshot のみ。収集対象の全体は [`.github/workflows/traffic-daily.yml`](../.github/workflows/traffic-daily.yml) の `repos` 配列が正本。

GitHub Traffic API は直近 14 日しか返さない。daily snapshot を取り続けることで、後追い不可能な long-term record を蓄積する。

## なぜ public か

これらのプロジェクトの AI 時代オーセンシティ姿勢の 1 軸が openness (希少性 → 拡散、排他性 → 派生、**囲い込み → 開放**)。観察ログを公開することは、観察対象の作品を公開していることと整合する。また、AI 経由の discovery (LLM / RAG indexer / AI coding assistant) が idea-rescue 系研究 repo にどう interaction するかを研究する人にとって、具体的なデータ点になる。

## 何が観察できるか

repo を横並びにすると、単 repo では noise にしか見えない signal が cross-repo の structural pattern として浮かび上がる:

- **Bot/crawler が支配的**: snapshot 開始から 2 週間（2026-05-05 まで）は、clones:views 比率が研究 repo すべてで 30:1 以上だった。プロフィール repo ([shimo4228](https://github.com/shimo4228/shimo4228)) は 80 clones に対し 0 views — 誰も *読んで* いないが、何かが *cloning* していた。その後は人の閲覧が増えて比率は下がっている。現在の値は dashboard の Clones / view 列で見られる。
- **Cross-repo crawler wave**: 同一日に複数 repo の clone が同時にピークを立てる。記事公開日に portfolio 全体を順に走査する pattern が観測できる (単 repo の event ではない)。
- **可視性の希少性 (admin-only)**: GitHub Traffic API の clone 数は push 権限を持つユーザにしか返らない。他人の repo の clone 行動は UI でも公開 API でも一切見えない。それゆえ個人 repo の clone 行動の longitudinal な公開データセットは事実上 wild にほぼ存在しない。stars / forks / watchers と違い、clone は外から数えられない数字。
- **時間の希少性**: 自分の repo の数字でさえ、API は直近 14 日しか返さない。蓄積を止めた瞬間に過去は後追い不能になる。

これは marketing 数値ではなく、AI-mediated discovery の field record として読む。蓄積されない過去 (時間) × 他人からは見えない数字 (可視性) の二重の希少性ゆえ、1 年後・3 年後にこの portfolio がどう発見されていったかを遡る人にとっても、admin の枠外から個人 repo の clone 行動を量で扱いたい研究者にとっても、この CC0 daily 記録は少数の参照点になる。

## どう読まないか

短期 (1-2 週) の変動には人間 signal がほとんど含まれない。既存の分析で観察された pattern:

- clone:view 比率 30:1 〜 215:1（snapshot 開始〜2026-05-05 の観測）— 当時は access の大半が非人間。その後は比率が下がっているので、現在の値は dashboard で見る
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

## Referrer（2026-10-11 追加）

`referrers/<repo>.jsonl` には、日次の実行ごとに、その repository について Traffic API が返す referrer を 1 行で記録する:

```json
{"date":"2026-10-12","window_days":14,"referrers":[{"referrer":"github.com","count":7,"uniques":3}],"fetched_at":"2026-10-12T00:30:40Z"}
```

API は referrer を **直近 14 日の合計** としてしか返さないので、連続する行は期間が重なる。日ごとの数ではなく、その時点の 14 日窓のスナップショットである。referrer は page view についてだけ得られ、clone には出どころの情報がない（clone は経路不明の到達のまま）。系列は 2026-10-11 に始まる。人の経路の view が意味のある量になったのは 2026-09 からなので、それ以前と比べる基準はない。authorship-strategy の framework では、これらは arrival proxy で、proxy の段で報告する（ADR-0024）。

## スターとフォロワー（2026-10-22 追加）

`stars.jsonl` は UTC の 1 日 1 行で、アカウントが持つ公開リポジトリ（fork を除く）のスター数・fork 数と
フォロワー数を記録します（`scripts/stars_snapshot.py`）。GitHub は現在のスター数しか持たないため、
週の増減はこの毎日の記録から読みます。

## 週のまとめ（2026-10-22 追加）

[`weekly/`](weekly/) に毎週月曜、前の週（月〜日、UTC）の 1 枚が足されます
（[`.github/workflows/weekly-summary.yml`](../.github/workflows/weekly-summary.yml) と `scripts/weekly_summary.py`）。
個人サイト <https://shimo4228.github.io/> の訪問（Cloudflare Web Analytics。secret `CF_API_TOKEN` /
`CF_ACCOUNT_ID` / `CF_SITE_TAG` があるとき）、リポジトリごとの GitHub 閲覧、スターとフォロワー、
14 日間の流入元、zenn-content `scripts/metrics/snapshots.jsonl` にある手集めの Zenn・Dev.to の値を並べます。
数字と日付だけを並べ、結論は書きません。読み方は上の「どう読まないか」に従います。取れなかった値は 0 とせず、
取れなかったと書きます。

## 更新頻度

UTC 00:30 daily、[`.github/workflows/traffic-daily.yml`](../.github/workflows/traffic-daily.yml) より。

## ライセンス

CC0 1.0 — public domain dedication。データ自体と同じ openness。
