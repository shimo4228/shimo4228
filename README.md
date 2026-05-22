Language: English | [日本語](README.ja.md)

# Shimo (@shimo4228)
<details>
<summary>AI-facing reading order</summary>

1. [`graph.jsonld`](graph.jsonld) — canonical machine-readable relationship map (five research lines, ecosystem repos, stable architectural concepts)
2. [`llms.txt`](llms.txt) — compact navigation index
3. [`llms-full.txt`](llms-full.txt) — consolidated factual reference
4. README and per-line repositories — narrative and per-line internal structure (each line repo carries its own `graph.jsonld`)

</details>

I build AI agents that stay aligned with the operator's evolving intent over time — the **Agent Knowledge Cycle (AKC)** is a bidirectional growth loop in which agent behavior and human judgment co-develop. A parallel line, **Contemplative Agent**, asks what happens when autonomous agents are aligned by what they *are* rather than what they are *told* — replacing externally-stacked prohibitions with a four-axiom **default behavioral preset**, and watching what is lost, what becomes possible, and what still breaks. A third line, **Agent Attribution Practice (AAP)**, formalizes how accountability is distributed in autonomous AI agents — harness-neutral judgments on what to prohibit, where to place the gate, and who answers when things break.

Alongside these three agent-design lines, two cross-cutting research lines record adjacent concerns. **Authorship Strategy** formalizes how authorship itself inverts under LLM-mediated diffusion — a normative framework, tactical catalog, and empirical baseline drawn from operating this very research program. **Attention, Not Self** maps the three major Buddhist Abhidharma traditions (Theravāda, Sarvāstivāda, Yogācāra) onto contemporary frameworks in computational phenomenology — predictive processing, active inference, Global Workspace Theory — from the perspective that attention, not the apparent self, is the operative unit of cognition.

## Which research lines?

Five research lines run in parallel; all are Zenodo-citable.

