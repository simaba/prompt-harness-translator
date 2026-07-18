from __future__ import annotations

from pathlib import Path
import re
from typing import Any, Collection

import yaml


FRONTMATTER_PATTERN = re.compile(
    r"^---\s*\r?\n(?P<frontmatter>.*?)\r?\n---\s*\r?\n?(?P<body>.*)$",
    flags=re.S,
)
TARGETS = {"codex", "cursor", "generic"}
# Compatibility constant for callers that inspect the source fields directly.
# Rendering now computes mapped fields per target instead of applying this set
# globally.
MAPPED_FIELDS = {"name", "description"}


class TranslationError(ValueError):
    """Raised when a prompt asset cannot be parsed or translated safely."""


def parse_simple_agent_markdown(text: str) -> dict[str, Any]:
    """Parse YAML frontmatter and preserve the original normalized result shape."""
    match = FRONTMATTER_PATTERN.match(text)
    if not match:
        raise TranslationError(
            "Unsupported source format: expected YAML frontmatter delimited by ---"
        )

    raw_frontmatter, body = match.group("frontmatter"), match.group("body")
    try:
        metadata = yaml.safe_load(raw_frontmatter) or {}
    except yaml.YAMLError as exc:
        raise TranslationError(f"Invalid YAML frontmatter: {exc}") from exc

    if not isinstance(metadata, dict):
        raise TranslationError("YAML frontmatter must be a mapping/object")

    name = metadata.get("name", "agent")
    description = metadata.get("description", "")
    if not isinstance(name, str) or not name.strip():
        raise TranslationError("frontmatter.name must be a non-empty string when provided")
    if not isinstance(description, str):
        raise TranslationError("frontmatter.description must be a string when provided")

    # Retain unsupported_fields for compatibility with existing callers. It
    # represents fields outside the original common source core, not the fields
    # unsupported by every target. Renderers calculate target-specific loss.
    unsupported = {
        key: value
        for key, value in metadata.items()
        if key not in MAPPED_FIELDS
    }
    return {
        "name": name.strip(),
        "description": description.strip(),
        "instructions": body.strip(),
        "metadata": metadata,
        "unsupported_fields": unsupported,
    }


def _unmapped_metadata(
    fields: dict[str, Any],
    mapped_fields: Collection[str],
) -> dict[str, Any]:
    mapped = set(mapped_fields)
    return {
        key: value
        for key, value in fields["metadata"].items()
        if key not in mapped
    }


def _lossy_warning(unmapped: dict[str, Any]) -> str:
    if not unmapped:
        return ""
    keys = ", ".join(sorted(unmapped))
    return (
        "> **Lossy conversion warning:** this target does not natively apply all "
        "source metadata. "
        f"Preserved for review: {keys}.\n\n"
    )


def _preserved_metadata_block(unmapped: dict[str, Any]) -> str:
    if not unmapped:
        return ""
    serialized = yaml.safe_dump(
        unmapped,
        sort_keys=True,
        allow_unicode=True,
    ).strip()
    return f"\n## Unmapped source metadata\n\n```yaml\n{serialized}\n```\n"


def render_codex(fields: dict[str, Any]) -> str:
    unmapped = _unmapped_metadata(fields, {"name", "description"})
    name = fields["name"]
    description = fields["description"]
    instructions = fields["instructions"]
    return (
        f"# {name}\n\n"
        f"{_lossy_warning(unmapped)}"
        f"{description}\n\n"
        f"## Instructions\n\n{instructions}\n"
        f"{_preserved_metadata_block(unmapped)}"
    )


def render_cursor(fields: dict[str, Any]) -> str:
    # The supported Cursor representation used by this utility has a name and a
    # rule body. Description and all other source metadata are preserved for
    # review rather than silently discarded or represented as enforced fields.
    unmapped = _unmapped_metadata(fields, {"name"})
    payload: dict[str, Any] = {
        "name": fields["name"],
        "rule": fields["instructions"],
    }
    if unmapped:
        payload["conversion_warning"] = (
            "Lossy conversion: review source_metadata before use; these fields "
            "are preserved but not enforced by the target representation."
        )
        payload["source_metadata"] = unmapped
    return yaml.safe_dump(payload, sort_keys=False, allow_unicode=True)


def render_generic(fields: dict[str, Any]) -> str:
    payload = dict(fields["metadata"])
    payload["instructions"] = fields["instructions"]
    return yaml.safe_dump(payload, sort_keys=False, allow_unicode=True)


def translate_text(text: str, target: str) -> str:
    fields = parse_simple_agent_markdown(text)
    normalized_target = target.lower()
    if normalized_target not in TARGETS:
        supported = ", ".join(sorted(TARGETS))
        raise TranslationError(
            f"Unsupported target: {target}. Supported targets: {supported}"
        )
    if normalized_target == "codex":
        return render_codex(fields)
    if normalized_target == "cursor":
        return render_cursor(fields)
    return render_generic(fields)


def translate_file(path: str | Path, target: str) -> str:
    return translate_text(Path(path).read_text(encoding="utf-8"), target)
