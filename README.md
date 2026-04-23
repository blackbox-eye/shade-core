# shade-core

`shade-core` is a build, contract, and QA layer with a minimal Python core.

## Status

- The repository combines foundation documentation, governance, and a small inspectable Python package.
- The Python core covers contract models, a minimal runtime decision slice, evaluation, and serialization.
- The build gate validates both baseline files and local pytest checks.

## Constraints

- No deploy.
- No VPS.
- No secrets.
- No production or integration.

## Working mode

- `main` is protected.
- Merge to `main` happens only through pull request.
- Signed commits are required.
- History stays linear.
- Work locally in VS Code and PowerShell.
- Copilot is used as an assistant, not an authority.

## Python core

- The package name is `shade_core`.
- The core is intentionally small and has no IO, persistence, or networking.
- Interfaces stay testable and inspectable.
