# PR QA gates

## Purpose

- Define the expected evidence and stop conditions for each common PR type.
- Use this with [PR workflow SOP](../governance/pr-workflow-sop.md) and [PR review and merge gates](../governance/pr-review-and-merge-gates.md).

## Docs-only PR

- Expected evidence: allowed files stay in docs or approved `.github` docs/template/instructions paths, `python -m pytest -q` passes, and the PR body records changed files and validation.
- Stop conditions: source code, tests, workflow YAML, or runtime behavior drift enters the diff; validation is missing; the PR is a micro change without justification.

## Test-only PR

- Expected evidence: diff stays test-scoped, `python -m pytest -q` passes, and the PR body states the test intent and changed files.
- Stop conditions: source files or runtime behavior drift enters the diff; validation fails; the test change cannot be explained as one cohesive bundle.

## Code PR

- Expected evidence: source and test changes stay inside the locked scope, `python -m pytest -q` passes, and the PR body states the contract or behavior touched.
- Stop conditions: the diff widens beyond the allowed files, behavior changes are undocumented, validation fails, or the bundle lacks supporting test evidence.

## Governance PR

- Expected evidence: diff stays in governance/onboarding/QA/release docs and approved `.github` docs/template/instructions paths, `python -m pytest -q` passes, and the PR body records bundle type, changed files, and validation.
- Stop conditions: workflow YAML, source code, tests, dependencies, or runtime behavior appear in the diff; the guidance becomes essay-like; the bundle is only a wording patch.

## Checkpoint PR

- Expected evidence: checkpoint or release docs match completed work, `python -m pytest -q` passes, and the PR body records scope and validation.
- Stop conditions: checkpoint claims are not backed by completed work, the diff widens outside the checkpoint scope, or required validation evidence is missing.

## Review-fix PR

- Expected evidence: diff stays tied to the cited review comments, `python -m pytest -q` passes again, and the PR body or review reply names the addressed review thread.
- Stop conditions: the fix bundle widens beyond the review comments, validation is not rerun, or the follow-up introduces new unrelated changes.