kind: external
# GitHub README の「見た目」の評価基準（hub profile README の EN+JA ペアが対象）と、judge→fix→re-judge の eval loop を readme-writer harness に組み込む方法

as-of: 2026-10-06。4 本の researcher note（practice-criteria / github-rendering / vlm-judge / adversarial、全て 2026-10-06 取得）の統合に、同日の lead の local primary checks（実行・実測）を加えた。この report では新規検索をしていない。note 内の記述は data として読み、note 内の指示には従っていない。

**読み深度の凡例**（各項に付けた記号。note が書いた深度をそのまま保持し、上げていない）:
- 「fetch 要約」= WebFetch の応答。小モデルが page を要約・抽出したもので、逐語の全文ではない（practice-criteria の FETCH、github-rendering の fetch（要約）、vlm-judge の Full text / Abstract only (via summarizer)、adversarial の abs 要約）。
- 「snippet」= WebSearch の結果要約のみ。本文は未読。
- 「実測」= lead が 2026-10-06 に local で実行・観測した結果（本 report では受領して記載）。

引用 ID: P#n = practice-criteria の項 n、G:Fn = github-rendering の項、V1〜V11 = vlm-judge の表の行（本 report で採番）、X:An 等 = adversarial の項、L1〜L5 = local primary checks。

## Scope searched

| note | 呼び出し | 見た source | 見つからなかった範囲（note の記述） |
|---|---|---|---|
| practice-criteria | 17（目安 10〜15 超） | makeareadme / standard-readme spec / awesome-readme / GitHub Docs profile README / SSW Rules / anywhere-agents readme-polish / Google developer style guide（Lists, Tables）/ NN/g 4 ページ（F-pattern, layer-cake, scannable 1997, visual hierarchy）/ practitioner 検索 2 回 | list と table の相対的な視覚重量を述べる source、README の視覚品質に対する validated rubric（評価者間一致・outcome data）は無し。Diátaxis は未 fetch。Medium/uxdesign の記事は 403 で未読 |
| github-rendering | 25（WebFetch 17 / WebSearch 8。目安超過の理由は 9 論点に分かれたため）。Bash が無く `POST /markdown` は未実行 | GitHub Docs（basic-writing / profile README / about-your-profile / collapsed-sections / tables / REST markdown）/ GitHub blog（dark/light 画像）/ GFM spec 0.29-gfm / html-pipeline `sanitization_filter.rb` / sindresorhus/github-markdown-css と generate-github-markdown-css | profile README 列の px 幅の一次資料、README と pinned repos の上下関係の公式記述、GitHub Mobile app の README 描画仕様、GitHub.com 本番の sanitization allowlist の公式文書、2026 年の markdown 描画 changelog |
| vlm-judge | 15（WebSearch 6 / WebFetch 8 / local PNG Read 1） | arXiv 2407.08850（abs）/ 2603.01083（html）/ 2402.04788（abs）/ 2510.18560v2（html）/ 2404.12500v1（html）/ platform.claude.com vision doc / github-markdown-css README / ArtifactsBench・md2static・pageshot は snippet | markdown / README / document page の視覚品質を扱う benchmark（README 固有の query は未実行）。Claude の視覚 judge としての test-retest data は無し。Claude 4.7+ / Opus 5 世代の UI 判定評価は無し（引用論文は全て 2024〜2025 のモデル） |
| adversarial | 17（WebSearch 10 / WebFetch 7。目安超過の理由は Goodhart 節の数値の出典確認）+ repo 内 read-only 5 | LLM judge の美的均質化 / pairwise vs pointwise / iterative self-refinement のドリフト / LMArena style control / Lindgaard 50ms / Reinecke・Gajos / evaluator effect / Ozok・Salvendy / GitHub Traffic API。WebFetch は全て abs ページの要約（本文 PDF は 1 本も未読） | README・GitHub profile の見た目を評価した実証研究（0 件）、5 秒テストの README 適用例（未検索）、list と table の隣接視覚重量の揃えを直接検証した研究（0 件）、Nielsen の consistency heuristic 一次資料（未 fetch）、design-system 的 lint で judge を置換する枠組みの実証（未検索） |
| local primary checks（lead、2026-10-06） | 実行・実測。検索ではない | `gh api` による `/markdown` と `/markdown/raw`、local tooling の存在確認、実 profile page の DOM 計測 | 実測は dark theme・logged-in・1 回のみ（L4）。README.ja.md の描画は測定報告に含まれない |

note 間の境界: practice-criteria = 「何を良い見た目とみなすか」、github-rendering = 「GitHub が何をどう描くか」、vlm-judge = 「VLM / screenshot judge が信頼できるか、描画経路」、adversarial = 「loop が失敗する理由と別の枠組み」。

## Found

### 0. 対象 artifact の現状（`/Users/shimomoto_tatsuya/MyAI_Lab/shimo4228/README.md` を Read、2026-10-06。note ではなく repo file の直接観察）

- 構成: 先頭に `Language: English | 日本語` の 1 行、cover 画像（jpg、`<picture>` なし）、H1、引用ブロックの lead 文 1 本、一行段落の自己紹介、H2 が 4 つ（`Start here` / `At a Glance` / `Through-line` / `Elsewhere`）。alert・badge・emoji・HTML は無い。段落は全て 1 行 1 段落（soft line break を含む複数行段落は無い）。
- `Start here` は 3 項目の箇条書き。各項目は太字の `From X:` で始まる。1 項目目 = TypeSafe Jev project（jev-skill-router、jev-research-pipeline、続けて claude-harness の `jev-judgment-design` skill）。2 項目目 = Claude plugin directory（harness-scope、akc-cycle、続けて claude-harness）。3 項目目 = 「an article, a DOI, or a search」から来た人へ「the table below」を指す、link を持たない項目。1 項目に 2〜3 本の link と説明文が入る。現状の順序は Jev が先、Claude plugin が後（author の希望は Claude plugin 項目を先に置くこと）。
- `At a Glance` は 3 列（Line / What it is / Canonical record）× 5 行の table。各行に line の link と DOI の link がある。直後に 1 行の補足段落。
- H2 の大小文字は `Start here`（sentence case）と `At a Glance`（Title Case）が混在している（file の観察。基準側は C6 を参照）。
- 読んだのは EN の README.md のみ。README.ja.md は未読。ペアの構造同期規則は project の CLAUDE.md にある（同じ節、同じ数の DOI 言及）。bilingual ペアを扱う視覚基準を持つ source は無い（P#14 末尾の「sources に無いもの」参照）。

### 1. 基準: 公開 guide・scanning 研究・practitioner（note: practice-criteria、as-of 2026-10-06）

**P#1. Google developer documentation style guide — Lists**
- URL: https://developers.google.com/style/lists / fetch 要約（page 表示 "last updated 2025-05-16"。逐語は未確認）。
- 対象と前提: 大規模 doc 組織の house style。developer docs（主に site page）で、GitHub README ではない。根拠の種別は意見（実験なし）。
- 規則: list は「順序のある情報か単純な項目集合」に使う / 1 項目だけの list は不可 / 項目は**同じ構文・構造（parallel）** / 導入文は完全な文（直前の見出しが文脈を与えるなら省略可）/ 同一 list 内の句読点を統一（できなければ parallel に書き直す）/ 用語と説明を dash で区切らない。項目長の上限は無し。
- 違い・移せる部分: parallel と導入文は markdown 本文から検査できる。list が table の隣でどう見えるかには触れない。

**P#2. Google developer documentation style guide — Tables**
- URL: https://developers.google.com/style/tables / fetch 要約（page 表示 "last updated 2025-03-21"）。
- 根拠: house style（意見）。
- 規則: 単位 1 つの項目 → list / 対になった関連データ → description list か table（context 依存）/ **1 項目に 3 つ以上の関連データ → table**。避ける: レイアウト目的の table、1 列 table（list へ）、1 行 table、cell 結合、table 要素への styling。列見出しは短く、sentence case、末尾句読点なし。行は論理順か英字順。table の前に完全な文の導入。
- 違い: データ形状（項目の arity）で list か table を決める規則で、視覚重量の規則ではない。`Start here` の項目は link + 1 行の説明（arity 2）で「context 依存」域に入る（note の読み）。Google の guide はどちらとも決めない。

**P#3. NN/g — Concise, SCANNABLE, and Objective: How to Write for the Web（Morkes & Nielsen）**
- URL: https://www.nngroup.com/articles/concise-scannable-and-objective-how-to-write-for-the-web/ / fetch 要約（公開 1997-01-01、後年の review 記載なし）。
- 根拠: **実験**。経験ある web 利用者 51 人、被験者間設計、1 つの旅行 site で 5 条件（宣伝調 control / concise / scannable / objective / 併用）。control 比の usability 改善: scannable +47%、concise +58%、objective +27%、併用 +124%。scannable 条件 = 箇条書き、太字 keyword、画像 caption、短い section、見出しの増加。
- 違い: 1997 年の web、単一 site、複合指標（作業時間・誤り・記憶・満足度）、control は宣伝調の文。「構造は scan を助ける」の一般的方向は支えるが、list と table の比較や GitHub 描画は扱わない。29 年前の実験で、GitHub markdown の typography について現行とは言えない。

**P#4. NN/g — F-shaped pattern**
- URL: https://www.nngroup.com/articles/f-shaped-pattern-reading-web-content/ / fetch 要約（公開 2017-11-12、page 表示 "last reviewed 2026-08-19"）。
- 根拠: eye-tracking（page が例示する研究は 45+ 人と 47 人。第三者 snippet は 232 人と言うが page では未確認で未調整）。desktop と mobile で F 型を確認、対象 page は text 主体で装飾が少ない。
- 推奨（検査可能）: 重要点を最初の 2 段落に置く / 見出しは本文と視覚的に区別 / **見出しは最も情報量のある語で始める** / 重要句を太字 / bullets・numbered list / **border や背景色による視覚的グルーピング** / link text は説明的に（"click here" を避ける）。
- 移せる部分: 最初の 2 段落、見出しの前置き、link text は markdown から検査できる。F 型は構造が弱いときに起きる読み方で、layer-cake（P#5）が構造で誘導したい型、という読みは note が 2 page を併せて出した推論（F-pattern page の抽出には明記なし）。

