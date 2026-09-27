# Hub README のリーン化（144 行 → 約 50 行）

## Context

hub repo（shimo4228）の README が「ボリューム過多」で、訪問者に「自分が何をしている人か」「どう役立つか」が端的に伝わらない。当初は personal note 1 行の修正依頼だったが、全体構成の見直しに拡大した。

**診断（決定的事実）**: README の下半分は機械サーフェスの重複だった。
- 機械の reading order は `graph.jsonld → llms.txt → llms-full.txt → README`（README は最後）。
- CLAUDE.md も役割分担を明記: **GitHub README = human navigational canonical / Pages・llms = 機械 canonical**。
- per-line 5 セクション・Supporting Ecosystem 25 行・Data/Writing 6 行は **llms.txt（48 link bullets）+ graph.jsonld（全 concept ノード・全 ecosystem repo・Person・3 papers）が既に網羅**（codex + Plan エージェント両方が確認）。

→ README は今、llms.txt の仕事を肩代わりして肥大化している。**人間ナビゲーションに絞り、網羅 inventory は専用サーフェスへ defer**（LLM が README 単体で復元できる情報フロアは残す）。cross-model 意見は codex（gpt-5.5, read-only）と Plan エージェントから取得済み。

## 著者が確定した選択

- **voice**: codex lean 版（independent researcher-builder / small, inspectable constraints）。※過去に「personal な声を残せ」と codex に指示した履歴があるが、今回 2 案を並べて lean を明示選択。
- **削減強度**: Level 1（大胆 = DEFER）。ecosystem/per-line を README から削除し llms.txt/graph を canonical inventory に。~50 行。CLAUDE.md のルールを同じ diff で微調整。

## Intended outcome

144 行 → **約 50 行**。開いて数十秒で「独立した researcher-builder が 5 本の引用可能な研究ラインを束ねる hub」「through-line は value-layer harness engineering」「自分に必要なラインへ飛べる」が分かる入口。機械フロア（5 lines + 5 concept DOIs + 概念定義 + 著者 identity + 機械サーフェスへのポインタ + 3 paper DOIs）は保持。

---

## 新しい README 構成（EN / JA 両方に適用）

| # | ブロック | 内容 | 現行からの操作 |
|---|---|---|---|
| 1 | lang switcher | `Language: English \| 日本語` | KEEP |
| 2 | `# Tatsuya Shimomoto (@shimo4228)` | H1 | KEEP |
| 3 | badges | DeepWiki + GitMCP | KEEP |
| 4 | blockquote（formal def） | 現行 7 行目をそのまま維持。hub の formal 定義 + through-line 定義（"past tools, permissions, evals → norms, constitutions, values, under one human-gated cycle"）。機械フロア + social preview を担う | KEEP as-is |
| 5 | opening paragraph（human） | lean voice の identity + map 免責（下記ドラフト）。現行 9・11 行を統合し personal list と value-layer bolt-on を除去 | 9+11 を MERGE→書き直し |
| 6 | `## At a Glance` + 5 行テーブル | 5 lines × role × stable concept × concept DOI（機械フロアの核）。直下に 1 文 caption（sibling-not-dependency + value-layer concept ページへのリンクを rescue） | KEEP（caption 追加） |
| 7 | `## Through-line` 1 段落 | value-layer harness engineering を 1 段落で。meditation → 価値層 → 2 lines の因果を統合（bolt-on でなく origin として）。cross-cutting 2 line も 1 節で | 25+27（2 密段落）を 1 段落に COMPRESS |
| 8 | `## Machine reading` | `graph.jsonld → llms.txt → llms-full.txt` + **「網羅 ecosystem inventory（supporting repos / datasets / writing surfaces）はこれらと concept index にある」の 1 文**（DEFER の mitigation ポインタ） | KEEP + ポインタ 1 文追加 |
| 9 | `## Papers` + 3 行テーブル | hub-level membership（3 paper DOIs）。intro を 1 節に圧縮 | KEEP（intro COMPRESS） |
| 10 | `## Citation and Identity` | ORCID / Wikidata / HF + CC0 + cite-by-concept-DOI | KEEP |

**CUT（README から削除、llms.txt/graph に defer）**: per-line 5 セクション（33–69）、Supporting Ecosystem 4 テーブル（81–127）、Data and Writing テーブル（129–138）。人間向けの writing 導線（articles / traffic dashboard）は Machine reading のポインタ文に 1 行で吸収するか、必要なら Citation 直前に 1 行 "Writing and data" として残す（実装時に最終判断、lean 優先）。

### opening paragraph ドラフト（EN、承認対象）

