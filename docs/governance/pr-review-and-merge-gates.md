# PR review and merge gates

## Purpose

- Define the operational stop/go gates around PR creation, review, CI, merge, and cleanup.
- Use this with [PR workflow SOP](pr-workflow-sop.md), [PR command bundles](pr-command-bundles.md), and [PR QA gates](../qa/pr-qa-gates.md).

## Before PR

- Scope is locked and the bundle stays at 2-4 related items unless a micro-PR exception is recorded.
- Diff is limited to the allowed files.
- The validation bundle has passed.
- When workflow docs, the PR template, or Copilot instructions change, the [repo consistency contract](../qa/repo-consistency-contract.md) stays aligned and `tests/test_repo_consistency.py` passes.
- The PR body fields are complete.
- Stop and ask ChatGPT/tovholder if the work drifted outside scope.

## After PR creation

- Confirm the base branch is `main`.
- Confirm the title and body match the locked scope.
- Confirm changed files and validation evidence are recorded.
- Request Copilot review in CLI or UI as available.
- Stop if the wrong base branch or incomplete body fields were used.

## Copilot review gate

- Keep Copilot review feedback inside the locked scope.
- Accept comments that improve the scoped bundle.
- Stop and ask ChatGPT/tovholder if Copilot pushes architecture, CI, deploy, integration, or dependency changes outside scope.

## Manual review gate

- Check bundle cohesion, diff shape, scope locks, and validation evidence.
- Resolve requested changes in one targeted follow-up bundle.
- Stop if review feedback expands the bundle into unrelated work.

## CI checks gate

- `pr-baseline` is green.
- No required check is failing.
- Stop if required checks are red, missing, or inconsistent with the local validation evidence.

## Merge decision gate

- AlphaAcces or the active operator keeps merge authority.
- Merge only when scope, reviews, and CI checks are clean.
- Do not merge with unresolved scope drift, missing validation, or unexplained extra commits.

## Post-merge cleanup gate

- Run the post-merge cleanup bundle.
- Confirm local `main` is current.
- Confirm the feature branch is removed locally when no longer needed.
- Stop if cleanup exposes stale local state or a new pytest failure.

## When to stop and ask ChatGPT/tovholder

- The task would land as a micro-PR without a listed exception.
- Scope, allowed files, or acceptance are unclear.
- Copilot or review feedback widens the task beyond the locked bundle.
- `python -m pytest -q` fails and the cause is not a clear local fix.
- Local `main` is not fast-forwardable.
- The PR body cannot honestly describe the bundle as one cohesive unit.