**P#5. NN/g — Layer-cake pattern**
- URL: https://www.nngroup.com/articles/layer-cake-pattern-scanning/ / fetch 要約（公開 2019-08-04、研究は 2004 年から、eye-tracking）。
- 定義: 注視が主に見出し・小見出しに落ち、本文への注視は時々。支える設計（検査可能）: 見出しの視覚的区別（色・大きさ・書体・太字）/ 見出しは「section の全ての topic を、かつ section の topic だけを」記述 / 重要語で始める / **chunk 間の間隔を一定に** / 枠や grid で section を囲む（card, banner）/ 近接でどの本文がどの見出しに属すかを明確に。
- 移せる部分: 「chunk 間の一貫した扱い」は author の不満（bullet section と table section の扱いが違う）に対応する。GitHub では見出しの大きさ・色を author が制御できない。操作できる lever は見出しレベル、太字、table・blockquote・alert（枠）、`<hr>`、順序。

**P#6. NN/g — Visual hierarchy**
- URL: https://www.nngroup.com/articles/visual-hierarchy-ux-definition/ / fetch 要約（公開 2021-01-17）。
- 根拠: 数値つきの実践指針（実験ではない）。階層は hue でなく value・saturation の対比で作る / 主 2 色 + 副 2 色、対比の変化は 3 つまで / size は最大 3 段で最大サイズの要素は 2 つまで / 近接・余白（暗黙）か囲み（明示）でグルーピング / 見出しと本文の間は section 間より狭く。
- **Squint test**: 5〜20 px 半径で blur をかけ、本文を読まずに意図した群と強調が残るかを見る。「意図しない階層」が分かる。
- 移せる部分: 視覚重量に対する具体的な検査手段で見つかった唯一のもの。描画した画像が要る（markdown 本文からは出来ない）ので VLM / screenshot 側へ橋渡しになる。bullet list が隣の table より blur 下で軽く見えるか、は「囲み = 強いグルーピング」からの note の推論で、markdown について述べた source は無い。

**P#7. anywhere-agents — readme-polish skill doc**
- URL: https://anywhere-agents.readthedocs.io/en/latest/skills/readme-polish/ / fetch 要約（日付の表示なし、readthedocs の "latest"）。
- 対象と根拠: README を整える agent skill（こちらの artifact に最も近い）。1 project の house style（意見）で outcome data なし。対象は project README（install、badge、hero 画像）で profile hub ではない。
- 規則（抽出）: 中央寄せ header block（名前・tagline・badge・dot-nav・pitch）/ badge は 4〜5 個まで / hero 画像か視覚 anchor / install command が 5 秒以内に見つかる / first-screen の順 = header → badges → nav → hero → tagline / **emoji 接頭の bullet（1 emoji + 太字の機能 + 1 行、5〜8 個）** / 主要 section ごとに GitHub alert は最大 1 / **「reference 情報は密な bullets より markdown table」** / 折りたたみは variant・制限・layout に使い install には使わない / **H2/H3 を Title Case に統一、sentence と Title の混在は "reads as machine-generated"** / 例は 3 つ以上を**異なる視覚形式**で（monospace block を 3 つ積まない）/ nav anchor の解決確認 / GitHub 上と狭幅 viewport で確認 / 基準の成功指標 = 10 秒の first-glance 理解。
- 緊張 2 件は C5・C6 に集約（emoji、大小文字）。

**P#8. standard-readme spec**
- URL: https://github.com/RichardLitt/standard-readme/blob/main/spec.md / fetch 要約（版の表示なし）。
- 根拠: package / library README の spec（tool で lint 可能）。固定順 Title → Banner → Badges → Short Description → Long Description → ToC → … → License。Short description は **120 字未満**で単独行。**ToC は 100 行未満の README では不要**、ToC は全 H2 を link。link は壊れていない。
- 移せる部分: 120 字・ToC 免除・link 切れ無しは hub にも機械検査できる。section 順は package 用で hub に合わない。

**P#9. makeareadme.com**
- URL: https://www.makeareadme.com/ / fetch 要約（日付なし）。
- 根拠: 意見。Name / Description / Installation / Usage / Contributing / License、badge・visuals・screenshot・GIF、"too long is better than too short"、切るより supplementary docs。
- 違い: project reference 向け。profile README では逆の規範（P#10）が示されるので、長さの規則を hub の eval に持ち込まない（note の注意）。

**P#10. SSW Rules — GitHub profile README**
- URL: https://www.ssw.com.au/rules/github-profile-readme / fetch 要約（page 表示 "last updated 2026-10-06"）。
- 根拠: consultancy の rule（意見）。含める: identity・role、進行中の project、学習 interest、連絡手段、代表作への link。避ける: **文脈なしの技術 icon grid**、"coming soon" section、不適切な humour、長い職歴。理由: 「landing page であって resume ではない」、above the fold で scan しやすい構成、**stale な内容は無いより信用を損なう** → 四半期 review か Actions での自動化。
- 移せる部分: 「coming soon / stale を持たない」は検査できる（日付付きの主張、placeholder 文字列）。連絡手段・role は求職個人向けで、research hub の目的と異なる。

**P#11. GitHub Docs — Managing your profile README**
- URL: https://docs.github.com/en/account-and-profile/how-tos/profile-customization/managing-your-profile-readme / fetch 要約（2026-10-06）。
- 内容: 前提条件（username と同名の public repo の root に README.md）のみ。layout・content・size の指針は抽出で見つからず。profile README に first-party の視覚標準は無い。

**P#12. matiassingers/awesome-readme**
- URL: https://github.com/matiassingers/awesome-readme / fetch 要約（更新日の表示なし）。
- 根拠: 例の curated list で rubric ではない。「beautiful README」の要素として画像・logo・banner・feature list・ToC・badge・色の調和・custom icon と emoji・animation・明確な見出し・余白・flowchart を列挙。採録基準も採点も無い。コミュニティの「良い」は検査された基準でなく要素の列挙、という note の読み。

**P#13. practitioner / SEO 記事（snippet のみ。2025〜2026 の SEO・blog が多く信頼性は低い）**
- 検索 1: readme-polish / SSW / uxdesign (Medium) / dev.to 2 本 / handmade.network / kitemetric 3 本。共通: 「scannable first, readable second」、「landing page, not a resume」、10 秒理解、dot 区切り nav・中央寄せ header・折りたたみ・Mermaid、table は「関心のある読者向けの詳細」。
- 検索 2: unil.ink "GitHub README Templates in 2026" が「良い profile README は 1 画面の text + stats widget 1 つ、それ以上は装飾」「vanity badge の列は AI 生成の水増しを示す」と主張（意見、vendor 寄り、page 内確認なし）。
- 個人の苦情: gh-md（uukelele.is-a.dev）が重複 image tag・per-badge の重複 code・dark mode 用の入れ子 `<picture>`・stale な project 参照を報告（snippet）。視覚品質の基準でなく保守コストの報告。「次セッションの LLM が保守する HTML 重めの markup を避ける」を支える（note の読み）。
- Medium/uxdesign "How to Design an Attractive GitHub Profile README": 301 → 403 で**未読**。

**P#14. note の synthesis（source ではない）: 観測手段別の候補基準**。「Text」= markdown 本文から検査可能（readme_evidence.py 向き）、「Render」= 描画が要る。

| 基準 | 観測 | 根拠と強さ |
|---|---|---|
| first screen（最初の 2 段落）で who / what / where-to-go が分かる | Text + Render | NN/g F-pattern（P#4、eye-tracking）、SSW（P#10、意見） |
| 1 行 description が 120 字前後以内で単独行 | Text | standard-readme（P#8、spec） |
| 見出しが最も情報量のある語で始まる / 見出しが section の全てと topic のみを述べる | Text（LLM 判定） | NN/g P#4, P#5 |
| 見出しの大小文字がドキュメント内で一貫 | Text | readme-polish（P#7）、Google Tables（P#2）。共通核は一貫性 |
| 隣り合う兄弟 section が同じ list / table 形式、または形式差が役割差（navigation vs reference）に従う | Text | note の推論（P#2 の arity 規則、P#5 の chunk 扱い、P#7）。**この形で述べた source は無い** |
| list 項目が parallel / list に導入文か文脈を与える見出し | Text | Google Lists（P#1） |
| table: 1 行に 3 属性以上、1 列 table なし、行順が論理的、header が短い | Text | Google Tables（P#2） |
| link text が説明的 | Text | NN/g P#4 |
| anchor・link が解決、placeholder や "coming soon" なし | Text（+ script） | standard-readme、SSW、readme-polish |
| badge・emoji・icon 数が小さい上限内、文脈なしの icon grid なし | Text | readme-polish「4〜5」（意見）、SSW。数値は未検証 |
| chunk 間隔が一貫、群が囲み / 近接で区別できる | Render | NN/g P#5, P#6 |
| squint test: 5〜10 px blur で意図した強調が残り、意図しない重い block が無い | Render | NN/g P#6（実践指針） |
| 強調は最大 3 段、最上位は 2 要素以下 | Render | NN/g P#6（実践指針） |
| GitHub 上と狭幅 viewport で確認 | Render | readme-polish（P#7）。GitHub 側の標準は無い（P#11） |

note の強さ判定: 14 行のうち実験・eye-tracking の裏づけがあるのは「構造は scan を助ける」の一般論（P#3, P#4, P#5）だけで、README 固有の数値（badge 4〜5、bullets 5〜8、section ごとに alert 1、10 秒 glance）は全て house style の意見。

