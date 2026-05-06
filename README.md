Language: English | [日本語](README.ja.md)

# Shimo (@shimo4228)

I build AI coding agents that get better from their own sessions instead of forgetting them — the **Agent Knowledge Cycle (AKC)**. A parallel line, **Contemplative Agent**, asks what happens when autonomous agents are aligned by what they *are* rather than what they are *told* — shifting alignment from external instruction to internal disposition. A third line, **Agent Attribution Practice (AAP)**, formalizes how accountability is distributed in autonomous AI agents — harness-neutral judgments on what to prohibit, where to place the gate, and who answers when things break.

## Which research lines?

Three research lines run in parallel; all are Zenodo-citable.

- **[Agent Knowledge Cycle (AKC)](https://github.com/shimo4228/agent-knowledge-cycle)** refers to a six-phase self-improvement loop for AI coding agents, structured as three stacked layers: principles, design patterns, and composable skills. [DOI 10.5281/zenodo.19200726](https://doi.org/10.5281/zenodo.19200726).
- **[Contemplative Agent](https://github.com/shimo4228/contemplative-agent)** refers to autonomous agents running on a local 9B model (qwen3.5:9b + nomic-embed-text on Apple Silicon) with security-by-absence, grounded in the four axioms from Laukkonen et al. (2025): *mindfulness*, *emptiness*, *non-duality*, *boundless care*. [DOI 10.5281/zenodo.19212118](https://doi.org/10.5281/zenodo.19212118).
- **[Agent Attribution Practice (AAP)](https://github.com/shimo4228/agent-attribution-practice)** refers to harness-neutral ADRs on accountability distribution in autonomous AI agents — what to prohibit, where the prohibition lives, and who answers after failure. A prohibition-strength hierarchy (absence > scaffolding enforcement > untrusted boundary) is paired with four Business AI Quadrants as the diagnostic frame for adoption. [DOI 10.5281/zenodo.19652013](https://doi.org/10.5281/zenodo.19652013).

## What is Agent Knowledge Cycle (AKC)?

[AKC](https://github.com/shimo4228/agent-knowledge-cycle) is defined as a cyclic self-improvement architecture: principles sit above design patterns sit above composable-skill implementations. So an agent's past sessions shape how it acts next time, instead of being thrown away. The cycle stays stable even as individual skills evolve, so AKC applies across unrelated projects without rediscovery.

## How does the AKC cycle work?

One iteration runs six phases — Research, Extract, Curate, Promote, Measure, Maintain — each bound to one composable skill. Skills pass artifacts forward; each artifact is evaluated before promotion.

```
Experience → learn-eval → skill-stocktake → rules-distill → Behavior change → ...
               (extract)    (curate)          (promote)            ↑
                                                            skill-comply
                                                              (measure)
                                              context-sync ← (maintain)
```

| Skill | Phase | What it does |
|-------|-------|-------------|
| [search-first](https://github.com/shimo4228/claude-skill-search-first) | Research | Search for existing solutions before building |
| [learn-eval](https://github.com/shimo4228/claude-skill-learn-eval) | Extract | Extract reusable patterns from sessions with quality gates |
| [skill-stocktake](https://github.com/shimo4228/claude-skill-stocktake) | Curate | Audit skills for staleness, conflicts, and redundancy |
| [rules-distill](https://github.com/shimo4228/claude-skill-rules-distill) | Promote | Distill cross-cutting principles from skills into rules |
| [skill-comply](https://github.com/shimo4228/claude-skill-comply) | Measure | Test whether agents actually follow their skills and rules |
| [context-sync](https://github.com/shimo4228/claude-skill-context-sync) | Maintain | Audit docs for role overlaps, stale content, and missing ADRs |

## How is the AKC framework structured?

Three layers stack on top of each other, each with a distinct concern. The principle layer refers to ADRs that record cross-cutting decisions — cycle-vs-harness framing, signal-first research, cognitive economy. The pattern layer refers to design-pattern skills that formalize recurring shapes (intake-filter design, when to use code vs LLM, how to layer them). The implementation layer refers to the composable skills above. Separating layers lets principles stay stable while implementations evolve. See the [AKC repo](https://github.com/shimo4228/agent-knowledge-cycle) for the current set in each layer.

**Scaffold dissolution** means that the skills are scaffolding, not the goal. Once the cycle has been internalized, the explicit skill invocations can be dropped entirely. [`docs/scaffold-dissolution.md`](https://github.com/shimo4228/agent-knowledge-cycle/blob/main/docs/scaffold-dissolution.md) records a full session in which every one of the six phases ran without any named skill being triggered — *the loop had simply become the default way to work*.

## What is the Contemplative Agent line?

Contemplative Agent is defined as an approach in which autonomous agents are grounded in the four axioms from [Laukkonen et al. (2025)](https://arxiv.org/abs/2504.15125) — mindfulness, emptiness, non-duality, and boundless care. In this line the axioms are adopted as an optional behavioral preset rather than an architectural dependency, so the underlying engineering remains reusable for agents that do not share the same ethical framing. The parallel question this line asks: *can an agent's alignment come from what it is rather than what it is told?*

## How does the contemplative-agent implement AKC?

**[contemplative-agent](https://github.com/shimo4228/contemplative-agent)** refers to a self-improving AI agent that runs entirely on a local 9B model — qwen3.5:9b for generation and nomic-embed-text for embeddings — on a single Apple Silicon Mac (~16 GB RAM). It applies **security-by-absence**: shell execution, arbitrary URL access, and filesystem traversal are not restricted by rules — the code was never written. The cognitive loop is a concrete implementation of AKC; see the contemplative-agent repo for the current six-phase mapping.

## What supports the Contemplative Agent ecosystem?

Supporting repositories refer to components that extend contemplative-agent without replacing its core — packaging ethics, exposing runtime data, or visualizing the formal model.

| Project | What it does |
|---------|-------------|
| [contemplative-agent-rules](https://github.com/shimo4228/contemplative-agent-rules) | Drop-in Claude Code rules implementing the four axioms — AILuminate (MLCommons safety benchmark) d=0.96, IPD (Iterated Prisoner's Dilemma) d>7 cooperation improvement |
| [contemplative-agent-cloud](https://github.com/shimo4228/contemplative-agent-cloud) | Optional managed-LLM backend — routes generation to Claude/OpenAI APIs while keeping the local embedding pipeline. Opt-in, not bundled |
| [contemplative-agent-data](https://github.com/shimo4228/contemplative-agent-data) | Live agent's identity, knowledge, and episode logs — auto-synced public dataset for research |

## What is the Agent Attribution Practice (AAP) line?

[AAP](https://github.com/shimo4228/agent-attribution-practice) refers to harness-neutral ADRs on accountability distribution in autonomous AI agents — what to prohibit, where the prohibition lives, and who answers after failure. A prohibition-strength hierarchy (absence > scaffolding enforcement > untrusted boundary) anchors the architecture, paired with four Business AI Quadrants — Script, Algorithmic Search, LLM Workflow, and Autonomous Agentic Loop — as the diagnostic frame for routing a piece of work to the architecture that preserves attribution. The judgments were extracted from contemplative-agent's operational practice, then re-expressed stripped of project identifiers so they can be adopted by any agent harness. AAP is the practice (content); AKC is the cycle (mechanism). [DOI 10.5281/zenodo.19652013](https://doi.org/10.5281/zenodo.19652013).

## What does shimo4228 release as open Claude Code tooling?

[claude-harness](https://github.com/shimo4228/claude-harness) refers to a public artifact of shimo4228's daily-use Claude Code skills, agents, and rules — 10 skills + 5 agents + 5 rules, mechanically collected from `~/.claude/` by the `origin: shimo4228` tag. The six AKC skills are also published as standalone `claude-skill-*` repositories, but claude-harness lets you read or fork the entire harness in one place. ECC-derived components (`origin: ECC` / `ECC-customized`) and auto-extracted artifacts are excluded.

## Writing

Writing refers to the long-form counterpart to the repos above — context, failures, and in-progress thinking that do not fit in code comments.

- **[zenn-content](https://github.com/shimo4228/zenn-content)** — Source of truth for the articles. Markdown sources are versioned here; many readers clone or fork directly. Mirrored to Zenn and Dev.to (below) for browser reading.
- **[Zenn](https://zenn.dev/shimo4228)** — Browser view of the Japanese articles. Claude Code and AI agent development; current focus: AKC skills, harness design, contemplative-agent case studies.
- **[Dev.to](https://dev.to/shimo4228)** — Browser view of the English mirror.

---

Start here: [agent-knowledge-cycle](https://github.com/shimo4228/agent-knowledge-cycle) for the framework, [contemplative-agent](https://github.com/shimo4228/contemplative-agent) to see it running, [agent-attribution-practice](https://github.com/shimo4228/agent-attribution-practice) for the governance judgments.

Repo traffic: [public dashboard](https://shimo4228.github.io/shimo4228/traffic/dashboard/) ([raw data](traffic/), CC0).
