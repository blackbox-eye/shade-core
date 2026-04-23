# Branch and PR rules

## Main

- `main` is protected.
- Direct push to `main` is not allowed.
- Merge to `main` happens only through pull request.

## Merge requirements

- Signed commits are required.
- History stays linear.
- Changes stay small and reviewable.
- Local review happens in VS Code before PR.
- Git workflow runs locally through PowerShell.
- The required `pr-baseline` check must pass.
- `pr-baseline` verifies baseline files and runs `python -m pytest`.

## PR flow

- Create a local branch.
- Commit with signing.
- Push the branch and open a pull request to `main`.
- Copilot may assist with text and drafts, but review and decision are manual.

## Not covered

- Deploy.
- VPS.
- Secrets.
