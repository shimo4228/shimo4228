# shimo4228 (hub repo)

This repo is a **hub**, not a source of truth. Its README / `llms.txt` / `llms-full.txt` aggregate links to the three independently-evolving research lines (AKC / Contemplative Agent / AAP) and the supporting ecosystem.

## Design rules for hub content

1. **No volatile state**. Do not put software versions, test counts, exact ADR/skill counts, or evolving skill-name enumerations here. Each line releases on its own cadence; replicating volatile state forces sync work and produces drift (e.g. `8 ADR ↔ 10 ADR` reversal between AKC and AAP). State queries → click-through to the line repo.

2. **Concept DOIs only**. All Zenodo links must use the **concept DOI** (parent record, always resolves to the latest version), never a version-specific DOI. Current concept DOIs:
   - AKC: `10.5281/zenodo.19200726`
   - Contemplative Agent: `10.5281/zenodo.19212118`
   - AAP: `10.5281/zenodo.19652013`

3. **Describe what something *is*, not what state it's *in***. Stable architectural facts (`three-layer structure`, `six-phase loop`, `local 9B stack on Apple Silicon`, `prohibition-strength hierarchy`, `Four Business AI Quadrants`) are fine. Counts, versions, enumerations of churning sets are not.

4. **Supporting repos table = membership only**. Add/remove a row when an ecosystem repo is added/retired. Do not edit the row's description for routine line releases.

## When *should* this hub be touched

- A **new structural concept** appears in a line (e.g. AAP added `Four Business AI Quadrants` — that earned a 1-句 mention).
- An **ecosystem repo** is added or retired.
- A **new research line** starts.
- The 3 concept DOIs themselves move (rare; only if a record is restructured on Zenodo).

Routine `vX.Y.Z` releases of any line should require **zero edits** here.

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

When in doubt about a fact, link to the source repo rather than transcribing.
