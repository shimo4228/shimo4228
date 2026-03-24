Language: English | [日本語](README.ja.md)

# Shimo (@shimo4228)

Two research lines: **practical self-improvement tools** for AI coding agents, and **contemplative AI** for autonomous agents.

## Featured Work

### [Agent Knowledge Cycle (AKC)](https://github.com/shimo4228/agent-knowledge-cycle)

A cyclic self-improvement architecture for AI coding agents — six composable skills forming a closed loop:

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
| [context-sync](https://github.com/shimo4228/claude-skill-context-sync) | Maintain | Audit documentation for role overlaps, stale content, and missing ADRs |

### Contemplative AI

**[contemplative-agent](https://github.com/shimo4228/contemplative-agent)** — Autonomous AI agent that distills its own experiences into knowledge and skills — sleep-time memory consolidation, identity refinement, and behavioral skill extraction, all running on local LLM via Ollama.

| Project | What it does |
|---------|-------------|
| [contemplative-agent-rules](https://github.com/shimo4228/contemplative-agent-rules) | Claude Code rules inspired by the four axioms — tested with IPD benchmarks |
| [active-inference-viz](https://github.com/shimo4228/active-inference-viz) | Interactive visualization of Active Inference dynamics |

### Applications

| Project | What it does |
|---------|-------------|
| [pdf2anki](https://github.com/shimo4228/pdf2anki) | PDF → Anki flashcard converter using AI |
| [daily-research](https://github.com/shimo4228/daily-research) | Automated daily AI research digest — zero Python, just shell + prompts |

## Writing

- **[Zenn](https://zenn.dev/shimo4228)** — Claude Code, AI agent development (Japanese)
- **[Dev.to](https://dev.to/shimo4228)** — English translations + original post
