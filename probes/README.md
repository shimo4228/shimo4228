# LLM Probe Data

Scheduled two-channel probes of frontier LLMs, measuring whether the ideas
and identifiers of [@shimo4228](https://github.com/shimo4228)'s research
ecosystem surface in model answers — and whether the author surfaces with them.

This is the measurement instrument that
[authorship-strategy ADR-0008](https://github.com/shimo4228/authorship-strategy/blob/main/docs/adr/0008-rag-era-attribution-diffusion.md)
calls for: attribution diffusion runs on two channels with different time
constants, and each channel needs its own probe. The protocol is recorded as
ADR-0011 in the same repository.

## Two channels, two probes

| Channel | Probe | Web search | Question asked | Failure mode measured |
|---|---|---|---|---|
| **Parametric** | retrieval-suppressed naming probe | OFF | "What is concept X? Who maintains it?" | concept absent from trained knowledge, or present without the author |
| **Retrieval** | search-grounded citation probe | ON | "Cite sources on topic Y with URLs and authors" | **ghost citation** — owned URL/DOI cited, author never named |

The channels are never blended into one score. A single blended metric hides
which channel is failing (ADR-0008).

Since probe set v2, **every prompt runs on both settings (A/B)**: the
per-question delta between arms isolates what retrieval adds with the
question held fixed. Two derived controls come free: citation-eliciting
prompts on the suppressed arm measure citations-from-memory
(hallucinated-citation floor), and the negative-control prompt on the
enabled arm measures grounded confabulation. A parametric arm is frozen per
model snapshot, so one parametric measurement pairs with every retrieval
run of that snapshot — the arms keep separate cadences.

## What one record contains

One JSON object per line in `data/parametric.jsonl` / `data/retrieval.jsonl`,
one line per (run × provider × probe). Key fields:

- `response_text` — the raw model answer, kept verbatim so detection can be
  re-run when the lexicon changes (`detect.detector_version` marks which
  lexicon produced a stored verdict)
- `cited_urls` + `citation_source` — `provider_metadata` when URLs come from
  the provider's citation/grounding fields, `text_regex` when regex-extracted
  from prose (weaker provenance, visible in the data rather than silent)
- `detect.author_named` / `detect.project_named` / `detect.doi_or_url_cited`
  — independent booleans; `detect.ghost_citation` is derived
  (`cited && !author_named`) and always re-derivable
- `model_requested` vs `model_returned` — makes silent snapshot drift visible
- `probe_set_version` + `prompt_sha256` — prompt-set changes are series
  breaks, never silent edits

Detection is deterministic string/regex matching (auditable), not LLM judging.
`author_named` means named **in prose**: an author handle visible only inside
a cited URL is exactly the ghost-citation scenario and does not count.

## How NOT to read this

- **Self-contamination**: this log is public and contains the coined terms and
  the author's name. Future training runs may ingest it, so the instrument
  feeds the very channel it measures. That is simultaneously a measurement
  confound and an on-thesis act of diffusion; it is stated rather than hidden.
- **Leading questions**: concept-recognition prompts presuppose the concept
  exists, and models confabulate agreeably. The negative-control probe (a
  plausible fake concept) quantifies that noise floor — read true-positive
  rates against it.
- **N=1**: one author's ecosystem, a handful of probes, five providers.
  Preliminary observations, not evidence.

## Running

```bash
cd runner
uv sync
uv run pytest                 # detectors, zero API calls
uv run probe_runner.py --dry-run
cp ../.env.example ../.env    # fill in API keys (git-ignored)
uv run probe_runner.py --provider anthropic --probe parametric-concept-akc  # smoke
uv run probe_runner.py --channel retrieval            # weekly retrieval run
uv run probe_runner.py --channel parametric --repeat 3  # model-entry event run
uv run probe_runner.py --currency-check               # monthly change-event detector
```

Cost guard: the runner aborts if a run exceeds `--cost-ceiling` (default $2).

## Scheduling

Scheduled locally via launchd (`scripts/run-weekly-retrieval.sh`, Sundays
10:17 JST; `scripts/run-monthly-currency.sh`, 1st of the month 10:47 JST —
a slot missed while the machine sleeps runs at the next wake, and every
record carries its own timestamp). The two channels are scheduled
differently:

- **Retrieval — weekly calendar cadence.** The citation pool's entry and
  decay dynamics move in days, even against frozen models.
- **Parametric — event-driven.** A frozen model's weights cannot change
  between runs, so re-probing the same model only measures response
  variance; the parametric signal lives *across model generations*. The
  full parametric set runs with `--repeat 3` (within-model variance) when
  a model enters the panel or is observed to have changed.
- **Currency check — monthly calendar cadence** (`--currency-check`). The
  change-event detector that makes the event-driven design workable:
  1. *silent-swap detection* — one minimal call per provider, comparing the
     served model identity (`model_returned`) against the last observation
     (non-dated aliases like `gpt-5.5` can be re-pointed silently);
  2. *catalog diff* — each provider's model-list endpoint is snapshotted to
     `data/model-catalog.jsonl` and diffed; new chat-family ids are
     reported (detection is automated, panel adoption stays a human
     judgment — which model is the widely-served default tier is a
     product-side fact no API reports);
  3. *staleness guard* — flags when `verified_current` in the config is
     older than `staleness_days` (default 90), forcing a periodic human
     re-verification of the default-tier choice.

  `--strict` makes change events exit non-zero, for scheduled runs.

Analysis convention: time series are segmented by `model_returned`. A model
change is an expected event, not contamination — cross-generation comparison
is the parametric channel's primary signal.

## License

CC0 1.0 for the compilation, same as [`../traffic/`](../traffic/). Model
outputs remain subject to each provider's terms.
