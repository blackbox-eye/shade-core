# Repo consistency contract

## Purpose

- Define what the repository consistency tests protect for the PR operations playbook.
- Keep the workflow model enforced as a repo-local contract, not docs-only guidance.

## Protected workflow surface

- `.github/PULL_REQUEST_TEMPLATE.md`
- `.github/copilot-instructions.md`
- `docs/governance/pr-workflow-sop.md`
- `docs/governance/pr-command-bundles.md`
- `docs/governance/copilot-bundle-prompts.md`
- `docs/governance/pr-review-and-merge-gates.md`
- `docs/qa/pr-qa-gates.md`
- `docs/qa/README.md`
- `docs/qa/test-strategy.md`

## What repo consistency tests protect

- Required playbook docs and instructions stay present.
- The canonical PR bundle taxonomy stays `docs`, `test`, `code`, `release`, `cleanup`, `hotfix`, `other`.
- PR body examples use a temp-file flow instead of writing `pr-body.md` in the repo root.
- The PR workflow SOP keeps 2-4 item bundle guidance, micro-PR exceptions, validation, Copilot non-merge authority, and post-merge cleanup.
- Governance and QA indexes keep linking to the enforced playbook docs.

## Worker orchestration contract-prep enforcement

- `tests/test_repo_consistency.py` keeps docs-to-code traceability explicit for the internal worker-orchestration plan, step, handoff, status, summary, review, validation, serialization, and prep-snapshot rows.
- The same test file enforces that worker-orchestration contract-prep additions must not widen `src/shade_core/__init__.py`.
- The same test file also protects non-runtime wording in the current architecture docs so this seam stays documented as contract-prep and preparation boundaries only.

## Manifest chain verification enforcement

- `tests/test_repo_consistency.py` keeps docs-to-code traceability explicit for the Manifest chain verification row (`src/shade_core/contract_gate.py`) and the Manifest verification snapshot row (`src/shade_core/bundle.py`).
- `validate_orchestration_manifest_chain` and `_build_manifest_verification_snapshot` are internal contract-prep symbols only; they must not be exported via `src/shade_core/__init__.py`.
- This enforcement is restricted to internal contract-prep cross-reference verification; it does not extend to runtime, integration, or deployment scope.

## Publication release-view consistency enforcement

- `tests/test_repo_consistency.py` keeps docs-to-code traceability explicit for the Publication release-view consistency row (`src/shade_core/contract_gate.py`) and the Publication release-view consistency snapshot row (`src/shade_core/bundle.py`).
- `validate_orchestration_publication_release_view_consistency` and `_build_publication_release_view_consistency_snapshot` are internal contract-prep symbols only; they must not be exported via `src/shade_core/__init__.py`.
- This enforcement is restricted to internal contract-prep verification of the release-view boundary; it does not extend to runtime, integration, or deployment scope.

## Unified orchestration contract snapshot enforcement

- `tests/test_repo_consistency.py` keeps docs-to-code traceability explicit for the Unified orchestration contract snapshot row (`src/shade_core/bundle.py`).
- `tests/test_bundle.py` keeps deterministic key order and controlled fragment composition explicit for `_build_unified_orchestration_contract_snapshot`.
- `_build_unified_orchestration_contract_snapshot` is internal contract-prep only and must not widen `src/shade_core/__init__.py`.
- The same test surface keeps `publication_release_view_consistency` and `manifest_chain_verification` aligned with their dedicated helper payloads while publication and release-view serialization stays controlled through `_build_publication_release_view_snapshot`.
- This enforcement is limited to internal contract-prep composition only; it does not implement runtime, routing, worker execution, adapters, memory, deploy, VPS, production integration, or release behavior.

## When to update tests

- A playbook rule changes intentionally in the same locked governance or QA bundle.
- A new enforced workflow doc becomes required.
- The canonical bundle taxonomy changes intentionally.
- The temp-file PR body rule changes intentionally.

## When not to update tests

- To silence drift in workflow docs that was not intentionally approved.
- To re-allow micro-task patterns as the default operating mode.
- To reintroduce repo-root `pr-body.md` guidance.
- To rename canonical bundle types ad hoc.

## Stop conditions

- Workflow docs, the PR template, or Copilot instructions change without keeping `tests/test_repo_consistency.py` green.
- A playbook edit would weaken the canonical taxonomy, validation gate, or merge-authority rules.
- Governance or QA indexes drop required links to the playbook or QA gate docs.
- The PR cannot explain why a repo consistency invariant changed.

## Relation to SOP and QA gates

- [PR workflow SOP](../governance/pr-workflow-sop.md) defines the operating model.
- [PR QA gates](pr-qa-gates.md) defines evidence and stop conditions by PR type.
- `tests/test_repo_consistency.py` enforces the stable repo-level invariants from those docs.
