from __future__ import annotations

from pathlib import Path
import re


def parse_simple_agent_markdown(text: str) -> dict:
    match = re.match(r"^---\n(.*?)\n---\n\n(.*)$", text, flags=re.S)
    if not match:
        raise ValueError("Unsupported source format")
    frontmatter, body = match.groups()
    fields = {}
    for line in frontmatter.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip()
    fields["instructions"] = body.strip()
    return fields


def render_codex(fields: dict) -> str:
    name = fields.get("name", "agent")
    description = fields.get("description", "")
    instructions = fields.get("instructions", "")
    return f"# {name}\n\n{description}\n\n## Instructions\n\n{instructions}\n"


def render_cursor(fields: dict) -> str:
    name = fields.get("name", "agent")
    instructions = fields.get("instructions", "")
    return f"name: {name}\nrule: |\n  {instructions.replace(chr(10), chr(10)+'  ')}\n"


def render_generic(fields: dict) -> str:
    return "\n".join(f"{k}: {v}" for k, v in fields.items())


def translate_text(text: str, target: str) -> str:
    fields = parse_simple_agent_markdown(text)
    target = target.lower()
    if target == "codex":
        return render_codex(fields)
    if target == "cursor":
        return render_cursor(fields)
    if target == "generic":
        return render_generic(fields)
    raise ValueError(f"Unsupported target: {target}")


def translate_file(path: str | Path, target: str) -> str:
    return translate_text(Path(path).read_text(encoding="utf-8"), target)
