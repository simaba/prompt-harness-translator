# Supported Formats and Conversion Limits

## Supported source shape

The translator currently accepts Markdown files with YAML frontmatter delimited by `---`. Both LF and CRLF line endings are supported.

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

| Target | Fields represented directly | Preserved for review | Important limit |
|---|---|---|---|
| `codex` | `name`, `description`, instruction body | every other source metadata field in a visible Markdown block | Preserved metadata is not automatically enforced by the runtime |
| `cursor` | `name`, instruction body as `rule` | `description` and every other source metadata field under `source_metadata` | Preserved metadata is not represented as an active Cursor control |
| `generic` | all source metadata plus `instructions` | not applicable; this is the preservation representation | The output is not an executable interoperability standard |

## Lossy conversion policy

Mapping is target-specific. A field is considered mapped only when the selected target representation has a direct place for it.

When a target cannot represent a source metadata field, the translator:

1. retains the field in the generated artifact;
2. places it in a clearly identified review-only section;
3. emits a visible lossy-conversion warning;
4. does not imply that the target runtime will enforce it.

The translator must not silently discard a source description, tool declaration, model preference, permission note, or other metadata merely because another target can represent that field.

## Not supported today

- arbitrary `AGENTS.md` conventions;
- provider-specific agent manifests outside the supported Markdown/YAML source shape;
- semantic or behavioral equivalence across targets;
- tool-permission, connector, policy, or hidden-runtime equivalence;
- every version of every prompt or agent ecosystem.

Review generated outputs before use. Similar-looking instruction text can behave differently across tools because defaults, policies, tools, and runtime implementations differ.
