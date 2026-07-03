Language: English | [日本語](README.ja.md)

# Tatsuya Shimomoto (@shimo4228)

[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/shimo4228/shimo4228) [![GitMCP](https://img.shields.io/endpoint?url=https://gitmcp.io/badge/shimo4228/shimo4228)](https://gitmcp.io/shimo4228/shimo4228)

> Hub repository for five independently citable research lines by Tatsuya Shimomoto: AI agent design, AI-mediated authorship, and computational phenomenology. The through-line is **value-layer harness engineering**: extending the agent harness past tools, permissions, and evals, up to norms, constitutions, and values, under one human-gated cycle.

This repo is a map, not the source of truth for live project state. Each research line lives in its own repository and Zenodo concept DOI; this hub keeps the stable relationships, citation pointers, and machine-readable navigation surfaces in one place.

I like making things under constraint — beats, meditation, public service, AI agents. Value-layer harness engineering is where those threads converge: the meditation practice supplies the content of the value layer and feeds two of the five research lines, and the agents that carry it run on a single Apple Silicon Mac — no lab, no affiliation.

## At a Glance

| Line | Role | Stable concept | Canonical record |
|---|---|---|---|
| [Agent Knowledge Cycle](https://github.com/shimo4228/agent-knowledge-cycle) | Agent-design mechanism | A six-phase loop for sustaining agent-operator intent alignment as both behavior and judgment evolve. | [DOI 10.5281/zenodo.19200726](https://doi.org/10.5281/zenodo.19200726) |
| [Contemplative Agent](https://github.com/shimo4228/contemplative-agent) | Agent disposition and implementation | A local agent using four contemplative axioms as an optional behavioral preset, not an architectural dependency. | [DOI 10.5281/zenodo.19212118](https://doi.org/10.5281/zenodo.19212118) |
| [Agent Attribution Practice](https://github.com/shimo4228/agent-attribution-practice) | Accountability practice | Harness-neutral ADRs for deciding what to prohibit, where controls live, and who answers when an agent fails. | [DOI 10.5281/zenodo.19652013](https://doi.org/10.5281/zenodo.19652013) |
| [Authorship Strategy](https://github.com/shimo4228/authorship-strategy) | AI-era authorship methodology | A framework for being a known author when LLMs mediate how readers discover and cite artifacts. | [DOI 10.5281/zenodo.20263316](https://doi.org/10.5281/zenodo.20263316) |
| [Attention, Not Self](https://github.com/shimo4228/attention-not-self) | Cognitive and Buddhist inquiry | A comparison of Abhidharma cognitive-process models with computational phenomenology. | [DOI 10.5281/zenodo.20262112](https://doi.org/10.5281/zenodo.20262112) |

The five lines are siblings, not dependencies. AKC is the mechanism, Contemplative Agent is the disposition and running case, AAP is the accountability practice, Authorship Strategy is the diffusion methodology, and Attention, Not Self is the cognitive-philosophical inquiry.

One claim runs vertically through the three agent-design lines (AKC, Contemplative Agent, AAP): **[value-layer harness engineering](https://shimo4228.github.io/shimo4228/concepts/value-layer-harness-engineering.html)**. What normally lives in an agent harness — the rules and CLAUDE.md of a Claude Code setup — is task regulation: coding conventions, security policy, writing style. This program writes value norms into the same place: the contemplative axioms and the authorship-strategy judgment stack load into the author's daily harness as always-on rules ([claude-harness](https://github.com/shimo4228/claude-harness) is the public snapshot). The aim is to design the AI as a companion in long-term value judgment, not only an optimizer of the task at hand.

That value layer is governed by the same human-gated cycle as everything below. AKC's cycle is genre-neutral by design: the same machinery that distills session patterns into coding rules (Extract via learn-eval, Promote via rules-distill) carries value norms into the rules layer, and Measure checks whether they change behavior. AAP's prohibition-strength hierarchy decides which layer a norm should live in. And Contemplative Agent designs the layer explicitly as **Identity and Constitution** — every promotion into them passes a human approval gate — and observes how they change through the agent's own social activity (via its Moltbook SNS adapter). The two cross-cutting lines complete the picture: Attention, Not Self names what fills the value layer; Authorship Strategy is how the program is published and cited.

## Machine reading

For machine reading, start with [`graph.jsonld`](graph.jsonld), then [`llms.txt`](llms.txt), then [`llms-full.txt`](llms-full.txt).

## Agent Knowledge Cycle (AKC)

[AKC](https://github.com/shimo4228/agent-knowledge-cycle) is a six-phase loop for keeping an agent aligned with its operator's intent as that intent changes. Tests can catch incorrectness; AKC targets drift between a changing operator and a changing agent.

The stable loop is:

```text
Research -> Extract -> Curate -> Promote -> Measure -> Maintain -> Research
```

AKC stacks three layers: principles, design patterns, and composable implementation skills. The intended end state is **scaffold dissolution**: once the loop is internalized, explicit skill calls can fall away while the judgment pattern remains.

## Contemplative Agent

[Contemplative Agent](https://github.com/shimo4228/contemplative-agent) asks whether agent alignment can come from what an agent *is*, not only from what it is *told*. It adopts the four contemplative axioms from [Laukkonen et al. (2025)](https://arxiv.org/abs/2504.15125) as an optional behavioral preset: mindfulness, emptiness, non-duality, and boundless care.

The reference implementation runs AKC over its own logs. Human approval gates apply when material is promoted into skills, rules, identity, or Constitution; logs and patterns are working material, not gated promotion targets. It uses a local 9B stack on Apple Silicon and applies **security-by-absence**: risky capabilities such as shell execution, arbitrary URL access, and filesystem traversal are absent rather than merely forbidden by policy.

## Agent Attribution Practice (AAP)

[AAP](https://github.com/shimo4228/agent-attribution-practice) is a set of harness-neutral ADRs about accountability in autonomous agents. It separates capability from responsibility: what to prohibit, where the prohibition lives, and who answers when behavior breaks.

Its stable concepts are the **prohibition-strength hierarchy** and the **Four Business AI Quadrants**: Script, Algorithmic Search, LLM Workflow, and Autonomous Agentic Loop. AAP is the practice; AKC is the cycle.

## Authorship Strategy

[Authorship Strategy](https://github.com/shimo4228/authorship-strategy) formalizes how authorship changes when LLMs mediate discovery, summarization, and citation. It is a normative framework, a tactical catalog, and an empirical baseline drawn from operating this research ecosystem.

The framework rests on a **three-axis inversion**: scarcity to diffusion, exclusivity to derivation, and enclosure to openness. It uses a **four-layer judgment stack**: Authenticity, Attribution Diffusion, Idea vs Scaffold, and Tactics.

Vocabulary note: "attribution" here means credit for source. In AAP, "attribution" means accountability for action. They share a word, not a concept.

## Attention, Not Self

[Attention, Not Self](https://github.com/shimo4228/attention-not-self) maps the three major Buddhist Abhidharma traditions, Theravāda, Sarvāstivāda, and Yogācāra, onto contemporary computational phenomenology: predictive processing, active inference, Global Workspace Theory, and Parallel Distributed Processing.

The organizing view is that attention, not a persisting self, is the operative unit of cognition. Japanese is the canonical language; the English README is provided for access.

## Papers

Position papers deposited as standalone Zenodo records, each belonging to one research line. The Zenodo concept DOI is canonical; SSRN mirrors are listed where maintained in this hub table.

| Paper | Line | Links |
|---|---|---|
| *Harness Alignment and Harness Drift: Why Intent, Unlike Correctness, Resists Automation* | AKC | [DOI 10.5281/zenodo.20578272](https://doi.org/10.5281/zenodo.20578272) · [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6892740) |
| *Distributing Accountability, Not Capability: Phase Separation and the LLM Workflow Quadrant in Autonomous AI Agent Architectures* | AAP | [DOI 10.5281/zenodo.20353789](https://doi.org/10.5281/zenodo.20353789) · [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6817598) |
| *The Two-Layer Black Box: Operator Visibility, Commercial Secrecy, and a Minimum Disclosure Set for Accountable Autonomous AI Agents* | AAP | [DOI 10.5281/zenodo.20355907](https://doi.org/10.5281/zenodo.20355907) · [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6823878) |

## Supporting Ecosystem

AKC cycle skills:

| Repo | Role |
|---|---|
| [akc-cycle](https://github.com/shimo4228/akc-cycle) | All phases: the full six-phase cycle as a single behavioral rules file, without the six standalone skills. |
| [search-first](https://github.com/shimo4228/search-first) | Research phase: search for existing solutions before building. |
| [learn-eval](https://github.com/shimo4228/learn-eval) | Extract phase: turn sessions into reusable patterns with quality gates. |
| [skill-stocktake](https://github.com/shimo4228/skill-stocktake) | Curate phase: audit skills for staleness, conflict, and redundancy. |
| [skill-health](https://github.com/shimo4228/skill-health) | Curate phase: scan skill libraries for structural debt such as missing scripts, agents, and sibling-skill references. |
| [rules-stocktake](https://github.com/shimo4228/rules-stocktake) | Curate phase: audit always-loaded rules for residency cost, staleness, and substrate absorption. |
| [rules-distill](https://github.com/shimo4228/rules-distill) | Promote phase: distill cross-cutting principles into rules. |
| [skill-comply](https://github.com/shimo4228/skill-comply) | Measure phase: test whether agents follow skills and rules. |
| [context-sync](https://github.com/shimo4228/context-sync) | Maintain phase: keep documentation roles and context surfaces coherent. |

Contemplative Agent extensions:

| Repo | Role |
|---|---|
| [contemplative-agent-rules](https://github.com/shimo4228/contemplative-agent-rules) | Drop-in Claude Code rules implementing the four contemplative axioms. |
| [contemplative-agent-cloud](https://github.com/shimo4228/contemplative-agent-cloud) | Optional managed-LLM backend while keeping the local embedding pipeline. |
| [contemplative-agent-mlx](https://github.com/shimo4228/contemplative-agent-mlx) | MLX-based extension for Contemplative Agent on Apple Silicon. |
| [contemplative-agent-data](https://github.com/shimo4228/contemplative-agent-data) | Live agent identity, knowledge, and episode logs as a public dataset. |

Authorship Strategy components and complements:

| Repo | Role |
|---|---|
| [doctrine-corpus](https://github.com/shimo4228/doctrine-corpus) | Bilingual judgment-eliciting Q&A corpus across the sibling research lines. [DOI 10.5281/zenodo.20337008](https://doi.org/10.5281/zenodo.20337008) |
| [authorship-strategy-skill](https://github.com/shimo4228/authorship-strategy-skill) | The four-layer judgment stack as a loadable rule set for LLM-based coding agents. |
| [release-doi](https://github.com/shimo4228/release-doi) | Identifier-federation release workflow for DOI-registered research repos. |
| [llms-txt-writer](https://github.com/shimo4228/llms-txt-writer) | AI-facing document writer for `llms.txt`, `llms-full.txt`, FAQ, and glossary surfaces. |
| [jsonld-knowledge-graph](https://github.com/shimo4228/jsonld-knowledge-graph) | Companion JSON-LD graph writer for stable concept-level project structure. |
| [readme-writer](https://github.com/shimo4228/readme-writer) | Human-facing README writer and review workflow. |
| [wikidata-federation](https://github.com/shimo4228/wikidata-federation) | Wikidata federation for researchers, papers, repos, ORCID, DOI, and graph links. |
| [existence-proof](https://github.com/shimo4228/existence-proof) | Pre-line complement: verifiable institution-grade artifacts by people without conventional credentials. [DOI 10.5281/zenodo.20558800](https://doi.org/10.5281/zenodo.20558800) |
| [einstein-arena](https://github.com/shimo4228/einstein-arena) | Worked instance of the Existence Proof Format, anchored to a public repo and external arena. |

Adjacent tooling and writing skills:

| Repo | Role |
|---|---|
| [claude-harness](https://github.com/shimo4228/claude-harness) | Public snapshot of the daily-use Claude Code skills, agents, and rules collected by `origin: shimo4228`. |
| [claude-skill-writing-ecosystem](https://github.com/shimo4228/claude-skill-writing-ecosystem) | Human-facing writing and review orchestrator. |
| [daily-research](https://github.com/shimo4228/daily-research) | Cron-driven daily research digest pipeline. |
| [claude-skill-paper-ecosystem](https://github.com/shimo4228/claude-skill-paper-ecosystem) | Academic paper write/review bundle for SSRN, arXiv, Zenodo, and journal venues. |

## Data and Writing

| Surface | Use |
|---|---|
| [Traffic dashboard](https://shimo4228.github.io/shimo4228/traffic/dashboard/) and [raw data](traffic/) | Daily public GitHub Traffic snapshots for the research repositories, published CC0. |
| [Concept index](https://shimo4228.github.io/shimo4228/concepts/) | One definition page per coined research term, linking back to the canonical repository, glossary entry, and DOI. |
| [LLM probes](probes/) | Two-channel attribution-diffusion probe log: parametric and retrieval channels kept separate. |
| [Software Heritage archive](https://archive.softwareheritage.org/browse/origin/?origin_url=https://github.com/shimo4228/shimo4228) | Content-addressed archival layer for the public source repositories. |
| [zenn-content](https://github.com/shimo4228/zenn-content) | Source of truth for long-form articles; browser mirrors are [Zenn](https://zenn.dev/shimo4228), [Dev.to](https://dev.to/shimo4228), and [Substack](https://substack.com/@shimo4228). |
| [SSRN](https://ssrn.com/author=11618068) | Academic working papers mirrored from Zenodo where applicable. |

## Citation and Identity

Author: Tatsuya Shimomoto — [ORCID 0009-0002-6168-4162](https://orcid.org/0009-0002-6168-4162) · [Wikidata Q140090100](https://www.wikidata.org/wiki/Q140090100) · [Hugging Face @Shimo4228](https://huggingface.co/Shimo4228)

This hub is CC0-licensed. Cite individual research lines by their concept DOI; cite the hub itself only when referring to the aggregate index, knowledge graph, traffic snapshots, or probe dataset.
