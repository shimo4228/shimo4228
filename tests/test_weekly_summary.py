"""Stdlib-only tests for the weekly one-page summary and its helpers."""
from datetime import date
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import cf_web_analytics  # noqa: E402  # pyright: ignore[reportMissingImports]
import stars_snapshot  # noqa: E402  # pyright: ignore[reportMissingImports]
import weekly_summary as ws  # noqa: E402  # pyright: ignore[reportMissingImports]


def write_jsonl(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(r) + "\n" for r in rows), encoding="utf-8")


def day(d, views):
    return {"date": d, "clones": {"count": 0, "uniques": 0}, "views": {"count": views, "uniques": views}}


class WeekTests(unittest.TestCase):
    def test_last_sunday(self):
        self.assertEqual(ws.last_sunday(date(2026, 10, 26)), date(2026, 10, 25))  # Monday
        self.assertEqual(ws.last_sunday(date(2026, 10, 25)), date(2026, 10, 18))  # Sunday itself is not done
        self.assertEqual(ws.last_sunday(date(2026, 10, 22)), date(2026, 10, 18))

    def test_week_bounds(self):
        self.assertEqual(
            ws.week_of(date(2026, 10, 18)),
            (date(2026, 10, 12), date(2026, 10, 18), date(2026, 10, 5), date(2026, 10, 11)),
        )


class RenderTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        t = self.root / "traffic"
        write_jsonl(t / "data/a.jsonl", [day(f"2026-10-{d:02d}", 2) for d in range(5, 19)])
        write_jsonl(t / "data/b.jsonl", [day("2026-10-13", 5)])
        write_jsonl(t / "referrers/a.jsonl", [{"date": "2026-10-18", "referrers": [
            {"referrer": "Google", "count": 3, "uniques": 1}, {"referrer": "t.co", "count": 4, "uniques": 2}]}])
        write_jsonl(t / "stars.jsonl", [
            {"date": "2026-10-11", "followers": 60, "repos": {"a": {"stars": 10, "forks": 0}}},
            {"date": "2026-10-18", "followers": 63, "repos": {"a": {"stars": 12, "forks": 0}}},
        ])

    def tearDown(self):
        self.tmp.cleanup()

    def page(self, **kw):
        t = self.root / "traffic"
        return ws.render(date(2026, 10, 18), t / "data", t / "referrers", t / "stars.jsonl",
                         kw.get("zenn"), kw.get("site"))

    def test_views_and_missing_days(self):
        p = self.page()
        self.assertIn("閲覧 **19**（前週 14、+5）", p)
        self.assertIn("| b（6 日欠測） | 5 | 0 | +5 | 5 |", p)

    def test_stars_change(self):
        p = self.page()
        self.assertIn("フォロワー **63**（週の差 +3）", p)
        self.assertIn("| a | 12 | +2 |", p)

    def test_referrer_buckets(self):
        p = self.page()
        self.assertIn("検索 3", p)
        self.assertIn("その他 4", p)

    def test_missing_sources_are_said_not_zeroed(self):
        p = self.page()
        self.assertIn("Cloudflare Web Analytics の値はまだ取り込んでいません", p)
        self.assertIn("snapshots.jsonl を読めませんでした", p)

    def test_zenn_and_site(self):
        z = self.root / "snap.jsonl"
        write_jsonl(z, [
            {"ts": "2026-10-11T00:00:00+00:00", "source": "zenn", "slug": "x", "liked": 4},
            {"ts": "2026-10-18T00:00:00+00:00", "source": "zenn", "slug": "x", "liked": 6},
            {"ts": "2026-10-18T00:00:00+00:00", "type": "followers", "zenn": 16, "devto": 748},
            {"ts": "2026-10-12T00:00:00+00:00", "source": "zenn_dash", "type": "account",
             "window": "last_1_month", "views": 3305},
        ])
        s = self.root / "site.json"
        s.write_text(json.dumps({"this": {"visits": 9, "pageviews": 20,
                                          "referers": [{"host": "", "visits": 5}],
                                          "paths": [{"path": "/", "pageviews": 12}]},
                                 "prev": {"visits": 4, "pageviews": 6}}), encoding="utf-8")
        p = self.page(zenn=z, site=s)
        self.assertIn("**6**（2026-10-11 の記録から +2）", p)
        self.assertIn("Zenn 16、Dev.to 748", p)
        self.assertIn("**3305**", p)
        self.assertIn("訪問 **9**（前週 4、+5）", p)
        self.assertIn("| （直接・不明） | 5 |", p)

    def test_site_error_is_reported(self):
        s = self.root / "site.json"
        s.write_text(json.dumps({"error": "bad token"}), encoding="utf-8")
        self.assertIn("取得できませんでした: bad token", self.page(site=s))

    def test_main_writes_page_and_index(self):
        ws.main(["--root", str(self.root), "--end", "2026-10-18"])
        weekly = self.root / "traffic/weekly"
        self.assertTrue((weekly / "2026-10-18.md").exists())
        self.assertIn("[2026-10-18](2026-10-18.md)", (weekly / "README.md").read_text(encoding="utf-8"))


class StarsMergeTests(unittest.TestCase):
    def test_same_day_replaced(self):
        lines = [json.dumps({"date": "2026-10-21", "followers": 1}), json.dumps({"date": "2026-10-22", "followers": 2})]
        out = stars_snapshot.merge(lines, {"date": "2026-10-22", "followers": 3})
        self.assertEqual([json.loads(l)["followers"] for l in out], [1, 3])


class CloudflareTests(unittest.TestCase):
    def test_missing_secrets(self):
        import os
        saved = {k: os.environ.pop(k, None) for k in ("CF_API_TOKEN", "CF_ACCOUNT_ID", "CF_SITE_TAG")}
        try:
            self.assertIn("error", cf_web_analytics.fetch(date(2026, 10, 18)))
        finally:
            for k, v in saved.items():
                if v is not None:
                    os.environ[k] = v

    def test_shape(self):
        data = {"data": {"viewer": {"accounts": [{
            "total": [{"count": 20, "sum": {"visits": 9}}],
            "prev": [],
            "referers": [{"sum": {"visits": 5}, "dimensions": {"refererHost": "t.co"}}],
            "paths": [{"count": 12, "dimensions": {"requestPath": "/"}}],
        }]}}}
        out = cf_web_analytics.shape(data, date(2026, 10, 12), date(2026, 10, 18))
        self.assertEqual(out["this"]["visits"], 9)
        self.assertEqual(out["prev"], {"visits": 0, "pageviews": 0})
        self.assertEqual(out["this"]["referers"][0]["host"], "t.co")


if __name__ == "__main__":
    unittest.main()
