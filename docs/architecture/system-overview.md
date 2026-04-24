# System overview

## Purpose

`shade-core` collects foundation documentation for architecture, governance, and local working mode.

## System frame

- `src/shade_core/` currently implements a minimal core of contract, gate, evaluation, serialization, bundle primitives, one internal runtime-fabric snapshot path, and three internal worker-task/orchestration contract objects as preparation boundaries.
- `src/shade_core/__init__.py` defines the stable root package API for that current minimal core.
- The remaining `src/shade_core/*.py` files are internal implementation modules behind the root package surface.
- Adapter-awareness in the current core is limited to one neutral typed handoff boundary for `artifact_ref`, `source_lane`, and `target_lane`.
- The current internal fabric links run state, handoff, decision, audit event, and evaluation gate result into one inspectable snapshot.
- The current internal contract layer also prepares worker-task, worker-result, and task-route boundaries as neutral typed objects. These do not implement orchestration behavior.
- `docs/architecture/` describes foundation structure, current boundaries, and documented V1 target contracts.
- `docs/governance/` describes rules and change control.
- `docs/onboarding/`, `docs/qa/`, and `docs/releases/` describe local working practice.

## Boundaries

- This level is short and repository-near.
- It does not describe deploy, VPS, production, or integration.
- It does not implement adapters, provider bindings, or runtime wiring for that handoff boundary.
- It does not claim full runtime orchestration as implemented today; the worker-task contract objects are preparation boundaries only.
- New architecture decisions are outside this foundation description.
