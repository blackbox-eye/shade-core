from __future__ import annotations

import ast
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
CURRENT_RUNTIME_SLICE_PATH = (
    REPO_ROOT / "docs" / "architecture" / "current-runtime-slice.md"
)
SYSTEM_OVERVIEW_PATH = REPO_ROOT / "docs" / "architecture" / "system-overview.md"
ROOT_PACKAGE_INIT_PATH = REPO_ROOT / "src" / "shade_core" / "__init__.py"
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
WORKER_ORCHESTRATION_CONTRACT_TRACEABILITY_ROWS = (
    (
        "Worker orchestration plan contract",
        "src/shade_core/models.py",
        "tests/test_models.py",
    ),
    (
        "Worker orchestration step contract",
        "src/shade_core/models.py",
        "tests/test_models.py",
    ),
    (
        "Worker orchestration handoff contract",
        "src/shade_core/models.py",
        "tests/test_models.py",
    ),
    (
        "Worker orchestration status contract",
        "src/shade_core/models.py",
        "tests/test_models.py",
    ),
    (
        "Worker orchestration summary contract",
        "src/shade_core/models.py",
        "tests/test_models.py",
    ),
    (
        "Worker orchestration review contract",
        "src/shade_core/models.py",
        "tests/test_models.py",
    ),
)
WORKER_ORCHESTRATION_VALIDATION_TRACEABILITY_ROWS = (
    (
        "Worker orchestration plan validation",
        "src/shade_core/contract_gate.py",
        "tests/test_contract_gate.py",
    ),
    (
        "Worker orchestration step validation",
        "src/shade_core/contract_gate.py",
        "tests/test_contract_gate.py",
    ),
    (
        "Worker orchestration handoff validation",
        "src/shade_core/contract_gate.py",
        "tests/test_contract_gate.py",
    ),
    (
        "Worker orchestration status validation",
        "src/shade_core/contract_gate.py",
        "tests/test_contract_gate.py",
    ),
    (
        "Worker orchestration summary validation",
        "src/shade_core/contract_gate.py",
        "tests/test_contract_gate.py",
    ),
    (
        "Worker orchestration review validation",
        "src/shade_core/contract_gate.py",
        "tests/test_contract_gate.py",
    ),
)
WORKER_ORCHESTRATION_SERIALIZATION_TRACEABILITY_ROWS = (
    (
        "Worker orchestration plan serialization",
        "src/shade_core/serialization.py",
        "tests/test_serialization.py",
    ),
    (
        "Worker orchestration step serialization",
        "src/shade_core/serialization.py",
        "tests/test_serialization.py",
    ),
    (
        "Worker orchestration handoff serialization",
        "src/shade_core/serialization.py",
        "tests/test_serialization.py",
    ),
    (
        "Worker orchestration status serialization",
        "src/shade_core/serialization.py",
        "tests/test_serialization.py",
    ),
    (
        "Worker orchestration summary serialization",
        "src/shade_core/serialization.py",
        "tests/test_serialization.py",
    ),
    (
        "Worker orchestration review serialization",
        "src/shade_core/serialization.py",
        "tests/test_serialization.py",
    ),
)
WORKER_ORCHESTRATION_ROOT_API_NAMES = (
    "WorkerOrchestrationPlan",
    "WorkerOrchestrationStep",
    "WorkerOrchestrationHandoff",
    "WorkerOrchestrationStatus",
    "WorkerOrchestrationSummary",
    "WorkerOrchestrationReview",
)
MANIFEST_CHAIN_VERIFICATION_TRACEABILITY_ROW = (
    "Manifest chain verification",
    "src/shade_core/contract_gate.py",
    "tests/test_contract_gate.py",
)
MANIFEST_VERIFICATION_SNAPSHOT_TRACEABILITY_ROW = (
    "Manifest verification snapshot",
    "src/shade_core/bundle.py",
    "tests/test_bundle.py",
)
EXPECTED_ROOT_PACKAGE_INIT_TEXT = '''"""Minimal package for shade-core."""

from .bundle import build_bundle
from .contract_gate import ContractGateResult, validate_state_contract
from .evaluation import evaluate
from .evaluation_gate import EvaluationGateResult, run_evaluation_gate
from .models import (
    ConfidenceRecord,
    MetaAuditEvent,
    RuntimeDecision,
    SelfModel,
    WorkerRegistry,
)
from .runtime_loop import audit_decision, decide
from .serialization import (
    serialize_evaluation_result,
    serialize_meta_audit_event,
    serialize_runtime_decision,
)
from .state import RunState

__all__ = [
    "__version__",
    "ContractGateResult",
    "ConfidenceRecord",
    "EvaluationGateResult",
    "MetaAuditEvent",
    "RunState",
    "RuntimeDecision",
    "SelfModel",
    "WorkerRegistry",
    "build_bundle",
    "evaluate",
    "run_evaluation_gate",
    "audit_decision",
    "decide",
    "serialize_evaluation_result",
    "serialize_meta_audit_event",
    "serialize_runtime_decision",
    "validate_state_contract",
]

__version__ = "0.1.0"
'''


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


