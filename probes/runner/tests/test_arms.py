"""A/B crossed-design (probe set v2) arm-expansion tests. Zero API budget."""

from pathlib import Path

import yaml

from probe_runner import probe_channels, prompt_sha256, render_prompt, select_arms

CONFIG_DIR = Path(__file__).resolve().parents[2] / "config"
V1 = yaml.safe_load((CONFIG_DIR / "probes-v1.yaml").read_text())
V2 = yaml.safe_load((CONFIG_DIR / "probes-v2.yaml").read_text())
V3 = yaml.safe_load((CONFIG_DIR / "probes-v3.yaml").read_text())
V4 = yaml.safe_load((CONFIG_DIR / "probes-v4.yaml").read_text())

V1_TO_V2_IDS = {
    "parametric-concept-akc": "concept-akc",
    "parametric-author-identity": "author-identity",
    "parametric-concept-inversion": "concept-inversion",
    "parametric-control-fake": "control-fake",
    "retrieval-concept-contemplative": "concept-contemplative",
    "retrieval-recommend-authorship": "recommend-authorship",
}


def test_every_v2_probe_runs_both_channels():
    for probe in V2["probes"]:
        assert probe_channels(probe) == ["parametric", "retrieval"], probe["id"]


def test_select_arms_channel_filter():
    all_arms = select_arms(V2, None, None)
    parametric = select_arms(V2, "parametric", None)
    retrieval = select_arms(V2, "retrieval", None)
    assert len(all_arms) == len(V2["probes"]) * 2
    assert len(parametric) == len(retrieval) == len(V2["probes"])
    assert all(ch == "parametric" for _, ch in parametric)


def test_select_arms_probe_filter():
    arms = select_arms(V2, None, "control-fake")
    assert {(p["id"], ch) for p, ch in arms} == {
        ("control-fake", "parametric"),
        ("control-fake", "retrieval"),
    }


def test_v1_single_channel_back_compat():
    assert probe_channels({"id": "x", "channel": "parametric"}) == ["parametric"]


def test_v1_v2_template_hash_continuity():
    # The A/B redesign renamed probe ids but kept templates byte-identical;
    # prompt_sha256 is the cross-version join key, so it must not move.
    v1_hashes = {p["id"]: prompt_sha256(render_prompt(p)) for p in V1["probes"]}
    v2_hashes = {p["id"]: prompt_sha256(render_prompt(p)) for p in V2["probes"]}
    for v1_id, v2_id in V1_TO_V2_IDS.items():
        assert v1_hashes[v1_id] == v2_hashes[v2_id], (v1_id, v2_id)


def test_v3_extends_v2_without_moving_shared_templates():
    v2_hashes = {p["id"]: prompt_sha256(render_prompt(p)) for p in V2["probes"]}
    v3_hashes = {p["id"]: prompt_sha256(render_prompt(p)) for p in V3["probes"]}
    for pid, h in v2_hashes.items():
        assert v3_hashes[pid] == h, pid
    assert set(v3_hashes) - set(v2_hashes) == {"concept-aap", "concept-ans"}
    # all five research lines now have a concept probe (gradient coverage)
    assert {p.get("expect", {}).get("project") for p in V3["probes"]} >= {
        "akc", "contemplative", "authorship", "aap", "ans",
    }
    assert len(select_arms(V3, None, None)) == len(V3["probes"]) * 2


def test_v4_retires_recommend_authorship_and_retargets():
    v3_ids = {p["id"] for p in V3["probes"]}
    v4_ids = {p["id"] for p in V4["probes"]}
    assert v3_ids - v4_ids == {"recommend-authorship"}
    assert v4_ids - v3_ids == {"recommend-contemplative"}
    # form-gradient pairing: same topic as the listing-form probe, so the
    # question form is the only variable between the two
    by_id = {p["id"]: p for p in V4["probes"]}
    assert (
        by_id["recommend-contemplative"]["vars"]["topic"]
        == by_id["concept-contemplative"]["vars"]["topic"]
    )
    # retained probes keep byte-identical templates (hash continuity)
    v3_hashes = {p["id"]: prompt_sha256(render_prompt(p)) for p in V3["probes"]}
    v4_hashes = {p["id"]: prompt_sha256(render_prompt(p)) for p in V4["probes"]}
    for pid in v3_ids & v4_ids:
        assert v3_hashes[pid] == v4_hashes[pid], pid
