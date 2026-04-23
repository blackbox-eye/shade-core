from __future__ import annotations

import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
WORKFLOW_PATH = REPO_ROOT / ".github" / "workflows" / "pr-baseline.yml"
TRACEABILITY_PATH = REPO_ROOT / "docs" / "qa" / "docs-to-code-traceability.md"
INDEX_PATHS = (
    REPO_ROOT / "docs" / "README.md",
    REPO_ROOT / "docs" / "architecture" / "README.md",
    REPO_ROOT / "docs" / "governance" / "README.md",
    REPO_ROOT / "docs" / "onboarding" / "README.md",
    REPO_ROOT / "docs" / "qa" / "README.md",
    REPO_ROOT / "docs" / "releases" / "README.md",
)
IGNORE_TOKENS = {"No current code file", "None"}


def test_pr_baseline_workflow_has_expected_tokens() -> None:
    assert WORKFLOW_PATH.is_file()

    workflow_text = WORKFLOW_PATH.read_text(encoding="utf-8")

    assert "name: pr-baseline" in workflow_text
    assert "python -m pytest" in workflow_text


def test_traceability_paths_exist() -> None:
    assert TRACEABILITY_PATH.is_file()

    traceability_text = TRACEABILITY_PATH.read_text(encoding="utf-8")

    for line in traceability_text.splitlines():
        if not line.startswith("|"):
            continue
        if "Code file" in line or "---" in line:
            continue

        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) < 4:
            continue

        for cell in (cells[1], cells[3]):
            if cell in IGNORE_TOKENS:
                continue

            for relative_path in re.findall(r"`([^`]+)`", cell):
                assert not Path(relative_path).is_absolute(), (
                    f"Path must be repo-relative, got absolute: {relative_path!r}"
                )
                resolved = (REPO_ROOT / relative_path).resolve()
                assert resolved.is_relative_to(REPO_ROOT), (
                    f"Resolved path escapes repo root: {resolved}"
                )
                assert resolved.is_file()


def test_docs_index_files_exist() -> None:
    for path in INDEX_PATHS:
        assert path.is_file()
