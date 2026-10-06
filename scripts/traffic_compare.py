"""Read-only views.count aggregation for fixed traffic cohorts."""
import argparse
from datetime import date, timedelta
import json
from pathlib import Path

LEGACY = (
    "contemplative-agent", "agent-knowledge-cycle", "agent-attribution-practice",
    "authorship-strategy", "attention-not-self", "contemplative-agent-data",
    "zenn-content", "claude-harness", "shimo4228",
)
ADDITIONAL = (
    "search-first", "skill-stocktake", "codex-review", "readme-writer",
    "llms-txt-writer", "harness-pruning",
)
GROUPS = {
    "legacy": LEGACY,
    "additional": ADDITIONAL,
    "claude-harness": ("claude-harness",),
    "total_reference": LEGACY + ADDITIONAL,
}


def aggregate(data_dir, start, end):
    if not data_dir.is_dir():
        raise ValueError(f"not a data directory: {data_dir}")
    records = {}
    for repo in LEGACY + ADDITIONAL:
        path = data_dir / f"{repo}.jsonl"
        records[repo] = {}
        if path.exists():
            for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                if not line.strip():
                    continue
                try:
                    row = json.loads(line)
                    day = parse_date(row["date"]).isoformat()
                    count = row["views"]["count"]
                    if type(count) is not int or count < 0:
                        raise ValueError("views.count must be a nonnegative integer")
                except (ValueError, KeyError, TypeError) as exc:
                    raise ValueError(f"{path}:{number}: invalid record: {exc}") from exc
                if day in records[repo]:
                    raise ValueError(f"{path}:{number}: duplicate date {day}")
                records[repo][day] = count
    days = [(start + timedelta(days=i)).isoformat()
            for i in range((end - start).days + 1)]
    groups = {}
    for name, repos in GROUPS.items():
        missing = {repo: [day for day in days if day not in records[repo]]
                   for repo in repos}
        missing = {repo: dates for repo, dates in missing.items() if dates}
        count = sum(records[repo][day] for repo in repos for day in days
                    if day in records[repo])
        expected = len(repos) * len(days)
        groups[name] = {
            "repos": list(repos), "complete": not missing,
            "views_count": None if missing else count,
            "partial_views_count": count,
            "expected_repo_days": expected,
            "observed_repo_days": expected - sum(map(len, missing.values())),
            "missing_files": [repo for repo in repos
                              if not (data_dir / f"{repo}.jsonl").exists()],
            "missing_dates": missing,
        }
    return {"start": start.isoformat(), "end": end.isoformat(),
            "timezone": "UTC", "inclusive": True, "days": len(days), "groups": groups}


def parse_date(value):
    parsed = date.fromisoformat(value)
    if parsed.isoformat() != value:
        raise ValueError("date must use YYYY-MM-DD")
    return parsed


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path,
                        default=Path(__file__).resolve().parents[1] / "traffic/data")
    parser.add_argument("--start", required=True, type=parse_date)
    parser.add_argument("--end", required=True, type=parse_date)
    args = parser.parse_args()
    if args.start > args.end:
        parser.error("--start must be on or before --end")
    try:
        result = aggregate(args.data_dir, args.start, args.end)
    except (ValueError, OSError) as exc:
        parser.error(str(exc))
    print(json.dumps(result, indent=2))
    return 0 if all(group["complete"] for group in result["groups"].values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
