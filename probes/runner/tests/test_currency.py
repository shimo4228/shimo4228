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


def test_chat_filter_covers_every_panel_provider():
    """Regression: qwen joined the panel 2026-06-12 but the family pattern
    kept only the four founding families until 2026-09-20, so qwen catalog
    additions raised no NEW MODEL event and the pin went unreviewed."""
    from providers import PROVIDERS

    one_id_per_provider = {
        "anthropic": "claude-sonnet-5",
        "openai": "gpt-6.0",
        "gemini": "gemini-3.7-flash",
        "xai": "grok-4.6",
        "qwen": "qwen3.8-max",
    }
    missing = sorted(set(PROVIDERS) - set(one_id_per_provider))
    assert not missing, f"no sample id for panel provider(s): {missing}"
    for provider, model_id in one_id_per_provider.items():
        assert filter_chat_candidates([model_id]) == [model_id], provider


def test_chat_filter_on_the_2026_09_01_dashscope_diff():
    """The real catalog diff that was silently dropped. DashScope also serves
    third-party models, so the family pattern has to keep those out too."""
    observed_new_ids = [
        "ZHIPU/GLM-5.3",
        "deepseek-v4-flash-0731",
        "deepseek-v4-pro-0813",
        "kimi-k3",
        "kimi/kimi-k3",
        "qwen-image-3.0",
        "qwen-image-3.0-pro",
        "qwen3.7-text-embedding",
        "qwen3.8-2.4t-a95b",
        "qwen3.8-27b",
        "qwen3.8-flash",
        "qwen3.8-max",
    ]
    assert filter_chat_candidates(observed_new_ids) == [
        "qwen3.8-2.4t-a95b",
        "qwen3.8-27b",
        "qwen3.8-flash",
        "qwen3.8-max",
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
