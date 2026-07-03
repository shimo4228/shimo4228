#!/usr/bin/env python3
"""Generate concept-term landing pages (concepts/*.html) + sitemap.xml.

Source of truth: scripts/concepts_data.json (curated term data, adapted from
each line's glossary — definitions must stay faithful to the line glossaries).

Deterministic and idempotent: same input -> byte-identical output, no
timestamps. Re-run after editing concepts_data.json, before committing:

    python3 scripts/build_concept_pages.py

Outputs:
    concepts/<slug>.html   one landing page per coined/distinctive term
    concepts/index.html    DefinedTermSet index of all terms
    sitemap.xml            all indexable Pages URLs (submit via GSC / Bing)

Stdlib only. No CI wiring — run by hand like sync_graph_jsonld_mirror.py.
"""

from __future__ import annotations

import html
import json
from pathlib import Path

BASE = "https://shimo4228.github.io/shimo4228"
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "concepts"

ORCID = "https://orcid.org/0009-0002-6168-4162"
PERSON = {
    "@id": ORCID,
    "@type": "Person",
    "name": "Tatsuya Shimomoto",
    "alternateName": "shimo4228",
    "sameAs": [
        "https://github.com/shimo4228",
        ORCID,
        "https://www.wikidata.org/wiki/Q140090100",
    ],
}

LABEL_TEXT = {
    "coined": "Coined term",
    "coined-name": "Research-line name",
    "distinctive": "Distinctive usage",
    "adopted": "Adopted term",
}

CSS = """
  body { font: 15px/1.65 -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; max-width: 44em; margin: 3em auto; padding: 0 1em; color: #333; }
  h1 { font-size: 1.45em; margin-bottom: .2em; } h2 { font-size: 1.05em; margin-top: 2em; }
  .meta { color: #666; font-size: .9em; margin-top: 0; }
  .sources { background: #f6f8fa; border: 1px solid #e1e4e8; border-radius: 6px; padding: .8em 1.2em; }
  .sources ul { margin: .4em 0; padding-left: 1.2em; } .sources li { margin: .3em 0; }
  ul.terms { padding-left: 1.2em; } ul.terms li { margin: .45em 0; }
  .ja { border-top: 1px solid #ddd; margin-top: 2em; padding-top: .5em; }
  footer { margin-top: 3em; font-size: .85em; color: #666; border-top: 1px solid #ddd; padding-top: 1em; }
  @media (prefers-color-scheme: dark) {
    body { background: #0f1115; color: #e5e7eb; } a { color: #818cf8; }
    .meta, footer { color: #9ca3af; } footer, .ja { border-color: #333; }
    .sources { background: #161a22; border-color: #2d333b; }
  }
"""

FOOTER = (
    '<footer><p><a href="index.html">Concept index</a> · '
    f'<a href="{BASE}/">Research program hub</a> · '
    '<a href="https://github.com/shimo4228">GitHub</a> · '
    f'<a href="{ORCID}">ORCID</a></p>'
    "<p>Part of the shimo4228 research program. Definitions are faithful "
    "adaptations of each line’s canonical glossary; the line repository "
    "is always the source of truth.</p></footer>"
)


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def meta_description(term: dict) -> str:
    text = term["def_en"].strip()
    if len(text) <= 158:
        return text
    cut = text[:158]
    cut = cut[: cut.rfind(" ")]
    return cut.rstrip(",;: ") + "…"


def jsonld_block(data: dict | list) -> str:
    return (
        '<script type="application/ld+json">\n'
        + json.dumps(data, indent=1, ensure_ascii=False)
        + "\n</script>"
    )


def term_jsonld(term: dict) -> dict:
    url = f"{BASE}/concepts/{term['slug']}.html"
    alternate = [a for a in term.get("aliases", [])]
    if term.get("name_ja"):
        alternate.append({"@value": term["name_ja"], "@language": "ja"})
    if term.get("name_zh"):
        alternate.append({"@value": term["name_zh"], "@language": "zh"})
    same_as = [s for s in (term.get("graph_id"), term.get("wikidata")) if s]
    defined_term = {
        "@type": "DefinedTerm",
        "@id": f"{url}#term",
        "name": term["name_en"],
        "description": term["def_en"],
        "inDefinedTermSet": f"{BASE}/concepts/",
        "url": url,
    }
    if term.get("doi"):
        defined_term["subjectOf"] = {"@id": f"https://doi.org/{term['doi']}"}
    if alternate:
        defined_term["alternateName"] = alternate
    if same_as:
        defined_term["sameAs"] = same_as
    faq = {
        "@type": "FAQPage",
        "@id": f"{url}#faq",
        "inLanguage": "en",
        "mainEntity": [
            {
                "@type": "Question",
                "name": q["q_en"],
                "acceptedAnswer": {"@type": "Answer", "text": q["a_en"]},
            }
            for q in term.get("faq", [])
        ],
    }
    page = {
        "@type": "WebPage",
        "@id": url,
        "name": f"{term['name_en']} — {term['gloss']}",
        "inLanguage": ["en", "ja"],
        "mainEntity": {"@id": f"{url}#term"},
        "author": PERSON,
        "isPartOf": {"@id": f"{BASE}/concepts/"},
    }
    graph = [page, defined_term]
    if term.get("faq"):
        graph.append(faq)
    return {"@context": "https://schema.org", "@graph": graph}


