# Governance

This folder describes the repository working rules and change control.

## Focus

- Rules for review, merge, and history.
- Requirements for traceability and collaboration.
- No deploy-, VPS-, or secrets-related documentation.

## Working frame

- `main` is protected.
- Merge to `main` happens only through pull request.
- Commits must be signed.
- History stays linear.
- Local work happens in VS Code and PowerShell.

## Key documents

- [Repo policy](repo-policy.md) is the authoritative governance base.
- [PR workflow SOP](pr-workflow-sop.md) is the operating model for bundle scope, validation, review, merge, and cleanup.
- [PR command bundles](pr-command-bundles.md) keeps the PowerShell-ready Git and PR commands.
- [Copilot bundle prompts](copilot-bundle-prompts.md) keeps reusable PR-level prompt templates.
- [PR review and merge gates](pr-review-and-merge-gates.md) keeps the stop/go review and merge gates.
- [Branch and PR rules](branch-pr-rules.md) keeps the short branch and merge policy.
- [Copilot instructions](../../.github/copilot-instructions.md) keeps Copilot execution inside the same operating model.
