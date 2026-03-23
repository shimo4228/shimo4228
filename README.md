Language: English | [日本語](README.ja.md)

# Shimo (@shimo4228)

Building developer tools for AI agent self-improvement, inspired by contemplative AI.

## Featured Work

### AI Agent Knowledge Lifecycle (contributed to [ECC](https://github.com/affaan-m/everything-claude-code))

Six skills that form a self-improvement loop for AI agents:

```
Experience → learn-eval → skill-stocktake → rules-distill → Behavior change → ...
               (extract)    (curate)          (promote)            ↑
                                                            skill-comply
                                                              (measure)
```

| Project | Role | What it does |
|---------|------|-------------|
| [search-first](https://github.com/shimo4228/claude-skill-search-first) | Research | Encourages agents to research existing solutions before building |
| [learn-eval](https://github.com/shimo4228/claude-skill-learn-eval) | Extract | Extracts reusable patterns from sessions with quality gates |
| [skill-stocktake](https://github.com/shimo4228/claude-skill-stocktake) | Curate | Audits installed skills for staleness, conflicts, and redundancy |
| [rules-distill](https://github.com/shimo4228/claude-skill-rules-distill) | Promote | Distills cross-cutting principles from skills into rules |
| [skill-comply](https://github.com/shimo4228/claude-skill-comply) | Measure | Tests whether agents actually follow skills via behavioral compliance testing |
| [context-sync](https://github.com/shimo4228/claude-skill-context-sync) | Maintain | Audits documentation roles, detects overlaps, migrates content, checks freshness |

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
