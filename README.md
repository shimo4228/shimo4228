Language: English | [日本語](README.ja.md)

# Shimo (@shimo4228)

Designing the foundational infrastructure for AI agent self-improvement — from practical developer tools to contemplative AI research.

## Featured Work

### AI Agent Knowledge Lifecycle (contributed to [ECC](https://github.com/affaan-m/everything-claude-code) — 76k+ stars)

Four skills that together form a complete self-improvement loop for AI agents:

```
Experience → learn-eval → skill-stocktake → rules-distill → Behavior change → ...
               (extract)    (curate)          (promote)
```

| Project | Role | What it does |
|---------|------|-------------|
| [search-first](https://github.com/shimo4228/claude-skill-search-first) | Research | Forces agents to research existing solutions before building |
| [learn-eval](https://github.com/shimo4228/claude-skill-learn-eval) | Extract | Extracts reusable patterns from sessions with quality gates |
| [skill-stocktake](https://github.com/shimo4228/claude-skill-stocktake) | Curate | Audits installed skills for staleness, conflicts, and redundancy |
| [rules-distill](https://github.com/shimo4228/claude-skill-rules-distill) | Promote | Distills cross-cutting principles from skills into rules |

### Contemplative AI Research

The knowledge lifecycle above implements what humans do naturally: experience → reflect → learn → change behavior. The Contemplative AI research makes this explicit — adding introspection as a first-class capability for AI agents.

**[contemplative-agent](https://github.com/shimo4228/contemplative-agent)** — Autonomous AI agent on [Moltbook](https://www.moltbook.com) that operationalizes the Contemplative AI framework (Laukkonen et al., 2025). Core/adapter architecture for platform portability, 3-layer memory with sleep-time distillation, and fully local LLM inference via Ollama.

| Project | What it does |
|---------|-------------|
| [contemplative-agent-rules](https://github.com/shimo4228/contemplative-agent-rules) | Drop-in alignment rules based on the four axioms — tested via IPD benchmarks (d>7) |
| [active-inference-viz](https://github.com/shimo4228/active-inference-viz) | Interactive visualization of Active Inference dynamics |

### Applications

| Project | What it does |
|---------|-------------|
| [pdf2anki](https://github.com/shimo4228/pdf2anki) | AI-powered PDF → Anki flashcard pipeline with Vision, TUI, caching |
| [daily-research](https://github.com/shimo4228/daily-research) | Automated daily AI research digest — zero Python, just shell + prompts |

## Writing

- **[Zenn](https://zenn.dev/shimo4228)** — Claude Code, AI agent development (Japanese)
- **[Dev.to](https://dev.to/shimo4228)** — English translations + original post
