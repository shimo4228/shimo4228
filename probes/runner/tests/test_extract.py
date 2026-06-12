"""Detector and citation-extraction tests. Zero API budget — fixtures only.

These tests are the main correctness gate: the detectors are the science.
"""

import json
from pathlib import Path

import pytest
import yaml

from extract import Lexicon, detect, extract_urls_from_text
from providers import (
    build_call_kwargs,
    extract_citations,
    extract_citations_responses,
    response_text,
    responses_output_text,
)

CONFIG = yaml.safe_load(
    (Path(__file__).resolve().parents[2] / "config" / "probes-v3.yaml").read_text()
)
LEXICON = Lexicon.from_config(CONFIG["detection"])
FIXTURES = Path(__file__).parent / "fixtures"


def load_fixture(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text())


# --- detect(): the four boolean outcomes ---------------------------------


def test_ghost_citation_cited_but_author_not_named():
    text = (
        "One relevant project is a contemplative behavioral preset framework "
        "for coding agents, available at "
        "https://github.com/shimo4228/contemplative-agent. It defines "
        "pre-action contemplation phases."
    )
    result = detect(text, ["https://github.com/shimo4228/contemplative-agent"], LEXICON)
    assert result["doi_or_url_cited"] is True
    assert result["author_named"] is False
    assert result["ghost_citation"] is True
    assert result["project_named"] is True


def test_negative_control_matches_nothing():
    text = (
        "I'm not aware of an established concept called 'Recursive Intent "
        "Lattice' in AI agent design. It does not appear in the literature "
        "I know. Could you share where you encountered the term?"
    )
    result = detect(text, [], LEXICON)
    assert result["author_named"] is False
    assert result["project_named"] is False
    assert result["doi_or_url_cited"] is False
    assert result["ghost_citation"] is False


def test_echo_guard_prompt_terms_do_not_count():
    # A denial that repeats the asked-about name must not count as naming.
    prompt = "What do you know about the researcher Tatsuya Shimomoto (GitHub: shimo4228)?"
    text = "I don't have information about Tatsuya Shimomoto or the account shimo4228."
    result = detect(text, [], LEXICON, prompt)
    assert result["author_named"] is False
    assert "Tatsuya Shimomoto" in result["matched"]["echoed"]["author"]


def test_echo_guard_keeps_non_prompt_aliases():
    # Knowledge the prompt did not supply still counts: the ORCID and a
    # project name were not in the prompt, so producing them is attribution.
    prompt = "What do you know about the researcher Tatsuya Shimomoto?"
    text = (
        "Tatsuya Shimomoto (ORCID 0009-0002-6168-4162) maintains the "
        "Agent Knowledge Cycle."
    )
    result = detect(text, [], LEXICON, prompt)
    assert result["author_named"] is True
    assert "0009-0002-6168-4162" in result["matched"]["author"]
    assert result["project_named"] is True


def test_echo_guard_concept_probe_project_echo():
    prompt = "In AI agent design, what is the 'Agent Knowledge Cycle'?"
    text = "The Agent Knowledge Cycle is not a concept I'm familiar with."
    result = detect(text, [], LEXICON, prompt)
    assert result["project_named"] is False
    assert result["matched"]["echoed"]["projects"]["akc"] == ["Agent Knowledge Cycle"]


def test_author_named_without_citation_is_not_ghost():
    text = (
        "The Agent Knowledge Cycle was proposed by Tatsuya Shimomoto, an "
        "independent researcher working on agent knowledge management."
    )
    result = detect(text, [], LEXICON)
    assert result["author_named"] is True
    assert result["project_named"] is True
    assert result["doi_or_url_cited"] is False
    assert result["ghost_citation"] is False


def test_full_attribution_owned_doi_in_prose():
    text = (
        "See shimo4228's Agent Knowledge Cycle, archived at "
        "DOI 10.5281/zenodo.19200726."
    )
    result = detect(text, [], LEXICON)
    assert result["author_named"] is True
    assert result["doi_or_url_cited"] is True
    assert result["ghost_citation"] is False
    assert "10.5281/zenodo.19200726" in result["matched"]["owned_dois"]


