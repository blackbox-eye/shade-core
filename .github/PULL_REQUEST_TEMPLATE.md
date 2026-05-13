# Pull request

## Purpose

Describe briefly why the change is made.

## Scope

- What is included.
- What is intentionally out of scope.
- No deploy, VPS, secrets, production, or integration.

## Scope locks

- [ ] No source code changes unless this is a code PR.
- [ ] No workflow/CI changes unless explicitly scoped.
- [ ] No runtime behavior changes unless explicitly scoped.
- [ ] No adapters/providers/memory/deploy/VPS/integration unless explicitly scoped.

## Validation

- Command: `python -m pytest -q`
- Result: _fill in_

## Checklist

- [ ] The change has been reviewed locally in VS Code.
- [ ] Commits are signed.
- [ ] History is linear.
- [ ] The PR targets `main`.
- [ ] Required check `pr-baseline` is green.
- [ ] The `pr-baseline` workflow's baseline file checks have passed.
- [ ] The validation section is complete.
