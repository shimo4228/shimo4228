Language: English | [日本語](README.ja.md)

![Cover art: five colored threads unfurl from a single ink brushstroke and flow into a hand-drawn Zen circle (ensō)](assets/readme-cover.jpg)

# Tatsuya Shimomoto

> Hub for five practice lines (long-running, independently citable projects) on AI agents, authorship, and attention, and the entry point to the tools I ship for Claude Code and for TypeSafe Jev, a decision model that answers typed questions with probabilities instead of text.

I'm Tatsuya Shimomoto (shimo4228). I build AI agents solo, with no lab and no affiliation; one of them runs on a local LLM on an M1 Mac, and one of the five lines is what I noticed about the mind in meditation, written down. If you build agent harnesses, think about accountability for autonomous agents, or care about authorship in the AI age, something here is for you. This repo is a map, not the source of truth: the lines and the tools live in their own repositories, and the hub keeps the stable relationships and citation pointers in one place.

## Start here

| If you came from | Start with |
|---|---|
| **Anthropic's Claude plugin directory** | [harness-scope](https://github.com/shimo4228/harness-scope): one global harness, and each repo picks what Claude sees. [akc-cycle](https://github.com/shimo4228/akc-cycle): the Agent Knowledge Cycle as a single rules file and a plugin. Then [claude-harness](https://github.com/shimo4228/claude-harness), the harness they come from. |
| **A TypeSafe Jev project** | [jev-skill-router](https://github.com/shimo4228/jev-skill-router): a Claude Code hook that asks Jev which installed skill fits the prompt. [jev-research-pipeline](https://github.com/shimo4228/jev-research-pipeline): daily research monitoring where code owns the loop, Jev judges, and Qwen writes. Then the `jev-judgment-design` skill in [claude-harness](https://github.com/shimo4228/claude-harness). |
| **An article, a DOI, or a search for one of the ideas** | The five lines in the table below. |

## At a glance

| Line | What it is |
|---|---|
| [Contemplative Agent](https://github.com/shimo4228/contemplative-agent)<br>[DOI](https://doi.org/10.5281/zenodo.19212118) | A local agent whose value layer is an explicit Constitution, amended from experience under human review. |
| [Agent Knowledge Cycle (AKC)](https://github.com/shimo4228/agent-knowledge-cycle)<br>[DOI](https://doi.org/10.5281/zenodo.19200726) | A six-phase loop that keeps an agent and its operator aligned while both change. |
| [Agent Attribution Practice (AAP)](https://github.com/shimo4228/agent-attribution-practice)<br>[DOI](https://doi.org/10.5281/zenodo.19652013) | Harness-neutral design records: what to prohibit, where controls live, who answers when an agent fails. |
| [Authorship Strategy](https://github.com/shimo4228/authorship-strategy)<br>[DOI](https://doi.org/10.5281/zenodo.20263316) | How an author stays findable when readers meet ideas through LLMs: open the work so the spread carries the origin. |
| [Attention, Not Self](https://github.com/shimo4228/attention-not-self)<br>[DOI](https://doi.org/10.5281/zenodo.20262112) | Essays and a knowledge graph from meditation, in the Abhidharma map of the mind beside computational phenomenology. |

The five lines are siblings, not dependencies: open whichever sits closest to your interest. The DOIs are Zenodo concept DOIs, parent links that always resolve to the latest version.

## Through-line

The three agent-design lines share one claim, [value-layer harness engineering](https://shimo4228.github.io/shimo4228/concepts/value-layer-harness-engineering.html): an agent harness can hold value norms in the same layer as its coding conventions, revised through the same human review. Contemplative Agent asks whether an agent can actually run with such a layer, AKC how the layer stays aligned with the operator as both change, and AAP who answers when it fails. [claude-harness](https://github.com/shimo4228/claude-harness) is the claim running: the public copy of the harness my agents work inside every day. My meditation practice is the source of Contemplative Agent and Attention, Not Self. Authorship Strategy is how the other lines, and itself, get published and cited.

## Elsewhere

- Writing: [Zenn](https://zenn.dev/shimo4228) · [Dev.to](https://dev.to/shimo4228) · [note](https://note.com/shimo4228) · [Substack](https://substack.com/@shimo4228); sources in [zenn-content](https://github.com/shimo4228/zenn-content)
- Data: GitHub traffic for the public repositories the hub tracks, as a [dashboard](https://shimo4228.github.io/shimo4228/traffic/dashboard/) and [raw data](traffic/), CC0; source archived at [Software Heritage](https://archive.softwareheritage.org/browse/origin/?origin_url=https://github.com/shimo4228/shimo4228)
- Machines: [`graph.jsonld`](graph.jsonld), then [`llms.txt`](llms.txt), then [`llms-full.txt`](llms-full.txt); the full ecosystem inventory lives there, and the [concept index](https://shimo4228.github.io/shimo4228/concepts/) defines each coined term. [DeepWiki](https://deepwiki.com/shimo4228/shimo4228) answers questions about this repo in chat
- Identity: [ORCID 0009-0002-6168-4162](https://orcid.org/0009-0002-6168-4162) · [Hugging Face @Shimo4228](https://huggingface.co/Shimo4228) · [`CITATION.cff`](CITATION.cff). The hub is CC0; cite each line by its concept DOI