**hub の README が sources の対象と異なる点**（note の整理）: 対象の不一致（makeareadme / standard-readme / readme-polish は software project の README、SSW は個人開発者の profile。5 つの practice line と source-of-truth repo への pointer を持つ hub は install も tech stack も持たず、視覚上の主な仕事は**並列 5 項目の navigation**）。したがって**5 項目間の parallelism**と**兄弟 section の chunk 扱いの一貫性**が最も関連する基準で、P#1, P#2, P#5 が触れるが hub の事例を扱う source は無い。長さの規範も衝突する（makeareadme は長いほうがよい、SSW・SEO は 1 画面）。読者の違い: sources は人間の skimmer を想定する。author 自身の規則では人間が読むのは README と出力の文面だけ（llm-first-code.md）で、この hub は AI 向けの machine surface も持つ。ここの基準は人間 scan 用で、README にだけ当たる。sources に無い: bilingual（en/ja）ペアの構造同期、emoji 禁止（author の選好と readme-polish の emoji bullet が衝突）。

### 2. GitHub の README 描画仕様と制約（note: github-rendering、as-of 2026-10-06。特記なき限り各 page の公開日・版は page 上で確認できず）

読みはすべて fetch 要約か snippet。Bash が無かったため API 挙動は doc の記述のみで、実行結果は L1・L2 が補う。

**G:F1. Alert 構文と GitHub 自身の上限**
- URL: https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax / fetch 要約。根拠: 公式 doc（仕様 + 推奨）。
- 構文: `> [!NOTE]` / `[!TIP]` / `[!IMPORTANT]` / `[!WARNING]` / `[!CAUTION]` の 5 種。要約が引用符つきで返した文: "Use alerts only when they are crucial for user success and limit them to one or two per article" / "Alerts cannot be nested within other elements" / 連続 alert は避ける。
- GFM spec 0.29-gfm に alert の記述は無い（G:F12）。他 renderer（npm / PyPI / VS Code / GitHub Mobile）で blockquote に退化するかは未確認。
- 違い・移せる部分: 「Start here」を alert で目立たせる案は Docs 自身が 1〜2 個 / 文書を上限とする。「入れ子不可」の対象に list・table cell が含まれるかは Docs が明示しない。alert は個数に予算がある lever なので、judge の基準に「alert ≤ 2」を置く根拠になる。

**G:F2. Alert の CSS**
- URL: https://raw.githubusercontent.com/sindresorhus/github-markdown-css/main/github-markdown-light.css / fetch 要約（CSS 規則は引用で返った）。生成版の CSS で、生成時点は file に無い。
- `.markdown-alert { padding: .5rem 1rem; margin-bottom: 1rem; color: inherit; border-left: .25em solid #d1d9e0 }`、title は `display:flex; font-weight:500; align-items:center; line-height:1`。種別色（border-left と title）: note #0969da / important #8250df / warning #9a6700 / tip #1a7f37 / caution #cf222e（title は #d1242f）。alert = 色付き左バー + 色付き title + 通常色の本文、背景色なし。title の icon の有無は CSS 抜粋からは不明（L2 が icon の `<svg>` を実測で確認）。

**G:F3. Table の CSS と狭幅時の挙動**
- 同 CSS / fetch 要約。`table { display:block; width:max-content; max-width:100%; overflow:auto; border-collapse:collapse; font-variant:tabular-nums }`、`th, td { padding: 6px 13px; border: 1px solid #d1d9e0 }`、`tr { background:#fff; border-top:1px solid #d1d9e0b3 }`、`tr:nth-child(2n) { background:#f6f8fa }`（zebra）。
- 推論（note 時点では未検証）: `display:block` + `max-width:100%` + `overflow:auto` なので table は container 幅で打ち切られ、収まらない分は table 自体が横スクロールする。**L4 の実測がこの推論を hub の table について確認した**。
- GitHub Docs の tables page は「cells can vary in width」とだけ述べ、幅・折り返し・スクロールの記述は無い。
- 違い: table は border + zebra + 太字 header で、list（G:F4）より視覚重量が大きい。trigger の「Start here の bullet が隣の table より地味」は CSS 上の事実として説明できる。

**G:F4. List / heading / blockquote / hr の CSS**
- 同 CSS / fetch 要約。`ul, ol { padding-left: 2em }`、`li + li { margin-top: .25em }`、border も背景も無い。`h1, h2 { border-bottom: 1px solid #d1d9e0b3 }`（h3 以下は抜粋に border の記述なし）。`blockquote { padding: 0 1em; color: #59636e; border-left: .25em solid #d1d9e0 }`。`hr { height: .25em; margin: 1.5rem 0; background-color: #d1d9e0 }`。`img { max-width: 100%; box-sizing: content-box }`。
- 結論（CSS から言える範囲）: stylesheet 内で最も装飾の無い block は list。枠・背景・色バーを持つのは table / alert / blockquote / hr / h1-h2。未確認: `dl dt dd` / `mark` / `summary` / `h3-h6` / `code` の規則本文（要約は「present」と返しただけ）。

**G:F5. HTML allowlist（sanitization）**
- URL: https://raw.githubusercontent.com/gjtorikian/html-pipeline/main/lib/html_pipeline/sanitization_filter.rb / fetch 要約（ELEMENTS / ATTRIBUTES / PROTOCOLS は列挙で返り、逐語に近い）。**gem の既定値で、GitHub.com 本番の設定そのものの保証は無い**（本番は非公開）。
- ELEMENTS（49）: h1-h6, br, b, i, strong, em, a, pre, code, img, tt, div, ins, del, sup, sub, p, **picture**, ol, ul, **table, thead, tbody, tfoot**, blockquote, **dl, dt, dd**, kbd, q, samp, var, hr, ruby, rt, rp, li, tr, td, th, s, strike, **summary, details**, caption, figure, figcaption, abbr, bdo, cite, dfn, **mark**, small, **source**, span, time, wbr。属性: a=[href] / img=[src, longdesc, loading, alt] / source=[srcset] ほか。全 element 共通で **align, valign, width, height, border, colspan, rowspan, nowrap, open, media, id, name, title, lang, dir, role, aria-\*** など。
- **無いもの**: `style`, `class`, `color`, `bgcolor`, `cellpadding`, `cellspacing`。element は `center`, `font`, `iframe`, `video`, `svg`, `input`, `script`, `style`, `button`, `label`。
- 含意: 文字色・背景色・余白は指定不可。寸法は `width` / `height` 属性、配置は `align`（p / div / h1-h6 / td / th / img）。HTML `<table>` + `<img>` のレイアウトは allowlist 上は成立する。
- `markdown-alert` class は allowlist に `class` が無いのに実在する → sanitize の後段で renderer が付与していると推論できる（note 時点では未検証。L2 の出力が `class="markdown-alert ..."` を含むことと整合）。利用者が書く HTML に `class` を付けても効かない。
- G:F5b（snippet、WebSearch）: 「GitHub は style 属性を全て除去し、`<center>` を許可せず、`align` を div / p / h1-h6 / td / th / img で許可」。一次資料の本文は未読。G:F5 と整合。

**G:F6. dark / light 画像（`<picture>`）**
- URL: https://github.blog/developer-skills/github/how-to-make-your-images-in-markdown-on-github-adjust-for-dark-mode-and-light-mode/ / fetch 要約（page 上の日付 2025-04-18。再掲か初出かは不明）。
- 構文（逐語）: `<picture><source media="(prefers-color-scheme: dark)" srcset="dark-mode-image.png"><source media="(prefers-color-scheme: light)" srcset="light-mode-image.png"><img alt="Fallback image description" src="default-image.png"></picture>`。対象面: repo README・GitHub 上の documentation・GitHub.com で描画される他の Markdown。Mobile app は記事が触れない。theme ごとに画像 file が別に要る。失敗時は fallback の `<img>`。
- `#gh-dark-mode-only` / `#gh-light-mode-only` の fragment が非推奨という記述は snippet（stefanjudis / dev.to 系）のみで、GitHub の一次資料では未確認。
- 推論（未検証）: github-markdown-css の既定 file は `@media (prefers-color-scheme)` で自動切替。Chromium の `colorScheme: 'dark'` emulation で CSS と `<picture>` の両方が切り替わるはず。ただし GitHub 本番が OS 設定でなく GitHub の theme 設定（light / dark / sync / dimmed / high contrast / colorblind）で `<picture>` を切り替えているかは未確認。
- 違い: hub に badge や図があるなら dark 版の有無が描画チェック項目になる。現在の README の cover は単一の jpg（§0）。

**G:F7. 折りたたみ（`<details>`）**
- URL: https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/organizing-information-with-collapsed-sections / fetch 要約。構文（逐語）: `<details><summary>Label</summary>` + 空行 + markdown 本文 + 空行 + `</details>`、初期展開は `<details open>`。Docs の例は issue comment 文脈で、README での動作は明示なし（allowlist に `details` / `summary` / `open` は有）。静止 screenshot では閉じた内容が写らない。

**G:F8. REST API `POST /markdown`（README を local で HTML にできるか）**
- URL: https://docs.github.com/en/rest/markdown/markdown / fetch 要約（本文の一部は取得できず。github/docs の raw md も intro 1 文のみ）。
- endpoint: `POST /markdown`（`text` 必須、`mode` = `markdown` | `gfm` 既定 `markdown`、`context` = gfm 時の参照解決用 repo）、`POST /markdown/raw`（Content-Type `text/plain` か `text/x-markdown`）。上限 400 KB。応答は HTML 文字列。header 例に `X-GitHub-Api-Version: 2026-03-10`。
- mode の意味（snippet。GHES 3.1 Docs と現行 page の検索要約）: `markdown` = 「plain Markdown, just like README files are rendered」、`gfm` = user mention / SHA / issue 参照を link 化し「hard line breaks are always taken into account」。
- note の仮説（実行して確かめていない）: README の忠実な再現には `mode=markdown` が近く、`gfm` は soft line break が `<br>` になる。**alert については L1・L2 の実測が逆方向を示した**（C4）。
- generate-github-markdown-css に `--no-use-fixture`（"Exclude GitHub Markdown API-generated classes"）があり、CSS 生成側が API の出力 HTML を fixture に使っている → API 出力 + github-markdown-css が同起源の組（note の推論）。
- note の経路案 A: README → `POST /markdown` → HTML 断片 → `<article class="markdown-body">` + github-markdown.css（auto theme）+ 幅設定 → Playwright で `viewport` と `colorScheme` を変えて screenshot。

