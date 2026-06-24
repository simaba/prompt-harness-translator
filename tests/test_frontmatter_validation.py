from __future__ import annotations

import pytest

from prompt_harness_translator.core import TranslationError, parse_simple_agent_markdown, translate_text


NESTED_SOURCE = """---
name: reviewer
description: |
  Review changes carefully:
  preserve safety constraints.
tools:
  read:
    enabled: true
  write:
    enabled: false
tags:
  - governance
  - evaluation
---

Provide a concise review.
"""


def test_nested_yaml_frontmatter_is_parsed_without_loss():
    fields = parse_simple_agent_markdown(NESTED_SOURCE)

    assert fields["name"] == "reviewer"
    assert fields["metadata"]["tools"]["read"]["enabled"] is True
    assert fields["metadata"]["tags"] == ["governance", "evaluation"]
    assert "tools" in fields["unsupported_fields"]


def test_codex_output_warns_and_preserves_unmapped_metadata():
    output = translate_text(NESTED_SOURCE, "codex")

    assert "Lossy conversion warning" in output
    assert "## Unmapped source metadata" in output
    assert "tools:" in output
    assert "tags:" in output


def test_cursor_output_keeps_unmapped_metadata_for_review():
    output = translate_text(NESTED_SOURCE, "cursor")

    assert "conversion_warning:" in output
    assert "source_metadata:" in output
    assert "enabled: true" in output


def test_invalid_yaml_frontmatter_fails_clearly():
    source = """---
name: [broken
---

Do work.
"""

    with pytest.raises(TranslationError, match="Invalid YAML frontmatter"):
        translate_text(source, "codex")


def test_invalid_target_reports_supported_targets():
    with pytest.raises(TranslationError, match="Supported targets"):
        translate_text(NESTED_SOURCE, "unknown")
