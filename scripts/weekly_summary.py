"""Write the weekly one-page summary: traffic/weekly/<week end>.md.

One page per week (Monday to Sunday, UTC) that puts the numbers collected
elsewhere side by side, so the week can be read without opening five
dashboards. It reads, never collects:

  traffic/data/<repo>.jsonl       GitHub views per repository (daily CI)
  traffic/referrers/<repo>.jsonl  GitHub referrers, rolling 14 days (daily CI)
  traffic/stars.jsonl             stars per repository and followers (daily CI)
  --zenn FILE                     zenn-content scripts/metrics/snapshots.jsonl
                                  (Zenn likes, Zenn dashboard views, Dev.to
                                  views, followers; collected by hand)
  --site FILE                     JSON from scripts/cf_web_analytics.py
                                  (visits to https://shimo4228.github.io/)

A missing source becomes a line saying so, never a zero. The page states
numbers and dates only; it draws no conclusions (one or two weeks carry
little signal: traffic/README.md, "How NOT to read this"). Stdlib only.
"""
import argparse
from collections import Counter
from datetime import date, datetime, timedelta, timezone
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from referrer_split import classify  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
BUCKET_LABEL = {"ai": "AI", "search": "検索", "github": "GitHub 内", "other": "その他"}


# ---------- reading ----------

def read_jsonl(path):
    rows = []
    if not path.exists():
        return rows
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return rows


def week_of(end):
    """(this week start, this week end, previous start, previous end)."""
    start = end - timedelta(days=6)
    return start, end, start - timedelta(days=7), start - timedelta(days=1)


def last_sunday(today):
    """The most recent Sunday strictly before today."""
    back = (today.weekday() + 1) % 7 or 7
    return today - timedelta(days=back)


def days(start, end):
    return [start + timedelta(days=i) for i in range((end - start).days + 1)]


def views(data_dir, start, end):
    """{repo: {"count", "uniques", "missing"}} over [start, end]."""
    out = {}
    for path in sorted(data_dir.glob("*.jsonl")):
        by_date = {}
        for row in read_jsonl(path):
            try:
                by_date[date.fromisoformat(row["date"])] = row["views"]
            except (KeyError, ValueError, TypeError):
                continue
        if not by_date:
            continue
        span = days(start, end)
        present = [by_date[d] for d in span if d in by_date]
        out[path.stem] = {
            "count": sum(v.get("count", 0) for v in present),
            "uniques": sum(v.get("uniques", 0) for v in present),
            "missing": len(span) - len(present),
        }
    return out


def stars_at(rows, day):
    """Latest stars row dated on or before day."""
    best = None
    for row in rows:
        try:
            d = date.fromisoformat(row["date"])
        except (KeyError, ValueError, TypeError):
            continue
        if d <= day and (best is None or d > best[0]):
            best = (d, row)
    return best


def referrers(ref_dir, end):
    """Sum each repository's latest 14-day snapshot dated end-3..end."""
    total = Counter()
    used = []
    for path in sorted(ref_dir.glob("*.jsonl")):
        best = None
        for row in read_jsonl(path):
            try:
                d = date.fromisoformat(row["date"])
            except (KeyError, ValueError, TypeError):
                continue
            if end - timedelta(days=3) <= d <= end and (best is None or d > best[0]):
                best = (d, row.get("referrers") or [])
        if best is None:
            continue
        used.append(best[0])
        for item in best[1]:
            if isinstance(item.get("count"), int):
                total[str(item.get("referrer", ""))] += item["count"]
    return total, (min(used) if used else None)


def batches(rows, source):
    """{ts date: [rows]} for one source, keyed by the date the batch was taken."""
    out = {}
    for row in rows:
        if row.get("source") != source:
            continue
        try:
            d = datetime.fromisoformat(row["ts"]).date()
        except (KeyError, ValueError, TypeError):
            continue
        out.setdefault(d, []).append(row)
    return out


def latest_two(batch_map, end):
    """Latest batch on or before end, and the latest one before that."""
    keys = sorted(d for d in batch_map if d <= end)
    cur = keys[-1] if keys else None
    prev = keys[-2] if len(keys) > 1 else None
    return cur, prev


# ---------- writing ----------

def signed(n):
    return f"+{n}" if n > 0 else ("±0" if n == 0 else str(n))


def change(cur, prev):
    if prev is None:
        return "—"
    return signed(cur - prev)