def test_unowned_zenodo_doi_does_not_count():
    text = "A related dataset is archived at DOI 10.5281/zenodo.99999999."
    result = detect(text, [], LEXICON)
    assert result["doi_or_url_cited"] is False


def test_authored_writing_surfaces_count_as_owned():
    # detector v3: the author's article surfaces are owned content (a real
    # GPT-5.5 answer cited the Zenn article and v2 missed it).
    result = detect(
        "A practical write-up covers this pattern.",
        ["https://zenn.dev/shimo4228/articles/coding-agent-memory-architecture"],
        LEXICON,
    )
    assert result["doi_or_url_cited"] is True


def test_unowned_cited_url_does_not_count():
    result = detect(
        "Several agent frameworks exist.",
        ["https://github.com/langchain-ai/langchain"],
        LEXICON,
    )
    assert result["doi_or_url_cited"] is False


def test_orcid_counts_as_author():
    text = "The author is identified by ORCID 0009-0002-6168-4162."
    assert detect(text, [], LEXICON)["author_named"] is True


def test_japanese_author_name_substring_match():
    text = "この研究は下本竜也によって維持されている。"
    assert detect(text, [], LEXICON)["author_named"] is True


def test_acronym_requires_word_boundary():
    # AKC inside a longer token must not match.
    assert detect("The BAKCEND framework is unrelated.", [], LEXICON)["project_named"] is False
    assert detect("AKC is a knowledge cycle.", [], LEXICON)["project_named"] is True


def test_author_alias_only_in_cited_url_is_ghost():
    # A handle visible only inside a cited URL is the ghost-citation
    # scenario: content cited, author not named in prose. The URL hit is
    # still recorded for auditability.
    result = detect(
        "An interesting repository covers this.",
        ["https://github.com/shimo4228/agent-knowledge-cycle"],
        LEXICON,
    )
    assert result["author_named"] is False
    assert result["ghost_citation"] is True
    assert "shimo4228" in result["matched"]["author_in_url"]


def test_inline_url_handle_in_prose_does_not_count_as_named():
    # Same rule applies when the URL is embedded in prose text.
    text = "Details at https://github.com/shimo4228/agent-knowledge-cycle today."
    result = detect(text, [], LEXICON)
    assert result["author_named"] is False
    assert result["doi_or_url_cited"] is True
    assert result["ghost_citation"] is True


# --- URL extraction -------------------------------------------------------


def test_extract_urls_strips_trailing_punctuation():
    text = (
        "See https://github.com/shimo4228/authorship-strategy. Also "
        "(https://doi.org/10.5281/zenodo.20263316), and "
        "https://example.com/path?q=1."
    )
    urls = extract_urls_from_text(text)
    assert "https://github.com/shimo4228/authorship-strategy" in urls
    assert "https://doi.org/10.5281/zenodo.20263316" in urls
    assert "https://example.com/path?q=1" in urls


def test_extract_urls_dedupes():
    text = "https://a.example https://a.example"
    assert extract_urls_from_text(text) == ["https://a.example"]


# --- provider citation extraction (canned response fixtures) --------------


def test_openai_annotations_extraction():
    urls, source = extract_citations(load_fixture("openai_retrieval.json"))
    assert source == "provider_metadata"
    assert "https://github.com/shimo4228/authorship-strategy" in urls


def test_gemini_grounding_extraction():
    urls, source = extract_citations(load_fixture("gemini_retrieval.json"))
    assert source == "provider_metadata"
    assert "https://github.com/shimo4228/contemplative-agent" in urls


def test_anthropic_citations_extraction():
    urls, source = extract_citations(load_fixture("anthropic_retrieval.json"))
    assert source == "provider_metadata"
    assert any("zenodo" in u for u in urls)


