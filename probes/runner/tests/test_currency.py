"""Currency-check logic tests. Pure functions only — zero API budget."""

import json
from datetime import date

from currency import (
    diff_catalog,
    filter_chat_candidates,
    is_stale,
    latest_per_provider,
)


def test_diff_catalog_new_and_removed():
    new, removed = diff_catalog(
        ["gpt-5.5", "gpt-5.1", "text-embedding-3-large"],
        ["gpt-5.5", "gpt-6.0", "text-embedding-3-large"],
    )
    assert new == ["gpt-6.0"]
    assert removed == ["gpt-5.1"]


def test_diff_catalog_identical_is_empty():
    assert diff_catalog(["a", "b"], ["b", "a"]) == ([], [])


def test_chat_filter_keeps_chat_families():
    ids = [
        "gpt-6.0",
        "claude-sonnet-4-6",
        "gemini-3.5-flash",
        "grok-4.4",
        "text-embedding-3-large",
        "grok-imagine-video-1.5-preview",
        "whisper-1",
        "gemini-3.5-flash-image",
        "gpt-5.5-realtime",
        "veo-3",
    ]
    assert filter_chat_candidates(ids) == [
        "gpt-6.0",
        "claude-sonnet-4-6",
        "gemini-3.5-flash",
        "grok-4.4",
    ]


def test_is_stale_boundary():
    # 2026-06-12 → 2026-09-10 is exactly 90 days (not stale at the boundary).
    assert is_stale("2026-06-12", date(2026, 9, 10), 90) is False
    assert is_stale("2026-06-12", date(2026, 9, 11), 90) is True   # 91 days
    assert is_stale("2026-06-12", date(2026, 9, 11), 91) is False
    assert is_stale("2026-06-12", date(2026, 6, 12), 90) is False  # same day


def test_latest_per_provider_takes_last_line(tmp_path):
    path = tmp_path / "currency.jsonl"
    lines = [
        {"provider": "openai", "model_returned": "gpt-5.5-old"},
        {"provider": "xai", "model_returned": "grok-4.3"},
        {"provider": "openai", "model_returned": "gpt-5.5-new"},
    ]
    path.write_text("\n".join(json.dumps(r) for r in lines) + "\n")
    latest = latest_per_provider(path)
    assert latest["openai"]["model_returned"] == "gpt-5.5-new"
    assert latest["xai"]["model_returned"] == "grok-4.3"


def test_latest_per_provider_missing_file(tmp_path):
    assert latest_per_provider(tmp_path / "nope.jsonl") == {}
