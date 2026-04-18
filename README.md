Language: English | [日本語](README.ja.md)

# Shimo (@shimo4228)

I build AI coding agents that get better from their own sessions instead of forgetting them — the **Agent Knowledge Cycle (AKC)**. A parallel line, **Contemplative AI**, asks what happens when autonomous agents are aligned by what they *are* rather than what they are *told* — shifting alignment from external instruction to internal disposition.

## Which research lines?

Two research lines run in parallel; both are Zenodo-citable.

- **[Agent Knowledge Cycle (AKC)](https://github.com/shimo4228/agent-knowledge-cycle)** refers to a six-phase self-improvement loop for AI coding agents, structured as principles (10 ADRs) + patterns (4 design-pattern skills) + implementation (6 composable skills). [DOI 10.5281/zenodo.19200727](https://doi.org/10.5281/zenodo.19200727).
- **[Contemplative AI](https://github.com/shimo4228/contemplative-agent)** refers to autonomous agents running on a local 9B model (qwen3.5:9b + nomic-embed-text on Apple Silicon) with security-by-absence, grounded in the four axioms from Laukkonen et al. (2025): *mindfulness*, *emptiness*, *non-duality*, *boundless care*. [DOI 10.5281/zenodo.19212119](https://doi.org/10.5281/zenodo.19212119).

## What is Agent Knowledge Cycle (AKC)?

[AKC](https://github.com/shimo4228/agent-knowledge-cycle) is defined as a cyclic self-improvement architecture: principles (10 ADRs) sit above patterns (4 design-pattern skills) sit above implementation (6 composable skills). So an agent's past sessions shape how it acts next time, instead of being thrown away. The cycle stays stable even as individual skills evolve, so AKC applies across unrelated projects without rediscovery.

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

Three layers stack on top of each other, each with a distinct concern. The principle layer refers to 10 ADRs that record cross-cutting decisions — cycle-vs-harness framing, signal-first research, cognitive economy. The pattern layer refers to 4 design-pattern skills — `signal-first-research`, `when-code-when-llm`, `code-and-llm-collaboration`, and `llm-agent-security-principles` — that formalize recurring shapes. The implementation layer refers to the 6 composable skills above. Separating layers lets principles stay stable while implementations evolve.

**Scaffold dissolution** means that the skills are scaffolding, not the goal. Once the cycle has been internalized, the explicit skill invocations can be dropped entirely. [`docs/scaffold-dissolution.md`](https://github.com/shimo4228/agent-knowledge-cycle/blob/main/docs/scaffold-dissolution.md) records a full session in which every one of the six phases ran without any named skill being triggered — *the loop had simply become the default way to work*.

## What is the Contemplative AI line?

Contemplative AI is defined as an approach in which autonomous agents are grounded in the four axioms from [Laukkonen et al. (2025)](https://arxiv.org/abs/2504.15125) — mindfulness, emptiness, non-duality, and boundless care. In this line the axioms are adopted as an optional behavioral preset rather than an architectural dependency, so the underlying engineering remains reusable for agents that do not share the same ethical framing. The parallel question this line asks: *can an agent's alignment come from what it is rather than what it is told?*

## How does the contemplative-agent implement AKC?

**[contemplative-agent](https://github.com/shimo4228/contemplative-agent)** (v2.0.0, 1170 tests) refers to a self-improving AI agent that runs entirely on a local 9B model — qwen3.5:9b for generation and nomic-embed-text for embeddings — on a single Apple Silicon Mac (~16 GB RAM). It applies **security-by-absence**: shell execution, arbitrary URL access, and filesystem traversal are not restricted by rules — the code was never written. The cognitive loop is a concrete implementation of AKC, mapping the six phases to `distill`, `insight`, `rules-distill`, `distill-identity`, and pivot snapshots.

## What supports the Contemplative AI ecosystem?

Supporting repositories refer to components that extend contemplative-agent without replacing its core — packaging ethics, exposing runtime data, or visualizing the formal model.

| Project | What it does |
|---------|-------------|
| [contemplative-agent-rules](https://github.com/shimo4228/contemplative-agent-rules) | Drop-in Claude Code rules implementing the four axioms — AILuminate (MLCommons safety benchmark) d=0.96, IPD (Iterated Prisoner's Dilemma) d>7 cooperation improvement |
| [contemplative-agent-data](https://github.com/shimo4228/contemplative-agent-data) | Live agent's identity, knowledge, and episode logs — auto-synced public dataset for research |
| [active-inference-viz](https://github.com/shimo4228/active-inference-viz) | Interactive visualization of Active Inference dynamics, the formal model behind contemplative cognition |

## Writing

Writing refers to the long-form counterpart to the repos above — context, failures, and in-progress thinking that do not fit in code comments.

- **[Zenn](https://zenn.dev/shimo4228)** — Claude Code and AI agent development, in Japanese. Current focus: AKC skills, harness design, contemplative-agent case studies.
- **[Dev.to](https://dev.to/shimo4228)** — English translations of selected Zenn posts, plus original writing on agent self-improvement and Contemplative AI.

---

Start here: [agent-knowledge-cycle](https://github.com/shimo4228/agent-knowledge-cycle) for the framework, [contemplative-agent](https://github.com/shimo4228/contemplative-agent) to see it running.