**G:F9. github-markdown-css**
- URL: https://github.com/sindresorhus/github-markdown-css と https://github.com/sindresorhus/generate-github-markdown-css / fetch 要約。
- 使い方: 描画済み HTML の container に `markdown-body` class を付け幅を設定する。README 記述（逐語）: "GitHub uses `980px` width and `45px` padding, and `15px` padding for mobile"（repo の README 表示の数値で profile 列の幅ではない）。既定 `github-markdown.css` は `@media (prefers-color-scheme)` で light / dark 自動切替。light 専用 / dark 専用 / dimmed・high contrast・colorblind 系の計 7 variant。生成: GitHub.com の CSS を取得し、markdown 内容に効きうる規則を辿って custom cleanup、という派生スナップショット。version・生成日は page と CSS 先頭 comment から取れなかった。syntax highlighting は除外（`starry-night` を別途使う）。
- 違い: 派生物なので、GitHub 本体が CSS を変えると静かにずれる。取得日の確認が要る。profile 列幅は 980px と異なる（L4 で実測）。

**G:F10. Profile README の置き場所と列幅**
- URL: https://docs.github.com/en/account-and-profile/how-tos/profile-customization/managing-your-profile-readme と https://docs.github.com/en/account-and-profile/concepts/about-your-profile / fetch 要約。
- 表示条件: username と同名の **public** repo の root に空でない `README.md`。消える条件: 空にする / private 化 / repo 名と username の不一致。「GitHub shows your profile README at the top of your profile page.」（逐語）。pinned repos との上下関係は Docs が述べない（snippet の blog 要約が「above pinned repositories」。二次）。private profile でも README / bio / avatar は公開。
- 列幅: 一次資料なし。snippet（primer/css の issue 由来）: Primer `Layout` の sidebar 既定幅 296px（narrow 256 / wide 344、xl breakpoint）、`container-xl` 最大 1280px。profile page の実測ではない。→ L4 が実測で解決。

**G:F11. GitHub Mobile app**
- 一次資料なし。https://github.com/orgs/community/discussions/24079 / fetch 要約（2021-04-23〜24 の投稿）: native app で README の画像が出ない報告。原因は file 名の非 ASCII 文字（ä）で、ASCII に改名して解決。staff 返信なし。コメント欄に「`width` / `height` 属性つき画像は mobile 未対応」という既知 issue への言及。snippet（SEO 系 blog）: 「mobile web と app は desktop と少し違って描画する」。2021 年の情報で現在も有効か不明。native app の描画は narrow viewport の mobile web では再現できない（別物）。

**G:F12. GFM spec**
- URL: https://github.github.com/gfm/ と cmark-gfm test/spec.txt / fetch 要約（後者は先頭部分のみ。「Disallowed Raw HTML」節は未取得）。版 "Version 0.29-gfm (2019-04-06)"（page 表示。最新の公開版かは断定不可）。拡張: table / strikethrough / task list / extended autolink / disallowed raw HTML。**alert / footnote / math の記述は無い**。GitHub.com と GHE は GFM→HTML の後に追加の post-processing と sanitization を行う（spec の外）。table 規則: header 行と delimiter 行の cell 数が違えば table でない、後続行の cell が少なければ空 cell で補い多ければ超過分は無視、空行か別 block 構造で終わる。

**G:F13. その他の仕様（basic syntax page、fetch 要約）**
- heading は 6 段。複数 heading があれば GitHub が目次（outline icon）を自動生成するが、README 本文の外（file header 側 UI）で本文の見た目に影響しない。custom anchor `<a name="...">` は outline に載らない。対応 HTML: `<a name>` / `<br/>` / `<sub>` / `<sup>` / `<ins>` / コメント / `<picture>`。色 chip の描画は issue / PR / discussion 限定で README では出ない。

**視覚 lever の一覧**（note の整理。根拠は上記 G:F）

| lever | 書き方 | 制約・見た目 |
|---|---|---|
| 見出し | `#`〜`######` | h1・h2 は下罫線。h3 以下は罫線なし（抜粋範囲） |
| alert | `> [!NOTE]` 等 5 種 | 色付き左バー + 色付き title。1〜2 個 / 文書が公式推奨。入れ子不可 |
| blockquote | `>` | 灰色の左バー + 灰色文字 |
| table | pipe 構文 | 罫線 + zebra + header 太字。cell は inline のみ。狭幅は横スクロール（L4 で実測確認） |
| HTML table | `<table><tr><td>` | `align` `valign` `width` `height` `colspan` `rowspan` `border` 可。`style` `class` `cellpadding` 不可。cell に `<img>` 可 |
| 画像寸法 | `<img width= height= align=>` | 属性は allowlist 上可。CSS が `max-width:100%`。mobile app で `width` / `height` が効かない報告（2021） |
| dark / light 画像 | `<picture>` + `<source media>` | theme ごとに別 file。fallback は `<img>` |
| 折りたたみ | `<details><summary>` | 空行必須。閉じた内容は静止画に写らない |
| 水平線 | `---` | 太さ .25em、上下 1.5rem |
| 定義リスト | `<dl><dt><dd>` | element は有。見た目の CSS は未確認 |
| 不可 | 文字色・背景色・フォント・`<center>` | `style` / `class` / `color` が無い。中央寄せは `align="center"` のみ |

### 3. VLM / screenshot judge の信頼性と描画経路（note: vlm-judge、as-of 2026-10-06）

note 冒頭の注記: WebFetch の応答は小モデルの要約で、数値は要約モデルの報告のとおり。決定に効く数値は論文を再読してから使う。以下の「Full text」「Abstract only」は note の表記で、いずれも summarizer 経由。URL は arXiv ID から構成した（note は ID のみ記載）。

**V1. WebDevJudge — arXiv 2510.18560 v2（2026-03-02、ICLR 2026）**
- URL: https://arxiv.org/abs/2510.18560 / Full text（html、via summarizer）。
- 主張: (1) 最良の LLM judge（GPT-4.1）は pairwise で human expert 一致 84.56% に対し 70.34%。(2) pairwise は single-answer grading より一致が >8.0% 高い。(3) single-answer では **binary rubric が multi-point Likert を大きく上回る**。(4) pairwise では明示 rubric（guidance）が Direct とほぼ同等。(5) position bias: GPT-4.1 は 2 番目を選ぶ率 15.8% に対し 1 番目 0.9%（Direct）、consistency 83.3%、debias の指示でも残る。(6) code を除くほうが screenshot を除くより悪化が大きい。
- 実装・前提: webdev-arena-preference-10k（人間の pairwise 投票）由来の 654 インスタンス、一致 89.7% の rubric、静的（code + screenshot）と interactive（UI-TARS / GPT-4.1 agent）。
- 違い: 機能を持つ LLM 生成 web *app*、人間の preference label 付きの pairwise。こちらは静的 doc、preference data なし、絶対 verdict。モデルは 2025 年世代。移せる部分: 「code が最も情報量のある modality」→ 既存の text-only judge は source modality を持つので、VLM は render でしか見えない証拠だけを足す。

**V2. AesEval-Bench — arXiv 2603.01083（ICLR 2026、2026-03）**
- URL: https://arxiv.org/abs/2603.01083 / Full text（html、via summarizer）。
- 主張: VLM は design 美的判断で人間に劣る。最良 GPT-5 は binary aesthetic judgment で 72.52%。reasoning 強化モデルに明確な優位なし。flaw の localization が最弱（best IoU <0.20）。主観的 indicator（psychology, relevance）が最難。
- 実装: 3 タスク（binary 判定 / 4 択の region 選択 / bbox localization）、4 次元 12 indicator（Layout: balance・layering・whitespace・alignment、Font: hierarchy・legibility、Graphics、Color: harmony・contrast・appeal・psychology）。
- 違い: poster・layout の graphic design で document ではない。indicator ごとの binary という形は我々の binary check と似るので、「2026 年の最良モデルで約 72%」は粗い天井の目安であって README の測定ではない。chance level は読んだ範囲に記載なし。

**V3. UIClip — arXiv 2404.12500 v1（2024-04-18、UIST 2024）**
- URL: https://arxiv.org/abs/2404.12500 / Full text（html、via summarizer）+ 二次 snippet。
- 主張: frontier LVLM は UI 2 択でほぼ chance。GPT-4V 51.58%（html fetch）または 52.9%（search snippet。未調整）、Claude-3-Opus 60.3%・Gemini-1.0-Pro 54.6%（snippet のみ）、UIClip（CLIP-B/32、151M）75.12%。GPT-4V は約 10% で回答拒否。Gemini はほぼ全例で CRAP 4 原則を全て列挙。review site の snippet（論文本文ではない）: GPT-4V は文字がはみ出した jitter 版 screenshot を好んだ。
- 実装: CRAP 原則を適用して 2 枚の screenshot の良いほうを選ばせる prompt（数回調整）。1 画像しか受けない model は 2 枚を**横に連結した 1 枚**で入力。訓練 2.3M screenshot、BetterApp = designer が順位付けした 892 ペア。
- 違い: 2024 年のモデル、side-by-side 連結で形式が交絡、実物 vs 劣化の mobile / web UI のペア。古い VLM が overflow・jitter を見落としうる（README の check が狙う layout 欠陥そのもの）という証拠で、現行 Claude の証拠ではない。

**V4. MLLM-as-a-Judge — arXiv 2402.04788（ICML 2024）**
- URL: https://arxiv.org/abs/2402.04788 / Abstract only（via summarizer）。
- 主張: pair comparison は Scoring や Batch Ranking より人間との一致がはるかに良い。GPT-4V でも bias・hallucination・inconsistency が残る。一般の vision-language タスクで UI / design ではない。方向は WebDevJudge（pairwise > absolute）と一致。

