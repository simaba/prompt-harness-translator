from __future__ import annotations

from pathlib import Path
import re
from typing import Any

import yaml


FRONTMATTER_PATTERN = re.compile(r"^---\s*\n(?P<frontmatter>.*?)\n---\s*\n?(?P<body>.*)$", flags=re.S)
TARGETS = {"codex", "cursor", "generic"}
MAPPED_FIELDS = {"name", "description"}


class TranslationError(ValueError):
    """Raised when a prompt asset cannot be parsed or translated safely."""


def parse_simple_agent_markdown(text: str) -> dict[str, Any]:
    """Parse YAML frontmatter and preserve metadata not supported by every target."""
    match = FRONTMATTER_PATTERN.match(text)
    if not match:
        raise TranslationError("Unsupported source format: expected YAML frontmatter delimited by ---")

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

    unsupported = {key: value for key, value in metadata.items() if key not in MAPPED_FIELDS}
    return {
        "name": name.strip(),
        "description": description.strip(),
        "instructions": body.strip(),
        "metadata": metadata,
        "unsupported_fields": unsupported,
    }


def _lossy_warning(fields: dict[str, Any]) -> str:
    unsupported = fields.get("unsupported_fields", {})
    if not unsupported:
        return ""
    keys = ", ".join(sorted(unsupported))
    return (
        "> **Lossy conversion warning:** this target does not natively apply all source metadata. "
        f"Preserved for review: {keys}.\n\n"
    )


def _preserved_metadata_block(fields: dict[str, Any]) -> str:
    unsupported = fields.get("unsupported_fields", {})
    if not unsupported:
        return ""
    serialized = yaml.safe_dump(unsupported, sort_keys=True, allow_unicode=True).strip()
    return f"\n## Unmapped source metadata\n\n```yaml\n{serialized}\n```\n"


def render_codex(fields: dict[str, Any]) -> str:
    name = fields["name"]
    description = fields["description"]
    instructions = fields["instructions"]
    return (
        f"# {name}\n\n"
        f"{_lossy_warning(fields)}"
        f"{description}\n\n"
        f"## Instructions\n\n{instructions}\n"
        f"{_preserved_metadata_block(fields)}"
    )


def render_cursor(fields: dict[str, Any]) -> str:
    payload: dict[str, Any] = {
        "name": fields["name"],
        "rule": fields["instructions"],
    }
    if fields["unsupported_fields"]:
        payload["conversion_warning"] = (
            "Lossy conversion: review source_metadata before use; these fields are not enforced by Cursor rules."
        )
        payload["source_metadata"] = fields["unsupported_fields"]
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
        raise TranslationError(f"Unsupported target: {target}. Supported targets: {supported}")
    if normalized_target == "codex":
        return render_codex(fields)
    if normalized_target == "cursor":
        return render_cursor(fields)
    return render_generic(fields)


def translate_file(path: str | Path, target: str) -> str:
    return translate_text(Path(path).read_text(encoding="utf-8"), target)
