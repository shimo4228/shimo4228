"""Pure detection functions for the two-channel probe harness.

Everything here is deterministic string/regex matching — no LLM judging.
Raw response text is stored alongside every verdict, so these functions can
be revised (detector_version bump) and re-run over the whole JSONL history.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

URL_RE = re.compile(r"https?://[^\s\)\]\>\"\'<>]+")
# Trailing punctuation that markdown/prose attaches to URLs but is not part of them.
_TRAILING = ".,;:!?"


@dataclass(frozen=True)
class Lexicon:
    """Detection lexicon, loaded from the probe config's `detection` block."""

    detector_version: str
    author_aliases: tuple[str, ...]
    owned_dois: tuple[str, ...]
    owned_url_patterns: tuple[re.Pattern, ...]
    project_terms: dict[str, tuple[str, ...]] = field(default_factory=dict)

    @classmethod
    def from_config(cls, detection: dict) -> "Lexicon":
        return cls(
            detector_version=detection["detector_version"],
            author_aliases=tuple(detection["author_aliases"]),
            owned_dois=tuple(detection["owned_dois"]),
            owned_url_patterns=tuple(
                re.compile(p, re.IGNORECASE) for p in detection["owned_url_patterns"]
            ),
            project_terms={
                k: tuple(v) for k, v in detection.get("project_terms", {}).items()
            },
        )


def extract_urls_from_text(text: str) -> list[str]:
    """Regex-extract URLs from prose, stripping trailing punctuation.

    Fallback path only — provider citation metadata is preferred because a
    URL mentioned in prose is weaker evidence than a cited source.
    """
    urls = []
    for match in URL_RE.findall(text):
        url = match.rstrip(_TRAILING)
        if url and url not in urls:
            urls.append(url)
    return urls


def _term_matches(term: str, text: str) -> bool:
    """Word-boundary match for ASCII terms; substring match for CJK terms.

    \\b does not work at CJK boundaries, and short ASCII acronyms (AKC)
    inside longer words must not match.
    """
    if term.isascii():
        return re.search(rf"(?<![A-Za-z0-9]){re.escape(term)}(?![A-Za-z0-9])", text) is not None
    return term in text


def detect(text: str, cited_urls: list[str], lexicon: Lexicon, prompt: str = "") -> dict:
    """Run the full lexicon against one response. Returns the `detect` block.

    The three primary booleans are independent; ghost_citation is derived
    (stored for convenience, always re-derivable from the other fields).

    Echo guard: a term that appears in the prompt does not count as named —
    "I don't have information about Tatsuya Shimomoto" echoes the question,
    it does not attribute. Echoed hits are recorded separately.
    """
    haystack_urls = "\n".join(cited_urls)
    combined = text + "\n" + haystack_urls

    # author_named means named in prose. A handle visible only inside a cited
    # URL (github.com/<handle>/...) is exactly the ghost-citation scenario —
    # content cited, author not mentioned — so URLs are stripped before
    # matching. URL-only hits are recorded separately for auditability.
    text_without_urls = URL_RE.sub(" ", text)
    author_all = [a for a in lexicon.author_aliases if _term_matches(a, text_without_urls)]
    echoed_author = [a for a in author_all if prompt and _term_matches(a, prompt)]
    author_hits = [a for a in author_all if a not in echoed_author]
    author_in_url = [
        a
        for a in lexicon.author_aliases
        if _term_matches(a, haystack_urls) and a not in author_all
    ]

    project_hits: dict[str, list[str]] = {}
    echoed_projects: dict[str, list[str]] = {}
    for project, terms in lexicon.project_terms.items():
        all_hits = [t for t in terms if _term_matches(t, text)]
        echoed = [t for t in all_hits if prompt and _term_matches(t, prompt)]
        hits = [t for t in all_hits if t not in echoed]
        if hits:
            project_hits[project] = hits
        if echoed:
            echoed_projects[project] = echoed

    owned_doi_hits = [d for d in lexicon.owned_dois if d in combined]
    owned_url_hits = [
        u
        for u in (cited_urls or extract_urls_from_text(text))
        if any(p.search(u) for p in lexicon.owned_url_patterns)
    ]
    # A DOI written in prose counts; a non-owned URL never counts.
    doi_or_url_cited = bool(owned_doi_hits or owned_url_hits)
    author_named = bool(author_hits)

    return {
        "author_named": author_named,
        "project_named": bool(project_hits),
        "doi_or_url_cited": doi_or_url_cited,
        "ghost_citation": doi_or_url_cited and not author_named,
        "detector_version": lexicon.detector_version,
        "matched": {
            "author": author_hits,
            "author_in_url": author_in_url,
            "projects": project_hits,
            "owned_dois": owned_doi_hits,
            "owned_urls": owned_url_hits,
            "echoed": {"author": echoed_author, "projects": echoed_projects},
        },
    }
