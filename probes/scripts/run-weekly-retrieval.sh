#!/bin/bash
# Weekly retrieval arms of the two-channel probe protocol (ADR-0011).
# Scheduled by launchd (com.shimo4228.probes-retrieval-weekly), Sunday
# 10:17 JST; launchd runs a missed slot at the next wake from sleep.
set -euo pipefail

REPO="$HOME/MyAI_Lab/shimo4228"
UV="$HOME/.local/bin/uv"
LOG_DIR="$REPO/probes/logs"
mkdir -p "$LOG_DIR"
LOG="$LOG_DIR/retrieval-$(date +%Y-%m-%d-%H%M).log"

{
  echo "=== weekly retrieval run $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
  cd "$REPO/probes/runner"
  "$UV" run probe_runner.py --channel retrieval --cost-ceiling 5.0

  cd "$REPO"
  git add probes/data/
  if git diff --cached --quiet; then
    echo "no new probe data to commit"
  else
    git commit -m "chore(probes): retrieval $(date -u +%Y-%m-%d)"
    git push
  fi
  echo "=== done $(date -u +%Y-%m-%dT%H:%M:%SZ) ==="
} >> "$LOG" 2>&1
