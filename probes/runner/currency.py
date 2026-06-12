"""Model-currency checks.

The parametric probe is event-driven: a frozen model's weights cannot change
between runs, so re-probing the same model only measures response variance.
What needs a calendar is the *detection of change events*. This module
implements the three automated detectors:

1. silent-swap detection — the served model identity behind a non-dated
   alias changed since the last observation
2. catalog diff — newly published (or removed) model ids per provider
   (detection is automated; panel adoption stays a human judgment)
3. staleness guard — the panel's default-tier choice has not been
   re-verified within its window

Pure functions are separated from HTTP fetchers so the logic is testable
with zero API budget.
"""

from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path

import httpx

# Coarse filter for "chat-model candidates" in catalog diffs. Report-only:
# it trims embedding/audio/image/video ids out of the new-model report, it
# does not decide panel membership.
_FAMILY = re.compile(r"claude|gpt|gemini|grok", re.IGNORECASE)
_EXCLUDE = re.compile(
    r"embed|tts|audio|whisper|moderation|image|imagen|video|veo|imagine|"
    r"dall-e|realtime|transcribe|guard|rerank|aqa|robotics|live|computer-use",
    re.IGNORECASE,
)

ENV_KEYS = {
    "anthropic": "ANTHROPIC_API_KEY",
    "openai": "OPENAI_API_KEY",
    "gemini": "GEMINI_API_KEY",
    "xai": "XAI_API_KEY",
    "qwen": "DASHSCOPE_API_KEY",
}


# --- pure functions --------------------------------------------------------


def diff_catalog(prev_ids: list[str], curr_ids: list[str]) -> tuple[list[str], list[str]]:
    """(new_ids, removed_ids) between two catalog snapshots."""
    prev, curr = set(prev_ids), set(curr_ids)
    return sorted(curr - prev), sorted(prev - curr)


def filter_chat_candidates(ids: list[str]) -> list[str]:
    """Keep ids that look like chat/completion models of the four families."""
    return [i for i in ids if _FAMILY.search(i) and not _EXCLUDE.search(i)]


def is_stale(verified_current: str, today: date, max_days: int) -> bool:
    """True when the panel verification date has aged past max_days."""
    verified = date.fromisoformat(str(verified_current))
    return (today - verified).days > max_days


def latest_per_provider(path: Path) -> dict[str, dict]:
    """Last JSONL record per provider — baseline for swap/catalog diffs."""
    latest: dict[str, dict] = {}
    if not path.exists():
        return latest
    with path.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            latest[rec["provider"]] = rec
    return latest


# --- HTTP fetchers (one minimal request per provider, no completion cost) --


def fetch_model_ids(provider: str, api_key: str, timeout: float = 30.0) -> list[str]:
    """Current model-id catalog from the provider's model-list endpoint."""
    if provider == "openai":
        return _fetch_openai_style("https://api.openai.com/v1/models", api_key, timeout)
    if provider == "xai":
        return _fetch_openai_style("https://api.x.ai/v1/models", api_key, timeout)
    if provider == "qwen":
        return _fetch_openai_style(
            "https://dashscope-intl.aliyuncs.com/compatible-mode/v1/models",
            api_key,
            timeout,
        )
    if provider == "anthropic":
        ids: list[str] = []
        url = "https://api.anthropic.com/v1/models?limit=100"
        headers = {"x-api-key": api_key, "anthropic-version": "2023-06-01"}
        while url:
            resp = httpx.get(url, headers=headers, timeout=timeout)
            resp.raise_for_status()
            body = resp.json()
            ids += [m["id"] for m in body.get("data", [])]
            last_id = body.get("last_id")
            url = (
                f"https://api.anthropic.com/v1/models?limit=100&after_id={last_id}"
                if body.get("has_more") and last_id
                else None
            )
        return sorted(ids)
    if provider == "gemini":
        ids = []
        base = "https://generativelanguage.googleapis.com/v1beta/models"
        page_token = None
        while True:
            params = {"key": api_key, "pageSize": 200}
            if page_token:
                params["pageToken"] = page_token
            resp = httpx.get(base, params=params, timeout=timeout)
            resp.raise_for_status()
            body = resp.json()
            ids += [m["name"].removeprefix("models/") for m in body.get("models", [])]
            page_token = body.get("nextPageToken")
            if not page_token:
                return sorted(ids)
    raise ValueError(f"unknown provider: {provider}")


def _fetch_openai_style(url: str, api_key: str, timeout: float) -> list[str]:
    resp = httpx.get(url, headers={"Authorization": f"Bearer {api_key}"}, timeout=timeout)
    resp.raise_for_status()
    return sorted(m["id"] for m in resp.json().get("data", []))
