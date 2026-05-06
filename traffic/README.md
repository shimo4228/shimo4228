# Traffic Data

Daily snapshots of the GitHub Traffic API for six public research repositories by [@shimo4228](https://github.com/shimo4228).

**Dashboard**: [shimo4228.github.io/shimo4228/traffic/dashboard/](https://shimo4228.github.io/shimo4228/traffic/dashboard/) — all six repos on one page (aggregate timeline, per-repo small multiples, clones:views ratio, raw table).

## What

Append-only JSONL time series under `data/`, one file per repository:

- [contemplative-agent](https://github.com/shimo4228/contemplative-agent)
- [agent-knowledge-cycle](https://github.com/shimo4228/agent-knowledge-cycle)
- [agent-attribution-practice](https://github.com/shimo4228/agent-attribution-practice)
- [contemplative-agent-data](https://github.com/shimo4228/contemplative-agent-data)
- [zenn-content](https://github.com/shimo4228/zenn-content)
- [shimo4228](https://github.com/shimo4228/shimo4228) (this profile repo)

GitHub's Traffic API only retains the last 14 days. Snapshotting daily accumulates a long-term record that is otherwise unrecoverable.

## Why public

Openness is one axis of the AI-era authenticity stance behind these projects (scarcity → diffusion, exclusivity → derivation, **enclosure → openness**). Publishing the observation log is consistent with publishing the work being observed. It also gives anyone studying AI-mediated discovery (LLMs, RAG indexers, AI coding assistants) a concrete data point on idea-rescue research repositories.

## What's observable here

Placing six repos side-by-side surfaces signals that look like noise on any single repo, but resolve into cross-repo structural patterns:

- **Bot/crawler dominance**: clones:views ratios exceed 30:1 across all six repos. The profile repo ([shimo4228](https://github.com/shimo4228/shimo4228)) has 80 clones against 0 views — nobody is *reading* it, but something is *cloning* it.
- **Cross-repo crawler waves**: clones spike simultaneously across multiple repos on the same dates. Article publication days appear to trigger walk-throughs of the entire portfolio (not single-repo events).
- **Visibility scarcity (admin-only)**: GitHub's Traffic clone counts are returned only to users with push access. Other repositories' clone behavior is invisible in both the UI and the public API. Longitudinal public datasets of personal-repo clone behavior are therefore essentially absent in the wild. Unlike stars / forks / watchers, clones cannot be counted from the outside.
- **Temporal scarcity**: even for one's own repo, the API returns only the last 14 days. The moment snapshotting stops, the past becomes unrecoverable.

Read this as a field record of AI-mediated discovery, not as marketing numbers. The dual scarcity — past data lost without continuous snapshotting (temporal) × clone counts hidden from non-admins (visibility) — makes this CC0 log a rare reference point both for someone tracing how this portfolio was discovered one or three years from now, and for any researcher who wants quantitative data on personal-repo clone behavior from outside the admin boundary.

## How NOT to read this

Short-term variation (one to two weeks) carries little human signal. Prior analysis found:

- clone:view ratios of 30:1 to 215:1 — most access is non-human
- article publication days create cross-repo crawler waves, not single-repo events
- README keyword edits do not move the numbers at observable scale

Treat this as a long-term observation log, not a marketing dashboard.

## Schema

One JSON object per line:

```json
{"date":"2026-05-05","clones":{"count":130,"uniques":42},"views":{"count":7,"uniques":5},"fetched_at":"2026-05-06T00:30:12Z"}
```

| Field | Source | Meaning |
|---|---|---|
| `date` | API `timestamp` (UTC midnight) | Aggregation date |
| `clones.count` | `/traffic/clones` `count` | Total clones (duplicates included) |
| `clones.uniques` | `/traffic/clones` `uniques` | Unique cloners |
| `views.count` | `/traffic/views` `count` | Total page views |
| `views.uniques` | `/traffic/views` `uniques` | Unique visitors |
| `fetched_at` | Workflow runtime (ISO 8601) | Snapshot capture time |

Repository identity is encoded in the filename, not in the line.

## Cadence

Daily at UTC 00:30 via [`.github/workflows/traffic-daily.yml`](../.github/workflows/traffic-daily.yml).

## License

CC0 1.0 — public domain dedication. Same openness as the data itself.