def _normalized_repo_text(path: Path) -> str:
    return _read_repo_text(path).replace("\r\n", "\n").strip()


def _line_with_prefix(text: str, prefix: str) -> str:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith(prefix):
            return stripped

    raise AssertionError(f"Could not find line starting with: {prefix!r}")


def _bundle_types_from_line(line: str) -> tuple[str, ...]:
    values = line.split(":", 1)[1].strip().strip("_<>")
    return tuple(part.strip() for part in values.split("|"))


def _module_all_exports(path: Path) -> tuple[str, ...]:
    module = ast.parse(_read_repo_text(path))
    all_assignments: list[ast.Assign] = []

    for node in module.body:
        if not isinstance(node, ast.Assign):
            continue

        for target in node.targets:
            if isinstance(target, ast.Name) and target.id == "__all__":
                all_assignments.append(node)
                break

    relative_path = path.relative_to(REPO_ROOT)
    assert len(all_assignments) == 1, (
        f"Expected exactly one top-level __all__ assignment in {relative_path}, "
        f"found {len(all_assignments)}"
    )

    value = ast.literal_eval(all_assignments[0].value)
    assert isinstance(value, list)
    assert all(isinstance(item, str) for item in value)
    return tuple(value)


def _assert_traceability_rows_present(
    traceability_text: str,
    rows: tuple[tuple[str, str, str], ...],
) -> None:
    for capability, code_path, test_path in rows:
        assert _traceability_has_row(
            traceability_text,
            capability,
            code_path,
            test_path,
        ), f"Missing traceability row for {capability!r}"


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


def test_traceability_includes_worker_orchestration_contract_rows() -> None:
    traceability_text = _read_repo_text(TRACEABILITY_PATH)

    _assert_traceability_rows_present(
        traceability_text,
        WORKER_ORCHESTRATION_CONTRACT_TRACEABILITY_ROWS,
    )


def test_traceability_includes_worker_orchestration_validation_rows() -> None:
    traceability_text = _read_repo_text(TRACEABILITY_PATH)

    _assert_traceability_rows_present(
        traceability_text,
        WORKER_ORCHESTRATION_VALIDATION_TRACEABILITY_ROWS,
    )


def test_traceability_includes_worker_orchestration_serialization_rows() -> None:
    traceability_text = _read_repo_text(TRACEABILITY_PATH)

    _assert_traceability_rows_present(
        traceability_text,
        WORKER_ORCHESTRATION_SERIALIZATION_TRACEABILITY_ROWS,
    )


def test_traceability_includes_worker_orchestration_prep_snapshot_row() -> None:
    traceability_text = _read_repo_text(TRACEABILITY_PATH)

    assert _traceability_has_row(
        traceability_text,
        "Worker orchestration prep snapshot",
        "src/shade_core/bundle.py",
        "tests/test_bundle.py",
    )