def section_github(lines, data_dir, start, end, pstart, pend):
    this, prev = views(data_dir, start, end), views(data_dir, pstart, pend)
    lines += ["## GitHub リポジトリの閲覧", ""]
    if not this:
        lines += ["traffic/data が見つかりません。", ""]
        return
    t_count = sum(v["count"] for v in this.values())
    t_uniq = sum(v["uniques"] for v in this.values())
    p_count = sum(v["count"] for v in prev.values())
    p_uniq = sum(v["uniques"] for v in prev.values())
    lines += [
        f"全 {len(this)} リポジトリの合計: 閲覧 **{t_count}**（前週 {p_count}、{signed(t_count - p_count)}）"
        f"、日ごとのユニーク訪問者の和 **{t_uniq}**（前週 {p_uniq}、{signed(t_uniq - p_uniq)}）。",
        "",
        "| リポジトリ | 閲覧 | 前週 | 差 | ユニーク（日の和） |",
        "|---|---:|---:|---:|---:|",
    ]
    ranked = sorted(this, key=lambda r: (-this[r]["count"], r))
    shown = [r for r in ranked if this[r]["count"] or prev.get(r, {}).get("count")]
    for repo in shown:
        c = this[repo]["count"]
        p = prev.get(repo, {}).get("count", 0)
        note = f"（{this[repo]['missing']} 日欠測）" if this[repo]["missing"] else ""
        lines.append(f"| {repo}{note} | {c} | {p} | {signed(c - p)} | {this[repo]['uniques']} |")
    if len(shown) < len(this):
        lines.append(f"| ほか {len(this) - len(shown)} リポジトリ | 0 | 0 | ±0 | 0 |")
    lines += [
        "",
        "ユニーク訪問者は GitHub が日ごとに数えた値の和で、同じ人が 2 日来れば 2 と数えます。",
        "",
    ]


def section_stars(lines, stars_file, start, end):
    rows = read_jsonl(stars_file)
    lines += ["## スターとフォロワー（GitHub）", ""]
    now = stars_at(rows, end)
    if now is None:
        lines += ["traffic/stars.jsonl の記録がまだありません（毎日の CI が記録を始めると載ります）。", ""]
        return
    before = stars_at(rows, start - timedelta(days=1))
    nd, nrow = now
    brow = before[1] if before else None
    repos = nrow.get("repos", {})
    brepos = (brow or {}).get("repos", {})
    total = sum(r.get("stars", 0) for r in repos.values())
    btotal = sum(r.get("stars", 0) for r in brepos.values()) if brow else None
    lines.append(
        f"{nd.isoformat()} 時点: フォロワー **{nrow.get('followers', '—')}**"
        f"（週の差 {change(nrow.get('followers', 0), brow.get('followers') if brow else None)}）、"
        f"スター合計 **{total}**（週の差 {change(total, btotal)}）。"
    )
    if not brow:
        lines.append("前週の記録がないため、差は記録が 1 週分たまってから出ます。")
    lines += ["", "| リポジトリ | スター | 週の差 |", "|---|---:|---:|"]
    ranked = sorted(repos, key=lambda r: (-repos[r].get("stars", 0), r))
    for repo in ranked[:10]:
        s = repos[repo].get("stars", 0)
        b = brepos.get(repo, {}).get("stars") if brow else None
        lines.append(f"| {repo} | {s} | {change(s, b)} |")
    lines.append("")


def section_referrers(lines, ref_dir, end):
    total, oldest = referrers(ref_dir, end)
    lines += ["## GitHub への流入元（直近 14 日）", ""]
    if not total:
        lines += ["週末時点の流入元の記録がありません。", ""]
        return
    buckets = Counter()
    for ref, n in total.items():
        buckets[classify(ref)] += n
    split = "、".join(f"{BUCKET_LABEL[b]} {buckets[b]}" for b in BUCKET_LABEL)
    lines += [
        f"GitHub が返す 14 日間の上位の流入元を全リポジトリで足した値です（{oldest.isoformat()} 以降の記録）。"
        "週ごとの値ではないので、前週とは比べません。",
        "",
        f"区分: {split}。",
        "",
        "| 流入元 | 閲覧 |",
        "|---|---:|",
    ]
    for ref, n in total.most_common(10):
        lines.append(f"| {ref} | {n} |")
    lines.append("")


def section_writing(lines, zenn_file, end):
    lines += ["## Zenn・Dev.to", ""]
    if zenn_file is None or not zenn_file.exists():
        lines += ["zenn-content の snapshots.jsonl を読めませんでした。", ""]
        return
    rows = read_jsonl(zenn_file)
    out = []

    followers = sorted(
        (r for r in rows if r.get("type") == "followers" and "ts" in r),
        key=lambda r: r["ts"],
    )
    followers = [r for r in followers if datetime.fromisoformat(r["ts"]).date() <= end]
    if followers:
        f = followers[-1]
        out.append(
            f"- フォロワー（{f['ts'][:10]} 記録）: Zenn {f.get('zenn', '—')}、Dev.to {f.get('devto', '—')}"
        )

    zenn = batches(rows, "zenn")
    cur, prev = latest_two(zenn, end)
    if cur:
        likes = sum(r.get("liked", 0) for r in zenn[cur])
        line = f"- Zenn いいね合計（{cur.isoformat()} 記録、{len(zenn[cur])} 本）: **{likes}**"
        if prev:
            line += f"（{prev.isoformat()} の記録から {signed(likes - sum(r.get('liked', 0) for r in zenn[prev]))}）"
        out.append(line)

    dash = [
        r for r in rows
        if r.get("source") == "zenn_dash" and r.get("type") == "account" and "ts" in r
        and datetime.fromisoformat(r["ts"]).date() <= end
    ]
    if dash:
        d = max(dash, key=lambda r: r["ts"])
        out.append(f"- Zenn 閲覧数（ダッシュボード、{d['ts'][:10]} 記録、{d.get('window', '')}）: **{d.get('views', '—')}**")

    devto = batches(rows, "devto")
    cur, prev = latest_two(devto, end)
    if cur:
        v = sum(r.get("views", 0) for r in devto[cur])
        line = f"- Dev.to 閲覧合計（{cur.isoformat()} 記録）: **{v}**"
        if prev:
            line += f"（{prev.isoformat()} の記録から {signed(v - sum(r.get('views', 0) for r in devto[prev]))}）"
        out.append(line)

    if not out:
        out.append("- 週末までの記録がありません。")
    stale = [
        d for d in (max(zenn) if zenn else None, max(devto) if devto else None)
        if d is not None and (end - d).days > 7
    ]
    lines += out
    lines += [
        "",
        "これらは手で集める記録です（zenn-content の `article-stocktake`）。日付が 1 週間より古ければ、"
        "その週の値ではありません。" if stale else "これらは手で集める記録です（zenn-content の `article-stocktake`）。",
        "",
    ]


