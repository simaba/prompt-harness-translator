# Prompt Harness Translator

A CLI utility for translating skills, agent definitions, and prompt packs across harness formats.

## Maturity

**Starter utility.**

This repository provides a thin translation layer and a testable conversion path for simple agent and prompt assets. It is not a complete interoperability standard or a full-fidelity converter across every harness ecosystem.

## Purpose

Prompt and harness assets are often shaped around one tool ecosystem. This repository introduces a canonical intermediate schema so prompt and agent assets can be translated more consistently between formats.

Supported concept areas include:

- Claude-style agent markdown
- generic `AGENTS.md`
- Cursor rules
- Codex-oriented instructions
- Gemini-oriented prompt or extension stubs

## Current capabilities

- canonical intermediate schema
- translators for a few simple target formats
- example source and generated artifacts
- tests for core conversions

## Quick start

```bash
pip install -e .
prompt-harness translate examples/sample_agent.md --target codex
prompt-harness translate examples/sample_agent.md --target cursor
```

## Design principle

Translation should preserve intent, role, constraints, and output expectations, while clearly flagging fields that do not map cleanly.

## Publication safety

Do not publish private or proprietary prompt assets in this repository.

Avoid committing:

- internal system prompts
- private agent instructions
- customer-specific workflows
- confidential tool names or endpoints
- API keys, tokens, or connector details
- employer-, vendor-, or client-specific operating instructions
- prompt assets that reveal security, moderation, or escalation policies not intended for public release

Use fictional examples that demonstrate structure without exposing private operating logic.

## Out of scope

This starter utility does not yet provide:

- full semantic equivalence across harnesses
- complete support for all prompt or agent formats
- automatic safety review of translated instructions
- compatibility with every version of every tool
- preservation of hidden or proprietary runtime behavior

## Roadmap

To mature into a stronger utility, this repository should add:

1. a compatibility matrix for supported source and target formats
2. schema validation for the intermediate representation
3. warning output for lossy conversions
4. more sample conversions with before-and-after explanations
5. tests for unsupported or partially supported fields

## Scope and disclaimer

This repository is shared in a personal capacity. It is not affiliated with or endorsed by Anthropic, OpenAI, Cursor, Google, or any other harness or tooling provider.

Generated translations should be reviewed manually before use. Prompt and agent behavior can change materially across harnesses even when instructions appear similar.

---

*Maintained by [Sima Bagheri](https://github.com/simaba).*
