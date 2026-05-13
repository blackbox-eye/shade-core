# Branch and PR rules

## Main

- `main` is protected.
- Direct push to `main` is not allowed.
- Merge to `main` happens only through pull request.
- The detailed operating flow lives in [PR workflow SOP](pr-workflow-sop.md).

## Merge requirements

- Signed commits are required.
- History stays linear.
- Changes stay reviewable and cohesive.
- Local review happens in VS Code before PR.
- Git workflow runs locally through PowerShell under the SOP, command bundle, review gate, and QA gate documents.
- The required `pr-baseline` check must pass.
- `pr-baseline` verifies baseline files and runs `python -m pytest`.
- PR bodies use the template fields for bundle type, scope, changed files, and validation.

## Bundle guidance

- Prefer larger reviewable bundles with 2-4 related changes.
- Avoid single-file micro PRs unless the work is safety, blocker, auth, cleanup, or hotfix scoped.
- Keep bundles cohesive; do not group unrelated work just to make a larger PR.

## PR flow

1. Lock scope before implementation.
2. Create one local branch per bundle.
3. Run the SOP validation gate before commit.
4. Commit with signing.
5. Push the branch and open a pull request to `main` with the required body fields.
6. Request Copilot review in CLI or UI as available and wait for required checks.
7. Merge only after required checks and Copilot/manual review pass.
8. Run the SOP post-merge cleanup gate.

Copilot is a reviewer and drafting assistant, not merge authority. Use [PR workflow SOP](pr-workflow-sop.md), [PR review and merge gates](pr-review-and-merge-gates.md), and [Copilot instructions](../../.github/copilot-instructions.md) for the full operating sequence.

## Not covered

- Deploy.
- VPS.
- Secrets.
