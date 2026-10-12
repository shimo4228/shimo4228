"""Stdlib-only tests for the monthly four-way referrer split."""
from datetime import date
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/referrer_split.py"
sys.path.insert(0, str(ROOT / "scripts"))
import referrer_split  # noqa: E402  # pyright: ignore[reportMissingImports]


class ClassifyTests(unittest.TestCase):
    def test_buckets(self):
        cases = {
            "chatgpt.com": "ai", "perplexity.ai": "ai", "claude.ai": "ai",
            "Google": "search", "Bing": "search", "search.brave.com": "search",
            "github.com": "github",
            "t.co": "other", "dev.to": "other", "google.com.evil": "other",
        }
        for referrer, bucket in cases.items():
            self.assertEqual(referrer_split.classify(referrer), bucket, referrer)


class WindowTests(unittest.TestCase):
    def test_second_window_does_not_overlap(self):
        dates = {date(2026, 10, d) for d in range(1, 32) if d <= 31}
        picked = referrer_split.pick_windows(dates, date(2026, 10, 31))
        self.assertEqual(picked, [date(2026, 10, 17), date(2026, 10, 31)])

    def test_single_window_when_history_is_short(self):
        picked = referrer_split.pick_windows({date(2026, 10, 11)}, date(2026, 11, 1))
        self.assertEqual(picked, [date(2026, 10, 11)])

    def test_nothing_before_as_of(self):
        self.assertEqual(referrer_split.pick_windows({date(2026, 10, 11)}, date(2026, 10, 1)), [])


class CommandTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=os.environ.get("TMPDIR"))
        self.addCleanup(self.temp.cleanup)
        self.data = Path(self.temp.name)

    def write(self, repo, rows):
        lines = [json.dumps({"date": d, "window_days": 14, "referrers": refs}) for d, refs in rows]
        (self.data / f"{repo}.jsonl").write_text("\n".join(lines) + "\n", encoding="utf-8")

    def run_script(self, *args):
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--data-dir", str(self.data), *args],
            capture_output=True, text=True,
        )

    def test_sums_two_windows_per_bucket(self):
        self.write("a", [
            ("2026-10-11", [{"referrer": "github.com", "count": 5, "uniques": 1},
                            {"referrer": "chatgpt.com", "count": 2, "uniques": 1}]),
            ("2026-10-20", [{"referrer": "github.com", "count": 99, "uniques": 9}]),
            ("2026-10-31", [{"referrer": "Google", "count": 3, "uniques": 2}]),
        ])
        self.write("b", [
            ("2026-10-11", [{"referrer": "t.co", "count": 4, "uniques": 4}]),
            ("2026-10-31", []),
        ])
        out = self.run_script("--as-of", "2026-11-01", "--format", "json")
        self.assertEqual(out.returncode, 0, out.stderr)
        result = json.loads(out.stdout)
        # 2026-10-20 overlaps the 2026-10-31 window and must not be counted.
        self.assertEqual(result["totals"], {"ai": 2, "search": 3, "github": 5, "other": 4})
        self.assertEqual(result["total"], 14)
        self.assertEqual([w["end"] for w in result["windows"]], ["2026-10-11", "2026-10-31"])

    def test_markdown_row_and_missing_note(self):
        self.write("a", [("2026-10-11", [{"referrer": "github.com", "count": 1, "uniques": 1}])])
        self.write("b", [("2026-10-12", [])])
        out = self.run_script("--as-of", "2026-10-11")
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertTrue(out.stdout.startswith("| 2026-10-11 | 2026-09-28 to 2026-10-11 | 0 (—) |"), out.stdout)
        self.assertIn("1 repository-windows missing", out.stdout)

    def test_bad_count_fails_loudly(self):
        self.write("a", [("2026-10-11", [{"referrer": "github.com", "count": -1, "uniques": 1}])])
        out = self.run_script("--as-of", "2026-10-11")
        self.assertEqual(out.returncode, 1)
        self.assertIn("nonnegative", out.stderr)

    def test_no_snapshot_before_as_of(self):
        self.write("a", [("2026-10-11", [])])
        out = self.run_script("--as-of", "2026-10-01")
        self.assertEqual(out.returncode, 1)
        self.assertIn("no snapshot", out.stderr)


if __name__ == "__main__":
    unittest.main()