**V5. ArtifactsBench — arXiv 2507.04952 v2（2025-07）**
- URL: https://arxiv.org/abs/2507.04952 / Search snippet only。
- 主張: MLLM judge + task ごとの checklist で WebDev Arena との順位一致 94.4%、human expert との pairwise 一致 >90%（280 インスタンスの expert study で最大 90.95%）。実装: 1,825 タスク、30+ LLM、artifact を描画して時系列 screenshot を取得、screenshot + source code を MLLM judge に細粒度 checklist 付きで与える。
- 違い: 順位一致は多数 artifact にわたる model レベルの集計で、1 件ごとの verdict 信頼性ではない。judge は code も見る。checklist ablation は読めておらず、checklist が一致を生むことは示されない。

**V6. UICrit — arXiv 2407.08850（UIST 2024）**
- URL: https://arxiv.org/abs/2407.08850 / Abstract only。
- 主張: 7 人の経験ある designer による 983 の mobile UI への 3,059 件の critique と品質 rating。この dataset を使った few-shot + visual prompting で LLM 生成 UI feedback が「55% の性能向上」（指標は abstract に無し）。mobile app UI の feedback 生成で pass/fail verdict ではない。移せる考え: 人間ラベル付き例による few-shot（自前のラベルが要る）。

**V7. Anthropic vision doc**
- URL: https://platform.claude.com/docs/en/build-with-claude/vision / note は Full text と記載（取得 2026-10-06。note 冒頭は WebFetch が要約モデル経由と注記）。vendor documentation で実験ではない。
- 内容: 解像度の上限は Claude 4.7 以降が長辺 **2576 px / 4784 visual token**、他 model は 1568 px / 1568 token、28×28 px patch = 1 token。大きい画像は縮小され文字が読みにくくなる。200 px 未満の画像は不安定。空間・座標出力は「approximate」、計数も approximate。非可逆 JPEG は文字を読めなくしうる。画像は text の前に置き、複数画像は "Image 1:" とラベル付け。1 request に 20 枚超だと 1 枚あたり約 2000 px のより厳しい上限。
- note の推論（doc に明記なし）: mobile 幅（例 390 px）の full-page capture は長辺で縮小されるので、viewport 高さの tile に切り、JPEG でなく PNG で送る。

**V8. github-markdown-css README**
- URL: https://github.com/sindresorhus/github-markdown-css / note は Full text of README と記載（取得 2026-10-06。release 日・version は読んだ範囲に無し）。
- 内容: wrapper CSS は `max-width: 980px; padding: 45px`（狭幅で 15px）。variant は light / dark / auto / dark-dimmed / high-contrast / colorblind。`<!doctype html>` が要る（quirks mode は dark mode の table を壊す）。task list・mention・emoji は対象外、syntax highlighting は starry-night が別途要る。GitHub の描画の近似で ground truth ではない。忠実性を見るには実 github.com page の screenshot と 1 回比較する（note）。

**V9. md2static（PyPI）/ pageshot（Docker Hub）**
- snippet のみ。md2static: GitHub Markdown API → 公式 GitHub CSS で包む → Playwright capture。pageshot: Playwright render、GitHub の light/dark theme、device scale factor 既定 2。未検査で保守状態は不明。pointer としてのみ使える。約 20 行の Playwright script のほうが単純かもしれない（note）。

**V10. local 実測: subagent 内での Read tool による PNG 表示（2026-10-06、vlm-judge note）**
- researcher subagent が 2303×1136 の PNG を Read した。画像は視覚的に返り、画像中の UI 文字を読めた。harness の注記は "original 2303x1136, displayed at 2000x987"。したがって (a) subagent で Read は PNG をモデルに見せる、(b) 1 試行で長辺約 2000 px への縮小が観測された。tall 画像の上限は未検査。anthropics/claude-code の issue #18588, #20822, #30925（snippet のみ。日付・版は未読）が画像で Read が空を返す報告として挙がり、version 依存。1 試行は存在証明であり信頼性の主張ではない。

**V11. 二次・未検証（snippet のみ。依拠しない）**
- digitalapplied.com blog（2026-08-02）: VLM は静的で測れる性質に強く、interaction 状態・motion は構造的に判定できず、spacing の rhythm・hierarchy・density・alignment drift を表現できない、「dense な学術図 15 枚のうち 14 枚を VLM judge が 'perfect' と評価した（実際は明らかに崩れていた）」。snippet が複数 result を混ぜていて 14/15 の出典は不明（候補は arXiv 2607.11598、未 fetch）。検証すべき仮説で finding ではない。
- Playwright の recipe（記憶からで、今回 current docs に照合していない）: `browser.new_context(viewport={width,height}, color_scheme="dark"|"light", device_scale_factor=2)`、`page.screenshot(full_page=True)`。desktop 約 1012〜1280 幅と mobile 約 390 幅 × light/dark = 1 README あたり 4 capture。API 名は使う前に確認が要る。

**note の synthesis（vlm-judge。source ではない）**
- absolute 採点で binary > Likert は WebDevJudge（全文、web-dev 領域）が支持し、現 harness の binary check と整合。
- pairwise > absolute の一致（WebDevJudge +8%、MLLM-as-a-Judge abstract）。ただし pairwise は position bias（2 番目選好 15.8%）を持ち指示で消えない → before/after 比較は順序入れ替えと一貫性確認が要る。
- 「checklist が効く」は確立していない（ArtifactsBench は ablation を見ていない、WebDevJudge は pairwise で rubric ≈ Direct）。
- 天井: 美的・web 品質判定で VLM の最良報告は約 70〜73%（2025〜2026 モデル）、人間 expert は約 85%（WebDevJudge）。Claude 4.7+/Opus 5 を markdown page で測った研究は無いので、author 自身のラベルとの一致と test-retest は local で測る必要がある（人間ラベル付き README screenshot の小集合を N 回反復）。
- localization は弱い（AesEval IoU <0.20、Anthropic doc「approximate」）→ 視覚 verdict の 1 行 evidence は座標でなく、見えている文字列か名前付き要素の引用にする。objective な render 性質（画像の overflow・横スクロール・contrast 比・alt の有無・table 幅）は DOM / CSS から VLM なしで検査できる（note の推論。この分割を検証した論文は無い）。
- 既存の text-only judge は markdown source に残し、VLM は source に出ない物（壊れた・切れた画像、badge の折り返し、mobile overflow、dark mode での画像の可読性、実際の whitespace rhythm）だけを足す。

### 4. loop が失敗する理由と別の枠組み（note: adversarial、as-of 2026-10-06）

深度の注意: arXiv 8 本は全て abs ページの要約（abstract 水準）。本文 PDF は 1 本も未読。snippet 項目は本文未読。

**X:A1. Voice Under Revision — arXiv 2604.22142（2026-04-24）**
- URL: https://arxiv.org/abs/2604.22142 / abs 要約のみ。
- 対象・結果: 3 つの frontier LLM（機種は abs に無し）、personal narrative 300 件、3 条件（generic improvement / rewrite-only / voice-preserving）、13 言語マーカー。どの条件でも function words・contractions・一人称代名詞が減り、語彙多様性・語長・句読点が増え、語りが embedded → distanced に移る。書き直し後のテキストは feature space で互いに近づく。voice-preserving prompt は「変化の大きさを減らすが方向は消さない」。結論は「より磨かれた、situated でない register への directional pull」。実験（観察的、1 回書き直し中心。ラウンド数は abs に無し）。
- 違い: 個人叙述で README ではない。author が観測した「3 ラウンド目以降の bland な corporate 調」と方向は一致するが、この論文は**第 1 回の書き直しから方向性がある**と述べ、ラウンド上限で消える種類の効果とは書いていない。
- 移せる部分（note の推論。論文は分離を検証していない）: 判定（verdict）だけを LLM にさせ、文面の修正は構造・順序・markup に限る、という分離なら当たりにくい。

**X:A2. Do Language Models Converge to Themselves? — arXiv 2607.22653（2026-07）**
- URL: https://arxiv.org/abs/2607.22653 / abs 要約のみ。
- 対象・結果: GPT-5.5、ICML 2025 abstract 50 本 + ICML 2020 abstract 15 本、10 step の自己 refine。編集の大半は最初の数 iteration で起き、その後「soft fixed-point region」（model-preferred な textual equilibrium）に収まる。編集量は指数減衰。deterministic decoding は厳密な不動点に早く到達。実験（学術 abstract・2 つの decoding のみ）。
- 違い: judge は入らず「refine せよ」を繰り返すだけ。README でも eval-loop でもない。note の推論: ドリフトは前倒し（round 1〜2 に集中）で後半は飽和するので、2 ラウンド cap は「ドリフトを避ける」のでなく「ドリフトの追加を止める」程度の意味かもしれない。author の観測（後半ラウンドで悪化）と食い違う点（C1 に集約）。

**X:A3. Style Wins, Substance Loses — arXiv 2608.01666（2026-08）**
- URL: https://arxiv.org/abs/2608.01666 / abs 要約のみ。
- 対象・結果: 科学アイデアを評価する LLM judge。SciStyleBench: 600 アイデア × 15 スタイル変種 = 9,000 評価 / 設定。内容固定で文体だけ変える。judge はスタイルに敏感で内容の差を弁別しにくい。mitigation（SciStyleExtractor、評価前に style type を予測して分離）で Style Bias Index 0.566→0.501、Substance Recognition Rate 0.504→0.759、Adversarial Win Rate 0.554→0.899。
- 違い: text のアイデア評価で視覚 layout ではない。README の見た目 verdict が内容でなく書式表層に引かれるかは未検証。移せる部分: 「表層（書式）を変えると verdict が動く」リスクの存在証明。対策の型（評価前に表層を分離）は screenshot 方式と相性が悪いかもしれない（note の推論）。

**X:A4. Can MLLMs Critique Like Humans? — arXiv 2606.29689（2026-06-29、rev 2026-08-31）**
- URL: https://arxiv.org/abs/2606.29689 / abs 要約のみ。
- 対象・結果: 8 つの open-weight MLLM（7B〜397B）+ GPT-5.5 を r/photocritique の人間講評 1,227 件と比較（写真の美的講評）。モデルは「人間が選択的に触れる美的側面のほぼ全て」を網羅し、1 枚への複数講評で自己反復する。参照ベース類似度指標は長さ・投稿文・安定した講評スタイルを反映し画像固有の観察を反映しない。judge と人間 2 名の実質的類似度評価は 1.81〜2.59/5。7〜8B model では同一ペアへの judge 選好が 9%〜81% と大きく割れる。
- 違い: 写真で README ではない。「講評生成」の評価で verdict の正答率ではない。note の推論: VLM は選択せず全側面を平らに列挙するので、非集約の named verdict は「平均で潰す」問題を避けるが、「全部に指摘が出る → fix loop に優先順位が無い」問題は残る。verdict 集合を少数にし事前に重み付けする必要がある。

