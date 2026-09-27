# gemini temperature 廃止予告への contingency 記録

## Context

2026-07-26 の retrieval run で、gemini の全 call に新しい警告が出るようになった:

> DeprecationWarning: `temperature`, `top_p`, and `top_k` continue to function for
> Gemini 3+ (gemini-3.5-flash) but are planned for removal in a future release.
> Move sampling guidance into the `system` instructions instead.

同じ「reasoning tier がサンプリング指定を拒否する」流れで、panel の 5 provider 中 2 つは
既に温度指定を落としている (`param_overrides` の `anthropic: temperature: null` /
`openai: temperature: null`、いずれも **hard reject を観測してから**追加した)。gemini は
まだ機能しているので、今動かすと**外部強制がないまま観測系列に sampling variance を持ち込む**
ことになる。よって今回は切り替えではなく、**発火条件つきの対応方針を instrument 側に記録する**
だけにする (著者判断 2026-07-26: config コメントのみ、既発行の empirical note は触らない)。

`probes/config/` は CC0 で公開されている instrument 正本なので、ここに日付つきで書けば
cadence の pre-registration と同格の事前記録として機能する。

## 変更するファイル

`~/MyAI_Lab/shimo4228/probes/config/probes-v6.yaml` — **コメントのみ**。1 ファイル、意味的変更ゼロ。

`param_overrides` ブロック (現 L86–103) の `gemini:` エントリに、既存の anthropic / openai
コメントと同じ体裁 (観測日 + provider の文言 + 判断) で以下を追記する:

1. **観測**: 2026-07-26 retrieval run で gemini 3+ の temperature/top_p/top_k 廃止予告を観測。
   現時点では機能しており reject はされていない。
2. **発火条件**: gemini が temperature を **hard reject** した時点 (openai / anthropic と同じ
   400-class エラー) で `probes-v7.yaml` を切り、`gemini: temperature: null` を入れる
   series break とする。予告段階では動かさない — 強制されていない sampling 変更は
   系列内変動を増やすだけで、観測量を改善しない。
3. **却下した代替**: 廃止予告が推奨する「sampling guidance を `system` instructions に移す」は
   **採らない**。probe は bare user prompt を刺激として固定しており、system message の追加は
   刺激そのものの変更 = 全 provider・全期間の比較可能性を壊す。温度を落として provider default
   に委ねる方が、既に anthropic / openai がそうなっている以上、系列として一貫する。
4. **静かな失効への注意**: 将来 gemini が reject せず **無視**するようになった場合、レコードの
   `temperature` フィールドは「要求した値」を記録するだけ (`runner/probe_runner.py:256` の
   コメントどおり) なので、実際の sampling とレコードが乖離しうる。予告文言が
   「removed」に変わったら reject を待たずに v7 を切る。

## やらないこと

- `temperature: null` の即時投入 (= v7 series break)。今回は準備のみで、発火は hard reject 時。
- DeprecationWarning の抑止。ログは冗長になるが、これが失効を検知する唯一の早期シグナルなので残す。
- `runner/` のコード変更。`build_call_kwargs` の override 機構 (`runner/providers.py:51-55`、
  `None` で param を除去) が既に v7 で必要な全機能を持っている。新規実装は不要。
- 既発行の `docs/empirical/probe-baseline-2026-06.md` への追記 (著者判断で scope 外)。

## Verification

1. `python3 -c "import yaml; yaml.safe_load(open('config/probes-v6.yaml'))"` — YAML パース通過。
2. `git diff` が **コメント行の追加のみ**であることを確認 (`param_overrides` の実効値が
   変わっていない = 既存 v6 レコードとの互換が保たれる)。
3. 実 call による確認は不要 (意味的変更なし)。次回 retrieval run は 2026-08-09 (ISO 週 32、偶数週)。

## Commit

hub repo (`~/MyAI_Lab/shimo4228`) は launchd が probes/traffic を自動コミットしているので、
`probes/config/probes-v6.yaml` のみを pathspec 指定で stage する。

```
docs(probes): record gemini temperature deprecation contingency
```

main 直コミット + push (probes 系の既存運用に合わせる)。