def section_site(lines, site_file):
    lines += ["## 個人サイト（shimo4228.github.io）", ""]
    if site_file is None or not site_file.exists():
        lines += [
            "Cloudflare Web Analytics の値はまだ取り込んでいません"
            "（リポジトリの secret `CF_API_TOKEN` / `CF_ACCOUNT_ID` / `CF_SITE_TAG` が要ります）。"
            "値は Cloudflare のダッシュボードで見られます。",
            "",
        ]
        return
    data = json.loads(site_file.read_text(encoding="utf-8"))
    if data.get("error"):
        lines += [f"Cloudflare から取得できませんでした: {data['error']}", ""]
        return
    this, prev = data.get("this", {}), data.get("prev", {})
    lines += [
        f"訪問 **{this.get('visits', 0)}**（前週 {prev.get('visits', 0)}、{signed(this.get('visits', 0) - prev.get('visits', 0))}）、"
        f"ページビュー **{this.get('pageviews', 0)}**（前週 {prev.get('pageviews', 0)}）。",
        "",
    ]
    if this.get("referers"):
        lines += ["| 流入元 | 訪問 |", "|---|---:|"]
        for r in this["referers"][:10]:
            lines.append(f"| {r.get('host') or '（直接・不明）'} | {r.get('visits', 0)} |")
        lines.append("")
    if this.get("paths"):
        lines += ["| ページ | ページビュー |", "|---|---:|"]
        for p in this["paths"][:10]:
            lines.append(f"| {p.get('path')} | {p.get('pageviews', 0)} |")
        lines.append("")


def render(end, data_dir, ref_dir, stars_file, zenn_file, site_file):
    start, end, pstart, pend = week_of(end)
    lines = [
        f"# 週のまとめ {start.isoformat()} 〜 {end.isoformat()}（UTC）",
        "",
        f"前週は {pstart.isoformat()} 〜 {pend.isoformat()}。数字と日付だけを並べ、良し悪しは書きません。"
        "1〜2 週の増減はほぼ雑音です（[How NOT to read this](../README.md#how-not-to-read-this)）。",
        "",
    ]
    section_site(lines, site_file)
    section_github(lines, data_dir, start, end, pstart, pend)
    section_stars(lines, stars_file, start, end)
    section_referrers(lines, ref_dir, end)
    section_writing(lines, zenn_file, end)
    return "\n".join(lines).rstrip() + "\n"


def write_index(weekly_dir):
    pages = sorted((p for p in weekly_dir.glob("*.md") if p.name != "README.md"), reverse=True)
    body = [
        "# 週のまとめ",
        "",
        "毎週月曜に `.github/workflows/weekly-summary.yml` が前の週（月〜日、UTC）の 1 枚を足します。"
        "手で編集しないでください（`scripts/weekly_summary.py` が書きます）。",
        "",
    ]
    body += [f"- [{p.stem}]({p.name})" for p in pages]
    (weekly_dir / "README.md").write_text("\n".join(body) + "\n", encoding="utf-8")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--end", type=date.fromisoformat, help="last day of the week (default: last Sunday, UTC)")
    ap.add_argument("--zenn", type=Path, help="zenn-content scripts/metrics/snapshots.jsonl")
    ap.add_argument("--site", type=Path, help="JSON written by scripts/cf_web_analytics.py")
    ap.add_argument("--root", type=Path, default=ROOT)
    ap.add_argument("--stdout", action="store_true", help="print instead of writing traffic/weekly/")
    args = ap.parse_args(argv)
    end = args.end or last_sunday(datetime.now(timezone.utc).date())
    traffic = args.root / "traffic"
    page = render(end, traffic / "data", traffic / "referrers", traffic / "stars.jsonl", args.zenn, args.site)
    if args.stdout:
        sys.stdout.write(page)
        return 0
    weekly = traffic / "weekly"
    weekly.mkdir(exist_ok=True)
    (weekly / f"{end.isoformat()}.md").write_text(page, encoding="utf-8")
    write_index(weekly)
    print(f"wrote traffic/weekly/{end.isoformat()}.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