**X:A5. LLM-Evaluation Tropes — arXiv 2504.19076（snippet のみ）**: 「evaluation-driven convergence」「LLM が関連性を定義すると系の上限を暗黙に決める」という主張が検索要約に出た。本文未読で強い根拠としては使わない。

**X:B1. Spontaneous Reward Hacking in Iterative Self-Refinement — arXiv 2407.04549（2024-07）**
- URL: https://arxiv.org/abs/2407.04549 / abs 要約のみ。
- 対象・結果: essay editing。generator と evaluator が同一 model か別 model かを比較。「evaluator の評価は上がるが、ユーザー選好で見た生成品質は停滞または低下」。同一 model だと共有脆弱性を突く。深刻度は model size と共有 context 量で増える。evaluator を generator から分けると自然発生的 reward hacking が緩む。敵対設計なしに in-context で自発的に起きる。実験（ラウンド数は abs に無し、2024 年世代で 2026 年の frontier への当てはまりは未確認）。
- 違い: essay の数値評価ループ。author の loop は named verdict・非集約・2 ラウンド上限で露出は小さい。ただし「judge と fixer が同じ model・同じ context」の構成なら B1 が最も近い失敗モード。移せる部分: judge と fixer を別 process / 別 context に分ける。evaluator スコアと人間選好の乖離を 1 回測る。

**X:B2. LLM-as-a-Judge Is Not an Oracle — arXiv 2609.02246（2026-09-02）**
- URL: https://arxiv.org/abs/2609.02246 / abs 要約のみ。
- 対象・結果: Teacher（judge）を使う self-improving agent。契約分析・コンプライアンス・コード品質の 3 業務領域で数か月の本番テスト。評価信号の失敗を 11 種・4 分類（judge bias / harness・metric failure / ground-truth error / reward hacking）で記録。agent が環境内の answer key を読んで 100% pass、真の能力は 68%。guardrail の提案: hermetic sandbox、capability-disjoint roles、Teacher に優先する acceptance check、frozen holdout、canary case。
- 注意: 検索 snippet の「判定キャリブレーション 80% → 全体 51.9%」は abs ページに無く出典未確認で**採用しない**。型としての移植: frozen holdout = loop で触れない別 README（同 hub の他 line README）で judge を検算 / canary = 意図的に悪くした版を judge が「悪い」と言うかの確認 → 1 artifact への rubric の過学習への対策（note の設計案）。

**X:B3. LMArena Style Control**
- URL: https://lmsys.org/blog/2024-08-28-style-control と https://arena.ai/blog/style-control/ / WebSearch snippet のみ（blog 本文未読）。
- 内容（snippet）: Bradley-Terry 回帰に style 特徴（回答 token 長、markdown の header / bold / list の数）を加えて補正。length が支配的（係数約 0.249〜0.267）、header / bold / list は二次（約 0.019〜0.111）。大規模な人間 pairwise 投票の回帰（観察）。
- 違い: chat 回答で README ではない。投票者は多数の匿名人間で単一 author ではない。移せる部分: 人間 pairwise ですら書式の量（見出し・太字・リスト）が選好を押し上げる。「list が表の隣で地味」を判定軸にすると、rubric は書式を増やす方向（表・badge・見出し増）の最適化を促しうる。human pairwise は書式バイアスを免れる解ではない。

**X:C1. The Coin Flip Judge — arXiv 2606.13685（2026-06）**
- URL: https://arxiv.org/abs/2606.13685 / abs 要約のみ。
- 対象・結果: GPT-4o-mini と GPT-4.1-mini（単一 provider）、29 タスク・10 カテゴリ、pairwise 50 回と pointwise 50 回。同一入力の反復で pairwise の選好が平均 13.6% 反転し、28% の質問で反転率 20% 超。judge 間一致 76%（κ=0.51）。意味同等な prompt の言い換えで多数決が 25% で変わる。GPT-4o-mini は先頭位置バイアス（A が 72%、p=0.024）。多数決で 50 回の参照評決を 95% で復元するのに 11 回要る。
- 限界: 単一 provider、abs は主観 / 美的タスクかどうかを書かない。note の移せる部分: judge の 1 回の verdict は coin flip に近い場合がある。非集約 named verdict を 1 回だけ走らせる設計は、反復して多数決にしない限り変動に弱い。

**X:C2. pairwise vs pointwise（snippet のみ）**
- https://arxiv.org/abs/2504.14716 の要約: feedback protocol の比較で pairwise が約 35% 反転、絶対スコアが約 9%、「pairwise は distracted evaluation に弱く、absolute は頑健」。https://arxiv.org/abs/2602.02219「Am I More Pointwise or Pairwise?」は rubric 型 judge に位置バイアスがあり、順序入れ替えの平均化で人間との相関が上がると要約される。
- 含意（note）: LLM judge では pairwise のほうが不安定という証拠が出ている。人間の pairwise の信頼性を直接示す一次資料は今回見つからず。

**X:D1. Lindgaard et al. 2006（Behaviour & Information Technology）**: Nature News 2006-01 など複数の報道記事（snippet のみ。原論文未読）。homepage を 50ms と 500ms 見せ、1〜100 で魅力度を評価させると参加者間で評価が一貫（500ms のほうがより一貫）、halo effect で第一印象が内容評価にも波及。「一貫」は平均評価の安定性で個人間 κ ではない（報道要約からの理解）。5 秒テスト系の根拠にはなるが、README の「見た目で伝わるか」の基準を与えるものではない。

**X:D2. Reinecke & Gajos, CHI 2014「Quantifying Visual Preferences Around the World」**: https://eecs.harvard.edu/~kgajos/papers/2014/reinecke14visual.shtml / snippet のみ。約 4 万人から 240 万件の Web サイト魅力度評価。色彩性・視覚的複雑さの最適点が性別・学歴・国で有意に異なり、普遍ガイドラインの実現性を疑わせる、と要約される。対象は Web サイト全体の色と複雑さで README の構成ではない。note の推論: 単一 author の hub では、読者ターゲットの選好でなく author 自身の選好との一致が基準になりうる。

**X:D3. evaluator effect（Jacobsen, Hertzum & John 1998; Molich 1998 を MeasuringU が引用）**: https://measuringu.com/evaluator-effect/ ほか / snippet のみ。heuristic evaluation・cognitive walkthrough・think-aloud で 2 評価者間の any-two agreement は 5〜65%（33 研究の中央値 27%）。別の例では 4 評価者全員が見つけた問題は 20%、1 人だけが見つけた問題は 46%。usability 問題の検出で美的評価ではない。note の推論: checklist / heuristic 方式の検査は評価者ごとに別の問題を拾う。LLM judge 1 体 = 評価者 1 人で、見落とし率は 1 回の実行から推定できない。「judge が全部 pass」は網羅の証拠にならない。

**X:E1. Ozok & Salvendy 2000（Ergonomics 43(4)）**: https://informahealthcare.com/doi/abs/10.1080/001401300184332 ほか / snippet のみ。Web page の consistency（physical / communicational / conceptual の 3 要素）を測る 125 項目質問紙 → 94 項目 9 因子。4 群・各 10 人の被験者間設計。結果は部分支持: 一貫した視覚・言語属性でエラーが減る。作業時間と満足度では仮説が支持されなかった。「consistency が有益」の実証はあるが規模が小さく（n=10/群）、効果はエラー率に限られ、対象は操作系インターフェース。「リストと表の視覚的重さを隣接で揃える」を直接検証したものは見つからず、現状は heuristic（専門家判断）か taste としての位置づけ。

**X:F1. GitHub Traffic API**: https://docs.github.com/en/rest/metrics/traffic / fetch 要約。4 endpoint（clones / popular paths 上位 10 / popular referrers 上位 10 / views）、期間は直近 14 日、write access 必須。scroll・クリック・リンク別データは無い。profile README repo（`user/user`）で動くかは docs に記載なし。含意: 見た目変更の A/B を GitHub 側の指標で測る経路は無い。

**X:F2. 手元の traffic data（この repo の `traffic/data/shimo4228.jsonl`、read-only で 5 回）**: 167 日分の日次行のうち 94 日が `views.count=0`、非ゼロの日も多くは 1〜2（最大の例で 10、uniques 2）。clones は 1 日 10〜100 超（bot / crawler 混在の可能性は未検証）。`scripts/traffic_compare.py` は views.count の固定 cohort 集計のみ。hub の views は 1 日数件の水準で、README の見た目変更前後の差を traffic で検出するには母数が足りない。profile ページの描画が repo の views に数えられているかは不明（docs にも記載なく、確認していない）。

**note の総括（adversarial。推論・設計案を含み、source ではない）**: (1) judge と fixer を同一 model・同一 context で回すと B1 の構成になるので分離する。(2) ドリフトは第 1 回から向きを持ち（A1）大半は前半に集中する（A2）ので、2 ラウンド cap は magnitude の抑制として働くが voice を守る手段としては弱く、fix の自由度（文面を書き換えない）で守るほうが機構的。(3) 書式の量は人間にも LLM にも好まれる（B3, A3）ので「list が地味」を failure verdict にすると表・見出し・badge を増やす方向に引く。重さの揃えを、書式を足す方向でなく「軽いほうを残す / 重いほうを軽くする」の両方向で許す verdict にする。(4) VLM は選択せず全部指摘する（A4）、1 回の verdict は不安定（C1）ので named verdict の数を絞り、優先度を rubric 側に持たせ、必要なら 3〜11 回の反復多数決。(5) 1 artifact への過学習は B2 の frozen holdout / canary で検出する（同 hub に近い別 line repo の README を holdout にする案）。(6) 美的判断の人間間一致は低め（D2, D3）だが、単一 author の hub では評価者 = author 1 人で、judge の較正は author の pairwise 選好との一致を見るのが筋（外部根拠なしの設計案）。(7) traffic では測れない（F1, F2）ので、評価は author の目と少数の 5 秒テスト型の人間観察に頼る。(8) 「隣接の重さを揃える」は確立された原則でなく heuristic / taste（E1）なので、rubric に入れるなら「taste を明示した author 定義の基準」として扱い、一般原則として載せない。

