from prompt_harness_translator.core import translate_text


SOURCE = """---
name: demo
description: Example role
tools: [\"Read\", \"Write\"]
model: reasoning
---

Do the thing carefully.
"""


def test_translate_codex():
    out = translate_text(SOURCE, "codex")
    assert "# demo" in out


def test_translate_cursor():
    out = translate_text(SOURCE, "cursor")
    assert "name: demo" in out
