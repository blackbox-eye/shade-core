# shade-core

`shade-core` is a build, contract, and QA layer with a minimal Python core.

## Status

- The repository combines foundation documentation, governance, and a small inspectable Python package.
- The Python core currently implements contract models, run state, contract validation, a minimal runtime decision slice, evaluation, evaluation gating, serialization, and bundle output.
- The broader V1 architecture documents still describe target contracts and boundaries beyond the currently implemented runtime surface.
- The required `pr-baseline` check validates baseline files and runs `python -m pytest` after editable install.

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
- The root package exposes a curated stable surface for the current minimal core.
- Interfaces stay testable and inspectable.