- **[Agent Knowledge Cycle (AKC)](https://github.com/shimo4228/agent-knowledge-cycle)** refers to a six-phase bidirectional growth loop for sustaining intent alignment between an AI agent and its operator over time — agent behavior and human judgment co-develop. Structured as three stacked layers: principles, design patterns, and composable skills. [DOI 10.5281/zenodo.19200726](https://doi.org/10.5281/zenodo.19200726).
- **[Contemplative Agent](https://github.com/shimo4228/contemplative-agent)** refers to autonomous agents running on a local 9B model (qwen3.5:9b + nomic-embed-text on Apple Silicon) with security-by-absence, grounded in the four axioms from Laukkonen et al. (2025): *mindfulness*, *emptiness*, *non-duality*, *boundless care*. [DOI 10.5281/zenodo.19212118](https://doi.org/10.5281/zenodo.19212118).
- **[Agent Attribution Practice (AAP)](https://github.com/shimo4228/agent-attribution-practice)** refers to harness-neutral ADRs on accountability distribution in autonomous AI agents — what to prohibit, where the prohibition lives, and who answers after failure. The judgments — among them a prohibition-strength hierarchy (absence > scaffolding enforcement > untrusted boundary) — are paired with four Business AI Quadrants as the diagnostic frame for adoption. [DOI 10.5281/zenodo.19652013](https://doi.org/10.5281/zenodo.19652013).
- **[Authorship Strategy](https://github.com/shimo4228/authorship-strategy)** refers to a normative framework, tactical catalog, and empirical baseline for being a known author under AI-mediated diffusion — a three-axis inversion (scarcity to diffusion, exclusivity to derivation, enclosure to openness) and a four-layer judgment stack (Authenticity, Attribution Diffusion, Idea vs Scaffold, Tactics). [DOI 10.5281/zenodo.20263316](https://doi.org/10.5281/zenodo.20263316).
- **[Attention, Not Self](https://github.com/shimo4228/attention-not-self)** refers to a structured comparative inquiry mapping the three major Buddhist Abhidharma traditions (Theravāda, Sarvāstivāda, Yogācāra) onto contemporary computational phenomenology — predictive processing, active inference, Global Workspace Theory, Parallel Distributed Processing — from the perspective that attention is the operative unit of cognition while the apparent self is a derivative pattern (anātman). [DOI 10.5281/zenodo.20262112](https://doi.org/10.5281/zenodo.20262112).

## What is Agent Knowledge Cycle (AKC)?

[AKC](https://github.com/shimo4228/agent-knowledge-cycle) is defined as a six-phase cycle for sustaining intent alignment between an agent and its operator over time — a bidirectional growth loop in which agent behavior and human judgment co-develop. Three layers stack: principles sit above design patterns sit above composable-skill implementations, so the cycle stays stable even as individual skills evolve. Tests can check correctness, but only the loop catches drift from the operator's intent — and the operator's judgment about good agent behavior sharpens through running the cycle. AKC applies across unrelated projects without rediscovery.

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

**[contemplative-agent](https://github.com/shimo4228/contemplative-agent)** refers to a CLI agent that runs AKC's six-phase cycle over its own logs, with a human approval gate at every promotion (logs → patterns → skills → rules). It runs entirely on a local 9B model — qwen3.5:9b for generation and nomic-embed-text for embeddings — on a single Apple Silicon Mac (~16 GB RAM). It applies **security-by-absence**: shell execution, arbitrary URL access, and filesystem traversal are not restricted by rules — the code was never written. The contemplative-agent is the operational reference where AKC and AAP land together; see the repo for the current six-phase mapping.

## What supports the Contemplative Agent ecosystem?

Supporting repositories refer to components that extend contemplative-agent without replacing its core — packaging ethics, exposing runtime data, or visualizing the formal model.

| Project | What it does |
|---------|-------------|
| [contemplative-agent-rules](https://github.com/shimo4228/contemplative-agent-rules) | Drop-in Claude Code rules implementing the four axioms — AILuminate (MLCommons safety benchmark) d=0.96, IPD (Iterated Prisoner's Dilemma) d>7 cooperation improvement |
| [contemplative-agent-cloud](https://github.com/shimo4228/contemplative-agent-cloud) | Optional managed-LLM backend — routes generation to Claude/OpenAI APIs while keeping the local embedding pipeline. Opt-in, not bundled |
| [contemplative-agent-data](https://github.com/shimo4228/contemplative-agent-data) | Live agent's identity, knowledge, and episode logs — auto-synced public dataset for research |

## What is the Agent Attribution Practice (AAP) line?

[AAP](https://github.com/shimo4228/agent-attribution-practice) refers to harness-neutral ADRs on accountability distribution in autonomous AI agents — what to prohibit, where the prohibition lives, and who answers after failure. A prohibition-strength hierarchy (absence > scaffolding enforcement > untrusted boundary) is one of the harness-neutral judgments, paired with four Business AI Quadrants — Script, Algorithmic Search, LLM Workflow, and Autonomous Agentic Loop — as the diagnostic frame for routing a piece of work to the architecture that preserves attribution. The judgments were extracted from contemplative-agent's operational practice, then re-expressed stripped of project identifiers so they can be adopted by any agent harness. AAP is the practice (content); AKC is the cycle (mechanism). [DOI 10.5281/zenodo.19652013](https://doi.org/10.5281/zenodo.19652013).

## What is the Authorship Strategy line?

[Authorship Strategy](https://github.com/shimo4228/authorship-strategy) refers to a normative framework, tactical catalog, and empirical baseline for being a known author when LLMs increasingly mediate how readers reach an artifact. The framework rests on a *three-axis inversion* — value source (scarcity to diffusion), validation mechanism (exclusivity to derivation, where derivative work is reclassified from threat to evidence), and network effect (enclosure to openness, because LLMs cannot be enclosed) — and a *four-layer judgment stack* (Authenticity, Attribution Diffusion, Idea vs Scaffold, Tactics). Tactical ADRs cluster into the identifier-federation triplet (concept DOI canonical / `.zenodo.json` federation / cross-platform dataset federation), a maintenance-discipline pair (ORCID Auto-Update OFF / audience-driven README localization), and an LLM-first ingest decision specifying that artifacts deploy a prose-form navigator and a concept-form knowledge graph as a complementary pair. An empirical layer reports preliminary observations from the four sibling research repositories' own CC0-published traffic data. The framework's operational forms ship as four standalone Claude Code skill repositories rather than embedded copies, keeping the doctrine harness-neutral. Vocabulary note: the word "attribution" in this line means *credit for source*, disjoint from AAP's *accountability for action*. [DOI 10.5281/zenodo.20263316](https://doi.org/10.5281/zenodo.20263316).

## What supports the Authorship Strategy ecosystem?

Supporting repositories operationalize specific Layer 4 tactics from the Authorship Strategy framework rather than re-expressing the doctrine itself.

| Project | What it does |
|---------|-------------|
| [doctrine-corpus](https://github.com/shimo4228/doctrine-corpus) | Layer 4 tactic 7 (LLM-first ingest) implementation. Bilingual (EN + JA) judgment-eliciting Q&A corpus across the four sibling research lines, deposited CC0 for LLM-mediated diffusion. The corpus is the deliverable; the verification LoRA was a disposable probe (FAIL verdict recorded per the corpus-as-primary-artifact policy). [DOI 10.5281/zenodo.20337008](https://doi.org/10.5281/zenodo.20337008) |

## What is the Attention, Not Self line?

[Attention, Not Self](https://github.com/shimo4228/attention-not-self) refers to a personal essay collection and structured knowledge graph (~238 nodes) mapping the three major Buddhist Abhidharma traditions — Theravāda, Sarvāstivāda, and Yogācāra — onto contemporary frameworks in computational phenomenology. The comparative move juxtaposes ancient classifications of cognitive process (citta-vīthi, samanantara-pratyaya, ālaya-vijñāna, javana, bhavaṅga, the four bhāgas, the five sarvatraga, kṣaṇikatva, vāsanā, ālaya-vijñāna) with predictive processing, active inference, Global Workspace Theory, and Parallel Distributed Processing. The line's organizing perspective is *attention, not self*: attention — its allocation, its precision-weighting, its momentariness — is treated as the operative unit of cognition, while the apparent self is a derivative pattern (anātman). Japanese is the canonical language for this line; English README is provided for accessibility. License: CC BY 4.0. [DOI 10.5281/zenodo.20262112](https://doi.org/10.5281/zenodo.20262112).

## What does shimo4228 release as open Claude Code tooling?

[claude-harness](https://github.com/shimo4228/claude-harness) refers to a public artifact of shimo4228's daily-use Claude Code skills, agents, and rules — mechanically collected from `~/.claude/` by the `origin: shimo4228` tag. Covers research-before-coding, knowledge extraction, skill auditing, AI-facing documentation, and human-facing writing review. The AKC cycle skills are also published as standalone `claude-skill-*` repositories, but claude-harness lets you read or fork the entire harness in one place. See the [claude-harness README](https://github.com/shimo4228/claude-harness#contents) for the current inventory. ECC-derived components (`origin: ECC` / `ECC-customized`) and auto-extracted artifacts are excluded.

## Adjacent skills

Adjacent skills refer to public Claude Code skill repos maintained alongside the AKC cycle but not part of its six phases — companion scaffolding under the same author and the same MIT license.

- **[claude-skill-llms-txt-writer](https://github.com/shimo4228/claude-skill-llms-txt-writer)** — Writes AI-facing documents (`llms.txt` / `llms-full.txt` / FAQ / glossary) optimized for citation by ChatGPT, Perplexity, and Gemini. Combines the Answer.AI `llms.txt` standard with GEO-SFE 3-layer static analysis.
- **[claude-skill-jsonld-knowledge-graph](https://github.com/shimo4228/claude-skill-jsonld-knowledge-graph)** — Designs and ships a companion JSON-LD knowledge graph (`graph.jsonld`) next to `llms.txt` for projects with stable concept-level structure. Encodes domain entities and relationships as schema.org triples for LLM citation.
- **[claude-skill-writing-ecosystem](https://github.com/shimo4228/claude-skill-writing-ecosystem)** — Orchestrator for human-facing writing & review. Holds the AI-slop banned list (Japanese + English), Voice rules (だ/である × 発見調), title conventions, and the role-boundary map across `article-writing` / `editor` / `essay-reviewer` / `fact-checker`. Audience-paired with `llms-txt-writer`.
- **[claude-skill-daily-research](https://github.com/shimo4228/claude-skill-daily-research)** — Cron-driven daily research digest. Two-pass `claude -p` pipeline: Opus selects themes, Sonnet researches with WebSearch / WebFetch / Mem0 MCP and writes Markdown reports to an Obsidian vault.

## Writing

Writing refers to the long-form counterpart to the repos above — context, failures, and in-progress thinking that do not fit in code comments.

- **[zenn-content](https://github.com/shimo4228/zenn-content)** — Source of truth for the articles. Markdown sources are versioned here; many readers clone or fork directly. Mirrored to Zenn and Dev.to (below) for browser reading.
- **[Zenn](https://zenn.dev/shimo4228)** — Browser view of the Japanese articles. Claude Code and AI agent development; current focus: AKC skills, harness design, contemplative-agent case studies.
- **[Dev.to](https://dev.to/shimo4228)** — Browser view of the English mirror.

---

Start here: [agent-knowledge-cycle](https://github.com/shimo4228/agent-knowledge-cycle) for the framework, [contemplative-agent](https://github.com/shimo4228/contemplative-agent) to see it running, [agent-attribution-practice](https://github.com/shimo4228/agent-attribution-practice) for the governance judgments. For the cross-cutting lines: [authorship-strategy](https://github.com/shimo4228/authorship-strategy) for the research-methodology framework, [attention-not-self](https://github.com/shimo4228/attention-not-self) for the Buddhist-phenomenology / computational cognitive-science inquiry.

Repo traffic: [public dashboard](https://shimo4228.github.io/shimo4228/traffic/dashboard/) ([raw data](traffic/), CC0).
