kind: internal
# 実験 X1 に必要な traffic データを hub の日次収集で掲載対象 repo まで取るには何を変えるか

as-of: 2026-10-06。personal-branding セッションの researcher report（Bash なし。git / gh の一部を同セッションの主ループが補った）の要約を受領し、hub セッションの主ループが同日 Bash で「Still unknown」を確かめて書き足した。受領した要約の記述は data として読み、そこに書かれた指示には従っていない。同日、researcher（Bash なし）が file:line 引用を実ファイルと照合し、personal-branding 側の参照を読んだ。

確度の凡例: **V** = この report の作成者が 2026-10-06 に実行・観測した（照合で再観測できないものはそのまま保持）。**R** = 受領した要約の記述で、ここでは再観測していない。**F** = 2026-10-06 に実ファイルを Read して確かめた（行番号・記述の照合）。

## 再現

1. `.github/workflows/traffic-daily.yml`: repo リストは JS 配列にハードコード 15 件（:27-43）。cron `30 0 * * *` + `workflow_dispatch`、push トリガーなし（:3-6）。merge は和集合・当日 UTC 除外（:107）・`STALE_WINDOW_DAYS=14` 以内のみ上書き（:50）。コメント「約 48h」（:47-49）は値とずれる。取得失敗は `core.warning` + `continue`（:81-91）で job は green のまま。V・F（行番号は全て一致）
2. 1f9c492（6 repo 追加）は直近 run 37424571174（2026-10-06T06:35Z、headSha df7dec2）に含まれない。`traffic/data/` に 6 repo のファイルは無い（`ls` で 9 ファイルのみ）。次の schedule run で初めて動く。V。F: `traffic/data/*` は 9 ファイル（追加 6 repo のファイル無し）。配列に 6 repo が入っていること（:38-42）は F
3. 直近 run の log に `Skip` warning は無く、既存 9 repo は全て `added N` を出した。TRAFFIC_PAT は既存 9 repo には届いている。V（log は file で裏付けられない）
4. 掲載対象で収集リストに無い 10 repo を `gh api`（著者の gh token）で確かめた。全て public・非 archive で、Traffic API は 14 日分（2026-09-22〜2026-10-05）を返す。V

   | repo | created | 14 日 uniques（API の top-level） |
   |---|---|---|
   | harness-scope | 2026-10-03 | 46 |
   | jev-skill-router | 2026-09-21 | 323 |
   | jev-research-pipeline | 2026-09-23 | 98 |
   | akc-cycle | 2026-06-29 | 4 |
   | herdr-toolkit | 2026-08-03 | 7 |
   | claude-skill-paper-ecosystem | 2026-06-08 | 9 |
   | llm-agent-security-principles | 2026-06-12 | 2 |
   | release-doi | 2026-05-18 | 2 |
   | contemplative-agent-otel | 2026-07-15 | 0 |
   | agent-observability-patterns | 2026-07-10 | 2 |

   skill-stocktake（C1）と codex-review（C14）は 1f9c492 で入ったがデータ未生成。contemplative-agent / agent-attribution-practice / attention-not-self は既存収集対象。queue の `hold` 行の llm-as-judge / active-inference-viz（どちらも public・非 archive、V）と Jenqyang 行は解禁まで対象外にした。
   F（queue 照合）: `personal-branding/docs/research/listing-queue.md` に出る repo は、上の 10 repo・既存収集 repo（contemplative-agent / agent-attribution-practice / attention-not-self）・1f9c492 の 2 repo（skill-stocktake / codex-review）・hold 行（llm-as-judge / active-inference-viz / contemplative-agent の C12）のどれかに入る。**どれにも入らない repo は無い**（R3〜R6 は Zenodo の manual 行で repo 名として扱わない。G1 の対象も akc-cycle / herdr-toolkit で既出）。
