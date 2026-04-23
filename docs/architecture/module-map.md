# Module map

## Purpose

This document shows the foundation-level map of the repository documentation areas.

## Areas

- `docs/architecture/` provides a short system overview, contract boundaries, and current-vs-future clarification.
- `docs/governance/` collects governance rules with repo-policy as the authoritative source.
- `docs/onboarding/` covers local working mode in VS Code and PowerShell.
- `docs/qa/` covers local baseline, docs-to-code traceability, and later test direction.
- `docs/releases/` covers short release preparation in the repository.

## Package surface

- The stable public package surface is the root `shade_core` import path defined by `src/shade_core/__init__.py`.
- The remaining `src/shade_core/*.py` files are implementation modules behind that public surface.

## Boundaries

The map does not describe deploy, VPS, production, integration, or secrets.
