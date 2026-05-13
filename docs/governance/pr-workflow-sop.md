# PR workflow SOP

## Purpose

- Define the production-mode PR operating model for AlphaAcces, ChatGPT/tovholder, and Copilot.
- Keep scope, prompts, command bundles, validation, review, and cleanup rules in one document.

## Companion docs

- [PR command bundles](pr-command-bundles.md) owns the copy/paste PowerShell command sets.
- [Copilot bundle prompts](copilot-bundle-prompts.md) owns reusable PR-level prompt templates.
- [PR review and merge gates](pr-review-and-merge-gates.md) owns the stop/go review flow.
- [PR QA gates](../qa/pr-qa-gates.md) owns PR-type evidence and stop conditions.

## Production-mode communication standard

- Start each bundle with goal, allowed files, required changes, hard forbidden scope, and acceptance.
- Keep prompts and status updates short, operational, and PR-oriented.
- Ask for one reviewable bundle, not serial micro-tasks, unless a listed micro-PR exception applies.
- End implementation handoffs with explicit changed files and explicit validation results.

## Roles and responsibilities

- AlphaAcces or the active operator: locks scope, owns allowed files, accepts the bundle, and keeps merge authority.
- ChatGPT/tovholder: shapes the bundle, restates hard locks, rejects drift, and escalates inefficient micro-task flow.
- Copilot: implements the scoped bundle, drafts PR text when asked, reports changed files and validation, and does not decide architecture or merge.

## Standard PR-level workflow

1. Lock scope before implementation.
2. Build one cohesive 2-4 item bundle and create one feature branch.
3. Choose the relevant prompt template, command bundle, review gate, and QA gate.
4. Give Copilot the allowed files, required changes, hard forbidden scope, and acceptance.
5. Implement only the locked bundle.
6. Run the validation bundle before commit.
7. Commit with signing.
8. Push and create the PR with the required body fields.
9. Request Copilot/manual review and wait for green checks.
10. Merge only when scope, checks, and review are clean.
11. Run the post-merge cleanup bundle.

## PR-level bundle sizing

- Prefer bundles with 2-4 related changes.
- Keep bundles cohesive and easy to review.
- Do not enlarge a bundle with unrelated work.
- Do not split a normal bundle into multiple micro-PRs.
- Use a micro-PR only when a listed exception applies and the PR body states why.

## Standard command bundles

- Use [PR command bundles](pr-command-bundles.md) as the default command source.
- Run the pre-implementation state gate before starting a fresh branch.
- Run the validation gate before commit.
- Use the commit gate before signing.
- Use the push and PR creation bundle with a body file.
- Run the post-merge sync and cleanup bundle after merge.
- Use the failed-test stop gate and stale-main recovery flow when needed.

## Larger Copilot prompt pattern

- Use [Copilot bundle prompts](copilot-bundle-prompts.md) when the bundle is larger than a wording edit or when drift risk is high.
- Keep the prompt shaped as goal, allowed files, required changes, hard forbidden scope, acceptance criteria, and validation commands.

## Validation gate

- Run the validation bundle before commit.
- Do not commit while `python -m pytest -q` fails.
- Do not commit while the diff has drifted outside the locked scope.
- Do not commit while `git status -sb` shows unrelated changes.
- Use [PR QA gates](../qa/pr-qa-gates.md) to match the evidence to the PR type.

## PR body requirements

- Use the PR template.
- State the purpose.
- State the bundle type.
- State the required changes in the bundle.
- State included scope and out-of-scope items.
- List changed files or areas.
- Record micro-PR justification when used.
- Record validation results.

## Reviewer, CI, and merge rules

- Use [PR review and merge gates](pr-review-and-merge-gates.md) as the detailed stop/go checklist.
- `pr-baseline` must be green.
- Copilot review may assist, but AlphaAcces or the active operator keeps merge authority.
- Manual review remains required before merge.
- Do not merge with scope drift, missing validation, or failing checks.

## Post-merge cleanup

- Run the post-merge cleanup bundle after merge.
- Confirm that local `main` is current and the deleted branch is no longer needed.

## When micro-PRs are allowed

- Safety work.
- Blocker removal.
- Auth-scoped fixes.
- Cleanup that should stay isolated.
- Hotfix work.

## Escalation rules

- If the requested change would produce a micro-PR without a listed exception, stop and rebundle to a 2-4 item PR.
- If repeated prompts keep touching the same area in tiny steps, roll them into one larger bundle before more implementation.
- If scope, allowed files, or acceptance are unclear, restate and relock before editing.
- If Copilot proposes architecture, workflow, CI, runtime, deploy, integration, or dependency work outside scope, reject it and relock.
- If review, CI, or local validation changes the task shape materially, stop and ask ChatGPT/tovholder before widening the bundle.

## Hard forbidden scope

- No source code changes unless this is a code PR.
- No workflow or CI changes unless explicitly scoped.
- No runtime behavior changes unless explicitly scoped.
- No dependency changes unless explicitly scoped.
- No adapters, providers, memory, deploy, VPS, or integration work unless explicitly scoped.
