# Copilot bundle prompts

## Purpose

- Reuse one PR-level prompt shape instead of issuing serial micro-tasks.
- Use these templates with [PR workflow SOP](pr-workflow-sop.md).
- Use [repo consistency contract](../qa/repo-consistency-contract.md) when a workflow bundle changes enforced playbook docs.

## Docs-only bundle

```text
Task: <docs bundle name>

Goal:
- <docs outcome>

Allowed files:
- docs/<path>
- .github/PULL_REQUEST_TEMPLATE.md
- .github/copilot-instructions.md

Required changes:
- <2-4 related doc changes>

Hard forbidden scope:
- No source code changes.
- No tests.
- No workflow/CI YAML changes.
- No dependencies.
- No runtime behavior.
- No adapters/providers/memory/deploy/VPS/integration work.

Acceptance criteria:
- Diff stays limited to the allowed files.
- Guidance stays concise and operational.
- Bundle is reviewable and not artificially small.

Validation commands:
- python -m pytest -q
- git diff --stat
- git diff -- <relevant-path>
- git status -sb
```

## Test-only bundle

```text
Task: <test bundle name>

Goal:
- <test outcome>

Allowed files:
- tests/<path>
- docs/qa/<path>

Required changes:
- <2-4 related test changes>

Hard forbidden scope:
- No source code changes unless explicitly scoped.
- No workflow/CI YAML changes.
- No dependencies.
- No deploy/VPS/integration changes.
- No unrelated docs cleanup.

Acceptance criteria:
- Diff stays limited to the allowed files.
- Test intent is clear from the PR body.
- Bundle remains test-scoped.

Validation commands:
- python -m pytest -q
- git diff --stat
- git diff -- tests/<path>
- git status -sb
```

## Code-contract bundle

```text
Task: <code contract bundle name>

Goal:
- <contract or behavior outcome>

Allowed files:
- src/<path>
- tests/<path>
- docs/<path>

Required changes:
- <2-4 related code or contract changes>

Hard forbidden scope:
- No workflow/CI YAML changes.
- No deploy/VPS/integration changes.
- No dependency changes unless explicitly scoped.
- No unrelated refactors.

Acceptance criteria:
- Diff stays limited to the allowed files.
- Contract or behavior change is stated in the PR body.
- Validation passes before commit.

Validation commands:
- python -m pytest -q
- git diff --stat
- git diff -- <relevant-path>
- git status -sb
```

## Workflow/governance bundle

```text
Task: <workflow bundle name>

Goal:
- <workflow or governance outcome>

Allowed files:
- docs/governance/<path>
- docs/onboarding/<path>
- docs/qa/<path>
- docs/releases/<path>
- .github/PULL_REQUEST_TEMPLATE.md
- .github/copilot-instructions.md

Required changes:
- <2-4 related workflow changes>

Hard forbidden scope:
- No source code changes.
- No tests.
- No workflow/CI YAML changes.
- No dependencies.
- No runtime behavior.
- No adapters/providers/memory/deploy/VPS/integration work.

Acceptance criteria:
- Diff stays limited to the allowed files.
- The workflow remains operational and non-essay-like.
- The bundle is a real PR-level unit, not a wording patch.
- The [repo consistency contract](../qa/repo-consistency-contract.md) stays aligned when enforced playbook docs change.

Validation commands:
- python -m pytest -q tests/test_repo_consistency.py
- python -m pytest -q
- git diff --stat
- git diff -- <relevant-path>
- git status -sb
```

## Checkpoint bundle

```text
Task: <checkpoint bundle name>

Goal:
- <checkpoint outcome>

Allowed files:
- docs/releases/<path>
- docs/qa/<path>

Required changes:
- <2-4 related checkpoint updates>

Hard forbidden scope:
- No source code changes.
- No tests.
- No workflow/CI YAML changes.
- No dependencies.
- No runtime behavior.
- No deploy/VPS/integration work.

Acceptance criteria:
- Checkpoint content matches completed work.
- Diff stays limited to the allowed files.
- Validation is recorded in the PR body.

Validation commands:
- python -m pytest -q
- git diff --stat
- git diff -- <relevant-path>
- git status -sb
```

## PR review fix bundle

```text
Task: <review fix bundle name>

Goal:
- Address the requested PR review fixes without widening scope.

Allowed files:
- <exact files tied to the review comments>

Required changes:
- <2-4 related review fixes>

Hard forbidden scope:
- No architecture changes.
- No workflow/CI YAML changes.
- No dependencies unless explicitly required by the review.
- No unrelated cleanup or opportunistic refactors.
- No scope widening beyond the cited review comments.

Acceptance criteria:
- Diff stays limited to the review-fix files.
- The PR body or follow-up comment cites the addressed review thread.
- Validation is rerun after the fixes.

Validation commands:
- python -m pytest -q
- git diff --stat
- git diff -- <relevant-path>
- git status -sb
```