# shellcheck shell=bash
# Shared helpers for the probe launchd scripts (run-weekly-retrieval.sh,
# run-gap-fill-retrieval.sh). Sourced, never executed directly.

# Single-writer git lock shared by every probe job that commits to this repo,
# so concurrent launchd firings — e.g. all slots bunched at the next wake after
# the Mac slept through Sunday — never race on the git index or interleave
# appends to the same channel log.
#
#   probe_git_lock          non-blocking: a SECONDARY job (gap-fill) exits
#                           cleanly if the lock is held; the next pass retries.
#   probe_git_lock <secs>   the PRIMARY job (weekly run) waits up to <secs> for
#                           the lock instead of dropping its sample. Without
#                           this, a gap-fill that wins the post-sleep wake race
#                           would make the weekly job exit before probing — and
#                           that gap-fill then skips too (no same-day run yet),
#                           losing the scheduled sample for a whole cadence.
#
# Uses an atomic mkdir (flock is not on stock macOS). A lock left by a process
# killed before its EXIT trap fired (e.g. SIGKILL) is stolen once it is older
# than an hour — far longer than any real run (~20 min worst case).
probe_git_lock() {
    local lockdir="/tmp/probes-git.lock.d" max_wait="${1:-0}" waited=0
    if [ -d "$lockdir" ]; then
        local age=$(( $(date +%s) - $(stat -f %m "$lockdir" 2>/dev/null || echo 0) ))
        if [ "$age" -gt 3600 ]; then
            echo "stealing stale git lock (age ${age}s)"
            rmdir "$lockdir" 2>/dev/null || true
        fi
    fi
    until mkdir "$lockdir" 2>/dev/null; do
        if [ "$waited" -ge "$max_wait" ]; then
            echo "another probe job holds the git lock — exiting"
            exit 0
        fi
        sleep 5
        waited=$((waited + 5))
    done
    trap 'rmdir "/tmp/probes-git.lock.d" 2>/dev/null || true' EXIT
}

# One-line Slack heartbeat for an unattended probe run, via the harness's
# shared notifier (~/.config/wiki-notify/slack-webhook, macOS notification as
# fallback). Reuses the existing channel rather than adding a second webhook.
#
# HEARTBEAT, not failure-only alert: every scheduled Sunday sends exactly one
# line, healthy runs included, so that SILENCE is itself the alarm. A notifier
# that only speaks up on errors cannot distinguish "all five providers fine"
# from "launchd never fired / the Mac slept through the window / the script
# died before the runner" — and those are the failures that hide longest. The
# 2026-08-23 anthropic key expiry sat unnoticed for a week precisely because
# nothing was obliged to report on a schedule.
#
# Never fails the caller: delivery problems are logged (the harness notifier
# already prints its own outcome) and swallowed, since a broken notifier must
# not abort the measurement it reports on.
probe_notify() {
    local title="$1" body="$2"
    bash "$HOME/.claude/scripts/notify-slack.sh" "$title" "$body" || true
}

# Render the one-line health summary for a run: "OK|WARN probes <date> ·
# <provider ok/expected> …". $1 = channel (retrieval|parametric), $2 = run_id
# or empty for the latest run in that channel log.
probe_summary() {
    local channel="$1" run_id="${2:-}"
    python3 "$SCRIPT_DIR/summarize_run.py" \
        "$REPO/probes/data/${channel}.jsonl" ${run_id:+"$run_id"} 2>&1 \
        || echo "probes: summary failed"
}

# Push HEAD onto origin/main, rebasing first so the traffic-snapshot job's
# concurrent commits do not reject the push. On any failure the commit stays
# local (a later pass pushes it) and the repo is left on a clean branch — a
# rebase conflict is aborted, never left half-applied to corrupt the next run.
probe_push() {
    if git pull --rebase origin main; then
        git push || echo "push failed — commit is local; a later pass will push"
    else
        git rebase --abort 2>/dev/null || true
        echo "pull --rebase failed — commit is local; a later pass will push"
    fi
}

# Stage probes/data and, if anything changed, commit with message $1 and push.
# Returns 0 if a commit was made, 1 if there was nothing to commit. Caller cwd
# must be the repo root.
probe_commit_data() {
    git add probes/data/
    if git diff --cached --quiet; then
        return 1
    fi
    git commit -m "$1"
    probe_push
    return 0
}

# Push commits that are already local but not yet upstream — e.g. a weekly
# commit whose push failed earlier — so "a later pass will push" holds even on
# a pass that has no new data of its own. Caller cwd must be the repo root.
probe_push_stranded() {
    if [ "$(git rev-list "@{u}..HEAD" --count 2>/dev/null || echo 0)" -gt 0 ]; then
        echo "pushing stranded local commit(s)"
        probe_push
    fi
}
