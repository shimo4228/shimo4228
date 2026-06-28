"""Gap-fill latest-run-id resolution tests. Zero API budget."""

import json
from pathlib import Path

from probe_runner import resolve_latest_run_id


def _write(path: Path, run_ids: list[str]) -> None:
    path.write_text(
        "\n".join(json.dumps({"run_id": rid, "provider": "gemini"}) for rid in run_ids)
        + "\n"
    )


def test_returns_none_when_file_absent(tmp_path):
    assert resolve_latest_run_id(tmp_path / "retrieval.jsonl") is None


def test_returns_none_for_empty_file(tmp_path):
    f = tmp_path / "retrieval.jsonl"
    f.write_text("")
    assert resolve_latest_run_id(f) is None


def test_picks_chronologically_latest_run_id(tmp_path):
    f = tmp_path / "retrieval.jsonl"
    _write(
        f,
        [
            "2026-06-14T01:17Z-retrieval",
            "2026-06-28T01:17Z-retrieval",  # latest
            "2026-06-12T23:21Z-retrieval",
        ],
    )
    assert resolve_latest_run_id(f) == "2026-06-28T01:17Z-retrieval"


def test_ignores_blank_lines(tmp_path):
    f = tmp_path / "retrieval.jsonl"
    f.write_text(
        json.dumps({"run_id": "2026-06-28T01:17Z-retrieval", "provider": "gemini"})
        + "\n\n"
    )
    assert resolve_latest_run_id(f) == "2026-06-28T01:17Z-retrieval"


def test_tolerates_truncated_trailing_line(tmp_path):
    # Gap-fill runs right after a possibly-interrupted run; a crash mid-write
    # leaves a partial last line. Resolution must heal, not crash.
    f = tmp_path / "retrieval.jsonl"
    f.write_text(
        json.dumps({"run_id": "2026-06-28T01:17Z-retrieval", "provider": "gemini"})
        + '\n{"run_id": "2026-06-28T14:17Z-retr'  # truncated, no newline
    )
    assert resolve_latest_run_id(f) == "2026-06-28T01:17Z-retrieval"


def test_ignores_non_string_run_id(tmp_path):
    f = tmp_path / "retrieval.jsonl"
    f.write_text(
        json.dumps({"run_id": 123, "provider": "gemini"})
        + "\n"
        + json.dumps({"run_id": "2026-06-28T01:17Z-retrieval", "provider": "gemini"})
        + "\n"
    )
    assert resolve_latest_run_id(f) == "2026-06-28T01:17Z-retrieval"


def test_iso_prefix_makes_lexicographic_equal_chronological(tmp_path):
    # Same date, later minute must win (lexicographic on the ISO prefix).
    f = tmp_path / "retrieval.jsonl"
    _write(
        f,
        [
            "2026-06-28T01:17Z-retrieval",
            "2026-06-28T14:17Z-retrieval",  # later same-day pass
        ],
    )
    assert resolve_latest_run_id(f) == "2026-06-28T14:17Z-retrieval"
