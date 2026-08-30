#!/bin/bash
# Retrieval arms of the two-channel probe protocol (ADR-0011).
# Scheduled by launchd (com.shimo4228.probes-retrieval-weekly), Sunday
# 10:17 JST; launchd runs a missed slot at the next wake from sleep.
#
# Cadence (pre-registered, see probe-baseline-2026-06 §Sampling cadence):
# launchd fires every Sunday, but the run is FORTNIGHTLY by default — it
# executes only on even ISO weeks — to halve API cost in the quiet period.
# The exception is the autumn-2026 observation window (the predicted
# parametric-transition period), during which it runs WEEKLY for finer
# temporal resolution around the event of interest.
#
# No -e: the runner exits non-zero when any probe errors (e.g. a provider
# 503 burst), but partial data must still be committed — errored cells are
# refilled later via same-run-id gap fill.
set -uo pipefail

REPO="$HOME/MyAI_Lab/shimo4228"
UV="$HOME/.local/bin/uv"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
LOG_DIR="$REPO/probes/logs"
mkdir -p "$LOG_DIR"
LOG="$LOG_DIR/retrieval-$(date +%Y-%m-%d-%H%M).log"
# shellcheck source=probes/scripts/_lib.sh
source "$SCRIPT_DIR/_lib.sh"

# Weekly window: run every week between these dates (inclusive); fortnightly
# otherwise. Adjust the end when the autumn observation window is reset.
WEEKLY_FROM="2026-09-01"
WEEKLY_TO="2026-11-30"

{
  RUN_DATE=$(date +%Y-%m-%d)
  WEEK=$(date +%V)                       # ISO week, zero-padded (e.g. 08)
  if [[ "$RUN_DATE" < "$WEEKLY_FROM" || "$RUN_DATE" > "$WEEKLY_TO" ]] \
       && (( 10#$WEEK % 2 != 0 )); then  # 10# avoids octal parse of 08/09
    echo "=== skip $(date -u +%Y-%m-%dT%H:%M:%SZ): odd ISO week $WEEK, fortnightly cadence (outside weekly window) ==="
    # Announce the skip too: the invariant is ONE line every Sunday, so a
    # silent Sunday always means something is wrong, never "this was a
    # fortnightly off-week".
    probe_notify "probes retrieval" "SKIP $RUN_DATE · odd ISO week $WEEK, fortnightly off-week"
    exit 0
  fi
  echo "=== retrieval run $(date -u +%Y-%m-%dT%H:%M:%SZ) (ISO week $WEEK) ==="
  probe_git_lock 1800  # primary run: wait out a gap-fill that won the wake race
  cd "$REPO/probes/runner" || exit 1
  "$UV" run probe_runner.py --channel retrieval --cost-budget 8.0
  echo "runner exit: $? (non-zero = errored cells, gap-fill later)"

  cd "$REPO" || exit 1
  # Rebase-aware commit+push (survives the traffic-snapshot job's concurrent
  # commits; a failed push stays local and the gap-fill pass pushes it).
  probe_commit_data "chore(probes): retrieval $(date -u +%Y-%m-%d)" \
    || echo "no new probe data to commit"

  # Heartbeat. Reports the run as it stands now; a WARN line here may still be
  # cleared by the same-day gap-fill passes, which is why the body says so
  # rather than demanding action on a transient provider 503.
  SUMMARY=$(probe_summary retrieval)
  echo "$SUMMARY"
  case "$SUMMARY" in
    WARN*) probe_notify "probes retrieval" "$SUMMARY
gap-fill retries at 14:17 / 18:17; you are pinged again only if it is still short." ;;
    *)     probe_notify "probes retrieval" "$SUMMARY" ;;
  esac
  echo "=== done $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
} >> "$LOG" 2>&1
