# Supported Formats and Conversion Limits

## Supported source shape

The translator currently accepts Markdown files with YAML frontmatter delimited by `---`.

```markdown
---
name: example-agent
description: A short description.
labels:
  - fictional
---

Write the instructions here.
```

Nested, list, and multiline YAML metadata is preserved. The parser validates that frontmatter is an object and validates the core `name` and `description` fields when they are present.

## Supported targets

| Target | Output behavior | Important limit |
|---|---|---|
| `codex` | Markdown instructions plus a visible lossy-conversion warning and preserved unmapped metadata | Preserved metadata is for review; it is not automatically enforced by the target runtime |
| `cursor` | YAML rule content with `source_metadata` and a conversion warning | Source-only settings do not automatically become runtime controls |
| `generic` | YAML containing source metadata and instructions | Preservation format only; not an executable interoperability standard |

## Lossy conversion policy

When a target cannot represent a source metadata field, the translator preserves the field and emits a warning. It must not silently drop the field or imply behavioral equivalence.

## Not supported today

- arbitrary `AGENTS.md` conventions
- provider-specific agent manifests outside the supported Markdown/YAML source shape
- tool-permission, connector, policy, or hidden-runtime equivalence
- every version of every prompt or agent ecosystem

Review generated outputs before use. Similar-looking instruction text can behave differently across tools because defaults, policies, tools, and runtime implementations differ.