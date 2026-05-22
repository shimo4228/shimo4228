# shimo4228 (hub repo)

This repo is a **hub**, not a source of truth. Its README / `llms.txt` / `llms-full.txt` aggregate links to the five independently-evolving research lines — three agent-design lines (AKC / Contemplative Agent / AAP) and two cross-cutting lines (Authorship Strategy / Attention Not Self) — and the supporting ecosystem.

## Design rules for hub content

1. **No volatile state**. Do not put software versions, test counts, exact ADR/skill counts, or evolving skill-name enumerations here. Each line releases on its own cadence; replicating volatile state forces sync work and produces drift (e.g. `8 ADR ↔ 10 ADR` reversal between AKC and AAP). State queries → click-through to the line repo.

2. **Concept DOIs only**. All Zenodo links must use the **concept DOI** (parent record, always resolves to the latest version), never a version-specific DOI. Current concept DOIs:
   - AKC: `10.5281/zenodo.19200726`
   - Contemplative Agent: `10.5281/zenodo.19212118`
   - AAP: `10.5281/zenodo.19652013`
   - Authorship Strategy: `10.5281/zenodo.20263316`
   - Attention Not Self: `10.5281/zenodo.20262112`

3. **Describe what something *is*, not what state it's *in***. Stable architectural facts (`three-layer structure`, `six-phase loop`, `local 9B stack on Apple Silicon`, `prohibition-strength hierarchy`, `Four Business AI Quadrants`) are fine. Counts, versions, enumerations of churning sets are not.

4. **Supporting repos table = membership only**. Add/remove a row when an ecosystem repo is added/retired. Do not edit the row's description for routine line releases.

## When *should* this hub be touched

- A **new structural concept** appears in a line (e.g. AAP added `Four Business AI Quadrants` — that earned a 1-句 mention).
- An **ecosystem repo** is added or retired.
- A **new research line** starts.
- The 3 concept DOIs themselves move (rare; only if a record is restructured on Zenodo).

Routine `vX.Y.Z` releases of any line should require **zero edits** here.

The `graph.jsonld` artifact follows the same triggers: a new `Concept`, `EcosystemRepo`, or `ResearchLine` adds the corresponding node and edges; nothing else does. The schema has no fields for versions, counts, or enumerations of churning sets, so routine releases cannot leak into the graph even by accident.

## Files in scope

- `README.md` / `README.ja.md` — human-facing hub
- `llms.txt` / `llms-full.txt` — AI-facing hub (Answer.AI llms.txt standard)
- `index.html` — redirect to traffic dashboard, no DOI/state references
- `traffic/` — auto-generated dashboard, do not hand-edit

## Language pair

`README.md` and `README.ja.md` must stay structurally synchronized — same sections, same number of DOI mentions, same ecosystem table rows. Quick check:

```bash
diff <(grep -c "doi.org/10.5281" README.md) <(grep -c "doi.org/10.5281" README.ja.md)
```

## Authority delegation

For each line, the source of truth is its own repo:

| Line | Source of truth |
|---|---|
| AKC structure / ADR list | `github.com/shimo4228/agent-knowledge-cycle` |
| Contemplative agent state / phase mapping | `github.com/shimo4228/contemplative-agent` |
| AAP ADRs / Quadrants details | `github.com/shimo4228/agent-attribution-practice` |
| Authorship Strategy thesis / ADRs / empirical baseline | `github.com/shimo4228/authorship-strategy` |
| Attention Not Self essays / knowledge graph (~238 nodes) | `github.com/shimo4228/attention-not-self` |

When in doubt about a fact, link to the source repo rather than transcribing.

## HF Datasets mirror

`graph.jsonld` is mirrored on Hugging Face Datasets (primary ingest source for LLM training pipelines and knowledge-graph crawlers; auto-converted to Parquet, loadable directly from `pandas` / `Polars`). Sync via the `hf-sync` skill: run `/hf-sync <Owner/dataset>` (or `bash ~/.claude/skills/hf-sync/sync.sh <Owner/dataset>`) from the project root, typically as the last step of the `release-doi` flow after `gh release create`. Local-only — uses the user's `hf login` token, no CI auth required.

Repo mapping:

| GitHub | HF dataset |
|---|---|
| `shimo4228/shimo4228` ← **this repo** (hub) | [`Shimo4228/research-program-hub`](https://huggingface.co/datasets/Shimo4228/research-program-hub) |
| `shimo4228/agent-knowledge-cycle` | [`Shimo4228/agent-knowledge-cycle`](https://huggingface.co/datasets/Shimo4228/agent-knowledge-cycle) |
| `shimo4228/contemplative-agent` (local clone: `contemplative-moltbook/`) | [`Shimo4228/contemplative-agent`](https://huggingface.co/datasets/Shimo4228/contemplative-agent) |
| `shimo4228/agent-attribution-practice` | [`Shimo4228/agent-attribution-practice`](https://huggingface.co/datasets/Shimo4228/agent-attribution-practice) |
| `shimo4228/authorship-strategy` | [`Shimo4228/authorship-strategy`](https://huggingface.co/datasets/Shimo4228/authorship-strategy) |
| `shimo4228/attention-not-self` | [`Shimo4228/attention-not-self`](https://huggingface.co/datasets/Shimo4228/attention-not-self) |

The HF-side `README.md` (dataset card) is HF-customized (mirror notice, cross-links to sibling datasets) and is not synced from this repo on graph updates. To edit the dataset card, manually run `hf upload Shimo4228/research-program-hub README.md --repo-type dataset`.

The HF hub dataset (`research-program-hub`) plays the same federation role for the HF side as this GitHub repo plays for the GitHub side: an entry point that lets crawlers hop between the three sibling lines. Keep both ends in sync conceptually even though file contents differ.
