#!/usr/bin/env python3
"""One-line health summary of a probe run, for the Slack heartbeat.

Reads the channel log and reports ok/expected cells per provider for one
run_id. Kept deliberately dumb: no state, no thresholds, no history — the
JSONL is the source of truth and this only reshapes it for a push message.

Usage:  summarize_run.py <channel-jsonl> [run_id]     (default: latest run)
Exit 0 always; a run with errored cells is signalled in the TEXT, not the
exit code, so the caller sends the same message either way.
"""

import json
import sys
from collections import defaultdict

PROVIDER_ORDER = ["anthropic", "openai", "gemini", "qwen", "xai"]


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("probes: summarize_run.py needs a channel log path")
        return 0
    path = argv[1]
    want = argv[2] if len(argv) > 2 else None

    try:
        with open(path, encoding="utf-8") as fh:
            rows = [json.loads(line) for line in fh if line.strip()]
    except (OSError, json.JSONDecodeError) as exc:
        # Never let the notifier crash the run it is reporting on.
        print(f"probes: cannot read {path} ({exc.__class__.__name__})")
        return 0

    if not rows:
        print("probes: channel log is empty")
        return 0

    run_id = want or max(r["run_id"] for r in rows)
    # Count CELLS (provider × probe), not rows: each gap-fill pass appends
    # another error stub for a cell that is still failing, so a row count
    # inflates a broken provider's denominator and makes the healthy columns
    # look short. A cell is ok if any of its rows succeeded.
    seen: dict[str, set[str]] = defaultdict(set)
    ok_cells: dict[str, set[str]] = defaultdict(set)
    for r in rows:
        if r.get("run_id") != run_id:
            continue
        prov, probe = r["provider"], r["probe_id"]
        seen[prov].add(probe)
        if not r.get("error"):
            ok_cells[prov].add(probe)

    if not seen:
        print(f"probes: no rows for run {run_id}")
        return 0

    # Expected cells = the widest probe set any provider attempted this run.
    expected = max(len(s) for s in seen.values())

    parts, bad = [], False
    ordered = [p for p in PROVIDER_ORDER if p in seen]
    ordered += [p for p in sorted(seen) if p not in PROVIDER_ORDER]
    for prov in ordered:
        ok = len(ok_cells[prov])
        mark = ""
        if ok < expected:
            mark = " !"
            bad = True
        parts.append(f"{prov} {ok}/{expected}{mark}")

    status = "WARN" if bad else "OK"
    print(f"{status} probes {run_id[:10]} · " + " · ".join(parts))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
