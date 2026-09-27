# shimo: 語彙ページの成熟化(定義充実・機械可読層・棚卸し)

## Context

`vocab.html`(https://shimo4228.github.io/shimo4228/vocab の実体)は `shimo:` 名前空間の dereference 先として公開済みだが、65 用語中 **52 用語が定型プレースホルダー**のまま。`<head>` の JSON-LD は定義なしの用語インデックスに留まり、`vocab.jsonld` は存在しない。さらに調査で以下が判明した:

- **derivedFrom / derivesFrom**: AAP 内で意図的な使い分けあり(`derivesFrom` = DOI/repo への正式アーティファクト系譜、`derivedFrom` = ADR の素材となった外部 essay)。表記ゆれではない → 差が分かる定義を両方に書く
- **inverseOf(AKC)/ invertsTo(authorship)**: 両方とも @context 宣言のみで**本文使用ゼロの死語彙** → 退役候補
- **covaresWith キータイポ**(authorship-strategy/graph.jsonld: @context 26行目 + 本文 193/208/224 行。IRI は正しく `shimo:covariesWith`)
- **未収載語彙 約21件**: doctrine-corpus(Shape, Observation, harvestedFrom, characterizesPairs, groupedAs, operationalizes, counteredBy, observedBy, shapeOrdinal)/ contemplative-agent-data(RetrievalView, DistillCommand, Artifact, SnapshotTaxonomy, lensOver, produces, producedBy, threshold, topK, snapshotKind)/ existence-proof(WorkingDoctrine, Tactic, isComplementOf, provenByAnchor, epistemicStatus, namingStatus, lineStatus)が vocab.html に無い
- 宣言のみ未使用の @context エントリ: akc `inverseOf`、auth `invertsTo` / `derivedFrom` / `citedBy`
- HTML 内 JSON-LD インデックスは 62 エントリ vs 表は 65 行 — 3 件の欠落を実行時に特定する

## ユーザー決定事項(確認済み)

1. 未収載語彙は**このパスで vocab.html に追加**(定義対象 52 → 約73 用語)
2. 他 repo の修正候補は **diff まで用意**(ローカル適用・未コミット・承認ゲートで提示)
3. 機械可読層は **vocab.jsonld を正本**とし、HTML 内 ld+json へ**同期スクリプトでミラー**(sync_graph_jsonld_mirror.py と同型)

## 制約(タスク指示より・必須)

- 既存 IRI は一文字も変更しない(リネーム望ましい場合も提案止まり)
- RDFS + schema:domainIncludes / rangeIncludes までの軽量オントロジー。OWL 公理化しない
- 定義文は既存文体(英語・一〜二文・簡潔)
- **git commit / push しない**。diff と判断一覧を提示して承認待ち(Human Approval Gate)

## 実装ステップ

### Phase 1: 定義の帰納(~73 用語)

エビデンスは収集済み(調査レポート: 全グラフの per-term 使用表 — 主語型 → 目的語型、件数、代表トリプル)。

1. 各プレースホルダー用語+新規追加用語について、使用実態から帰納した一〜二文の英語定義をドラフト。主語→目的語の型パターン併記(例: `alignsWith: ADR → ADR | Axiom`)。単一使用箇所の用語は "single-use" と明記
2. 優先順: 意味論的に重い用語から — alignsWith, gatedBy, supersedes, supersededBy, withdrawnBy, partiallySupersededBy(CA ADR ライフサイクル群)、strongerThan, enforcementLocus(AAP 禁止強度)、vocabularyDisjoint(homonym 分離・双方向)、derivedFrom / derivesFrom(差分明示)
3. 定義は使用実態の要約に徹する(新しい意味の発明をしない)。根拠となる file:line を成果物一覧表に記録
4. vocab.html の表セルを更新 + 未収載 約21 用語の行を該当セクション(Classes / Object properties / Datatype properties)にアルファベット順で追加。"Used by" 列に doctrine-corpus / contemplative-agent-data / existence-proof への graph.jsonld リンクを追加(ページの既存リンク形式に合わせる)

### Phase 2: 機械可読層

1. 現状確認(記録用): `curl -sI -H "Accept: application/ld+json" https://shimo4228.github.io/shimo4228/vocab` で conneg 不可を確認(GitHub Pages の既知制約の実証)
2. **`vocab.jsonld` 新規作成(正本)**:
   - @context: rdfs / rdf / schema / shimo プレフィックス
   - 各用語ノード: `@id` = 既存 IRI と完全一致(`https://shimo4228.github.io/shimo4228/vocab#Term`)、`@type` = `rdfs:Class` or `rdf:Property`、`rdfs:label`(en / ja)、`rdfs:comment`(Phase 1 定義)、`schema:domainIncludes` / `schema:rangeIncludes`、`rdfs:isDefinedBy`
   - `DefinedTermSet` メタデータノード(creator = ORCID 等、既存 HTML 内ブロックから引き継ぎ)
   - 15 の hub-level concept インスタンス(`#concept/…`)も `DefinedTerm` として収録(description 付き — 現在 HTML 表のみに存在する情報の機械可読化)
3. **`scripts/sync_vocab_jsonld_mirror.py` 新規作成**: vocab.jsonld を読み、vocab.html 内の `<script type="application/ld+json">` ブロックを置換(sync_graph_jsonld_mirror.py のパターンを踏襲)。実行して HTML 内ブロックを定義付き完全版に更新
4. vocab.html `<head>` に `<link rel="alternate" type="application/ld+json" href="vocab.jsonld">` を追加
5. 配置方式は選択肢 **c(埋め込み + 隣接ファイル)を採用**。根拠: 埋め込みは HTML クローラー(schema.org 系)向け、隣接ファイルは `Accept` 不問の直接 fetch(LLM ツール・rdflib 等)向けで、届く読者集団が異なる。drift はスクリプト同期で構造的に排除
6. **Doc Sync(同一 diff 内)**: ハブ CLAUDE.md の "Files in scope" に vocab.jsonld と同期スクリプトの運用規約(vocab.jsonld が正本、編集後にスクリプト実行)を追記

### Phase 3: 棚卸しレポート + 他 repo diff

1. **判定確定(エビデンス収集済み)**:
   - derivedFrom / derivesFrom → **意図的区別**(AAP)。両定義に差を明記。auth の宣言のみ `derivedFrom` は未使用宣言として削除 diff 対象
   - inverseOf / invertsTo → **死語彙**(両方とも使用ゼロ)。退役を提案: akc / auth の @context エントリ削除 diff + vocab.html の 2 行削除を提案(承認ゲートで判断)
2. **他 repo への未コミット diff 適用**(提示用):
   - `authorship-strategy/graph.jsonld`: `covaresWith` キー → `covariesWith`(4 箇所。IRI 不変)、未使用宣言 `invertsTo` / `derivedFrom` / `citedBy` の削除
   - `agent-knowledge-cycle/graph.jsonld`: 未使用宣言 `inverseOf` の削除
   - 各 repo の HF ミラー・dashboard ミラー等への波及は**実施せず**チェックリストに記載(commit 後の作業のため)
3. **使用ゼロ語彙の全数確認**: vocab.html 全 65 行 × 全グラフ使用実績のクロス表を機械生成(scratchpad の小スクリプト)。inverseOf / invertsTo 以外の退役候補が無いか確定。HTML 内 JSON-LD インデックス 62 vs 表 65 の欠落 3 件も特定し修正(vocab.jsonld 生成で自然解消)

## 変更ファイル

| ファイル | 変更 |
|---|---|
| `vocab.html` | 52 定義置換 + 約21 行追加 + `<link rel="alternate">` + ld+json ブロック(スクリプト再生成) |
| `vocab.jsonld` | 新規(正本) |
| `scripts/sync_vocab_jsonld_mirror.py` | 新規(既存 `scripts/sync_graph_jsonld_mirror.py` のパターン踏襲) |
| `CLAUDE.md`(ハブ) | Files in scope に vocab.jsonld 運用規約を追記 |
| `../authorship-strategy/graph.jsonld` | covariesWith キー修正 + 未使用宣言 3 件削除(diff 提示のみ) |
| `../agent-knowledge-cycle/graph.jsonld` | 未使用宣言 inverseOf 削除(diff 提示のみ) |

## 成果物(承認ゲートで提示)

1. **定義ドラフト一覧表**: 用語 / 現状(placeholder or 新規) / 提案定義 / 型パターン / 根拠 file:line / single-use フラグ
2. **vocab.jsonld** + 配置方式 3 案の比較と採用根拠(c 案)
3. **棚卸しレポート**: 表記ゆれ判定(derivedFrom 系 = 意図的、inverseOf 系 = 死語彙)、covaresWith タイポ、退役候補、未収載→追加した用語一覧
4. **残作業チェックリスト**: commit(hub + 他 2 repo)、`sync_graph_jsonld_mirror.py` 再実行要否の確認、HF dataset ミラー再同期(/hf-sync)、公開後の `curl` での vocab.jsonld 到達確認、検索コンソール再送の要否

## 検証(commit なし)

1. `python -c "import json; json.load(open('vocab.jsonld'))"` — パース確認
2. scratchpad スクリプトで三方向クロスチェック: vocab.jsonld の全 @id ⇄ vocab.html アンカー ⇄ 全グラフ使用実績(IRI 完全一致・欠落ゼロ・既存 IRI 不変)
3. `python scripts/sync_vocab_jsonld_mirror.py` 実行 → idempotent 確認(再実行で diff ゼロ)
4. 修正後の `authorship-strategy/graph.jsonld` / `agent-knowledge-cycle/graph.jsonld` の JSON パース確認
5. `git status` / `git diff` を全 3 repo で提示 → **Human Approval Gate で停止**(commit しない)
