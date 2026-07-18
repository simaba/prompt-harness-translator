import yaml

from prompt_harness_translator.core import translate_text


SOURCE = """---
name: demo
description: Example role
tools: ["Read", "Write"]
model: reasoning
---

Do the thing carefully.
"""


def test_translate_codex_maps_description_and_preserves_other_metadata():
    out = translate_text(SOURCE, "codex")

    assert "# demo" in out
    assert "Example role" in out
    assert "Lossy conversion warning" in out
    assert "tools:" in out
    assert "model: reasoning" in out


def test_translate_cursor_preserves_description_in_source_metadata():
    out = translate_text(SOURCE, "cursor")
    payload = yaml.safe_load(out)

    assert payload["name"] == "demo"
    assert payload["rule"] == "Do the thing carefully."
    assert "Lossy conversion" in payload["conversion_warning"]
    assert payload["source_metadata"]["description"] == "Example role"
    assert payload["source_metadata"]["tools"] == ["Read", "Write"]
    assert payload["source_metadata"]["model"] == "reasoning"


def test_generic_preserves_all_source_metadata_without_loss_warning():
    out = translate_text(SOURCE, "generic")
    payload = yaml.safe_load(out)

    assert payload["name"] == "demo"
    assert payload["description"] == "Example role"
    assert payload["tools"] == ["Read", "Write"]
    assert payload["model"] == "reasoning"
    assert payload["instructions"] == "Do the thing carefully."
    assert "conversion_warning" not in payload


def test_crlf_frontmatter_is_supported():
    source = SOURCE.replace("\n", "\r\n")

    out = translate_text(source, "generic")
    payload = yaml.safe_load(out)

    assert payload["name"] == "demo"
    assert payload["instructions"] == "Do the thing carefully."


def test_cursor_without_description_has_no_false_description_warning():
    source = """---
name: demo
---

Do the thing carefully.
"""

    out = translate_text(source, "cursor")
    payload = yaml.safe_load(out)

    assert "source_metadata" not in payload
    assert "conversion_warning" not in payload
