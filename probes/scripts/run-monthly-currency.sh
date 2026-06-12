#!/bin/bash
# Monthly currency check (ADR-0011): silent-swap detection, catalog diff,
# staleness guard. Scheduled by launchd
# (com.shimo4228.probes-currency-monthly), 1st of the month 10:47 JST.
# On change events, a macOS notification fires — panel adoption and
# parametric event runs stay human decisions.
set -uo pipefail

REPO="$HOME/MyAI_Lab/shimo4228"
UV="$HOME/.local/bin/uv"
LOG_DIR="$REPO/probes/logs"
mkdir -p "$LOG_DIR"
LOG="$LOG_DIR/currency-$(date +%Y-%m-%d).log"

{
  echo "=== monthly currency check $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
  cd "$REPO/probes/runner"
  "$UV" run probe_runner.py --currency-check --strict
  STATUS=$?
  echo "currency check exit: $STATUS"

  cd "$REPO"
  git add probes/data/
  if git diff --cached --quiet; then
    echo "no new currency data to commit"
  else
    git commit -m "chore(probes): currency check $(date -u +%Y-%m-%d)"
    git push
  fi

  if [ "$STATUS" -ne 0 ]; then
    /usr/bin/osascript -e 'display notification "Model change events detected — see probes/logs and consider a parametric event run" with title "probes: currency check"'
  fi
  echo "=== done $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
} >> "$LOG" 2>&1