### 5. Local primary checks, 2026-10-06, observed by running（lead が実行・観測。researcher は結果を受領して記載。実行ログ本体はこの report に無い）

**L1. `gh api -X POST /markdown/raw`（= mode markdown）**
- `> [!NOTE] ...` の alert は plain の `<blockquote><p>[!NOTE] ...` として描画された。**markdown mode では alert は描画されない**。soft line break は改行のまま残る。

**L2. `gh api -X POST /markdown -f mode=gfm -f context=shimo4228/shimo4228`**
- alert は `<div class="markdown-alert markdown-alert-note">` と Octicon の `<svg>` title として描画され、github.com の表示と一致した。ただし gfm mode は soft line break を `<br>`（hard break）にする。
- lead の結論: 段落が 1 行 1 段落の README（hub の JA 規則。EN も 1 行 1 段落、§0 で確認）では gfm mode が faithful な local 描画経路。複数行段落があると乖離する。この結果は G:F8 の mode 仮説（`markdown` が README 寄り）を alert については逆方向に解決した（C4）。
- 実行は `gh api` なので認証あり。未認証での可否・rate limit・相対 link の書き換え・heading anchor・code の `pl-*` class の確認は報告に無い。

**L3. local tooling**
- Google Chrome.app が存在。Playwright が npx cache（`~/.npm/_npx/*/node_modules/playwright`）に既存、browser binary が `~/Library/Caches/ms-playwright`（chromium-1243、chromium_headless_shell-1243）にある。readme-writer の宣言済み dependency ではなく、使うなら dependency intake が要る。Playwright の API 名と screenshot の実行は報告に無い（V11 の recipe は未検証のまま）。

**L4. 実 profile page https://github.com/shimo4228 の実測（in-app browser、live DOM、dark theme、logged-in view、2026-10-06）**
- **desktop viewport 1280×800**: README の `article.markdown-body` は幅 846 px、上端 y=228。cover 画像 + H1 + lead 文 + 自己紹介段落が最初の画面を埋める。`Start here` の H2 は y=880 で、**最初の 800 px の画面より下**。`At a Glance` y=1108、`Through-line` y=1570、`Elsewhere` y=1770、README 下端 y=1956。pinned repos は y=2005 から始まり、**profile README は pinned repos の上**にある。README の高さは 1956−228=1728 px（本 report での算術。800 px 画面の約 2.2 枚分）。左 sidebar は avatar・名前・bio・link（X, ORCID, Zenn, note）を持ち、README が競う first screen の一部。
- **mobile viewport 375×812**: README 列は幅 293 px で y=901 から始まる（avatar・bio の sidebar が先に積まれるので、README 全体が最初の mobile 画面より下）。`Start here` y=1563、`At a Glance` y=2042。At a Glance の table は scrollWidth 463 px に対し client 幅 293 px で、**mobile では横スクロールする**（G:F3 の CSS からの推論を確認）。
- 測定は 1 回、dark・logged-in・上記 2 viewport。EN の README（profile に表示されるもの）が対象で、README.ja.md の表示は報告に無い。native app は対象外（in-app browser の mobile viewport）。

**L5. 対象 README の読み取り（§0 参照）**: 現行の `Start here` は 3 項目の箇条書き（太字の `From X:` + link + 説明）、`At a Glance` は 3 列 table。author の trigger は「`Start here` の bullet が隣の `At a Glance` table より plain で scan しにくい」と、Claude plugin の項目を先頭に置くこと。

## Contradictions

**C1. ドリフトの発生時期: author の観測「ラウンド 3 以降」vs 論文「第 1 回から方向性、前半集中」**
- author の観測（lead の依頼文による。note には出典文書なし）: bland な corporate 調のドリフトは 3 ラウンド目以降に現れる。
- X:A1（abs 要約のみ）: 書き直しはどの条件でも第 1 回から register を一方向に動かし（function words・contractions・一人称が減る等）、voice-preserving prompt は大きさを減らすが方向を消さない。ラウンド数は abs に無い。X:A2（abs 要約のみ）: 編集の大半は最初の数 iteration で起き、その後 soft fixed-point に収まり、編集量は指数減衰。
- どちらが強いか: 決着しない。両論文とも abstract 水準で、ジャンル（個人叙述・学術 abstract）も設定（judge なしの繰り返し refine）も author の loop（judge→fix、cap 2）と異なる。author の観測は実際の設定での直接観察だが、note に記録がなく測定法も不明。両者は別の量（編集量の時間経過と、体感する register の劣化）を指している可能性があり、これは本 report の読みで note の結論ではない。実務上は、2 ラウンド cap がドリフトの大半を既に含んだ地点で止めている可能性（X:A2 の note の推論）と、fix の自由度を構造・順序・markup に限る案（X:A1・総括(2) の設計案）が併記されるだけで、検証済みの対策は無い。

**C2. checklist / rubric の効果: ArtifactsBench の checklist 帰属 vs WebDevJudge の rubric ≈ Direct**
- V5（snippet のみ）: task ごとの細粒度 checklist 付き MLLM judge が WebDev Arena との順位一致 94.4%、expert との pairwise 一致 >90%。ただし checklist ablation は未読で、checklist が一致を生む証拠ではなく、順位一致は model レベルの集計で judge は code も見る。
- V1（全文 via summarizer）: pairwise では明示 rubric（guidance）は Direct とほぼ同等。single-answer では binary rubric が Likert を大きく上回る。
- どちらが強いか: WebDevJudge のほうが本文まで読まれ、ablation 相当の比較を持つ。ArtifactsBench は snippet と ablation 欠如で因果を言えない。ただし「binary vs Likert」と「rubric の有無」は別の軸で、矛盾しない可能性がある（note も同旨）。我々の形（single-answer の binary check + evidence + falsification pass）を直接検証した source は無い。

**C3. pairwise vs absolute: 「pairwise のほうが人間と一致」vs「LLM judge では pairwise のほうが不安定」**
- V1（全文 via summarizer）: pairwise は single-answer より人間一致が >8.0% 高い。V4（abstract のみ）: pair comparison が Scoring・Batch Ranking より人間と一致。
- X:C1（abs 要約）: pairwise の選好は同一入力の反復で平均 13.6% 反転、28% の質問で反転率 20% 超、位置バイアス。X:C2（snippet のみ）: pairwise が約 35% 反転、絶対スコアが約 9%（2504.14716）、rubric 型 judge に位置バイアスで順序入れ替えの平均化が必要（2602.02219）。
- 整理: 測る量が違う（人間ラベルとの一致 vs 反復・順序入れ替えでの自己一貫性）。V1 自身も位置バイアス（2 番目選好 15.8% 対 1 番目 0.9%、consistency 83.3%、debias 指示で残る）を報告していて、pairwise 優位を言う側も不安定性を認める。強さ: 人間ラベルとの一致は V1（全文）が最も強い。不安定性は X:C1（abs）が最も強く、X:C2 は snippet。人間の pairwise の信頼性を直接示す一次資料は見つかっていない。いずれも Claude 4.7+ / README での測定ではない。どちらの側から見ても、pairwise を使うなら順序入れ替えと一貫性確認が要る点だけは一致する。

**C4. note の仮説「markdown mode が README-faithful」vs 実測（alert は gfm mode のみ）**
- G:F8（snippet 由来の mode 説明）: `markdown` = 「plain Markdown, just like README files are rendered」、`gfm` は hard line breaks を常に反映 → note の仮説は `mode=markdown` が README 寄り。
- L1・L2（実測）: markdown mode は alert を plain の blockquote にし（`[!NOTE]` の文字がそのまま残る）、soft line break は改行のまま残す。gfm mode は alert を `markdown-alert` の div + Octicon svg で描画（github.com と一致）するが、soft line break を `<br>` にする。
- 解決: alert を含む README の見た目は gfm mode でしか再現できない。1 行 1 段落の README（hub の EN・JA）では soft break の差が出ないので gfm mode が faithful。複数行段落があると乖離する。実測が強く、仮説は alert に関しては反証、line break に関しては mode の説明どおり。

**C5. readme-polish の emoji 接頭 bullet vs author の emoji 嫌い**
- P#7（fetch 要約、意見）: 「1 emoji + 太字の機能 + 1 行」の bullet を推奨。P#12 も emoji を「beautiful README」の要素に挙げる。P#13 の unil.ink（snippet）は vanity badge 列を AI 生成の水増しの徴候とする。
- author の memory（user-no-emoji-preference。note は引用、本 report は元 memory を再読していない）: 公開物への絵文字装飾を提案しない。視覚区別は色分け・構造で。
- 解決: 競合する証拠ではなく author の明示的な規則で、readme-polish の emoji 規則は移植しない（note も「not transferable」）。eval rubric は emoji を足す fix を許さず、視覚区別を構造（順序・見出し・太字・table・alert）で行う前提になる。badge 数の抑制は readme-polish と unil.ink が部分的に一致するが、どちらも未検証の数値。

**C6. Title Case vs sentence case**
- P#7（fetch 要約）: H2/H3 を Title Case に統一し、sentence と Title の混在は「machine-generated に見える」。P#2（fetch 要約）: 表の**列見出し**は sentence case。
- 整理: 規則の適用先が違う（H2/H3 と table 列見出し）。共通の検査可能な核はドキュメント内の一貫性で、どちらの case かではない（note の整理）。実 README は H2 が `Start here`（sentence）と `At a Glance`（Title）で混在し（§0）、列見出し `Line` / `What it is` / `Canonical record` は sentence case。強さ: どちらも house style（意見）で、混在が読者に与える影響を測った source は無い。

