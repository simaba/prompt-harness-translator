# Supported Formats and Conversion Limits

## Source shape supported today

The translator accepts Markdown with YAML frontmatter delimited by `---`.

```markdown
---
name: example-agent
description: A short description.
labels:
  - fictional
---

Write the instructions here.
```

The parser validates that the frontmatter is a mapping and that `name` and `description`, when provided, are strings. Nested, list, and multiline YAML values are preserved as metadata.

## Targets supported today

| Target | Output behavior | Known limit |
|---|---|---|
| `codex` | Markdown instructions with a visible conversion warning and preserved unmapped metadata | Metadata is documented, not automatically enforced by a Codex runtime |
| `cursor` | YAML rule content with `source_metadata` and a conversion warning | Source-only settings are not automatically translated into Cursor behavior |
| `generic` | YAML containing the original metadata plus instructions | This is a preservation format, not an executable harness contract |

## Lossy conversion policy

When the target does not have a direct representation for a source metadata field, the translator must preserve the field and show a warning. It must not silently discard it or imply that the target will enforce it.

## Not currently supported

The repository does not yet provide dedicated parsers or renderers for:

- arbitrary `AGENTS.md` conventions
- harness-specific Claude agent definitions
- Gemini extensions or tool manifests
- hidden runtime settings, policy behavior, tool permissions, or provider-specific execution semantics

Review generated outputs before use. Instruction text alone is not proof of behavioral equivalence across harnesses.
