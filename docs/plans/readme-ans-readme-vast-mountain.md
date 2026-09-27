# README 書き換え計画 — オーセンシティを軸に（ANS の研究者フレーミング除去を含む）

## Context

著者指摘（2026-08-21）: README で「計算論的現象学」が著者の研究主題のように前面に出ている。
実態は **Attention, Not Self (ANS) がアビダルマを計算論的現象学と接続している**だけで、
著者がその分野を研究しているわけではない。この drift はオーセンシティ（著者の戦略的価値、
`practitioner-identity.md`: 研究者ではない Practitioner、DOI は手段）を毀損する。

照合結果（read-only）:

- **ANS line repo の自己記述**（正本）: 「仏教アビダルマと計算論的現象学の接点を探る**個人的な探究プロジェクト**」。エッセイ 9 本 + 対照表 + 知識グラフ
- **hub README.md**
  - L9 blockquote: 著者の主題を `AI agent design, AI-mediated authorship, and computational phenomenology` の 3 本柱として並列 → **CP を著者の主題に格上げしている**（最大の問題）
  - L25 ANS 行: role `How the mind works (Buddhism × cognitive science)`、concept `… read against computational phenomenology, the computational modeling of experience`
  - 「program」語が 3 箇所（L33 `This program`、L46 / L60 `the whole program`）— research program の響き
- **README.ja.md**: L9 `計算論的現象学（体験を計算のモデルで捉える研究）`、L23 `…と突き合わせる研究`。「研究」と明記している
- hub の他面（`llms.txt` L66 / `graph.jsonld` L194）は「personal essay collection」と正しく書いており、README だけが drift。`index.html` L71 は中立的な一句で今回の対象外

CLAUDE.md の hub 規則は維持: 揮発状態なし / concept DOI のみ / README 2 言語の構造同期 / claude-harness の例外的扱い / Papers 節を再追加しない / 絵文字なし。

## 方針（オーセンシティ軸）

1. **ANS は「私の瞑想から出たエッセイ集」として置く。** 計算論的現象学は ANS 行の中で、
   アビダルマを突き合わせる**相手**として 1 回だけ・従属的に出す（ANS repo の自己記述に忠実）。
   冒頭 blockquote からは消す
2. **著者の主題を「エージェント設計 / AI 時代の著者性 / 心の働き（瞑想実践から）」**に据え直す。
   既存の図（`M["My meditation practice"] --> ANS`）は既に正しい構図なので、本文をそこへ揃える
3. **研究者語彙を実践者語彙へ**: `program` → `this work` / `the five lines`、`研究` → `探究`・`エッセイ`、
   `research` は使わない。「claim」は concept page 名と連動しているので残す
4. **何であるかを言い、何でないかは最小限に**（既成カテゴリへの回収を避ける rule）。
   「ラボも所属もなく一人で作っている」「DOI は肩書きではなく道具」は既にあるので保持・強化
5. 失敗・状態のサニタイズをしない（user-style rule）。新規の飾り語・絵文字は入れない

## 構成（Step 1 = 著者確認事項。節見出しは現行を維持し、中身を書き換える）

| 節 | 答える読者の問い | 変更 |
|---|---|---|
| blockquote + lead | 誰が何をまとめた repo か | 3 本柱から CP を除去。「AI エージェント設計・AI 時代の著者性・瞑想実践から見た心の働き」 |
| At a Glance | 5 本それぞれが何か | ANS 行を書き換え: role「瞑想実践から出たエッセイ」、concept「自分の瞑想の記録を、古典仏教の心の分析（アビダルマ）で読み、現代の計算モデル（計算論的現象学）と突き合わせた個人のエッセイ集と知識グラフ」相当。他 4 行は据え置き |
| Through-line | 3 本を貫く主張 | `program` → 実践者語彙。内容は不変 |
| mermaid + 一文要約 | 全体の関係 | `publishes the whole program` → `publishes all five lines` 相当。JA は現状ほぼ適切 |
| Writing and data / Machine reading / Citation | 導線 | 据え置き（Citation の「probe dataset」説明は保持） |

造語予算: 現行と同じ（value-layer harness engineering / contemplative axioms / Constitution / ADR /
concept DOI / harness）。新規造語なし。

## 実行手順（skill: `readme-writer` の改稿ループ）

1. EN 本文を本体が直接書く（サブエージェントに委譲しない）
2. `uv run --quiet --directory ~/.claude/skills/readme-writer python -m scripts.readme_evidence README.md`
   → `readme-judge`（fresh context）。Fix は span 単位で 1 回再判定、上限 2 ラウンド
3. panel 並列: `readme-reviewer` + `readme-clarity-reviewer`（verdict 級の不一致だけ著者へ）
4. JA 版を同じフロア・同じ見出し・ですます調で書き、clarity-reviewer の cross-language 軸 + judge を 1 回
5. fact 照合（read-only）: `llms.txt` / `llms-full.txt` / `graph.jsonld` の ANS 記述と矛盾しないこと
6. 著者通読 GO → commit（git は 1 call 1 コマンド、`git -C`）

## 変更ファイル

- `README.md`
- `README.ja.md`

他面（`llms.txt` / `graph.jsonld` / `index.html`）は今回触らない。必要なら別件。

## Verification

```bash
# 2 言語の DOI 言及数パリティ（CLAUDE.md）
diff <(grep -c "doi.org/10.5281" README.md) <(grep -c "doi.org/10.5281" README.ja.md)
# 研究者フレーミングの残存チェック
grep -n -i "research\|program\b" README.md; grep -n "研究" README.ja.md
# 見出し構造の同期
diff <(grep '^#' README.md) <(grep '^#' README.ja.md | sed 's/.*//')  # 件数比較
# 証拠スクリプト
uv run --quiet --directory ~/.claude/skills/readme-writer python -m scripts.readme_evidence README.md --text
```
