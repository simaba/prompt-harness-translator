# prompt-harness-translator

A CLI utility that translates skills, agent definitions, and prompt packs across harness formats.

## Problem

Prompt and harness assets are often trapped in one ecosystem. This repo creates a thin translation layer between common structures such as:

- Claude-style agent markdown
- generic `AGENTS.md`
- Cursor rules
- Codex-oriented instructions
- Gemini-oriented prompt or extension stubs

## What this starter repo includes

- a canonical intermediate schema
- translators for a few simple target formats
- example source and generated artifacts
- tests for the core conversions

## Quick start

```bash
pip install -e .
prompt-harness translate examples/sample_agent.md --target codex
prompt-harness translate examples/sample_agent.md --target cursor
```

## Design rule

Translation should preserve intent, role, constraints, and output expectations, while clearly flagging fields that do not map cleanly.
