"""End-to-end, stdlib-only traffic comparison tests."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/traffic_compare.py"
LEGACY = (
    "contemplative-agent", "agent-knowledge-cycle", "agent-attribution-practice",
    "authorship-strategy", "attention-not-self", "contemplative-agent-data",
    "zenn-content", "claude-harness", "shimo4228",
)
ADDITIONAL = (
    "search-first", "skill-stocktake", "codex-review", "readme-writer",
    "llms-txt-writer", "harness-pruning",
)


class TrafficCompareTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=os.environ.get("TMPDIR"))
        self.addCleanup(self.temp.cleanup)
        self.data = Path(self.temp.name)
        for repo in LEGACY + ADDITIONAL:
            self.write(repo, [("2026-09-18", 1)])

    def write(self, repo, records):
        (self.data / f"{repo}.jsonl").write_text("".join(
            json.dumps({"date": day, "views": {"count": count}}) + "\n"
            for day, count in records
        ), encoding="utf-8")

    def run_cli(self, start="2026-09-18", end="2026-09-18", data=None):
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--data-dir", str(data or self.data),
             "--start", start, "--end", end],
            capture_output=True, text=True, check=False,
        )

    def report(self, **kwargs):
        result = self.run_cli(**kwargs)
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)

    def test_legacy_is_stable_when_additional_and_unlisted_files_appear(self):
        for repo in ADDITIONAL:
            (self.data / f"{repo}.jsonl").unlink()
        before = self.run_cli()
        self.assertTrue(before.stdout, before.stderr)
        before_legacy = json.loads(before.stdout)["groups"]["legacy"]
        for repo in ADDITIONAL:
            self.write(repo, [("2026-09-18", 10)])
        (self.data / "unlisted.jsonl").write_text("not JSON", encoding="utf-8")
        after = self.report()
        self.assertEqual(after["groups"]["legacy"], before_legacy)
        self.assertEqual(before_legacy["repos"], list(LEGACY))
        self.assertEqual(before_legacy["views_count"], 9)
        self.assertEqual(after["groups"]["additional"]["repos"], list(ADDITIONAL))
        self.assertEqual(after["groups"]["additional"]["views_count"], 60)
        self.assertEqual(after["groups"]["claude-harness"]["views_count"], 1)
        self.assertEqual(after["groups"]["total_reference"]["views_count"], 69)

    def test_missing_file_or_day_is_partial_not_zero(self):
        (self.data / "search-first.jsonl").unlink()
        self.write("claude-harness", [])
        result = self.run_cli()
        self.assertEqual(result.returncode, 1, result.stderr)
        groups = json.loads(result.stdout)["groups"]
        for name in ("legacy", "additional", "claude-harness", "total_reference"):
            self.assertFalse(groups[name]["complete"])
            self.assertIsNone(groups[name]["views_count"])
        self.assertEqual(groups["legacy"]["partial_views_count"], 8)
        self.assertEqual(groups["legacy"]["expected_repo_days"], 9)
        self.assertEqual(groups["legacy"]["observed_repo_days"], 8)
        self.assertEqual(groups["legacy"]["missing_dates"],
                         {"claude-harness": ["2026-09-18"]})
        self.assertEqual(groups["additional"]["missing_files"], ["search-first"])
        self.assertEqual(groups["claude-harness"]["partial_views_count"], 0)

    def test_window_includes_both_utc_date_endpoints(self):
        for repo in LEGACY + ADDITIONAL:
            self.write(repo, [("2026-09-17", 100), ("2026-09-18", 2),
                              ("2026-09-19", 3), ("2026-09-20", 100)])
        report = self.report(end="2026-09-19")
        self.assertEqual(report["timezone"], "UTC")
        self.assertTrue(report["inclusive"])
        self.assertEqual(report["days"], 2)
        self.assertEqual(report["groups"]["legacy"]["views_count"], 45)
        self.assertEqual(report["groups"]["legacy"]["observed_repo_days"], 18)

    def test_invalid_window_is_rejected_without_report(self):
        for start, end in (("20260918", "2026-09-18"),
                           ("2026-02-30", "2026-09-18"),
                           ("2026-09-19", "2026-09-18")):
            with self.subTest(start=start, end=end):
                result = self.run_cli(start=start, end=end)
                self.assertEqual(result.returncode, 2)
                self.assertEqual(result.stdout, "")
                self.assertIn("error:", result.stderr)

    def test_malformed_records_are_rejected_with_file_and_line(self):
        invalid = [
            "not JSON", "[]", "null", '{}',
            '{"date":"2026-02-30","views":{"count":1}}',
            '{"date":"20260918","views":{"count":1}}',
            '{"date":"2026-09-18","views":{}}',
            '{"date":"2026-09-18","views":{"count":-1}}',
            '{"date":"2026-09-18","views":{"count":true}}',
            '{"date":"2026-09-18","views":{"count":1.5}}',
            '{"date":"2026-09-18","views":{"count":"1"}}',
        ]
        for line in invalid:
            with self.subTest(line=line):
                (self.data / "shimo4228.jsonl").write_text(line + "\n", encoding="utf-8")
                result = self.run_cli()
                self.assertEqual(result.returncode, 2, result.stderr)
                self.assertEqual(result.stdout, "")
                self.assertIn("shimo4228.jsonl:1:", result.stderr)
                self.assertNotIn("Traceback", result.stderr)

    def test_duplicate_dates_are_rejected_even_outside_window(self):
        for count in (1, 2):
            with self.subTest(count=count):
                self.write("shimo4228", [("2026-09-17", 1), ("2026-09-17", count)])
                result = self.run_cli()
                self.assertEqual(result.returncode, 2)
                self.assertEqual(result.stdout, "")
                self.assertIn("shimo4228.jsonl:2: duplicate date 2026-09-17", result.stderr)

    def test_real_baseline_matches_independent_sum_and_is_read_only(self):
        data = ROOT / "traffic/data"
        before = {repo: (data / f"{repo}.jsonl").read_bytes() for repo in LEGACY}
        result = self.run_cli(start="2026-09-18", end="2026-10-01", data=data)
        # Missing new-repo files need not invalidate a complete legacy group.
        self.assertIn(result.returncode, (0, 1), result.stderr)
        report = json.loads(result.stdout)
        independent = sum(
            row["views"]["count"] for content in before.values()
            for line in content.decode().splitlines() if line.strip()
            for row in [json.loads(line)] if "2026-09-18" <= row["date"] <= "2026-10-01"
        )
        self.assertEqual(independent, 140)
        self.assertEqual(report["groups"]["legacy"]["views_count"], independent)
        self.assertTrue(report["groups"]["legacy"]["complete"])
        self.assertEqual(report["groups"]["legacy"]["observed_repo_days"], 126)
        self.assertEqual(report["groups"]["claude-harness"]["views_count"], 14)
        self.assertEqual(before, {repo: (data / f"{repo}.jsonl").read_bytes() for repo in LEGACY})

    def test_invalid_data_directory_is_rejected(self):
        for path in (self.data / "nonexistent", self.data / "shimo4228.jsonl"):
            with self.subTest(path=path):
                result = self.run_cli(data=path)
                self.assertEqual(result.returncode, 2)
                self.assertEqual(result.stdout, "")
                self.assertIn("data directory", result.stderr)


if __name__ == "__main__":
    unittest.main()
