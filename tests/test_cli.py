from __future__ import annotations

import sys

import pytest

from prompt_harness_translator import cli


def test_cli_reports_missing_source_file_without_traceback(monkeypatch, capsys) -> None:
    monkeypatch.setattr(
        sys,
        "argv",
        ["prompt-harness", "translate", "does-not-exist.md", "--target", "codex"],
    )

    with pytest.raises(SystemExit) as exit_info:
        cli.main()

    captured = capsys.readouterr()
    assert exit_info.value.code == 2
    assert "does-not-exist.md" in captured.err
    assert "Traceback" not in captured.err


def test_cli_reports_unsupported_target_without_traceback(monkeypatch, tmp_path, capsys) -> None:
    source = tmp_path / "agent.md"
    source.write_text("---\nname: demo\n---\nInstruction", encoding="utf-8")
    monkeypatch.setattr(
        sys,
        "argv",
        ["prompt-harness", "translate", str(source), "--target", "unsupported"],
    )

    with pytest.raises(SystemExit) as exit_info:
        cli.main()

    captured = capsys.readouterr()
    assert exit_info.value.code == 2
    assert "Unsupported target" in captured.err
    assert "Traceback" not in captured.err
