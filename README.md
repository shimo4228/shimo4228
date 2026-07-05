Language: English | [日本語](README.ja.md)

# Tatsuya Shimomoto (@shimo4228)

[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/shimo4228/shimo4228) [![GitMCP](https://img.shields.io/endpoint?url=https://gitmcp.io/badge/shimo4228/shimo4228)](https://gitmcp.io/shimo4228/shimo4228)

> Hub repository for five independently citable research lines by Tatsuya Shimomoto: AI agent design, AI-mediated authorship, and computational phenomenology. The three agent-design lines share one claim — see [Through-line](#through-line).

I'm Tatsuya Shimomoto — I build AI agents solo, on one Apple Silicon Mac, with no lab and no affiliation, working out what good practice looks like in the AI age. The papers and DOIs are tools in that, not a title — how I keep the work citable, durable, and traceable. This repo is a map, not the source of truth for live state — each research line has its own repository and Zenodo concept DOI, and the hub keeps their stable relationships and citation pointers in one place.

## At a Glance

| Line | Role | Stable concept | Canonical record |
|---|---|---|---|
| [Agent Knowledge Cycle](https://github.com/shimo4228/agent-knowledge-cycle) | Agent-design mechanism | A six-phase loop for sustaining agent-operator intent alignment as both behavior and judgment evolve. | [DOI 10.5281/zenodo.19200726](https://doi.org/10.5281/zenodo.19200726) |
| [Contemplative Agent](https://github.com/shimo4228/contemplative-agent) | Agent disposition and implementation | A local agent using four contemplative axioms as an optional behavioral preset, not an architectural dependency. | [DOI 10.5281/zenodo.19212118](https://doi.org/10.5281/zenodo.19212118) |
| [Agent Attribution Practice](https://github.com/shimo4228/agent-attribution-practice) | Accountability practice | Harness-neutral ADRs for deciding what to prohibit, where controls live, and who answers when an agent fails. | [DOI 10.5281/zenodo.19652013](https://doi.org/10.5281/zenodo.19652013) |
| [Authorship Strategy](https://github.com/shimo4228/authorship-strategy) | AI-era authorship methodology | A framework for being a known author when LLMs mediate how readers discover and cite artifacts. | [DOI 10.5281/zenodo.20263316](https://doi.org/10.5281/zenodo.20263316) |
| [Attention, Not Self](https://github.com/shimo4228/attention-not-self) | Cognitive and Buddhist inquiry | A comparison of Abhidharma cognitive-process models with computational phenomenology. | [DOI 10.5281/zenodo.20262112](https://doi.org/10.5281/zenodo.20262112) |

The five lines are siblings, not dependencies — any one can be adopted alone.

## Through-line

One claim runs through the three agent-design lines (AKC, Contemplative Agent, AAP): **[value-layer harness engineering](https://shimo4228.github.io/shimo4228/concepts/value-layer-harness-engineering.html)**. An agent harness normally holds task regulation — coding conventions, security policy, writing style; this program writes value norms (the contemplative axioms, an authorship-strategy judgment stack) into the same layer and governs them with the same human-gated cycle as everything below ([claude-harness](https://github.com/shimo4228/claude-harness) is the public snapshot). The contemplative content of that value layer comes from the author's meditation practice, which also sources two of the five lines; Authorship Strategy is how the whole program is published and cited.

## Papers

Position papers deposited as standalone Zenodo records, each belonging to one line; the concept DOI is canonical, with SSRN mirrors where maintained.

| Paper | Line | Links |
|---|---|---|
| *Harness Alignment and Harness Drift: Why Intent, Unlike Correctness, Resists Automation* | AKC | [DOI 10.5281/zenodo.20578272](https://doi.org/10.5281/zenodo.20578272) · [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6892740) |
| *Distributing Accountability, Not Capability: Phase Separation and the LLM Workflow Quadrant in Autonomous AI Agent Architectures* | AAP | [DOI 10.5281/zenodo.20353789](https://doi.org/10.5281/zenodo.20353789) · [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6817598) |
| *The Two-Layer Black Box: Operator Visibility, Commercial Secrecy, and a Minimum Disclosure Set for Accountable Autonomous AI Agents* | AAP | [DOI 10.5281/zenodo.20355907](https://doi.org/10.5281/zenodo.20355907) · [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6823878) |

## Writing and data

Long-form articles: [Zenn](https://zenn.dev/shimo4228) · [Dev.to](https://dev.to/shimo4228) · [Substack](https://substack.com/@shimo4228) (sources in [zenn-content](https://github.com/shimo4228/zenn-content)). Public GitHub-traffic [dashboard](https://shimo4228.github.io/shimo4228/traffic/dashboard/) and [raw data](traffic/), CC0. Source is archived content-addressed at [Software Heritage](https://archive.softwareheritage.org/browse/origin/?origin_url=https://github.com/shimo4228/shimo4228).

## Machine reading

For machines, start with [`graph.jsonld`](graph.jsonld), then [`llms.txt`](llms.txt), then [`llms-full.txt`](llms-full.txt). The full ecosystem inventory — supporting repositories, datasets, and probe surfaces — lives in those files and the [concept index](https://shimo4228.github.io/shimo4228/concepts/), not in this README.

## Citation and Identity

Author: Tatsuya Shimomoto — [ORCID 0009-0002-6168-4162](https://orcid.org/0009-0002-6168-4162) · [Wikidata Q140090100](https://www.wikidata.org/wiki/Q140090100) · [Hugging Face @Shimo4228](https://huggingface.co/Shimo4228)

This hub is CC0-licensed. Cite individual research lines by their concept DOI; cite the hub itself only when referring to the aggregate index, knowledge graph, traffic snapshots, or probe dataset.
