"""Fetch one week of Cloudflare Web Analytics for the personal site, as JSON.

The site (https://shimo4228.github.io/) carries the Cloudflare Web Analytics
beacon. This asks Cloudflare's GraphQL Analytics API for the week ending --end
(Monday to Sunday, UTC) and the week before, and writes:

  {"this": {"visits", "pageviews", "referers": [...], "paths": [...]},
   "prev": {"visits", "pageviews"}, "start", "end"}

or {"error": "..."} when the request fails, so the weekly page says why
instead of showing zeros. Needs CF_API_TOKEN (Account Analytics: Read),
CF_ACCOUNT_ID and CF_SITE_TAG (the site tag from Web Analytics → Manage site).
Stdlib only.
"""
import argparse
from datetime import date, timedelta
import json
import os
from pathlib import Path
import sys
import urllib.request

API = "https://api.cloudflare.com/client/v4/graphql"
QUERY = """
query($account: String!, $site: String!, $start: Date!, $end: Date!, $pstart: Date!, $pend: Date!) {
  viewer {
    accounts(filter: {accountTag: $account}) {
      total: rumPageloadEventsAdaptiveGroups(limit: 1, filter: {siteTag: $site, date_geq: $start, date_leq: $end}) {
        count
        sum { visits }
      }
      prev: rumPageloadEventsAdaptiveGroups(limit: 1, filter: {siteTag: $site, date_geq: $pstart, date_leq: $pend}) {
        count
        sum { visits }
      }
      referers: rumPageloadEventsAdaptiveGroups(limit: 10, orderBy: [sum_visits_DESC],
          filter: {siteTag: $site, date_geq: $start, date_leq: $end}) {
        sum { visits }
        dimensions { refererHost }
      }
      paths: rumPageloadEventsAdaptiveGroups(limit: 10, orderBy: [count_DESC],
          filter: {siteTag: $site, date_geq: $start, date_leq: $end}) {
        count
        dimensions { requestPath }
      }
    }
  }
}
"""


def totals(groups):
    g = groups[0] if groups else {}
    return {"visits": (g.get("sum") or {}).get("visits", 0), "pageviews": g.get("count", 0)}


def shape(data, start, end):
    acct = data["data"]["viewer"]["accounts"][0]
    this = totals(acct["total"])
    this["referers"] = [
        {"host": g["dimensions"]["refererHost"], "visits": g["sum"]["visits"]} for g in acct["referers"]
    ]
    this["paths"] = [{"path": g["dimensions"]["requestPath"], "pageviews": g["count"]} for g in acct["paths"]]
    return {"start": start.isoformat(), "end": end.isoformat(), "this": this, "prev": totals(acct["prev"])}


def fetch(end):
    start = end - timedelta(days=6)
    env = {k: os.environ.get(k) for k in ("CF_API_TOKEN", "CF_ACCOUNT_ID", "CF_SITE_TAG")}
    missing = [k for k, v in env.items() if not v]
    if missing:
        return {"error": "secret がありません: " + ", ".join(missing)}
    body = json.dumps({
        "query": QUERY,
        "variables": {
            "account": env["CF_ACCOUNT_ID"], "site": env["CF_SITE_TAG"],
            "start": start.isoformat(), "end": end.isoformat(),
            "pstart": (start - timedelta(days=7)).isoformat(), "pend": (start - timedelta(days=1)).isoformat(),
        },
    }).encode()
    req = urllib.request.Request(API, data=body, headers={
        "Authorization": f"Bearer {env['CF_API_TOKEN']}", "Content-Type": "application/json",
    })
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.load(r)
        if data.get("errors"):
            return {"error": "; ".join(e.get("message", "?") for e in data["errors"])}
        return shape(data, start, end)
    except Exception as exc:  # the weekly page reports it; the workflow goes on
        return {"error": f"{type(exc).__name__}: {exc}"}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--end", type=date.fromisoformat, required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args(argv)
    result = fetch(args.end)
    args.out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(result.get("error") or f"site: {result['this']['visits']} visits")
    return 0


if __name__ == "__main__":
    sys.exit(main())
