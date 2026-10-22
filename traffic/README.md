# Traffic Data

Daily snapshots of the GitHub Traffic API for the public repositories listed below by [@shimo4228](https://github.com/shimo4228).

**Dashboard**: [shimo4228.github.io/shimo4228/traffic/dashboard/](https://shimo4228.github.io/shimo4228/traffic/dashboard/) — the repos in its `REPOS` list on one page, built for phones: four metrics (unique visitors, views, unique cloners, clones) over 30 days / 90 days / all time, a daily chart, an all-time calendar, a sortable repo list with a per-repo chart, the raw table, and the attribution probes.

## What

Append-only JSONL time series under `data/`, one file per repository:

- [contemplative-agent](https://github.com/shimo4228/contemplative-agent)
- [agent-knowledge-cycle](https://github.com/shimo4228/agent-knowledge-cycle)
- [agent-attribution-practice](https://github.com/shimo4228/agent-attribution-practice)
- [authorship-strategy](https://github.com/shimo4228/authorship-strategy)
- [attention-not-self](https://github.com/shimo4228/attention-not-self)
- [contemplative-agent-data](https://github.com/shimo4228/contemplative-agent-data)
- [zenn-content](https://github.com/shimo4228/zenn-content)
- [claude-harness](https://github.com/shimo4228/claude-harness) (public Claude Code harness — skills / agents / rules)
- [shimo4228](https://github.com/shimo4228/shimo4228) (this profile repo)

Snapshot only (not on the dashboard; added 2026-10-06): the skill repositories exported from claude-harness and its retirement ledger —
[search-first](https://github.com/shimo4228/search-first), [skill-stocktake](https://github.com/shimo4228/skill-stocktake), [codex-review](https://github.com/shimo4228/codex-review), [readme-writer](https://github.com/shimo4228/readme-writer), [llms-txt-writer](https://github.com/shimo4228/llms-txt-writer), [harness-pruning](https://github.com/shimo4228/harness-pruning).

Added 2026-10-07: repositories submitted to external lists such as awesome lists. Four of them (harness-scope, jev-skill-router, jev-research-pipeline, akc-cycle) are also on the dashboard; the rest are snapshot only. The `repos` array in [`.github/workflows/traffic-daily.yml`](../.github/workflows/traffic-daily.yml) is the full list of collected repositories.

GitHub's Traffic API only retains the last 14 days. Snapshotting daily accumulates a long-term record that is otherwise unrecoverable.

## Why public

Openness is one axis of the AI-era authenticity stance behind these projects (scarcity → diffusion, exclusivity → derivation, **enclosure → openness**). Publishing the observation log is consistent with publishing the work being observed. It also gives anyone studying AI-mediated discovery (LLMs, RAG indexers, AI coding assistants) a concrete data point on idea-rescue research repositories.

## What's observable here

Placing the repos side-by-side surfaces signals that look like noise on any single repo, but resolve into cross-repo structural patterns:

- **Bot/crawler dominance**: in the first two weeks of snapshots (to 2026-05-05), clones:views ratios exceeded 30:1 across the research repos, and the profile repo ([shimo4228](https://github.com/shimo4228/shimo4228)) had 80 clones against 0 views — nobody was *reading* it, but something was *cloning* it. The ratio has fallen since as human views grew; the dashboard's Clones / view column shows the current value per repo.
- **Cross-repo crawler waves**: clones spike simultaneously across multiple repos on the same dates. Article publication days appear to trigger walk-throughs of the entire portfolio (not single-repo events).
- **Visibility scarcity (admin-only)**: GitHub's Traffic clone counts are returned only to users with push access. Other repositories' clone behavior is invisible in both the UI and the public API. Longitudinal public datasets of personal-repo clone behavior are therefore essentially absent in the wild. Unlike stars / forks / watchers, clones cannot be counted from the outside.
- **Temporal scarcity**: even for one's own repo, the API returns only the last 14 days. The moment snapshotting stops, the past becomes unrecoverable.

Read this as a field record of AI-mediated discovery, not as marketing numbers. The dual scarcity — past data lost without continuous snapshotting (temporal) × clone counts hidden from non-admins (visibility) — makes this CC0 log a rare reference point both for someone tracing how this portfolio was discovered one or three years from now, and for any researcher who wants quantitative data on personal-repo clone behavior from outside the admin boundary.

## How NOT to read this

Short-term variation (one to two weeks) carries little human signal. The first analysis (snapshots to 2026-05-05) found:

- clone:view ratios of 30:1 to 215:1 — most access was non-human then; the ratio has fallen since, so read the current value on the dashboard
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

## Referrers (added 2026-10-11)

`referrers/<repo>.jsonl` holds one line per daily run with the referrers the
Traffic API reports for that repository:

```json
{"date":"2026-10-12","window_days":14,"referrers":[{"referrer":"github.com","count":7,"uniques":3}],"fetched_at":"2026-10-12T00:30:40Z"}
```

The API returns referrers only as a **rolling 14-day aggregate**, so
consecutive lines overlap; they are snapshots of a window, not daily counts.
Referrers describe page views only — the API gives no origin for clones,
which remain arrivals of unknown route. The series starts on 2026-10-11;
human-route page views had become a meaningful share only from 2026-09, so
there is no earlier baseline to compare with. In the authorship-strategy
framework these are arrival proxies, reported in the proxy tier (ADR-0024).

## Stars and followers (added 2026-10-22)

`stars.jsonl` holds one line per UTC day: the star and fork counts of every
public repository the account owns (forks left out) and the follower count,
from `scripts/stars_snapshot.py`. GitHub keeps only the current star count, so
this daily line is what makes a weekly change readable.

```json
{"date":"2026-10-22","followers":63,"repos":{"contemplative-agent":{"stars":12,"forks":1}},"fetched_at":"2026-10-22T00:31:05+00:00"}
```

## Weekly summary (added 2026-10-22)

[`weekly/`](weekly/) gets one page every Monday for the week before (Monday to
Sunday, UTC), written by [`.github/workflows/weekly-summary.yml`](../.github/workflows/weekly-summary.yml)
with `scripts/weekly_summary.py`. It puts side by side: visits to the personal
site <https://shimo4228.github.io/> (Cloudflare Web Analytics, when the
`CF_API_TOKEN` / `CF_ACCOUNT_ID` / `CF_SITE_TAG` secrets are set), GitHub views
per repository, stars and followers, the 14-day referrers, and the
hand-collected Zenn / Dev.to numbers from zenn-content
`scripts/metrics/snapshots.jsonl`. It states numbers and dates only and draws
no conclusions; read it with "How NOT to read this" above. A source that is
missing is named as missing, never shown as zero.

## Cadence

Daily at UTC 00:30 via [`.github/workflows/traffic-daily.yml`](../.github/workflows/traffic-daily.yml).

## License

CC0 1.0 — public domain dedication. Same openness as the data itself.
