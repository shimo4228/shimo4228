"""Two-channel LLM probe runner.

Sends versioned controlled prompts to four model providers and appends one
JSONL line per (run × provider × probe) to probes/data/<channel>.jsonl.

Channels (never blended — see authorship-strategy ADR-0008):
  parametric — web search OFF; measures what the model names from trained knowledge
  retrieval  — web search ON; measures whether owned identifiers are cited

The parametric channel is event-driven (a frozen model's weights cannot
change between runs): run the full parametric set with --repeat 3 when a
model enters the panel, and run --currency-check monthly to detect the
change events (silent alias swaps, new catalog ids, stale verification).

Usage:
  uv run probe_runner.py --dry-run
  uv run probe_runner.py --provider anthropic --probe parametric-concept-akc
  uv run probe_runner.py --channel parametric --repeat 3
  uv run probe_runner.py --channel retrieval
  uv run probe_runner.py --channel retrieval --run-id latest  # gap-fill last run
  uv run probe_runner.py --currency-check [--strict]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import yaml
from dotenv import load_dotenv

from currency import (
    ENV_KEYS,
    diff_catalog,
    fetch_model_ids,
    filter_chat_candidates,
    is_stale,
    latest_per_provider,
)
from extract import Lexicon, detect
from providers import (
    PROVIDERS,
    RESPONSES_PROVIDERS,
    build_call_kwargs,
    extract_citations,
    extract_citations_responses,
    resolve_redirect_urls,
    response_text,
    responses_call,
    responses_output_text,
)

RUNNER_VERSION = "0.4.0"  # 0.4.0: --run-id latest (scheduled gap-fill); 0.3.0: per-provider call throttle (anthropic input-TPM); 0.2.0: responses-API retrieval (openai/xai), redirect resolution, qwen thinking off
HERE = Path(__file__).resolve().parent
DEFAULT_CONFIG = HERE.parent / "config" / "probes-v4.yaml"
DEFAULT_DATA_DIR = HERE.parent / "data"

# Minimum seconds between successive calls to the same provider, measured
# start-to-start. Operational throttle (not part of the experiment / prompt
# hash): a single anthropic retrieval probe accumulates 20k-68k input tokens
# across its agentic web-search loop, so two back-to-back calls blow the org's
# 30k input-tokens-per-minute limit on claude-sonnet. ~60s start-to-start keeps
# the run under the cap; big calls that already take >60s incur no extra wait.
# Providers absent from this map are uncapped.
PROVIDER_MIN_INTERVAL_S = {"anthropic": 60.0}
_last_call_start: dict[str, float] = {}


def throttle(provider: str) -> None:
    """Sleep so successive same-provider calls respect PROVIDER_MIN_INTERVAL_S.

    No-op for the first call to a provider in a run (nothing to space against),
    so single-probe gap-fills never wait.
    """
    interval = PROVIDER_MIN_INTERVAL_S.get(provider, 0.0)
    last = _last_call_start.get(provider)
    if interval and last is not None:
        wait = interval - (time.monotonic() - last)
        if wait > 0:
            print(f"  throttle: {provider} sleeping {wait:.0f}s (input-TPM)", flush=True)
            time.sleep(wait)
    _last_call_start[provider] = time.monotonic()


def render_prompt(probe: dict) -> str:
    return probe["template"].format(**probe.get("vars", {}))


def prompt_sha256(prompt: str) -> str:
    return hashlib.sha256(prompt.encode("utf-8")).hexdigest()


def load_config(path: Path) -> dict:
    with path.open() as f:
        config = yaml.safe_load(f)
    for key in ("version", "models", "detection", "probes"):
        if key not in config:
            raise ValueError(f"config missing required key: {key}")
    return config


def existing_triples(data_file: Path) -> set[tuple[str, str, str]]:
    """(run_id, provider, probe_id) triples already written successfully.

    Errored records are excluded so re-invoking with the same --run-id
    retries exactly the failed calls (gap fill); the errored lines stay in
    the append-only log, and analysis prefers the non-error record.
    """
    triples = set()
    if not data_file.exists():
        return triples
    with data_file.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue  # tolerate a truncated trailing write (crash mid-run)
            # Pre-guard records could be error-free yet empty (degenerate);
            # treat those as not-done so a retry can fill them.
            if rec.get("error") is None and (rec.get("response_text") or rec.get("cited_urls")):
                triples.add((rec["run_id"], rec["provider"], rec["probe_id"]))
    return triples


def resolve_latest_run_id(data_file: Path) -> str | None:
    """Most recent run_id in an append-only channel log (for gap-fill).

    run_ids are `<UTC ISO8601>-<channel>`, so the timestamp prefix makes
    lexicographic max == chronological latest within one channel file. A
    scheduled gap-fill pass uses this so it need not know the run's date;
    combined with existing_triples() it retries exactly the unfilled cells.
    """
    latest = None
    if not data_file.exists():
        return None
    with data_file.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rid = json.loads(line).get("run_id")
            except json.JSONDecodeError:
                continue  # tolerate a truncated trailing write (crash mid-run)
            if isinstance(rid, str) and (latest is None or rid > latest):
                latest = rid
    return latest


def probe_channels(probe: dict) -> list[str]:
    """Channels a probe runs on. v2 probes carry `channels` (A/B crossed
    design — same prompt, both settings); v1 probes carried a single
    `channel`, still accepted for older config files."""
    if "channels" in probe:
        return list(probe["channels"])
    return [probe["channel"]]


def select_arms(
    config: dict, channel: str | None, probe_id: str | None
) -> list[tuple[dict, str]]:
    """(probe, channel) execution arms matching the filters."""
    arms = []
    for probe in config["probes"]:
        if probe_id and probe["id"] != probe_id:
            continue
        for ch in probe_channels(probe):
            if channel and ch != channel:
                continue
            arms.append((probe, ch))
    return arms


def token_cost(
    provider: str,
    model: str,
    prompt_tokens: int | None,
    completion_tokens: int | None,
) -> float | None:
    """USD token cost via litellm's price map; None if the model is unmapped.

    Used for the responses-endpoint providers (openai/xai), whose direct-HTTP
    path bypasses litellm's automatic cost map. custom_llm_provider is required
    so unprefixed ids like "grok-4.3" resolve to the right price table. Token
    cost captures ~96-100% of the real bill; the web-search tool fee (a few %
    on retrieval) is not itemized.
    """
    import litellm

    try:
        prompt_cost, completion_cost = litellm.cost_per_token(
            model=model,
            prompt_tokens=prompt_tokens or 0,
            completion_tokens=completion_tokens or 0,
            custom_llm_provider=provider,
        )
        return prompt_cost + completion_cost
    except Exception:
        return None


def run_one(provider: str, probe: dict, channel: str, config: dict, run_id: str) -> dict:
    """One API call → one JSONL record (dict)."""
    from importlib.metadata import version as pkg_version

    import litellm

    # Reasoning-tier models reject explicit temperature; drop unsupported
    # params at the provider boundary instead of failing the probe. The
    # record's temperature field documents what was requested.
    litellm.drop_params = True

    model = config["models"][provider]
    prompt = render_prompt(probe)
    defaults = config.get("defaults", {})
    # openai/xai retrieval lives on the responses endpoint (chat completions
    # returns no citation metadata there) — direct HTTP adapter.
    use_responses = provider in RESPONSES_PROVIDERS and channel == "retrieval"
    kwargs = (
        None
        if use_responses
        else build_call_kwargs(
            provider,
            model,
            prompt,
            channel,
            defaults,
            (config.get("param_overrides") or {}).get(provider),
        )
    )
    record = {
        "run_id": run_id,
        "ts": datetime.now(timezone.utc).isoformat(),
        "channel": channel,
        "provider": provider,
        "model_requested": model,
        "model_returned": None,
        "probe_id": probe["id"],
        "probe_set_version": config["version"],
        "prompt_sha256": prompt_sha256(prompt),
        "temperature": (kwargs or {}).get("temperature"),  # None = provider default
        "web_search_enabled": channel == "retrieval",
        "response_text": "",
        "cited_urls": [],
        "citation_source": "none",
        "detect": None,
        "usage": None,
        "error": None,
        "runner": {"version": RUNNER_VERSION, "litellm": pkg_version("litellm")},
    }
    try:
        if use_responses:
            response_dict = responses_call(
                provider,
                model,
                prompt,
                (config.get("param_overrides") or {}).get(provider, {}).get(
                    "max_tokens"
                )
                or defaults.get("max_tokens", 1024),
                os.environ.get(ENV_KEYS[provider], ""),
            )
            text = responses_output_text(response_dict)
            cited_urls, citation_source = extract_citations_responses(response_dict)
            usage = response_dict.get("usage") or {}
            prompt_tokens = usage.get("input_tokens")
            completion_tokens = usage.get("output_tokens")
            # responses endpoint bypasses litellm's auto cost map; price the
            # tokens ourselves (web-search tool fee, a few %, is not itemized).
            cost = token_cost(provider, model, prompt_tokens, completion_tokens)
        else:
            # In-call retry with backoff for transient provider failures
            # (429/503) — observed: gemini-3.5-flash returned 503 bursts
            # lasting minutes. Cross-run gaps are still fillable via
            # same-run-id retries; this just absorbs the short tail.
            response = litellm.completion(**kwargs, num_retries=2)
            response_dict = response.model_dump()
            text = response_text(response_dict)
            cited_urls, citation_source = extract_citations(response_dict)
            usage = response_dict.get("usage") or {}
            prompt_tokens = usage.get("prompt_tokens")
            completion_tokens = usage.get("completion_tokens")
            try:
                cost = litellm.completion_cost(completion_response=response)
            except Exception:
                cost = None
        record["model_returned"] = response_dict.get("model")
        record["response_text"] = text
        resolved_urls, any_resolved = resolve_redirect_urls(cited_urls)
        if any_resolved:
            record["cited_urls_unresolved"] = cited_urls
            cited_urls = resolved_urls
        record["cited_urls"] = cited_urls
        record["citation_source"] = citation_source
        record["detect"] = detect(
            text, cited_urls, Lexicon.from_config(config["detection"]), prompt
        )
        record["usage"] = {
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "cost_usd": round(cost, 6) if cost is not None else None,
        }
        if not text and not cited_urls:
            # A degenerate call (e.g. reasoning tokens exhausting max_tokens)
            # must not count as an observation; marking it an error keeps it
            # out of analysis and lets a same-run-id retry fill the gap.
            record["error"] = (
                "EmptyResponse: no visible text "
                f"(completion_tokens={completion_tokens}; check reasoning token budget)"
            )
    except Exception as exc:  # recorded, not raised — one bad call must not kill a run
        record["error"] = f"{type(exc).__name__}: {exc}"
    return record


def run_currency_check(config: dict, data_dir: Path, strict: bool) -> int:
    """Monthly change-event detector. Exit 0 = no events; 3 = events found
    (only when strict); per-provider errors are recorded, not fatal."""
    import litellm

    data_dir.mkdir(parents=True, exist_ok=True)
    catalog_path = data_dir / "model-catalog.jsonl"
    currency_path = data_dir / "currency.jsonl"
    prev_catalog = latest_per_provider(catalog_path)
    prev_currency = latest_per_provider(currency_path)
    ts = datetime.now(timezone.utc).isoformat()
    events: list[str] = []

    stale = is_stale(
        config.get("verified_current", "1970-01-01"),
        datetime.now(timezone.utc).date(),
        int(config.get("staleness_days", 90)),
    )
    if stale:
        events.append(
            f"STALE: panel verification ({config.get('verified_current')}) is older "
            f"than {config.get('staleness_days', 90)} days — re-verify the default "
            "tier per provider and update verified_current in the config"
        )

    for provider in PROVIDERS:
        api_key = os.environ.get(ENV_KEYS[provider], "")
        record = {
            "ts": ts,
            "provider": provider,
            "pinned_model": config["models"][provider],
            "model_returned": None,
            "previous_model_returned": (prev_currency.get(provider) or {}).get("model_returned"),
            "swap_detected": False,
            "catalog_new_ids": [],
            "catalog_removed_ids": [],
            "catalog_new_chat_candidates": [],
            # pyyaml parses an unquoted ISO date as datetime.date — stringify
            "verified_current": str(config.get("verified_current", "")),
            "stale": stale,
            "error": None,
        }
        if not api_key:
            record["error"] = f"missing {ENV_KEYS[provider]}"
        else:
            # 1. silent-swap detection: one minimal completion, compare the
            #    served model identity against the last observation. Routed
            #    through build_call_kwargs so provider transport adjustments
            #    (endpoint overrides, param overrides) apply to the ping too.
            try:
                ping_kwargs = build_call_kwargs(
                    provider,
                    config["models"][provider],
                    "ping",
                    "parametric",
                    {"temperature": 0, "max_tokens": 16},
                    (config.get("param_overrides") or {}).get(provider),
                )
                ping_kwargs["max_tokens"] = 16
                resp = litellm.completion(**ping_kwargs, num_retries=2)
                record["model_returned"] = resp.model_dump().get("model")
                prev = record["previous_model_returned"]
                if prev is not None and record["model_returned"] != prev:
                    record["swap_detected"] = True
                    events.append(
                        f"SWAP {provider}: {prev} -> {record['model_returned']} "
                        "(silent change behind the pinned alias — series break; "
                        "consider a parametric full run)"
                    )
            except Exception as exc:
                record["error"] = f"ping: {type(exc).__name__}: {exc}"
            # 2. catalog diff: newly published / removed model ids.
            try:
                ids = fetch_model_ids(provider, api_key)
                with catalog_path.open("a") as f:
                    f.write(json.dumps({"ts": ts, "provider": provider, "models": ids}) + "\n")
                prev_ids = (prev_catalog.get(provider) or {}).get("models")
                if prev_ids is None:
                    print(f"{provider}: catalog baseline established ({len(ids)} ids)")
                else:
                    new, removed = diff_catalog(prev_ids, ids)
                    record["catalog_new_ids"] = new
                    record["catalog_removed_ids"] = removed
                    record["catalog_new_chat_candidates"] = filter_chat_candidates(new)
                    for mid in record["catalog_new_chat_candidates"]:
                        events.append(
                            f"NEW MODEL {provider}: {mid} (panel adoption is a "
                            "human judgment — check the provider's default tier)"
                        )
            except Exception as exc:
                err = f"catalog: {type(exc).__name__}: {exc}"
                record["error"] = f"{record['error']}; {err}" if record["error"] else err
        if record["error"]:
            events.append(f"ERROR {provider}: {record['error']}")
        with currency_path.open("a") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
        print(
            f"{provider}: served={record['model_returned']} swap={record['swap_detected']} "
            f"new_chat_ids={len(record['catalog_new_chat_candidates'])} "
            f"err={record['error'] or '-'}"
        )

    if events:
        print("\n== change events ==")
        for e in events:
            print(f"- {e}")
        return 3 if strict else 0
    print("\nno change events — panel is current")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--channel", choices=["parametric", "retrieval"], default=None,
                        help="run only this channel (default: both)")
    parser.add_argument("--provider", action="append", choices=PROVIDERS, default=None,
                        help="repeatable; default: all four providers")
    parser.add_argument("--probe", default=None, help="run only this probe id")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--data-dir", type=Path, default=DEFAULT_DATA_DIR)
    parser.add_argument("--run-id", default=None,
                        help="default: <UTC timestamp>-<channel|all>; "
                             "'latest' resolves the most recent run in the "
                             "channel log to gap-fill its unfilled cells")
    parser.add_argument("--cost-budget", type=float, default=10.0,
                        help="soft budget (USD): warn once if cumulative cost "
                             "exceeds this, but do not abort (the run is a bounded "
                             "probe×provider×repeat loop, so cost cannot run away)")
    parser.add_argument("--repeat", type=int, default=1,
                        help="repetitions per (probe × provider), for within-model "
                             "variance at model-entry events (run_id gets -rN suffix)")
    parser.add_argument("--dry-run", action="store_true",
                        help="render prompts, validate config, write nothing, call nothing")
    parser.add_argument("--currency-check", action="store_true",
                        help="detect model-change events (silent swaps, new catalog ids, "
                             "stale verification) instead of probing")
    parser.add_argument("--strict", action="store_true",
                        help="with --currency-check: exit 3 when change events are found")
    args = parser.parse_args(argv)

    load_dotenv(HERE.parent / ".env")
    load_dotenv()  # cwd .env, if any

    config = load_config(args.config)
    Lexicon.from_config(config["detection"])  # validate lexicon early

    if args.currency_check:
        return run_currency_check(config, args.data_dir, args.strict)

    providers = args.provider or list(PROVIDERS)
    arms = select_arms(config, args.channel, args.probe)
    if not arms:
        print("no probe arms match the given filters", file=sys.stderr)
        return 1

    if args.run_id == "latest":
        # Gap-fill mode: resolve the most recent run from the channel log and
        # retry only its unfilled cells (provider 503 bursts can outlast the
        # in-call retry, so a delayed pass mops up what the live run missed).
        if args.repeat > 1:
            # Resolving "latest" picks one rep's run_id (e.g. -r3); appending a
            # fresh -rN on top would match nothing and re-run every cell.
            print("--run-id latest is incompatible with --repeat", file=sys.stderr)
            return 1
        if not args.channel:
            print("--run-id latest requires --channel", file=sys.stderr)
            return 1
        run_id = resolve_latest_run_id(args.data_dir / f"{args.channel}.jsonl")
        if run_id is None:
            print(
                f"--run-id latest: no prior runs in {args.channel}.jsonl",
                file=sys.stderr,
            )
            return 1
        print(f"# gap-fill: resolved latest run-id = {run_id}")
    else:
        run_id = args.run_id or (
            datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ")
            + "-" + (args.channel or "all")
        )

    if args.dry_run:
        print(f"# dry-run — config {args.config.name} (probe set {config['version']})")
        print(f"# run_id would be: {run_id}")
        print(f"# providers: {', '.join(providers)}")
        print(f"# calls that would be made: {len(arms) * len(providers) * max(args.repeat, 1)}")
        for probe, channel in arms:
            prompt = render_prompt(probe)
            print(f"\n## {probe['id']} [{channel}] sha256={prompt_sha256(prompt)[:16]}…")
            print(prompt)
        return 0

    args.data_dir.mkdir(parents=True, exist_ok=True)
    total_cost = 0.0
    budget_warned = False
    written = skipped = errors = 0
    rep_run_ids = (
        [run_id]
        if args.repeat <= 1
        else [f"{run_id}-r{n}" for n in range(1, args.repeat + 1)]
    )

    for rep_run_id in rep_run_ids:
        for probe, channel in arms:
            data_file = args.data_dir / f"{channel}.jsonl"
            triples = existing_triples(data_file)
            for provider in providers:
                key = (rep_run_id, provider, probe["id"])
                if key in triples:
                    print(f"skip duplicate: {provider} × {probe['id']} (run {rep_run_id})")
                    skipped += 1
                    continue
                print(
                    f"probe: {provider} × {probe['id']} [{channel}] ({rep_run_id}) …",
                    flush=True,
                )
                throttle(provider)
                record = run_one(provider, probe, channel, config, rep_run_id)
                with data_file.open("a") as f:
                    f.write(json.dumps(record, ensure_ascii=False) + "\n")
                if record["error"]:
                    errors += 1
                    print(f"  ERROR: {record['error']}", file=sys.stderr)
                else:
                    written += 1
                    cost = (record["usage"] or {}).get("cost_usd") or 0.0
                    total_cost += cost
                    d = record["detect"]
                    print(
                        f"  author={d['author_named']} project={d['project_named']} "
                        f"cited={d['doi_or_url_cited']} ghost={d['ghost_citation']} "
                        f"src={record['citation_source']} cost=${cost:.4f}"
                    )
                if not budget_warned and total_cost > args.cost_budget:
                    print(
                        f"  WARNING: cost budget ${args.cost_budget} exceeded "
                        f"(${total_cost:.4f}) — continuing (run is bounded)",
                        file=sys.stderr,
                    )
                    budget_warned = True

    print(
        f"\nrun {run_id}: {written} written, {skipped} skipped, "
        f"{errors} errors, total ${total_cost:.4f}"
    )
    return 0 if errors == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
