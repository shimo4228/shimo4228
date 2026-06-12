# LLM Probe Data

[@shimo4228](https://github.com/shimo4228) の研究エコシステムのアイデアと識別子が
frontier LLM の回答に現れるか——そして**著者が一緒に現れるか**——を定期測定する
two-channel probe のログ。

これは [authorship-strategy ADR-0008](https://github.com/shimo4228/authorship-strategy/blob/main/docs/adr/0008-rag-era-attribution-diffusion.ja.md)
が要請した測定器にあたる: attribution diffusion は時定数の異なる 2 チャネルで動き、
チャネルごとに別の probe が要る。プロトコルは同 repo の ADR-0011 に記録される。

## 2 チャネル、2 種類の probe

| Channel | Probe | Web 検索 | 問い | 測定する failure mode |
|---|---|---|---|---|
| **Parametric** | retrieval-suppressed naming probe | OFF | 「概念 X とは何か？誰が維持しているか？」 | 概念が訓練済み知識に無い、または概念はあるが著者が出ない |
| **Retrieval** | search-grounded citation probe | ON | 「トピック Y の出典を URL と著者名つきで」 | **ghost citation** — 自分の URL/DOI は引用されるが著者名が一度も出ない |

2 チャネルは決して単一スコアに混合しない。混合指標はどちらのチャネルが
失敗しているかを隠す (ADR-0008)。

## 1 レコードの中身

`data/parametric.jsonl` / `data/retrieval.jsonl` に 1 行 1 JSON
(run × provider × probe ごと)。主要フィールド:

- `response_text` — モデル回答の raw 全文。lexicon 改訂時に検出を再実行できるよう
  verbatim 保持 (`detect.detector_version` がどの lexicon の判定かを示す)
- `cited_urls` + `citation_source` — provider の citation/grounding metadata 由来なら
  `provider_metadata`、本文からの regex 抽出なら `text_regex` (弱い provenance である
  ことをデータ上に明示)
- `detect.author_named` / `detect.project_named` / `detect.doi_or_url_cited`
  — 独立 boolean。`detect.ghost_citation` は導出値 (`cited && !author_named`)
- `model_requested` vs `model_returned` — silent な snapshot drift を可視化
- `probe_set_version` + `prompt_sha256` — prompt set の変更は常に可視な series break

検出は決定論的な文字列/regex 照合 (監査可能)。LLM judge は使わない。
`author_named` は **prose 中で名指しされた**ことを意味する: 引用 URL の中にだけ
handle が見えるのはまさに ghost citation のシナリオなのでカウントしない。

## 読み方の注意

- **自己汚染**: このログは公開され、造語と著者名を含む。将来の訓練がこれを
  取り込みうるため、測定器が測定対象チャネルに燃料を供給する。これは測定交絡で
  あると同時に thesis に沿った diffusion 行為でもある——隠さず明記する。
- **誘導質問**: 概念認識 prompt は概念の実在を前提とし、モデルは迎合的に
  confabulate する。negative-control probe (もっともらしい架空概念) がその
  noise floor を定量化する。true-positive はそれと対照して読む。
- **N=1**: 一人の著者・少数 probe・5 provider。preliminary observation であって
  evidence ではない。

## 実行

```bash
cd runner
uv sync
uv run pytest                 # 検出器テスト、API 呼び出しゼロ
uv run probe_runner.py --dry-run
cp ../.env.example ../.env    # API キーを記入 (git-ignored)
uv run probe_runner.py --provider anthropic --probe parametric-concept-akc  # smoke
uv run probe_runner.py --channel retrieval            # 週次 retrieval run
uv run probe_runner.py --channel parametric --repeat 3  # モデル参入 event run
uv run probe_runner.py --currency-check               # 月次の変化検出
```

コストガード: 1 run が `--cost-ceiling` (default $2) を超えたら中断する。

## Scheduling

プロトタイプ期は手動。クリーンな手動 run が 2 回成立した後に自動化を追加する。
2 チャネルの schedule は異なる:

- **Retrieval — 週次 calendar cadence.** citation pool の entry / decay は
  モデルが凍結されていても日単位で動く。
- **Parametric — event 駆動.** 凍結モデルの weights は run 間で変化しないので、
  同一モデルへの再 probe は応答分散しか測らない; parametric の信号は
  **モデル世代間**にしか住まない。full parametric set はモデルの panel 参入時
  または変化検出時に `--repeat 3` (within-model 分散用) で走る。
- **Currency check — 月次 calendar cadence** (`--currency-check`)。
  event 駆動設計を成立させる変化検出器:
  1. *silent-swap 検出* — provider ごとに最小 1 call、served model identity
     (`model_returned`) を前回観測と比較 (`gpt-5.5` のような非日付 alias は
     裏で silent に差し替えられうる);
  2. *catalog diff* — 各社の model 一覧 API を `data/model-catalog.jsonl` に
     snapshot して diff、chat 系の新 ID を報告 (検出は自動、panel への採用は
     人間の判断 — どれが広く served される default tier かは API に存在しない
     製品側の事実);
  3. *staleness guard* — config の `verified_current` が `staleness_days`
     (default 90) より古いと flag し、default tier 選定の定期的な人間再検証を
     強制する。

  `--strict` を付けると変化 event 検出時に非ゼロ exit する (定期実行用)。

分析規約: 時系列は `model_returned` で分割する。モデル変更は汚染ではなく
期待されるイベントであり、世代間比較こそが parametric channel の主信号である。

## License

CC0 1.0 ([`../traffic/`](../traffic/) と同じ)。モデル出力は各 provider の
規約に従う。
