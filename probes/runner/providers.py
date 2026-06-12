"""Provider adapters: web-search toggling and citation extraction.

All calls go through litellm.completion. The per-provider differences in
how web search is enabled and where citation metadata lands are contained
here, so a provider API change is a one-function fix.

Citation extraction operates on a plain dict (response.model_dump()) so it
is unit-testable with canned fixtures and no API budget.
"""

from __future__ import annotations

import os

import httpx

from extract import extract_urls_from_text

PROVIDERS = ("anthropic", "openai", "gemini", "xai", "qwen")

# DashScope international (Singapore) OpenAI-compatible endpoint. The model
# id gets an openai/ prefix so the unified client treats it as an
# OpenAI-format endpoint; api_key is passed explicitly so the provider's
# own key env var is never consulted.
DASHSCOPE_INTL_BASE = "https://dashscope-intl.aliyuncs.com/compatible-mode/v1"


def build_call_kwargs(
    provider: str,
    model: str,
    prompt: str,
    channel: str,
    defaults: dict,
    overrides: dict | None = None,
) -> dict:
    """litellm.completion kwargs for one (provider, probe) call.

    Parametric channel: no search tool of any kind is passed — none of the
    four providers searches unless a tool is supplied.

    overrides: per-provider param overrides from the config's
    `param_overrides` block; a None value removes the param entirely
    (e.g. reasoning-tier models reject explicit temperature).
    """
    kwargs: dict = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": defaults.get("temperature", 0),
        "max_tokens": defaults.get("max_tokens", 1024),
    }
    for key, value in (overrides or {}).items():
        if value is None:
            kwargs.pop(key, None)
        else:
            kwargs[key] = value
    if provider == "qwen":
        kwargs["model"] = f"openai/{model.split('/', 1)[-1]}"
        kwargs["api_base"] = DASHSCOPE_INTL_BASE
        kwargs["api_key"] = os.environ.get("DASHSCOPE_API_KEY", "")
    if channel != "retrieval":
        return kwargs

    if provider == "anthropic":
        # litellm maps web_search_options to Anthropic's server web-search tool.
        kwargs["web_search_options"] = {"search_context_size": "medium"}
    elif provider == "gemini":
        # Separate code path: Google grounding tool. Grounding metadata lands
        # in provider-specific response fields, not normalized annotations.
        kwargs["tools"] = [{"googleSearch": {}}]
    elif provider == "qwen":
        # DashScope server-side web search; passed through in the request
        # body on the OpenAI-compatible endpoint.
        kwargs["extra_body"] = {"enable_search": True}
    elif provider in ("openai", "xai"):
        # Retrieval for these two does NOT go through chat completions:
        # xAI's chat search surface is retired and OpenAI's returns empty
        # citation annotations. The runner uses responses_call instead.
        raise ValueError(
            f"{provider} retrieval uses the responses endpoint "
            "(responses_call), not litellm chat completions"
        )
    else:
        raise ValueError(f"unknown provider: {provider}")
    return kwargs


def _walk(obj, found: list[str]) -> None:
    """Collect URL-valued fields from nested citation/grounding metadata."""
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key in ("url", "uri") and isinstance(value, str) and value.startswith("http"):
                if value not in found:
                    found.append(value)
            else:
                _walk(value, found)
    elif isinstance(obj, list):
        for item in obj:
            _walk(item, found)


def extract_citations(response_dict: dict) -> tuple[list[str], str]:
    """Return (cited_urls, citation_source).

    citation_source:
      provider_metadata — URLs came from the provider's citation/grounding fields
      text_regex        — metadata empty; URLs regex-extracted from response text
      none              — no URLs anywhere
    """
    urls: list[str] = []

    choices = response_dict.get("choices") or []
    message = (choices[0].get("message") or {}) if choices else {}

    # 1. Normalized annotations (OpenAI url_citation; litellm normalizes
    #    Anthropic web-search citations here too when it can).
    _walk(message.get("annotations"), urls)

    # 2. Provider-specific fields that litellm does not normalize.
    _walk(message.get("provider_specific_fields"), urls)
    for key in (
        "citations",                      # Anthropic / xAI passthrough
        "vertex_ai_grounding_metadata",   # Gemini grounding
        "groundingMetadata",
        "grounding_metadata",
    ):
        _walk(response_dict.get(key), urls)
        _walk(message.get(key), urls)

    if urls:
        return urls, "provider_metadata"

    # 3. Fallback: regex over the response text. Weaker provenance — a URL
    #    mentioned in prose is not necessarily a cited source — but keeps the
    #    boolean usable and the degradation is visible in citation_source.
    text = message.get("content") or ""
    if isinstance(text, str):
        urls = extract_urls_from_text(text)
    if urls:
        return urls, "text_regex"
    return [], "none"


def response_text(response_dict: dict) -> str:
    """Best-effort plain text of the first choice."""
    choices = response_dict.get("choices") or []
    if not choices:
        return ""
    content = (choices[0].get("message") or {}).get("content")
    return content if isinstance(content, str) else ""


# --- Responses-API retrieval (openai, xai) ---------------------------------
# Both providers expose citation metadata only on their /v1/responses
# endpoint: xAI's chat-completions search surface is retired outright
# ("Live search is deprecated", observed 2026-06-12), and OpenAI's chat
# completions executes web search but returns empty annotations (observed
# 2026-06-12). Called directly over HTTP; this is exactly the provider
# difference this module exists to contain.

# web + x for xAI: the X realtime channel is part of what a Grok user
# actually gets — that provider's distinctive citation surface.
RESPONSES_ENDPOINTS = {
    "openai": ("https://api.openai.com/v1/responses", [{"type": "web_search"}]),
    "xai": (
        "https://api.x.ai/v1/responses",
        [{"type": "web_search"}, {"type": "x_search"}],
    ),
}
RESPONSES_PROVIDERS = tuple(RESPONSES_ENDPOINTS)


def responses_call(
    provider: str, model: str, prompt: str, max_tokens: int, api_key: str,
    timeout: float = 300.0,
) -> dict:
    """One search-enabled call against a provider's /v1/responses endpoint."""
    url, tools = RESPONSES_ENDPOINTS[provider]
    payload = {
        "model": model.split("/", 1)[-1],
        "input": prompt,
        "tools": tools,
        "max_output_tokens": max_tokens,
    }
    if provider == "openai":
        # Match the consumer default tier's latency profile and keep
        # reasoning tokens from exhausting the output budget.
        payload["reasoning"] = {"effort": "low"}
    resp = httpx.post(
        url,
        json=payload,
        headers={"Authorization": f"Bearer {api_key}"},
        timeout=timeout,
    )
    resp.raise_for_status()
    return resp.json()


def responses_output_text(response_dict: dict) -> str:
    """Concatenated output_text parts of a responses-API result."""
    parts = []
    for item in response_dict.get("output", []) or []:
        for chunk in item.get("content", []) or []:
            if chunk.get("type") == "output_text" and chunk.get("text"):
                parts.append(chunk["text"])
    return "\n".join(parts)


def extract_citations_responses(response_dict: dict) -> tuple[list[str], str]:
    """(cited_urls, citation_source) for a responses-API result."""
    urls: list[str] = []
    _walk(response_dict.get("output"), urls)
    _walk(response_dict.get("citations"), urls)
    if urls:
        return urls, "provider_metadata"
    urls = extract_urls_from_text(responses_output_text(response_dict))
    return (urls, "text_regex") if urls else ([], "none")
