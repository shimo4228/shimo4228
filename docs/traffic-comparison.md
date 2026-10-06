# Traffic 比較 — 固定 cohort と明示 window

`scripts/traffic_compare.py` は Python 標準ライブラリだけで既存 JSONL を読む CLI。
ネットワークアクセス・データ書き換え・収集 workflow / dashboard の変更は行わない。
集計対象は `views.count`（閲覧回数）のみ。unique visitors や clone 数は足さない。

## 固定 cohort

- `legacy`: contemplative-agent, agent-knowledge-cycle, agent-attribution-practice,
  authorship-strategy, attention-not-self, contemplative-agent-data, zenn-content,
  claude-harness, shimo4228（従来の 9 repo）。基準行との比較はこの系列。
- `additional`: search-first, skill-stocktake, codex-review, readme-writer,
  llms-txt-writer, harness-pruning（追加の 6 repo）。独立系列として読む。
- `claude-harness`: 単独系列。legacy にも含まれるため、legacy に再加算しない。
- `total_reference`: legacy + additional の固定 15 repo。参考値のみ。
  従来の 9 repo 基準と比較しない。

対象ファイルは上記 repo 名の `traffic/data/<repo>.jsonl` に限定する。
ファイルの追加や workflow の repo 配列変更で legacy の母集団は変わらない。
cohort の改訂は新系列として扱い、過去の定義を上書きしない。

## 使用

hub repo root で実行する（データの既定パスはスクリプト基準なので他の cwd でも動く）:

```bash
python3 scripts/traffic_compare.py --start 2026-09-18 --end 2026-10-01
python3 scripts/traffic_compare.py --start 2026-09-20 --end 2026-10-03
python3 scripts/traffic_compare.py --data-dir traffic/data --start 2026-09-18 --end 2026-10-01
python3 -m unittest discover -s tests -v
```

start / end は必須の `YYYY-MM-DD`。JSONL の `date` は **traffic の UTC 日付**であり、
取得時刻 `fetched_at` や JST 日付ではない。両端を含める。
CLI は window を自動で動かさない。14 日比較なら終了日から 13 日前を開始日にする。
UTC で当日を除いた終了日を選び、各系列の completeness を確認する。
UTC の日が閉じても、収集の遅延や既存 workflow による再取得で数値は変わり得る。
期間終了・全レコード存在は API 数値の最終確定を保証しない。

## 出力・欠測・エラー

stdout は JSON。各 group の `repos` に母集団を記載し、次を返す:

- `complete`: 指定 window のすべての repo × 日に有効なレコードがあるか。
- `views_count`: complete な系列だけに数値を返す。不完全なら `null`。
- `partial_views_count`: 存在するレコードのみの部分和。**欠測があれば比較値ではない**。
  レコードが一つもない場合の `0` も、閲覧がゼロだった証拠ではない。
- `expected_repo_days` / `observed_repo_days`: 必要数と観測数。
- `missing_files` / `missing_dates`: 欠測 repo と日付。不存在をゼロ補完しない。

終了コード: `0` = 全系列 complete、`1` = 少なくとも一系列が不完全（JSON は出力）、
`2` = 入力・データエラー（stderr に理由、集計 JSON は出さない）。
追加系列が不完全でも、legacy が complete なら legacy の集計は有効。
比較する二つの window は同じ cohort・同じ日数で、両方 complete なものだけ使う。
CLI は増減率や効果判定を出さない。

固定 cohort の全ファイル・全行を検証する（window 外も対象）。空行は無視する。
必要な `date` / `views.count` が不正、負数、bool、非整数ならファイル名・行番号付きで拒否。
同じ repo の日付重複は、同じ値でも拒否し、最後の行で上書きしない。
`clones` / `uniques` / `fetched_at` は計算に使わず、検証対象外。
固定 cohort 外のファイルは読まない。

## 2026-10-04 ローカル実データ確認

personal-branding の scorecard 基準行 `140 / 14（09-18〜10-01、9 repo）` は保持する。
`2026-09-18`〜`2026-10-01` の実データ集計は legacy **140**（126/126 repo-days）、
claude-harness **14**（14/14 日）で一致した。この期間はローカルで確認できた最新の
完全な legacy 14 日 window でもある。追加 6 repo のファイルは未存在で、
additional は `null`（0/84）、total_reference も `null`（126/210）。終了コードは `1`。

当日 UTC を除く直近 14 日 `2026-09-20`〜`2026-10-03` は legacy **部分和 123**
（108/126）、claude-harness **部分和 13**（12/14）。従来 9 repo の全てで
`2026-10-02` と `2026-10-03` が欠測。追加 6 repo もファイル未存在。
両系列の `views_count` は `null`、終了コードは `1`。
これらの部分和を基準の 140 / 14 と比較して増減を判定しない。
