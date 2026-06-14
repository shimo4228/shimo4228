"""token_cost tests — responses-endpoint pricing via litellm's local map.

litellm bundles its price map, so these run offline (zero API budget).
"""

from probe_runner import token_cost


def test_mapped_openai_model_returns_positive_cost():
    cost = token_cost("openai", "gpt-5.5", 1000, 1000)
    assert isinstance(cost, float) and cost > 0


def test_mapped_xai_model_resolves_via_provider():
    """grok-4.3 is ambiguous without the provider; custom_llm_provider fixes it."""
    cost = token_cost("xai", "grok-4.3", 1000, 1000)
    assert isinstance(cost, float) and cost > 0


def test_zero_tokens_is_zero_cost():
    assert token_cost("openai", "gpt-5.5", 0, 0) == 0.0


def test_none_tokens_treated_as_zero():
    assert token_cost("openai", "gpt-5.5", None, None) == 0.0


def test_unmapped_model_returns_none():
    assert token_cost("openai", "not-a-real-model-xyz", 1000, 1000) is None
