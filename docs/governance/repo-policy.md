# Repo policy

## Purpose

This file is the repository's authoritative governance foundation for work in `shade-core`.

## Governance rules

- `main` is protected.
- Direct push to `main` is not allowed.
- Changes enter through pull request.
- History stays linear.
- Commits must be signed.
- The required repository check is `pr-baseline`.

## Working mode

- Changes stay scoped, reviewable, and normally bundled as 2-4 related items.
- Pull requests must describe purpose, bundle type, scope, changed files or areas, and validation.
- Branch protection must not be bypassed.
- `pr-baseline` verifies baseline files and runs `python -m pytest`.

The operating model for AlphaAcces, ChatGPT/tovholder, and Copilot lives in [PR workflow SOP](pr-workflow-sop.md), [PR command bundles](pr-command-bundles.md), and [PR review and merge gates](pr-review-and-merge-gates.md).

## Scope boundaries

- The repository describes local working mode, foundation documentation, and a minimal Python core.
- Deploy is not part of this scope.
- VPS is not part of this scope.
- Secrets must not live in the repository.

## Supporting files

- [PR workflow SOP](pr-workflow-sop.md) is the operational supplement for bundle flow, review, and cleanup.
- [PR command bundles](pr-command-bundles.md) is the operational supplement for repeatable PowerShell command sets.
- [Copilot bundle prompts](copilot-bundle-prompts.md) is the operational supplement for PR-level Copilot prompts.
- [PR review and merge gates](pr-review-and-merge-gates.md) is the operational supplement for stop/go review decisions.
- [Branch and PR rules](branch-pr-rules.md) is a short practical supplement to this policy.
- [Copilot instructions](../../.github/copilot-instructions.md) applies the same operating model to Copilot execution.
- Supporting documents may specify procedure, but they must not weaken this policy.
