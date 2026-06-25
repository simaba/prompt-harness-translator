# Prompt Harness Translator

A small CLI utility for translating one supported Markdown/YAML prompt-asset shape into a few reviewable target representations.

## Maturity

**Starter utility.**

The translator is intentionally narrow: it preserves structured YAML frontmatter, renders a limited set of targets, and warns when a target cannot represent source metadata. It is not an interoperability standard or a guarantee of behavioral equivalence.

## Start here

- [Supported formats and limits](docs/SUPPORTED_FORMATS.md)
- [Public Release Checklist](docs/PUBLIC_RELEASE_CHECKLIST.md)
- [Changelog](CHANGELOG.md)

## Current capabilities

- accepts Markdown with YAML frontmatter delimited by `---`
- validates frontmatter structure plus `name`/`description` types when present
- preserves nested, list, and multiline YAML metadata
- renders `codex`, `cursor`, and `generic` outputs
- preserves unmapped metadata and emits a visible lossy-conversion warning where needed
- includes tests for nested YAML, multiline fields, invalid input, and unsupported targets

## Quick start

```bash
python -m pip install -e .
prompt-harness translate examples/sample_agent.md --target codex
prompt-harness translate examples/sample_agent.md --target cursor
prompt-harness translate examples/sample_agent.md --target generic
```

## Translation rule

Generated output should preserve the source intent where the target can represent it. When a field cannot map directly, the translator retains it for human review and states that the conversion is lossy.

Do not treat generated text as proof that two runtimes will behave identically.

## Publication safety

Use only fictional, generic, or fully sanitized prompt assets.

Do not publish:

- internal system prompts or private agent instructions
- customer-specific workflows or proprietary tool names
- endpoints, credentials, tokens, connector details, or private environment configuration
- employer-, vendor-, or client-specific operating instructions
- security, moderation, escalation, or policy logic not intended for public release

## Out of scope

This utility does not provide:

- full semantic equivalence across tools
- arbitrary `AGENTS.md` parsing
- complete support for all agent/prompt formats
- automatic safety review of generated instructions
- preservation of hidden runtime behavior, tool permissions, or provider policy
- compatibility with every version of every ecosystem

## Next quality steps

1. version the normalized internal representation
2. add golden fixtures for each supported target
3. add more regression tests for quoted and unknown metadata
4. document changes when a supported target format evolves

## Scope and disclaimer

This repository is shared in a personal capacity. Generated artifacts should be manually reviewed before use. Prompt and agent behavior can change materially across runtimes even when instruction text appears similar.

---

*Maintained by [Sima Bagheri](https://github.com/simaba.*