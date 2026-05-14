# Test strategy

## Purpose

This file covers only local repo baseline, PR baseline, and later test direction.

## Current baseline

- Local changes are reviewed in VS Code.
- Scope is locked before implementation and kept within the intended bundle.
- Simple repository and file checks can be run locally in PowerShell.
- The current pytest suite covers the implemented minimal Python core.
- The current pytest suite also includes deterministic repo consistency coverage for stable workflow and documented path drift.
- Pull request is the fixed quality gate before merge.
- The `pr-baseline` workflow verifies baseline files and runs `python -m pytest`.

The operating sequence for validation and cleanup lives in [PR workflow SOP](../governance/pr-workflow-sop.md).
The enforced workflow invariants live in [repo consistency contract](repo-consistency-contract.md).

## Standard validation gate

- Run the SOP validation gate before commit.
- The standard local gate stays `git diff --stat`, relevant `git diff`, `python -m pytest -q`, and `git status -sb`.
- Record validation results and changed files in the PR body.
- Use [PR QA gates](pr-qa-gates.md) for PR-type evidence and stop conditions.
- When workflow docs, the PR template, or Copilot instructions change, keep `tests/test_repo_consistency.py` green against the [repo consistency contract](repo-consistency-contract.md).

## Before pull request

- Content has been read through locally.
- The branch is dedicated to one cohesive bundle.
- Preferred bundle size is 2-4 related changes.
- Single-file micro PRs are reserved for safety, blocker, auth, cleanup, or hotfix work.
- Baseline checks have been completed before commit.
- PR checks, Copilot review when requested, and manual review complete before merge.

## Post-merge cleanup gate

- Run the SOP cleanup gate after merge.

## Later direction

- Test coverage can expand as code and modules grow.
- New tests must follow the repository's simple foundation frame.
- Docs-to-code alignment is tracked in `docs/qa/docs-to-code-traceability.md`.

## Boundaries

This strategy does not cover deploy, VPS, production, or integration.
