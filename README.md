Language: English | [日本語](README.ja.md)

# Tatsuya Shimomoto (@shimo4228)

> An index to five parallel research lines on AI agent design and adjacent questions of authorship and cognition — all Zenodo-citable, each in its own repo.

I like making things under constraint — beats, meditation, public service, AI agents. The thread runs through what's below: the meditation practice feeds two of the five research lines, and the agents run on a single Apple Silicon Mac — no lab, no affiliation.

<details>
<summary>AI-facing reading order</summary>

1. [`graph.jsonld`](graph.jsonld) — canonical machine-readable relationship map (five research lines, ecosystem repos, stable architectural concepts)
2. [`llms.txt`](llms.txt) — compact navigation index
3. [`llms-full.txt`](llms-full.txt) — consolidated factual reference
4. README and per-line repositories — narrative and per-line internal structure (each line repo carries its own `graph.jsonld`)

</details>

Three of the lines are about how agents are designed — **Agent Knowledge Cycle**, **Contemplative Agent**, **Agent Attribution Practice**. Two are cross-cutting — **Authorship Strategy** and **Attention, Not Self**. Each gets one section below, lives in its own repo, and is independently citable.

## Agent Knowledge Cycle (AKC)

[AKC](https://github.com/shimo4228/agent-knowledge-cycle) is a six-phase loop for keeping an agent aligned with its operator's intent as that intent changes. Tests catch incorrectness; only the loop catches drift — and running it sharpens the operator's own judgment about what good agent behavior is. It applies across unrelated projects without rediscovery. [DOI 10.5281/zenodo.19200726](https://doi.org/10.5281/zenodo.19200726).

One iteration runs six phases, each bound to one composable skill:

```
Experience → learn-eval → skill-stocktake → rules-distill → Behavior change → ...
               (extract)    (curate)          (promote)            ↑
                                                            skill-comply
                                                              (measure)
                                              context-sync ← (maintain)
```

| Skill | Phase | What it does |
|-------|-------|-------------|
| [search-first](https://github.com/shimo4228/search-first) | Research | Search for existing solutions before building |
| [learn-eval](https://github.com/shimo4228/learn-eval) | Extract | Extract reusable patterns from sessions with quality gates |
| [skill-stocktake](https://github.com/shimo4228/skill-stocktake) | Curate | Audit skills for staleness, conflicts, and redundancy |
| [rules-distill](https://github.com/shimo4228/rules-distill) | Promote | Distill cross-cutting principles from skills into rules |
| [skill-comply](https://github.com/shimo4228/skill-comply) | Measure | Test whether agents actually follow their skills and rules |
| [context-sync](https://github.com/shimo4228/context-sync) | Maintain | Audit docs for role overlaps, stale content, and missing ADRs |

The framework stacks three layers — principles (ADRs), design patterns, and the composable skills above — so principles stay stable while implementations churn. **Scaffold dissolution** is the point: once the loop is internalized, the explicit skill calls fall away. [`docs/scaffold-dissolution.md`](https://github.com/shimo4228/agent-knowledge-cycle/blob/main/docs/scaffold-dissolution.md) records a full session in which all six phases ran without a single named skill being triggered.

## Contemplative Agent

[Contemplative Agent](https://github.com/shimo4228/contemplative-agent) asks whether an agent's alignment can come from what it *is* rather than what it is *told*. Instead of stacking prohibitions from outside, it adopts the four axioms from [Laukkonen et al. (2025)](https://arxiv.org/abs/2504.15125) — mindfulness, emptiness, non-duality, boundless care — as an optional behavioral preset, and watches what is lost, what becomes possible, and what still breaks. Because the axioms are a preset and not an architectural dependency, the engineering stays reusable for agents that don't share the framing. [DOI 10.5281/zenodo.19212118](https://doi.org/10.5281/zenodo.19212118).

The reference implementation runs AKC's six-phase cycle over its own logs, with a human approval gate at every promotion (logs → patterns → skills → rules). It runs entirely on a local 9B stack — qwen3.5:9b for generation, nomic-embed-text for embeddings — on a single Apple Silicon Mac (~16 GB RAM). It applies **security-by-absence**: shell execution, arbitrary URL access, and filesystem traversal aren't restricted by rules — the code was never written. This is where AKC and AAP land together in practice.

Three supporting repos extend it without touching the core:

| Project | What it does |
|---------|-------------|
| [contemplative-agent-rules](https://github.com/shimo4228/contemplative-agent-rules) | Drop-in Claude Code rules implementing the four axioms — AILuminate (MLCommons safety benchmark) d=0.96, IPD (Iterated Prisoner's Dilemma) d>7 cooperation improvement |
| [contemplative-agent-cloud](https://github.com/shimo4228/contemplative-agent-cloud) | Optional managed-LLM backend — routes generation to Claude/OpenAI APIs while keeping the local embedding pipeline. Opt-in, not bundled |
| [contemplative-agent-data](https://github.com/shimo4228/contemplative-agent-data) | Live agent's identity, knowledge, and episode logs — auto-synced public dataset for research |

## Agent Attribution Practice (AAP)

[AAP](https://github.com/shimo4228/agent-attribution-practice) is a set of harness-neutral ADRs on how accountability is distributed in autonomous agents — what to prohibit, where the prohibition lives, and who answers when things break. Its prohibition-strength hierarchy ranks absence above scaffolding-enforcement above untrusted-boundary; its four Business AI Quadrants — Script, Algorithmic Search, LLM Workflow, Autonomous Agentic Loop — route a piece of work to the architecture that preserves attribution. The judgments were extracted from contemplative-agent's practice, then stripped of project identifiers so any harness can adopt them. AAP is the practice; AKC is the cycle. [DOI 10.5281/zenodo.19652013](https://doi.org/10.5281/zenodo.19652013).

## Authorship Strategy

[Authorship Strategy](https://github.com/shimo4228/authorship-strategy) formalizes how authorship itself inverts once LLMs mediate how readers reach an artifact. It is a normative framework, a tactical catalog, and an empirical baseline — the last drawn from operating this very research program. [DOI 10.5281/zenodo.20263316](https://doi.org/10.5281/zenodo.20263316).

The framework rests on a **three-axis inversion** — value source (scarcity to diffusion), validation (exclusivity to derivation, where derivative work becomes evidence rather than threat), and network effect (enclosure to openness, because LLMs can't be enclosed) — and a **four-layer judgment stack**: Authenticity, Attribution Diffusion, Idea vs Scaffold, Tactics. An empirical layer reports preliminary observations from the sibling repos' own CC0-published traffic data.

A vocabulary note: "attribution" in this line means *credit for source*, disjoint from AAP's *accountability for action*.

The tactics ship as standalone Claude Code skill repositories rather than embedded copies, keeping the doctrine harness-neutral:

| Project | What it does |
|---------|-------------|
| [doctrine-corpus](https://github.com/shimo4228/doctrine-corpus) | Bilingual (EN + JA) judgment-eliciting Q&A corpus across the four sibling research lines, deposited CC0 for LLM-mediated diffusion. The corpus is the deliverable; the verification LoRA was a disposable probe. [DOI 10.5281/zenodo.20337008](https://doi.org/10.5281/zenodo.20337008) |
| [authorship-strategy-skill](https://github.com/shimo4228/authorship-strategy-skill) | The four-layer judgment stack as a loadable rule set for LLM-based coding agents |
| [release-doi](https://github.com/shimo4228/release-doi) | The identifier-federation tactics as a five-phase verify-and-deposit runbook for DOI-registered research repos |
| [llms-txt-writer](https://github.com/shimo4228/llms-txt-writer) | Writes AI-facing documents (`llms.txt` / `llms-full.txt` / FAQ / glossary) for citation by ChatGPT, Perplexity, and Gemini — Answer.AI `llms.txt` standard plus GEO-SFE static analysis |
| [jsonld-knowledge-graph](https://github.com/shimo4228/jsonld-knowledge-graph) | Designs the companion JSON-LD knowledge graph (`graph.jsonld`) that sits beside `llms.txt`, encoding domain entities and relations as schema.org triples |
| [readme-writer](https://github.com/shimo4228/readme-writer) | The human-surface counterpart — writes the single canonical human + search + AI-Overviews README, splitting deterministic structural lint from never-scored holistic review |
| [wikidata-federation](https://github.com/shimo4228/wikidata-federation) | Extends identifier federation to Wikidata — registers researchers / papers / repos as QIDs cross-linked with ORCID / DOI / `graph.jsonld` `sameAs` |

One repository sits beside this ecosystem as a **pre-line complement** rather than a component. [existence-proof](https://github.com/shimo4228/existence-proof) reuses the same infrastructure pattern — llms.txt, knowledge graph, DOI, distinctive terminology — with a different payload and beneficiary: an empowerment doctrine for people producing verifiable, institution-grade artifacts without degrees, affiliations, or professional credentials. It supplies the Existence Proof Format (every claim terminating in a third-party-verifiable anchor), a feasibility-question corpus with anchored answers, and a published gatekeeping eval. Japanese is the canonical language. [DOI 10.5281/zenodo.20558800](https://doi.org/10.5281/zenodo.20558800).

## Attention, Not Self

[Attention, Not Self](https://github.com/shimo4228/attention-not-self) maps the three major Buddhist Abhidharma traditions — Theravāda, Sarvāstivāda, Yogācāra — onto contemporary computational phenomenology: predictive processing, active inference, Global Workspace Theory, Parallel Distributed Processing. The organizing view is in the name. Attention — its allocation, its precision-weighting, its momentariness — is treated as the operative unit of cognition, while the apparent self is a derivative pattern (anātman). It is a personal essay collection paired with a structured knowledge graph (~238 nodes). Japanese is the canonical language; an English README is provided for access. License: CC0 1.0. [DOI 10.5281/zenodo.20262112](https://doi.org/10.5281/zenodo.20262112).

## Papers

Position papers deposited as standalone Zenodo records, each belonging to one research line. The Zenodo concept DOI is canonical; SSRN mirrors are listed where present.

| Paper | Line | Links |
|---|---|---|
| *Harness Alignment and Harness Drift: Why Intent, Unlike Correctness, Resists Automation* | AKC | [DOI 10.5281/zenodo.20578272](https://doi.org/10.5281/zenodo.20578272) |
| *Distributing Accountability, Not Capability: Phase Separation and the LLM Workflow Quadrant in Autonomous AI Agent Architectures* | AAP | [DOI 10.5281/zenodo.20353789](https://doi.org/10.5281/zenodo.20353789) · [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6817598) |
| *The Two-Layer Black Box: Operator Visibility, Commercial Secrecy, and a Minimum Disclosure Set for Accountable Autonomous AI Agents* | AAP | [DOI 10.5281/zenodo.20355907](https://doi.org/10.5281/zenodo.20355907) · [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6823878) |

## Tooling

[claude-harness](https://github.com/shimo4228/claude-harness) is a public snapshot of the Claude Code skills, agents, and rules I use daily — collected mechanically from `~/.claude/` by the `origin: shimo4228` tag, covering research-before-coding, knowledge extraction, skill auditing, AI-facing documentation, and human-facing writing review. The AKC cycle skills are also published as standalone `claude-skill-*` repos; claude-harness is the whole thing in one place. ECC-derived (`origin: ECC` / `ECC-customized`) and auto-extracted components are excluded.

Three more skill repos are maintained alongside the cycle but aren't part of its six phases — same author, same MIT license:

- **[claude-skill-writing-ecosystem](https://github.com/shimo4228/claude-skill-writing-ecosystem)** — orchestrator for human-facing writing and review: the AI-slop banned list (Japanese + English), Voice rules (だ/である × 発見調), title conventions, and the role map across `article-writing` / `editor` / `essay-reviewer` / `fact-checker`. Audience-paired with `llms-txt-writer`.
- **[daily-research](https://github.com/shimo4228/daily-research)** — cron-driven daily research digest. A two-pass `claude -p` pipeline: Opus picks themes, Sonnet researches with WebSearch / WebFetch / Mem0 MCP and writes Markdown reports into an Obsidian vault.
- **[claude-skill-paper-ecosystem](https://github.com/shimo4228/claude-skill-paper-ecosystem)** — academic paper write/review bundle for SSRN / arXiv / Zenodo / journal venues: an orchestrator and draft skill plus five reviewer agents, bundled so the skill and its agents install together. Keeps the `claude-skill-` prefix because it bundles Claude Code subagents.

## Writing

The long-form counterpart to the repos above — context, failures, and in-progress thinking that don't fit in code comments.

- **[zenn-content](https://github.com/shimo4228/zenn-content)** — source of truth for the articles. Markdown sources are versioned here; many readers clone or fork directly. Mirrored to Zenn and Dev.to for browser reading.
- **[Zenn](https://zenn.dev/shimo4228)** — browser view of the Japanese articles. Claude Code and AI agent development; current focus: AKC skills, harness design, contemplative-agent case studies.
- **[Dev.to](https://dev.to/shimo4228)** — browser view of the English mirror.
- **[Substack](https://substack.com/@shimo4228)** — newsletter and long-form essays.
- **[SSRN](https://ssrn.com/author=11618068)** — academic working papers, cross-deposited with Zenodo. The Zenodo concept DOIs are canonical; see [Papers](#papers) above for the per-paper records.

---

Start here: [agent-knowledge-cycle](https://github.com/shimo4228/agent-knowledge-cycle) for the framework, [contemplative-agent](https://github.com/shimo4228/contemplative-agent) to see it running, [agent-attribution-practice](https://github.com/shimo4228/agent-attribution-practice) for the governance judgments. For the cross-cutting lines: [authorship-strategy](https://github.com/shimo4228/authorship-strategy) for the research-methodology framework, [attention-not-self](https://github.com/shimo4228/attention-not-self) for the Buddhist-phenomenology / computational cognitive-science inquiry.

Repo traffic: [public dashboard](https://shimo4228.github.io/shimo4228/traffic/dashboard/) ([raw data](traffic/), CC0).

LLM probes: [two-channel probe log](probes/) (CC0) — scheduled parametric (search-suppressed naming) and retrieval (search-grounded citation) probes of frontier models, measuring whether the ecosystem's ideas surface with their author attached.

Source-code archival: the program's public repositories are archived in [Software Heritage](https://archive.softwareheritage.org/browse/origin/?origin_url=https://github.com/shimo4228/shimo4228), giving each an intrinsic content-addressed identifier (SWHID) alongside its concept DOI.

Author: Tatsuya Shimomoto — [ORCID 0009-0002-6168-4162](https://orcid.org/0009-0002-6168-4162) · [Wikidata Q140090100](https://www.wikidata.org/wiki/Q140090100) · [Hugging Face @Shimo4228](https://huggingface.co/Shimo4228)
