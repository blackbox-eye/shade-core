# shade-core

`shade-core` is a build, contract, and QA layer with a minimal Python core.

## Status

- The repository combines foundation documentation, governance, and a small inspectable Python package.
- The Python core currently implements contract models, run state, contract validation, a minimal runtime decision slice, evaluation, evaluation gating, serialization, bundle output, and one internal runtime-fabric snapshot path.
- The broader V1 architecture documents still describe target contracts and boundaries beyond the currently implemented runtime surface.
- The required `pr-baseline` check validates baseline files and runs `python -m pytest` after editable install.
- The existing pytest path also includes one narrow repo consistency check for baseline workflow tokens, documented code and test paths, and core docs index files.
- Six foundation build bundles have been completed and merged to `main`; `main` passes the baseline `python -m pytest` check.
- The first completed post-foundation 3-bundle cycle has been merged to `main`.

## Checkpoint

The completed foundation bundle set is recorded in `docs/releases/checkpoint-foundation-bundles.md`.

The first completed post-foundation 3-bundle cycle is recorded in `docs/releases/checkpoint-post-foundation-cycle-1.md`.

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
- The stable public package surface is the root `shade_core` import path.
- Internal modules under `src/shade_core/` implement that path and are not separately described here as stable package entrypoints.
- Interfaces stay testable and inspectable.