> I'm Tatsuya Shimomoto — an independent researcher-builder working solo, on one Apple Silicon Mac, with no lab and no affiliation. I keep the whole practice under small, inspectable constraints: public repositories, DOI records, and human approval gates. This repo is a map, not the source of truth for live state — each research line has its own repository and Zenodo concept DOI, and the hub keeps their stable relationships and citation pointers in one place.

- codex lean voice（"independent researcher-builder" / "small, inspectable constraints"）を採用しつつ、**durable な authenticity シグナル「solo, one Apple Silicon Mac, no lab, no affiliation」を保持**（著者が一貫して残してきた要素。今回の不満は概念の bolt-on と 4-thread list であって、この concrete fact ではない）。blockquote が 5 lines / 3 domains を既に述べるので opening では重複させない。
- **JA ミラー**: だ/である・発見調（です/ます 不可）。技術語（harness / permission / eval / human-gated cycle / concept DOI）は現行 JA 同様に英語のまま。よりアフォリズム的で主語省略気味に。

### Through-line ドラフト（EN、要点）

> One claim runs through the three agent-design lines (AKC, Contemplative Agent, AAP): **[value-layer harness engineering](https://shimo4228.github.io/shimo4228/concepts/value-layer-harness-engineering.html)**. An agent harness normally holds task regulation — coding conventions, security policy, writing style; this program writes value norms (the contemplative axioms, an authorship judgment stack) into the same layer and governs them with the same human-gated cycle as everything below. The contemplative content of that value layer comes from the author's meditation practice, which also sources two of the five lines; Authorship Strategy is how the whole program is published and cited.

meditation は「where those threads converge」の retrofit でなく、価値層の中身の **origin** として因果的に登場 → チグハグ解消。

---

## CLAUDE.md の同 diff 更新（DEFER に伴う必須）

ecosystem テーブルを README から外すため、以下を同じ diff で修正（後追い PR にしない）:

1. **Design rule 4**「Supporting repos table = membership only …」→ 「ecosystem membership は機械サーフェス（`llms.txt` / `graph.jsonld`）が canonical。README はポインタのみ。ecosystem の増減はそちらで反映」に書き換え。
2. **When *should* this hub be touched** の「An ecosystem repo is added or retired」→ 反映先を README 行でなく `llms.txt` + `graph.jsonld`（EcosystemRepo ノード）に変更。
3. **Language pair** 節の「same sections, same number of DOI mentions, same ecosystem table rows」→「…, same Papers rows」に変更（ecosystem テーブルが README から消えるため）。DOI parity クイックチェックは不変（下記 Verification で 8 = 8 を確認）。

**llms.txt / graph.jsonld / index.html / concept ページ / vocab.html は変更不要**（削除内容を既に保持。DEFER は情報を移動せず、README から参照に切り替えるだけ）。

## DOI parity への影響

README の DOI 言及は 10 → **8**（At a Glance の 5 line + Papers の 3）。doctrine-corpus（20337008）と existence-proof（20558800）の 2 concept DOI は README から外れるが llms.txt/graph に残存。EN/JA 両方 8 になるので parity（8 = 8）は保持。

---

## 実装 chain（種別: docs — hub rewrite + rule 変更）

- **実装**: `readme-writer` skill を vehicle にする（canonical README ツール + structural lint 内蔵）。EN を書き、JA を構造ミラー。CLAUDE.md 3 点を同 diff で修正。
- **Doc review**: readme-writer lint（EN/JA 両方）+ `context-sync`（README ↔ CLAUDE.md の役割整合を確認、ecosystem 記述の drift 検出）。コード変更なしのため python/security/codex review は不発火（codex の設計意見は取得済み）。
- **Verify**: 下記。
- ユーザー介入点: この Plan 承認 → Verify 結果確認 の 2 点。

## Verification

1. **DOI parity（CLAUDE.md 規約）**: `diff <(grep -c "doi.org/10.5281" README.md) <(grep -c "doi.org/10.5281" README.ja.md)` → 差分なし（8 = 8）。
2. **構造ミラー**: 両 README の見出し・行構成が一致し、machine floor 5 要素（5 lines+DOI / 概念定義 / through-line / 著者 identity / 機械サーフェス pointer / 3 paper DOI）が揃うことを目視。
3. **defer 先の存在確認**: cut した各項目が llms.txt / graph.jsonld に実在することを再 grep（cut 前に確認、切っても情報が消えていないことを保証）。
4. **CLAUDE.md 整合**: rule 4 / when-to-touch / language-pair 節が README の新実態と一致しているか確認（context-sync）。
5. **視覚確認**: GitHub 上での見え方相当を目視（~50 行、開いて数十秒で who/what/how が分かるか）。
6. **`git status` / `git diff`**: 変更が README.md / README.ja.md / CLAUDE.md の 3 ファイルに限定されていることを確認。