def test_root_package_keeps_worker_orchestration_symbols_out_of_public_api() -> None:
    root_exports = _module_all_exports(ROOT_PACKAGE_INIT_PATH)

    for name in WORKER_ORCHESTRATION_ROOT_API_NAMES:
        assert name not in root_exports


def test_root_package_init_file_matches_locked_public_api_surface() -> None:
    assert _normalized_repo_text(ROOT_PACKAGE_INIT_PATH) == (
        EXPECTED_ROOT_PACKAGE_INIT_TEXT.strip()
    )


def test_worker_orchestration_architecture_docs_use_contract_prep_wording() -> None:
    current_runtime_slice_text = _read_repo_text(CURRENT_RUNTIME_SLICE_PATH)
    system_overview_text = _read_repo_text(SYSTEM_OVERVIEW_PATH)

    assert "contract-prep" in current_runtime_slice_text
    assert "preparation boundaries" in system_overview_text
    assert "Worker orchestration behavior." in current_runtime_slice_text
    assert "typed preparation boundaries only" in system_overview_text


def test_worker_orchestration_architecture_docs_keep_runtime_and_integration_out_of_scope() -> None:
    current_runtime_slice_text = _read_repo_text(CURRENT_RUNTIME_SLICE_PATH)
    system_overview_text = _read_repo_text(SYSTEM_OVERVIEW_PATH)

    expected_current_runtime_tokens = (
        "do not execute worker selection, worker steps, routing, transitions, closure, publication, or release behavior.",
        "- Adapter or provider implementations.",
        "- Memory layer behavior.",
        "- Deploy or VPS behavior.",
        "- Production integration.",
    )
    expected_system_overview_tokens = (
        "do not implement planning, worker execution, routing, or runtime orchestration behavior.",
        "It does not describe deploy, VPS, production, or integration.",
        "It does not implement adapters, provider bindings, or runtime wiring for that handoff boundary.",
    )

    for token in expected_current_runtime_tokens:
        assert token in current_runtime_slice_text

    for token in expected_system_overview_tokens:
        assert token in system_overview_text


def test_repo_consistency_contract_describes_worker_orchestration_contract_prep_enforcement() -> None:
    contract_text = _read_repo_text(REPO_CONSISTENCY_CONTRACT_PATH)

    assert "## Worker orchestration contract-prep enforcement" in contract_text
    expected_tokens = (
        "docs-to-code traceability",
        "must not widen `src/shade_core/__init__.py`",
        "non-runtime wording",
    )

    for token in expected_tokens:
        assert token in contract_text


def test_traceability_includes_manifest_chain_verification_row() -> None:
    traceability_text = _read_repo_text(TRACEABILITY_PATH)

    assert _traceability_has_row(
        traceability_text,
        *MANIFEST_CHAIN_VERIFICATION_TRACEABILITY_ROW,
    )


def test_traceability_includes_manifest_verification_snapshot_row() -> None:
    traceability_text = _read_repo_text(TRACEABILITY_PATH)

    assert _traceability_has_row(
        traceability_text,
        *MANIFEST_VERIFICATION_SNAPSHOT_TRACEABILITY_ROW,
    )


def test_repo_consistency_contract_describes_manifest_chain_verification_enforcement() -> None:
    contract_text = _read_repo_text(REPO_CONSISTENCY_CONTRACT_PATH)

    assert "## Manifest chain verification enforcement" in contract_text
    expected_tokens = (
        "docs-to-code traceability",
        "Manifest chain verification",
        "Manifest verification snapshot",
        "validate_orchestration_manifest_chain",
        "_build_manifest_verification_snapshot",
        "must not be exported via `src/shade_core/__init__.py`",
        "runtime",
        "integration",
        "deployment",
    )

    for token in expected_tokens:
        assert token in contract_text
