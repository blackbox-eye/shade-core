# Pull request

Follow the [PR workflow SOP](../docs/governance/pr-workflow-sop.md) for bundle, validation, review, and cleanup rules.

## Purpose

Describe briefly why the change is made.

## Scope

- Bundle type: _docs | test | code | release | cleanup | hotfix | other_
- Required changes in this bundle: _fill in 2-4 related items_
- Included: _fill in_
- Out of scope: _fill in_
- Changed files or areas: _fill in_
- Micro-PR justification if applicable: _n/a_
- Bundle target: one cohesive PR with 2-4 related changes unless a valid micro-PR exception applies.

## Scope locks

- [ ] No source code changes unless this is a code PR.
- [ ] No workflow/CI changes unless explicitly scoped.
- [ ] No runtime behavior changes unless explicitly scoped.
- [ ] No dependency changes unless explicitly scoped.
- [ ] No adapters/providers/memory/deploy/VPS/integration unless explicitly scoped.

## Validation

- Command: `python -m pytest -q`
- Result: _fill in_

## Checklist

- [ ] The change has been reviewed locally in VS Code.
- [ ] Commits are signed.
- [ ] History is linear.
- [ ] The PR targets `main`.
- [ ] Bundle type, changed files or areas, and micro-PR justification are complete.
- [ ] The PR title and body match the locked scope.
- [ ] Required check `pr-baseline` is green.
- [ ] The `pr-baseline` workflow's baseline file checks have passed.
- [ ] The validation section is complete.