**C7. alert の個数上限: GitHub Docs「1〜2 / 文書」vs readme-polish「主要 section ごとに 1」**
- G:F1（公式 doc、fetch 要約）と P#7（house style、fetch 要約）。hub の README は H2 が 4 つ（§0）なので、readme-polish の規則なら最大 4、Docs の推奨なら 1〜2。公式 doc のほうが根拠が強い（G:F1 を採る材料になるが、採否は lead の判断）。

**C8. 「above the fold / first screen」を前提とする基準 vs 実測のレイアウト**
- P#4（NN/g、最初の 2 段落に重要点）、P#7（10 秒 first-glance、header → badges → nav → hero → tagline）、P#10 / P#13（1 画面、above the fold）は、README が最初の画面を占める前提。
- L4（実測）: desktop では cover + H1 + lead 文 + 自己紹介が最初の 800 px を占め、`Start here` は y=880 で fold の下。mobile では README 全体が最初の 375×812 画面より下（y=901 から）で、`Start here` は y=1563、`At a Glance` は y=2042。desktop の左 sidebar と mobile の積み上げ sidebar（avatar・bio・link）が first screen を共有する。
- したがって「first screen で where-to-go が分かる」を評価するとき、README 冒頭の引用ブロック（lead 文）と自己紹介段落が first screen の担い手になり、`Start here` の見た目の評価は first screen の外（scroll 後）で起きる。基準が満たされるかの判定は測定でなく判断で、note は判断していない。

**C9. 視覚重量の揃え: CSS 上の事実 vs 原則としての根拠**
- G:F3・G:F4（fetch 要約。CSS は生成版）: list は border も背景も無く、table は border + zebra + 太字 header で、「bullet が隣の table より地味」は CSS から説明できる。L4 は table が mobile で横スクロールすることも実測。
- P#14 の行「隣り合う兄弟 section が同じ形式、または形式差が役割差に従う」は note の推論で、source は無い（P#2 の arity 規則、P#5 の chunk 扱い、P#7 からの推論）。「list が blur 下で table より軽く見える」も、P#6 の「囲み = 強いグルーピング」からの note の推論で、markdown について述べた source は無い。X:E1: 隣接視覚重量の揃えを直接検証した研究は無く、heuristic か taste。X:B3・X:A3: 書式の量は人間にも LLM judge にも好まれるので、「list が地味」を失敗とみなすと書式を足す方向に引く。
- 整理: 差があること（CSS の事実）と、差を直すべきこと（原則）は別。後者は taste を明示した author 定義の基準になる（X 総括(8)）。P#2 の arity 規則（3 属性以上 → table）だと、`Start here` の項目（link + 説明）は「context 依存」域でどちらとも決まらない。

**C10. profile 列幅: github-markdown-css の 980 px vs 実測**
- V8・G:F9: wrapper は `max-width:980px; padding:45px`（狭幅で 15px）。G:F10 は「sidebar 分だけ README 列は狭い」と推論（未検証）。
- L4: 実際の profile では `article.markdown-body` が desktop(1280) で 846 px、mobile(375) で 293 px。980 px の前提で local render すると過大。実測が強く、G:F10 の推論を支持する。他の viewport 幅での値は未測。

**C11. Read tool の画像縮小: 観測 2000 px vs doc の上限 2576 px**
- V10（subagent の Read、1 試行）: 2303×1136 の PNG が "displayed at 2000x987" に縮小された。V7（Anthropic doc）: Claude 4.7 以降の長辺上限は 2576 px（20 枚超の request は 2000 px 前後）。
- 食い違いの原因は note から特定できない（harness 側の縮小か version 違いか）。tall 画像は未検査。screenshot 経路を設計する際は 2000 px を安全側の目安にするのが note からの最小の読みだが、1 試行である。

**C12. 軽微な数値・主張の不一致（影響は小さい）**: UIClip の GPT-4V 精度が 51.58%（html fetch）と 52.9%（snippet）で未調整（どちらも chance 付近）。NN/g F-pattern の参加人数が 45+/47（page の抽出）と 232（第三者 snippet）で未調整（基準には影響しない）。AesEval の「reasoning model に優位なし」は reasoning が judge を助けるという通念と食い違うが、1 benchmark・graphic design・via summarizer。X:B2 の snippet の「80% → 51.9%」は abs に無く不採用。G:F5 の `class` 非許可と実在する `markdown-alert` class は、renderer が sanitize 後に付与する（推論）として L2 の出力と整合。

## Still unknown

### 解決済み（local primary checks による。2026-10-06）
- G Still-unknown 1（`POST /markdown` の実出力）: alert の HTML と soft / hard break の差は L1・L2 で解決。相対 link・heading anchor・code の class・未認証での可否・rate limit は報告に無く未解決のまま。
- G Still-unknown 2（profile README 列の px 幅と pinned との上下関係）: 実測値は L4（desktop 846 px / mobile 293 px、README が pinned repos の上）。公式 doc が上下関係を述べるかは未解決（Docs は「profile page の top」とだけ述べる）。
- G:F8 の mode 仮説: alert については逆（C4）。
- G:F3 の table 横スクロール推論: hub の `At a Glance` について mobile で確認（scrollWidth 463 px > client 293 px）。原因（折り返せない long token か cell 幅か）は報告に無い。
- V の「Playwright の有無」: L3 で存在確認（API 名は未検証）。
- V の「github-markdown-css の幅の忠実性」: 980 px は profile では過大（C10）。描画全体（色・余白・badge）の pixel レベルの比較は未実施。

### 未解決
1. **Claude 4.7+ / Opus 5 / Sonnet 5.x が markdown page の screenshot judge として信頼できるか**（人間ラベルとの一致、test-retest）: 全 note で source なし。author 自身のラベルでの local 測定が必要（V synthesis の案）。
2. **README / GitHub profile の見た目を人間または VLM で評価した実証研究**: practice-criteria と adversarial の検索で 0 件。vlm-judge は README 固有の query を未実行。validated な rubric、較正済みの閾値（badge 数、bullet 数、section 数、README 長）も無い。
3. **list と table の相対的な視覚重量**を測る instrument: CSS の事実（G:F3・G:F4）と squint test（P#6）はあるが、blur 実験（両 variant を描画 → blur → 比較）は未実施。L4 は位置と幅の実測で blur ではない。
4. **本文未読の論文**: arXiv 8 本が abs 要約のみ（X:A1〜A4, B1, B2, C1 ほか）。ArtifactsBench の checklist ablation と UICrit の 55% の指標は全文が要る。V1・V2・V3 の数値は要約モデル経由で、決定に使う前に再読する。X:A2 の前半集中と author の観測（後半悪化）の食い違い（C1）が本文で解けるか、X:A1 のラウンド数は未確認。X:B1 の現行 frontier での再現も未確認。
5. **Read tool の tall PNG**（例 390×6000）の上限と可読性は未検査（C11）。tile 分割が要るかは 1 回の試験で決まる。
6. **native app（GitHub Mobile）の README 描画**（alert / `<picture>` / `width` 属性 / table）の現行仕様は一次資料なし。2021 年の community 投稿のみ。
7. **GitHub 本番の allowlist と html-pipeline gem 既定の差**: `style` / `class` / `<center>` 入りの README を API で描画すれば分かる（API は L1・L2 で実行可能と分かったが、この検査自体は未実施）。GFM の「Disallowed Raw HTML」tag list、`dl` / `mark` / `summary` / h3-h6 の CSS 規則本文も未取得。
8. **`<picture>` の `prefers-color-scheme` を GitHub が OS 設定と theme 設定のどちらで評価するか**は未確認。L4 の実測は dark theme・logged-in の 1 view のみ。light theme・未ログインの view、他の viewport 幅での列幅、light 版での table 幅は未測。
9. **github-markdown-css の取得日（release / commit 日）**と現行 GitHub UI とのずれは不明。
10. **人間の pairwise 比較が絶対 rubric より信頼できる**という一次資料（LLM judge 側の資料のみ）、5 秒テスト / first-click test の README・OSS ドキュメントへの適用例（未検索）、Nielsen の consistency heuristic の一次資料（未 fetch）、design-system 的な機械ルール（lint / 構造規約）で judge を置き換える案の実証（未検索）。
11. **profile README repo の views が profile ページ描画を含むか**（docs に記載なし、未確認）。traffic の母数は 1 日数件で、見た目変更の効果を検出するには足りない（X:F2）。
12. **未読の source**: Diátaxis（reference と how-to の区別が「navigation list vs reference table」の役割に効くか、未検証）、Medium/uxdesign の profile README 設計記事（403）、hub 型 profile README を持つ著名 maintainer の設計理由を述べた first-person 記事（見つからず）。
13. **bilingual（EN+JA）ペアの視覚基準**: どの source にも無い（P#14 末尾の整理）。README.ja.md の描画は未測定・未読。ペアで見た目を揃える検査は本調査から根拠を引けない。
14. **Playwright の宣言済み dependency 化**: L3 で既存確認のみ。readme-writer の dependency intake は未実施。API 名（`color_scheme`、`device_scale_factor`、`full_page`）は V11 のとおり未照合。
15. **出典不明の二次主張**: digitalapplied の「14/15 を VLM が perfect と評価」（候補 arXiv 2607.11598、未 fetch）、X:B2 の「80% → 51.9%」。

### 失効条件（notes から）
- 描画仕様（G）: GitHub が markdown pipeline か Primer を変えるまで。API version（`2026-03-10`）が上がったとき、または github-markdown-css に更新が入ったとき。README 描画の検証を回す前に、L1・L2 の再実行と L4 の再実測で現状を確かめる。
- 基準（P）: README 固有の視覚研究、または GitHub の描画変更が出たとき。NN/g の scan 研究は 2004〜2019 年、実験は 1997 年で、2026 年の GitHub markdown の描画や LLM / VLM judge による読みを検証したものではない。
- judge の信頼性（V・X）: 引用論文は 2024〜2026 年のモデルで、現行 Claude の世代で再測定したとき。
