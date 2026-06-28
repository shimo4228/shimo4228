#!/bin/bash
# Delayed gap-fill for the retrieval channel (ADR-0011).
# Scheduled by launchd (com.shimo4228.probes-gapfill-retrieval) a few hours
# AFTER the weekly run, in two passes (14:17 and 18:17 JST).
#
# Why a separate delayed job: gemini-3.5-flash returns 503 "high demand"
# bursts that can outlast the in-call retry (num_retries=2) AND last tens of
# minutes — observed 2026-06-28: 4 cells needed ~21 min to clear. Hammering
# inside the live run wastes wall-clock and bloats the append-only log with
# error stubs; a single pass hours later, when the burst has cleared, fills
# the gap with one stub per still-failing cell.
#
# Idempotent: --run-id latest resolves the most recent retrieval run and
# existing_triples() skips already-filled cells, so this retries EXACTLY the
# unfilled ones. Safe to run when there is no gap (it commits nothing).
#
# Freshness gate: only the SAME-DAY run is gap-filled. The retrieval signal
# (citation pool) moves in days, so back-filling a run from a previous day
# (e.g. an odd Sunday resolving the prior fortnight's run) would stamp a stale
# value under an old run_id. A documented hole beats a misattributed point.
#
# No -e: the runner exits non-zero while cells remain errored (the second
# pass mops them up); the partial fill still commits.
set -uo pipefail

REPO="$HOME/MyAI_Lab/shimo4228"
UV="$HOME/.local/bin/uv"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
LOG_DIR="$REPO/probes/logs"
mkdir -p "$LOG_DIR"
LOG="$LOG_DIR/gapfill-retrieval-$(date +%Y-%m-%d-%H%M).log"
# shellcheck source=probes/scripts/_lib.sh
source "$SCRIPT_DIR/_lib.sh"

{
  echo "=== gap-fill retrieval $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
  probe_git_lock
  cd "$REPO/probes/runner" || exit 1

  # Freshness gate: resolve the latest run-id (dry-run = no API calls) and only
  # gap-fill if it is from today (UTC, matching the run_id stamp).
  LATEST=$("$UV" run probe_runner.py --channel retrieval --run-id latest --dry-run 2>/dev/null \
             | sed -n 's/^# gap-fill: resolved latest run-id = //p')
  TODAY=$(date -u +%Y-%m-%d)
  case "$LATEST" in
    "$TODAY"T*)
      "$UV" run probe_runner.py --channel retrieval --run-id latest --cost-budget 2.0
      echo "runner exit: $? (non-zero = cells still erroring, next pass retries)"
      ;;
    *)
      echo "latest run (${LATEST:-none}) is not from today ($TODAY) — skip stale gap-fill"
      ;;
  esac

  cd "$REPO" || exit 1
  if probe_commit_data "chore(probes): gap-fill retrieval $(date -u +%Y-%m-%d)"; then
    :  # committed (push handled inside, with deferral on failure)
  else
    echo "no gap to fill (all cells filled, or all still erroring)"
    probe_push_stranded  # still push a weekly commit whose push failed earlier
  fi
  echo "=== done $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
} >> "$LOG" 2>&1
