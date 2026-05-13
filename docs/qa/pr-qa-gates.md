# PR QA gates

## Purpose

- Define the expected evidence and stop conditions for each common PR type.
- Use this with [PR workflow SOP](../governance/pr-workflow-sop.md) and [PR review and merge gates](../governance/pr-review-and-merge-gates.md).

## Docs PR

- Expected evidence: allowed files stay in docs or approved `.github` docs/template/instructions paths, `python -m pytest -q` passes, and the PR body records changed files and validation.
- Stop conditions: source code, tests, workflow YAML, or runtime behavior drift enters the diff; validation is missing; the PR is a micro change without justification.

## Test PR

- Expected evidence: diff stays test-scoped, `python -m pytest -q` passes, and the PR body states the test intent and changed files.
- Stop conditions: source files or runtime behavior drift enters the diff; validation fails; the test change cannot be explained as one cohesive bundle.

## Code PR

- Expected evidence: source and test changes stay inside the locked scope, `python -m pytest -q` passes, and the PR body states the contract or behavior touched.
- Stop conditions: the diff widens beyond the allowed files, behavior changes are undocumented, validation fails, or the bundle lacks supporting test evidence.

## Release PR

- Expected evidence: release-scoped docs match completed work, `python -m pytest -q` passes, and the PR body records scope, changed files, and validation.
- Stop conditions: release claims are not backed by completed work, the diff widens outside release scope, or required validation evidence is missing.

## Cleanup PR

- Expected evidence: diff stays tied to the cleanup or review-fix scope, `python -m pytest -q` passes again, and the PR body names the cleanup target or review thread when relevant.
- Stop conditions: the cleanup widens into unrelated work, validation is not rerun, or the follow-up introduces new unrelated changes.

## Hotfix PR

- Expected evidence: urgent fix scope is recorded, the diff stays tightly locked, `python -m pytest -q` passes, and any needed follow-up cleanup is noted.
- Stop conditions: the hotfix scope grows into normal feature work, validation is missing, or the urgency case is not stated.

## Other PR

- Expected evidence: the PR body explains why the bundle does not fit `docs`, `test`, `code`, `release`, `cleanup`, or `hotfix`, the diff stays inside the locked scope, and `python -m pytest -q` passes.
- Stop conditions: `other` is used to avoid naming a clear scope, validation is missing, or the bundle would be clearer as one of the standard bundle types.