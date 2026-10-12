"""Read-only four-way split of repository referrers for one monthly reading.

The daily CI step stores, per repository, the Traffic API's rolling 14-day
referrer list (top referrers only) in traffic/referrers/<repo>.jsonl. Daily
snapshots overlap, so a reading never adds them up day by day. It takes the
latest snapshot on or before --as-of and the latest one at least 14 days
before that, so the two windows do not overlap, and sums `count` per bucket:

  ai      AI answer engines (an explicit domain list)
  search  search engines (the API's own labels plus search domains)
  github  github.com itself (profile, other repositories, GitHub search)
  other   every other referrer (social posts, articles, unknown sites)

`uniques` is not summed: it is deduplicated per repository and window, so a
sum across them double counts. Stdlib only.
"""
import argparse
from collections import Counter, defaultdict
from datetime import date, timedelta
import json
from pathlib import Path
import subprocess
import sys

WINDOW_DAYS = 14
AI_DOMAINS = {
    "chatgpt.com", "chat.openai.com", "openai.com",
    "perplexity.ai", "www.perplexity.ai",
    "claude.ai",
    "copilot.microsoft.com",
    "gemini.google.com", "bard.google.com",
    "you.com", "phind.com", "poe.com", "meta.ai", "www.meta.ai",
    "grok.com", "chat.deepseek.com", "chat.mistral.ai", "duck.ai",
}
SEARCH_LABELS = {"Google", "Bing", "Yahoo", "DuckDuckGo", "Baidu", "Yandex"}
SEARCH_DOMAINS = {
    "search.brave.com", "ecosia.org", "www.ecosia.org", "startpage.com",
    "www.startpage.com", "kagi.com", "search.yahoo.co.jp", "search.naver.com",
    "yandex.ru", "yandex.com", "baidu.com", "www.baidu.com", "www.bing.com",
    "www.google.com", "duckduckgo.com",
}
BUCKETS = ("ai", "search", "github", "other")


def classify(referrer):
    name = referrer.strip()
    host = name.lower()
    if host in AI_DOMAINS:
        return "ai"
    if name in SEARCH_LABELS or host in SEARCH_DOMAINS:
        return "search"
    if host == "github.com":
        return "github"
    return "other"


def read_working_tree(data_dir):
    if not data_dir.is_dir():
        raise ValueError(f"not a data directory: {data_dir}")
    return {p.stem: p.read_text(encoding="utf-8") for p in sorted(data_dir.glob("*.jsonl"))}


def read_git_ref(repo_root, ref, rel_dir):
    def git(*args):
        return subprocess.run(
            ["git", "-C", str(repo_root), *args],
            check=True, capture_output=True, text=True,
        ).stdout
    names = [n for n in git("ls-tree", "--name-only", ref, f"{rel_dir}/").splitlines() if n.endswith(".jsonl")]
    return {Path(n).stem: git("show", f"{ref}:{n}") for n in names}


def parse_rows(texts):
    """{repo: {date: [referrer dicts]}}; later duplicate dates win."""
    rows = defaultdict(dict)
    for repo, text in texts.items():
        for number, line in enumerate(text.splitlines(), 1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
                day = date.fromisoformat(row["date"])
                refs = row["referrers"]
                if not isinstance(refs, list):
                    raise ValueError("referrers must be a list")
            except (KeyError, ValueError, TypeError) as exc:
                raise ValueError(f"{repo}.jsonl line {number}: {exc}") from exc
            rows[repo][day] = refs
    return rows


def pick_windows(snapshot_dates, as_of):
    """Latest snapshot <= as_of, then the latest <= that minus 14 days."""
    first = max((d for d in snapshot_dates if d <= as_of), default=None)
    if first is None:
        return []
    picked = [first]
    second = max((d for d in snapshot_dates if d <= first - timedelta(days=WINDOW_DAYS)), default=None)
    if second is not None:
        picked.append(second)
    return sorted(picked)


def split(rows, as_of):
    dates = {d for per_repo in rows.values() for d in per_repo}
    windows = pick_windows(dates, as_of)
    totals = Counter({b: 0 for b in BUCKETS})
    by_referrer = {b: Counter() for b in BUCKETS}
    missing = []
    for window in windows:
        for repo in sorted(rows):
            refs = rows[repo].get(window)
            if refs is None:
                missing.append(f"{repo}@{window.isoformat()}")
                continue
            for item in refs:
                count = item.get("count")
                if type(count) is not int or count < 0:
                    raise ValueError(f"{repo}@{window}: count must be a nonnegative integer")
                bucket = classify(str(item.get("referrer", "")))
                totals[bucket] += count
                by_referrer[bucket][item.get("referrer")] += count
    return {
        "as_of": as_of.isoformat(),
        "windows": [
            {"start": (w - timedelta(days=WINDOW_DAYS - 1)).isoformat(), "end": w.isoformat()}
            for w in windows
        ],
        "totals": {b: totals[b] for b in BUCKETS},
        "total": sum(totals.values()),
        "top": {b: by_referrer[b].most_common(3) for b in BUCKETS},
        "repos": len(rows),
        "missing": missing,
    }


def to_markdown_row(result):
    windows = ", ".join(f"{w['start']} to {w['end']}" for w in result["windows"]) or "none"
    t = result["totals"]
    def top(bucket):
        return ", ".join(f"{name} {n}" for name, n in result["top"][bucket]) or "—"
    note = f"{result['repos']} repositories"
    if result["missing"]:
        note += f"; {len(result['missing'])} repository-windows missing"
    return (
        f"| {result['as_of']} | {windows} | {t['ai']} ({top('ai')}) | {t['search']} ({top('search')}) "
        f"| {t['github']} | {t['other']} ({top('other')}) | {result['total']} | {note} |"
    )


def main(argv=None):
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description="Four-way split of repository referrers for one monthly reading.")
    parser.add_argument("--as-of", required=True, type=date.fromisoformat)
    parser.add_argument("--data-dir", type=Path, default=root / "traffic/referrers")
    parser.add_argument("--git-ref", help="read the data from this ref (e.g. origin/main) instead of the working tree")
    parser.add_argument("--format", choices=("md", "json"), default="md")
    args = parser.parse_args(argv)
    try:
        if args.git_ref:
            texts = read_git_ref(root, args.git_ref, "traffic/referrers")
        else:
            texts = read_working_tree(args.data_dir)
        result = split(parse_rows(texts), args.as_of)
    except (ValueError, subprocess.CalledProcessError) as exc:
        print(f"referrer_split: {exc}", file=sys.stderr)
        return 1
    if not result["windows"]:
        print(f"referrer_split: no snapshot on or before {args.as_of}", file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False) if args.format == "json" else to_markdown_row(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
