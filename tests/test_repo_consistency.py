from __future__ import annotations

import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
WORKFLOW_PATH = REPO_ROOT / ".github" / "workflows" / "pr-baseline.yml"
PR_TEMPLATE_PATH = REPO_ROOT / ".github" / "PULL_REQUEST_TEMPLATE.md"
COPILOT_INSTRUCTIONS_PATH = REPO_ROOT / ".github" / "copilot-instructions.md"
TRACEABILITY_PATH = REPO_ROOT / "docs" / "qa" / "docs-to-code-traceability.md"
GOVERNANCE_INDEX_PATH = REPO_ROOT / "docs" / "governance" / "README.md"
QA_INDEX_PATH = REPO_ROOT / "docs" / "qa" / "README.md"
TEST_STRATEGY_PATH = REPO_ROOT / "docs" / "qa" / "test-strategy.md"
PR_WORKFLOW_SOP_PATH = REPO_ROOT / "docs" / "governance" / "pr-workflow-sop.md"
PR_COMMAND_BUNDLES_PATH = REPO_ROOT / "docs" / "governance" / "pr-command-bundles.md"
COPILOT_BUNDLE_PROMPTS_PATH = REPO_ROOT / "docs" / "governance" / "copilot-bundle-prompts.md"
PR_REVIEW_AND_MERGE_GATES_PATH = (
    REPO_ROOT / "docs" / "governance" / "pr-review-and-merge-gates.md"
)
PR_QA_GATES_PATH = REPO_ROOT / "docs" / "qa" / "pr-qa-gates.md"
REPO_CONSISTENCY_CONTRACT_PATH = (
    REPO_ROOT / "docs" / "qa" / "repo-consistency-contract.md"
)
INDEX_PATHS = (
    REPO_ROOT / "docs" / "README.md",
    REPO_ROOT / "docs" / "architecture" / "README.md",
    REPO_ROOT / "docs" / "governance" / "README.md",
    REPO_ROOT / "docs" / "onboarding" / "README.md",
    REPO_ROOT / "docs" / "qa" / "README.md",
    REPO_ROOT / "docs" / "releases" / "README.md",
)
IGNORE_TOKENS = {"No current code file", "None"}
PLAYBOOK_PATHS = (
    COPILOT_INSTRUCTIONS_PATH,
    PR_WORKFLOW_SOP_PATH,
    PR_COMMAND_BUNDLES_PATH,
    COPILOT_BUNDLE_PROMPTS_PATH,
    PR_REVIEW_AND_MERGE_GATES_PATH,
    PR_QA_GATES_PATH,
    REPO_CONSISTENCY_CONTRACT_PATH,
)
CANONICAL_BUNDLE_TYPES = (
    "docs",
    "test",
    "code",
    "release",
    "cleanup",
    "hotfix",
    "other",
)
LEGACY_BUNDLE_TYPES = {"governance", "checkpoint", "review-fix"}
CANONICAL_BUNDLE_TYPE_PATHS = (
    PR_TEMPLATE_PATH,
    PR_COMMAND_BUNDLES_PATH,
)


def _traceability_has_row(
    traceability_text: str,
    capability: str,
    code_path: str,
    test_path: str,
) -> bool:
    pattern = re.compile(
        rf"^\|\s*{re.escape(capability)}\s*\|\s*`{re.escape(code_path)}`\s*\|.*\|\s*`{re.escape(test_path)}`\s*\|\s*$",
        re.MULTILINE,
    )

    return pattern.search(traceability_text) is not None


def _read_repo_text(path: Path) -> str:
    assert path.is_file(), f"Missing required file: {path.relative_to(REPO_ROOT)}"
    return path.read_text(encoding="utf-8")


def _line_with_prefix(text: str, prefix: str) -> str:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith(prefix):
            return stripped

    raise AssertionError(f"Could not find line starting with: {prefix!r}")


def _bundle_types_from_line(line: str) -> tuple[str, ...]:
    values = line.split(":", 1)[1].strip().strip("_<>")
    return tuple(part.strip() for part in values.split("|"))


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


def test_traceability_includes_runtime_fabric_consistency_guards() -> None:
    traceability_text = TRACEABILITY_PATH.read_text(encoding="utf-8")

    assert _traceability_has_row(
        traceability_text,
        "Runtime fabric consistency guards",
        "src/shade_core/bundle.py",
        "tests/test_bundle.py",
    )


def test_traceability_includes_runtime_evaluation_guard_verification() -> None:
    traceability_text = TRACEABILITY_PATH.read_text(encoding="utf-8")

    assert _traceability_has_row(
        traceability_text,
        "Runtime evaluation guard verification",
        "src/shade_core/bundle.py",
        "tests/test_bundle.py",
    )


def test_traceability_includes_runtime_evaluation_fabric_serialization() -> None:
    traceability_text = TRACEABILITY_PATH.read_text(encoding="utf-8")

    assert _traceability_has_row(
        traceability_text,
        "Runtime evaluation fabric serialization",
        "src/shade_core/bundle.py",
        "tests/test_bundle.py",
    )


def test_traceability_includes_runtime_evaluation_verification_summary() -> None:
    traceability_text = TRACEABILITY_PATH.read_text(encoding="utf-8")

    assert _traceability_has_row(
        traceability_text,
        "Runtime evaluation verification summary",
        "src/shade_core/bundle.py",
        "tests/test_bundle.py",
    )


def test_traceability_includes_runtime_evaluation_verification_contract() -> None:
    traceability_text = TRACEABILITY_PATH.read_text(encoding="utf-8")

    assert _traceability_has_row(
        traceability_text,
        "Runtime evaluation verification contract",
        "src/shade_core/contract_gate.py",
        "tests/test_contract_gate.py",
    )


