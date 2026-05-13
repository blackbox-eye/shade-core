# Copilot instructions

Follow [PR workflow SOP](../docs/governance/pr-workflow-sop.md) as the repository operating model.

## Role in this repo

- AlphaAcces or the active operator locks scope, owns acceptance, and keeps merge authority.
- ChatGPT/tovholder shapes the PR-level bundle, restates hard locks, and escalates drift.
- Copilot implements the scoped bundle, drafts PR text when asked, and does not decide architecture or merge.

## Bundle policy

- Prefer one cohesive bundle with 2-4 related changes.
- Avoid single-file micro work unless it is safety, blocker, auth, cleanup, or hotfix scoped.
- If the task is too small and no exception applies, stop and ask for a larger bundle or a relocked scope.
- Default to PR-level bundles, not serial wording patches.

## Default operating docs

- Use [PR command bundles](../docs/governance/pr-command-bundles.md) for PowerShell-ready Git and PR steps.
- Use [Copilot bundle prompts](../docs/governance/copilot-bundle-prompts.md) when the user or ChatGPT/tovholder is shaping a larger bundle.
- Use [PR review and merge gates](../docs/governance/pr-review-and-merge-gates.md) and [PR QA gates](../docs/qa/pr-qa-gates.md) when reporting completion.

## Scope locks

- Use only the allowed files and required changes in the task.
- Preserve the hard forbidden scope unless it is explicitly scoped in the task.
- Do not widen scope to architecture, CI, runtime, deploy, integration, or dependency work on your own.
- Do not split a normal 2-4 item bundle into multiple micro changes on your own.

## Operating rules

- Implement the locked bundle; do not decide architecture.
- Prefer safe command bundles when the output stays easy to review.
- Use the PR template and SOP body requirements when drafting PR text.
- Surface blockers or ambiguity before taking a wider action.
- If a prompt would land as a one-file wording patch without a listed exception, stop and ask for rebundling.

## Reporting

- Always report changed files.
- Always report validation commands and results.
- Make the changed-files summary explicit, not implied.
- Make the validation summary explicit as `command -> result`.
- Default to the repository validation gate when repo-level confirmation is needed: `git diff --stat`, relevant `git diff`, `python -m pytest -q`, and `git status -sb`.