"""Append today's stars, forks and followers to traffic/stars.jsonl.

GitHub keeps only the current star count, so a weekly change needs a daily
record. One line per UTC day: every public repository the account owns (forks
left out) and the follower count. A second run on the same day replaces that
day's line. Stdlib only; GITHUB_TOKEN raises the rate limit but is optional,
since all of this is public.
"""
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import sys
import urllib.request

OWNER = "shimo4228"
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "traffic" / "stars.jsonl"


def get(url):
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json", "User-Agent": OWNER})
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def snapshot():
    repos = {}
    page = 1
    while True:
        batch = get(f"https://api.github.com/users/{OWNER}/repos?type=owner&per_page=100&page={page}")
        for r in batch:
            if not r.get("fork") and not r.get("private"):
                repos[r["name"]] = {"stars": r["stargazers_count"], "forks": r["forks_count"]}
        if len(batch) < 100:
            break
        page += 1
    user = get(f"https://api.github.com/users/{OWNER}")
    now = datetime.now(timezone.utc)
    return {
        "date": now.date().isoformat(),
        "followers": user["followers"],
        "repos": dict(sorted(repos.items())),
        "fetched_at": now.isoformat(timespec="seconds"),
    }


def merge(lines, row):
    kept = [l for l in lines if l.strip() and json.loads(l).get("date") != row["date"]]
    return kept + [json.dumps(row, ensure_ascii=False, separators=(",", ":"))]


def main():
    row = snapshot()
    lines = OUT.read_text(encoding="utf-8").splitlines() if OUT.exists() else []
    OUT.write_text("\n".join(merge(lines, row)) + "\n", encoding="utf-8")
    print(f"{row['date']}: {len(row['repos'])} repos, {sum(r['stars'] for r in row['repos'].values())} stars, "
          f"{row['followers']} followers")
    return 0


if __name__ == "__main__":
    sys.exit(main())