def test_traceability_row_match_does_not_require_trailing_whitespace() -> None:
    traceability_text = (
        "| Runtime fabric consistency guards | `src/shade_core/bundle.py` | "
        "Implemented as internal helpers validating prepared and serialized runtime/evaluation fabric invariants without changing snapshot output | `tests/test_bundle.py` |\n"
    )

    assert _traceability_has_row(
        traceability_text,
        "Runtime fabric consistency guards",
        "src/shade_core/bundle.py",
        "tests/test_bundle.py",
    )


def test_docs_index_files_exist() -> None:
    for path in INDEX_PATHS:
        assert path.is_file()


def test_pr_operations_playbook_files_exist() -> None:
    for path in PLAYBOOK_PATHS:
        assert path.is_file(), f"Missing required playbook file: {path.relative_to(REPO_ROOT)}"


def test_pr_template_uses_canonical_bundle_type_taxonomy() -> None:
    pr_template_text = _read_repo_text(PR_TEMPLATE_PATH)
    bundle_type_line = _line_with_prefix(pr_template_text, "- Bundle type:")

    assert bundle_type_line == (
        "- Bundle type: _" + " | ".join(CANONICAL_BUNDLE_TYPES) + "_"
    )


def test_canonical_bundle_type_lists_block_legacy_values() -> None:
    for path in CANONICAL_BUNDLE_TYPE_PATHS:
        bundle_type_line = _line_with_prefix(_read_repo_text(path), "- Bundle type:")
        bundle_types = _bundle_types_from_line(bundle_type_line)

        assert bundle_types == CANONICAL_BUNDLE_TYPES
        assert LEGACY_BUNDLE_TYPES.isdisjoint(bundle_types)


def test_pr_command_bundles_use_temp_pr_body_file_flow() -> None:
    command_bundle_text = _read_repo_text(PR_COMMAND_BUNDLES_PATH)

    assert r".\pr-body.md" not in command_bundle_text
    assert 'Join-Path $env:TEMP "shade-core-pr-body.md"' in command_bundle_text
    assert "Set-Content -Path $prBodyFile" in command_bundle_text
    assert "gh pr create --base main --title \"<title>\" --body-file $prBodyFile" in command_bundle_text
    assert "Remove-Item $prBodyFile -ErrorAction SilentlyContinue" in command_bundle_text


def test_pr_workflow_sop_contains_core_operating_controls() -> None:
    sop_text = _read_repo_text(PR_WORKFLOW_SOP_PATH)

    expected_tokens = (
        "2-4 related changes",
        "Use a micro-PR only when a listed exception applies",
        "Copilot review may assist, but AlphaAcces or the active operator keeps merge authority.",
        "## Validation gate",
        "## Post-merge cleanup",
    )

    for token in expected_tokens:
        assert token in sop_text


def test_repo_consistency_contract_contains_expected_sections() -> None:
    contract_text = _read_repo_text(REPO_CONSISTENCY_CONTRACT_PATH)

    expected_sections = (
        "## Protected workflow surface",
        "## What repo consistency tests protect",
        "## When to update tests",
        "## When not to update tests",
        "## Stop conditions",
        "## Relation to SOP and QA gates",
    )

    for section in expected_sections:
        assert section in contract_text


def test_repo_consistency_contract_names_enforced_workflow_docs() -> None:
    contract_text = _read_repo_text(REPO_CONSISTENCY_CONTRACT_PATH)

    expected_paths = (
        ".github/copilot-instructions.md",
        "docs/governance/pr-workflow-sop.md",
        "docs/governance/pr-command-bundles.md",
        "docs/governance/copilot-bundle-prompts.md",
        "docs/governance/pr-review-and-merge-gates.md",
        "docs/qa/pr-qa-gates.md",
    )

    for relative_path in expected_paths:
        assert relative_path in contract_text


def test_governance_index_links_to_pr_playbook_docs() -> None:
    governance_index_text = _read_repo_text(GOVERNANCE_INDEX_PATH)

    expected_links = (
        "[PR workflow SOP](pr-workflow-sop.md)",
        "[PR command bundles](pr-command-bundles.md)",
        "[Copilot bundle prompts](copilot-bundle-prompts.md)",
        "[PR review and merge gates](pr-review-and-merge-gates.md)",
        "[Repo consistency contract](../qa/repo-consistency-contract.md)",
    )

    for link in expected_links:
        assert link in governance_index_text


def test_qa_index_links_to_playbook_and_gate_docs() -> None:
    qa_index_text = _read_repo_text(QA_INDEX_PATH)

    expected_links = (
        "[PR workflow SOP](../governance/pr-workflow-sop.md)",
        "[test strategy](test-strategy.md)",
        "[PR QA gates](pr-qa-gates.md)",
        "[Repo consistency contract](repo-consistency-contract.md)",
    )

    for link in expected_links:
        assert link in qa_index_text


def test_qa_docs_link_to_repo_consistency_contract() -> None:
    expected_link = "[repo consistency contract](repo-consistency-contract.md)"

    assert expected_link in _read_repo_text(TEST_STRATEGY_PATH)
    assert expected_link in _read_repo_text(PR_QA_GATES_PATH)


def test_governance_docs_reference_repo_consistency_contract() -> None:
    assert (
        "[Repo consistency contract](../qa/repo-consistency-contract.md)"
        in _read_repo_text(PR_WORKFLOW_SOP_PATH)
    )
    assert (
        "[Repo consistency contract](../docs/qa/repo-consistency-contract.md)"
        in _read_repo_text(COPILOT_INSTRUCTIONS_PATH)
    )