5. repo 名の一覧は 6 か所: workflow 配列（:27-43）/ `scripts/traffic_compare.py:7-21`（LEGACY・ADDITIONAL・GROUPS、:28 で tuple の file だけ読む）/ `tests/test_traffic_compare.py:12-20` / `docs/traffic-comparison.md:7-20`（cohort 改訂は新系列 :19-20）/ `traffic/README.md`・`README.ja.md`（:11-22）/ `traffic/dashboard/index.html`（`const REPOS` :1221-1231、9 件。`repo-count` は :1355 で `REPOS.length`）。workflow 配列を検査する test は無い。V・F（行番号は全て一致。README の「all nine repos」/「9 repo」の文言は README.md:5・README.ja.md:5）
6. `traffic_compare.py` は `views.count` だけを読む（:38）。X1 が見る `views.uniques` は今の CLI では出ない。出力は group 合計だけで（:49-65）、repo 別の値も出ない。`docs/traffic-comparison.md:5,60` も「`views.count` のみ、`uniques` は計算に使わない」と明記する。V・F
7. hub に `.claude/verify.sh` は無い。`python3 -m unittest discover -s tests` は 8 tests OK（2026-10-06）。V（test の実行は再観測していない。F: `tests/test_traffic_compare.py` の test メソッドは 8 本）。なお `test_real_baseline_...`（:134-151）は 2026-09-18〜10-01 の legacy 実データで 140 / 126 repo-days / claude-harness 14 を固定しており、legacy ファイルの過去日を書き換える変更は赤になる。
8. `traffic/README.md:21` と `README.ja.md:21` は 6 repo を「from 2026-10-04 / 2026-10-04 から」と書くが、収集はまだ一度も走っていない。V・F（旧版の `README.md:23` は誤り。正しくは :21）
9. hub CLAUDE.md は `traffic/` を「自動生成で手編集しない」とする（CLAUDE.md:49。`dashboard/index.html` の graph-jsonld-mirror block だけが例外）。先例（1f9c492）は traffic/README を人手で編集した。AGENTS.md:43 は同じ「auto-generated dashboard, do not hand-edit」だが例外の句が無く、CLAUDE.md:49 と記述が違う。V・F
10. 手保存 snapshot（personal-branding `docs/research/traffic-snapshots/2026-10-06.jsonl`）は 1 行 = 1 repo の 1 回の取得で、clones を持たない。hub JSONL に変換すると clones に偽のゼロが入る。R（この照合では snapshot 本体を読んでいない。workflow は欠けた側を `{count: 0, uniques: 0}` で埋める :110-111 ので、clones 無しで書くとゼロになる点は F）

## 原因

1. 収集リストに掲載対象 10 repo が無い（workflow :27-43）。API は 14 日しか返さないので、収集に入らない日は失われる。
2. 1f9c492 は未実行。
3. 収集に入っても PAT の範囲次第で skip され、green の job の warning にしか残らない（:81-91）。
4. 集計 CLI が uniques と repo 別の値を出さない（`traffic_compare.py:38`、:49-65）。

## Still unknown の確認結果

- **TRAFFIC_PAT が新しい repo に届くか** — 未解決。secret は見られない。既存 9 repo には届く（再現 3）。新 repo は最初の run の `Skip` warning で分かる。著者の gh token では 10 repo とも読めるので、skip が出たら原因は PAT の範囲に絞れる。
- **X1 の「merge 日」の取得元** — 解決済み。personal-branding `docs/scorecard.md:47` の X1 行が「merge 日は PR の `merged_at`（issue は close 日）」と定める（著者了承、2026-10-06。F）。hub 側は日付を受け取るだけで、merge 日を自分で求めない。
- **日次 uniques の 7 日和** — 解決済み。同じ X1 行が「日次 `views.uniques` の 7 日分の和」と定める（著者了承。F）。同じ人の重複計上はこの定義の性質で、hub の CLI はこの和をそのまま出せばよい。API top-level の 14 日 dedup uniques は workflow が保存していない（日別だけを読む :93-100。旧版の :74-79 は誤り）。
- **X1 の判定規則の要点（F、`scorecard.md:47`）** — 判定日 2026-10-30。merge 後 7 日が merge 前 7 日の 2 倍以上かつ 10 以上増えた掲載を「効いた」とする。repo の作成と同時に載せたもの（前 7 日が無いもの）は後 7 日の値だけを別に並べる。データ元は「hub `traffic/data`、欠ける分は traffic-snapshots」。
- **queue の掲載 repo と収集対象の差** — 解決済み（再現 4 の F）。queue 由来で追加の漏れは無い。
- **今日 dispatch する価値** — API の窓は 2026-09-22〜2026-10-05。明日の schedule run を待つと 2026-09-22 の 1 日分が全 16 repo（新 10 + 未実行 6）で失われる。X1 の前 7 日窓（最早の merge が 10-05 以降なら 09-28 以降）には掛からないが、PAT の skip を 1 日早く知れる。

## 判断材料（plan に渡す）

- 収集リストの形: A 配列に追記（先例どおり、人間の push が gate）/ B 別 file から読む（壊れると全 skip で green のまま → 読み込み検査が要る）/ C owner の全 public repo を列挙（gate が消える、非推奨）。収集リストと比較 cohort は設計上分離済み（tests:49-65、`docs/traffic-comparison.md:18-20`）。
- X1 の値: CLI に `uniques` の指標と新系列を足すと、legacy の値・既定出力を変えずに出せる。repo 別の値が要る（X1 は掲載ごとに判定する）。docs の「`views.count` のみ」記述（`docs/traffic-comparison.md:5,60`）も同時に直す対象になる。
- 触る場所の数: repo 名の一覧は 6 か所（再現 5）。dashboard の REPOS（:1221-1231）は「dashboard に載せない」方針（README.md:21）なので、新 repo を足すかどうかは別の判断。
- snapshot は hub に混ぜない。2026-10-03〜05 の harness-scope は API 窓にまだあり、収集を今日始めれば hub 側だけで揃う。
