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

- Changes stay small, scoped, and reviewable.
- Pull requests should briefly describe purpose and scope.
- Branch protection must not be bypassed.
- `pr-baseline` verifies baseline files and runs `python -m pytest`.

## Scope boundaries

- The repository describes local working mode, foundation documentation, and a minimal Python core.
- Deploy is not part of this scope.
- VPS is not part of this scope.
- Secrets must not live in the repository.

## Supporting files

- `branch-protection.md` is a short practical supplement file to this policy.
- Other documents must not extend or change the rules in this file.