def render_term(term: dict, by_slug: dict) -> str:
    url = f"{BASE}/concepts/{term['slug']}.html"
    name = esc(term["name_en"])
    title = f"{name} — {esc(term['gloss'])} | shimo4228 research program"
    desc = esc(meta_description(term))
    label = LABEL_TEXT.get(term["label"], term["label"])
    alias_note = ""
    if term.get("aliases"):
        alias_note = " · also known as " + esc(", ".join(term["aliases"]))
    ja_name = f" ({esc(term['name_ja'])})" if term.get("name_ja") else ""

    related = ""
    rel_terms = [by_slug[s] for s in term.get("related", []) if s in by_slug]
    if rel_terms:
        items = "".join(
            f'<li><a href="{r["slug"]}.html">{esc(r["name_en"])}</a> — {esc(r["gloss"])}</li>'
            for r in rel_terms
        )
        related = f"<h2>Related terms</h2><ul class=\"terms\">{items}</ul>"

    faq_html = ""
    if term.get("faq"):
        blocks = "".join(
            f"<h3>{esc(q['q_en'])}</h3><p>{esc(q['a_en'])}</p>" for q in term["faq"]
        )
        faq_html = f"<h2>FAQ</h2>{blocks}"

    ja_section = ""
    if term.get("def_ja"):
        ja_title = esc(term.get("name_ja") or term["name_en"])
        ja_section = (
            f'<div class="ja" lang="ja"><h2>{ja_title}（日本語）</h2>'
            f"<p>{esc(term['def_ja'])}</p></div>"
        )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light dark">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="article">
<meta property="og:title" content="{name} — {esc(term['gloss'])}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
{jsonld_block(term_jsonld(term))}
<style>{CSS}</style>
</head>
<body>
<h1>{name}{ja_name}</h1>
<p class="meta">{label} · {esc(term['line'])}{alias_note}</p>
<p>{esc(term['def_en'])}</p>
<p>{esc(term['origin_en'])}</p>

<h2>Canonical sources</h2>
<div class="sources"><ul>
<li>Repository: <a href="{esc(term['line_repo'])}">{esc(term['line_repo'].removeprefix('https://'))}</a></li>
{f'<li>Concept DOI: <a href="https://doi.org/{esc(term["doi"])}">{esc(term["doi"])}</a></li>' if term.get('doi') else ''}
<li>Glossary entry: <a href="{esc(term['glossary_url'])}">canonical definition</a></li>
</ul></div>

{faq_html}
{related}
{ja_section}
{FOOTER}
</body>
</html>
"""


def render_index(terms: list) -> str:
    url = f"{BASE}/concepts/"
    by_line: dict[str, list] = {}
    for t in terms:
        by_line.setdefault(t["line"], []).append(t)

    sections = ""
    for line, ts in by_line.items():
        items = "".join(
            f'<li><a href="{t["slug"]}.html">{esc(t["name_en"])}</a> — {esc(t["gloss"])}</li>'
            for t in ts
        )
        sections += f"<h2>{esc(line)}</h2><ul class=\"terms\">{items}</ul>"

    termset = {
        "@context": "https://schema.org",
        "@type": "DefinedTermSet",
        "@id": url,
        "name": "shimo4228 research program — concept index",
        "description": (
            "Index of coined and distinctively used research terms of the "
            "shimo4228 research program, one definition page per term, each "
            "linking back to its canonical repository, glossary entry, and DOI."
        ),
        "creator": PERSON,
        "hasDefinedTerm": [
            {
                "@type": "DefinedTerm",
                "@id": f"{BASE}/concepts/{t['slug']}.html#term",
                "name": t["name_en"],
                "url": f"{BASE}/concepts/{t['slug']}.html",
            }
            for t in terms
        ],
    }

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light dark">
<title>Concept index — coined research terms | shimo4228 research program</title>
<meta name="description" content="One definition page per coined research term of the shimo4228 research program: Agent Knowledge Cycle, three-axis inversion, attribution diffusion, and more.">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:title" content="Concept index — shimo4228 research program">
<meta property="og:description" content="One definition page per coined research term, each linking back to its canonical repository, glossary entry, and DOI.">
<meta property="og:url" content="{url}">
{jsonld_block(termset)}
<style>{CSS}</style>
</head>
<body>
<h1>Concept index</h1>
<p>One page per coined or distinctively used term of the
<a href="{BASE}/">shimo4228 research program</a>. Each page carries the
definition (English and Japanese), origin, and links to the canonical
repository, glossary entry, and concept DOI. The line repositories remain the
source of truth; these pages exist so that a term heard elsewhere can be
traced back to its origin.</p>
{sections}
{FOOTER}
</body>
</html>
"""


def render_sitemap(terms: list) -> str:
    urls = [
        f"{BASE}/",
        f"{BASE}/vocab",
        f"{BASE}/traffic/dashboard/",
        f"{BASE}/concepts/",
    ] + [f"{BASE}/concepts/{t['slug']}.html" for t in terms]
    entries = "\n".join(f"  <url><loc>{u}</loc></url>" for u in urls)
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{entries}\n</urlset>\n"
    )


def main() -> None:
    data = json.loads((ROOT / "scripts" / "concepts_data.json").read_text())
    terms = data["terms"]
    by_slug = {t["slug"]: t for t in terms}
    OUT.mkdir(exist_ok=True)

    for t in terms:
        (OUT / f"{t['slug']}.html").write_text(render_term(t, by_slug))
    (OUT / "index.html").write_text(render_index(terms))
    (ROOT / "sitemap.xml").write_text(render_sitemap(terms))
    print(f"wrote {len(terms)} term pages + index + sitemap.xml")


if __name__ == "__main__":
    main()
