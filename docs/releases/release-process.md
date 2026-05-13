# Release process

## Purpose

This file describes only the short repository part of release preparation.

## Working mode

- Gather release-relevant changes in a separate branch.
- Review changes locally in VS Code.
- Use PowerShell for commit and push.
- Follow [PR workflow SOP](../governance/pr-workflow-sop.md) for release bundle sizing, validation, review, merge, and cleanup.
- Use [PR command bundles](../governance/pr-command-bundles.md) for Git and PR steps and [PR review and merge gates](../governance/pr-review-and-merge-gates.md) before merge.
- Open a pull request with the template fields for release scope, changed files, validation, and micro-PR justification when used.

## Minimum before merge

- Baseline checks have been completed.
- `pr-baseline` is green.
- The change has been reviewed.
- The repository rules in repo-policy have been followed.
- Any micro-sized release PR is explicitly justified.

## Boundaries

This process does not cover deploy, VPS, production, integration, or secrets.