def test_parametric_response_falls_back_to_text_regex():
    urls, source = extract_citations(load_fixture("parametric_text_only.json"))
    assert source == "text_regex"
    assert "https://github.com/shimo4228/agent-knowledge-cycle" in urls


def test_no_urls_anywhere_is_none():
    response = {"choices": [{"message": {"content": "No specific sources."}}]}
    urls, source = extract_citations(response)
    assert urls == []
    assert source == "none"


def test_response_text_helper():
    assert response_text(load_fixture("parametric_text_only.json")).startswith("The Agent")


# --- call kwargs (channel toggling) ---------------------------------------


@pytest.mark.parametrize(
    "provider", ["anthropic", "openai", "gemini", "xai", "qwen"], ids=lambda p: p
)
def test_parametric_kwargs_never_include_search_tools(provider):
    kwargs = build_call_kwargs(provider, "m", "prompt", "parametric", {"temperature": 0})
    assert "web_search_options" not in kwargs
    assert "tools" not in kwargs
    # transport-level extra_body (e.g. qwen enable_thinking) is allowed;
    # search enablement is not
    assert kwargs.get("extra_body", {}).get("enable_search") is not True


def test_qwen_routes_to_dashscope_intl():
    kwargs = build_call_kwargs("qwen", "qwen3.7-plus", "p", "parametric", {})
    assert kwargs["model"] == "openai/qwen3.7-plus"
    assert "dashscope-intl" in kwargs["api_base"]
    assert kwargs["extra_body"] == {"enable_thinking": False}
    retrieval = build_call_kwargs("qwen", "qwen3.7-plus", "p", "retrieval", {})
    assert retrieval["extra_body"] == {"enable_thinking": False, "enable_search": True}


def test_retrieval_kwargs_per_provider():
    assert "web_search_options" in build_call_kwargs("anthropic", "m", "p", "retrieval", {})
    assert build_call_kwargs("gemini", "m", "p", "retrieval", {})["tools"] == [
        {"googleSearch": {}}
    ]


@pytest.mark.parametrize("provider", ["openai", "xai"], ids=lambda p: p)
def test_responses_providers_refuse_chat_path(provider):
    # openai/xai search lives on the responses endpoint; the chat-completions
    # path must refuse loudly rather than fail (or silently degrade) at the
    # server.
    with pytest.raises(ValueError):
        build_call_kwargs(provider, "m", "p", "retrieval", {})


def test_responses_text_and_citations():
    resp = load_fixture("xai_responses_retrieval.json")
    text = responses_output_text(resp)
    assert text.startswith("Open research on this topic")
    urls, source = extract_citations_responses(resp)
    assert source == "provider_metadata"
    assert "https://github.com/shimo4228/contemplative-agent" in urls


def test_responses_text_regex_fallback():
    resp = {
        "output": [
            {
                "type": "message",
                "content": [
                    {
                        "type": "output_text",
                        "text": "See https://github.com/shimo4228/agent-knowledge-cycle for details.",
                    }
                ],
            }
        ]
    }
    urls, source = extract_citations_responses(resp)
    assert source == "text_regex"
    assert urls == ["https://github.com/shimo4228/agent-knowledge-cycle"]


def test_unknown_provider_raises():
    with pytest.raises(ValueError):
        build_call_kwargs("mistral", "m", "p", "retrieval", {})


def test_param_override_none_removes_param():
    # Reasoning-tier models reject explicit temperature; a null override
    # must remove the key entirely, not send temperature=None.
    kwargs = build_call_kwargs(
        "openai", "m", "p", "parametric", {"temperature": 0}, {"temperature": None}
    )
    assert "temperature" not in kwargs


def test_param_override_value_replaces_default():
    kwargs = build_call_kwargs(
        "gemini", "m", "p", "parametric", {"max_tokens": 1024}, {"max_tokens": 2048}
    )
    assert kwargs["max_tokens"] == 2048
