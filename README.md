# Prompt Harness Translator

A CLI utility that translates skills, agent definitions, and prompt packs across harness formats.

## Status

**Starter utility.**

This repo provides a thin translation layer and testable conversion path for simple agent and prompt assets. It is not yet a complete interoperability standard or a full-fidelity converter across every harness ecosystem.

## Problem

Prompt and harness assets are often trapped in one ecosystem. This repo creates a translation layer between common structures such as:

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

## Public-safe use rule

Do not publish private or proprietary prompt assets in this repository.

Avoid committing:

- internal system prompts
- private agent instructions
- customer-specific workflows
- confidential tool names or endpoints
- API keys, tokens, or connector details
- employer, vendor, or client-specific operating instructions
- prompt assets that reveal security, moderation, or escalation policies not intended for public release

Use fictional examples that demonstrate structure without exposing private operating logic.

## What this repo does not claim yet

This repository does **not** yet claim:

- full semantic equivalence across harnesses
- complete support for all prompt or agent formats
- automatic safety review of translated instructions
- compatibility with every version of every tool
- preservation of hidden or proprietary runtime behavior

## Next maturity step

To make this repo stronger before public promotion, add:

1. a compatibility matrix for supported source and target formats
2. schema validation for the intermediate representation
3. warning output for lossy conversions
4. more sample conversions with before/after explanations
5. tests for unsupported or partially supported fields

## Scope and disclaimer

This repository is shared in a personal capacity. It is not affiliated with or endorsed by Anthropic, OpenAI, Cursor, Google, or any other harness or tooling provider.

Generated translations should be reviewed manually before use. Prompt and agent behavior can change materially across harnesses even when instructions appear similar.

---

*Maintained by [Sima Bagheri](https://github.com/simaba).*
