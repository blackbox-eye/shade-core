# System overview

## Purpose

`shade-core` collects foundation documentation for architecture, governance, and local working mode.

## System frame

- `src/shade_core/` currently implements a minimal core of contract, gate, evaluation, serialization, and bundle primitives.
- `src/shade_core/__init__.py` defines the stable root package API for that current minimal core.
- The remaining `src/shade_core/*.py` files are internal implementation modules behind the root package surface.
- `docs/architecture/` describes foundation structure, current boundaries, and documented V1 target contracts.
- `docs/governance/` describes rules and change control.
- `docs/onboarding/`, `docs/qa/`, and `docs/releases/` describe local working practice.

## Boundaries

- This level is short and repository-near.
- It does not describe deploy, VPS, production, or integration.
- It does not claim full runtime orchestration as implemented today.
- New architecture decisions are outside this foundation description.
