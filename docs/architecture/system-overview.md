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
- The current internal contract layer also prepares orchestration-checkpoint and orchestration-junction boundaries as neutral typed bridge objects between the current worker-result and route layer and the current transition-prep layer. These do not implement orchestration or routing behavior.
- The current internal contract layer also prepares task-transition and run-transition boundaries as neutral typed objects. These prepare step-junction boundaries without implementing step transitions.
- The current internal contract layer also prepares orchestration-verification and orchestration-outcome boundaries as neutral typed bridge objects between the current checkpoint/junction plus transition-prep layer and the current decision/evaluation side. These do not implement verification, evaluation, or decision behavior.
- The current internal contract layer also prepares orchestration-evidence and orchestration-gate boundaries as neutral typed bridge objects between the current verification/outcome seam and the current evaluation-gate and audit side. These do not implement evidence, gate, evaluation-gate, or audit behavior.
- The current internal contract layer also prepares orchestration-audit and orchestration-closure boundaries as neutral typed bridge objects between the current evidence/gate seam and the current audit and closing end. These do not implement audit, closure, evaluation-gate, decision, or runtime behavior.
- The current internal contract layer also prepares orchestration-lineage and orchestration-manifest boundaries as neutral typed bridge objects that consolidate the already-built contract chain into one inspectable description. These do not implement lineage, manifest, decision, audit, or runtime behavior.
- The current internal contract layer also prepares orchestration-review and orchestration-assertion boundaries as neutral typed bridge objects that consolidate the manifest, lineage, and closure references into one inspectable review and assertion record. These do not implement review, assertion, manifest, or runtime behavior.
- The current internal contract layer also prepares orchestration-publication and orchestration-release-view boundaries as neutral typed bridge objects that consolidate the assertion and review references, with release-view also linking publication and release-view references, into one inspectable publication and release-view record. These do not implement publication, release, assertion, review, or runtime behavior.
- `docs/architecture/` describes foundation structure, current boundaries, and documented V1 target contracts.
- `docs/governance/` describes rules and change control.
- `docs/onboarding/`, `docs/qa/`, and `docs/releases/` describe local working practice.

## Boundaries

- This level is short and repository-near.
- It does not describe deploy, VPS, production, or integration.
- It does not implement adapters, provider bindings, or runtime wiring for that handoff boundary.
- It does not claim full runtime orchestration as implemented today; the worker-task contract objects are preparation boundaries only.
- It does not claim checkpoint or junction execution behavior as implemented today; those bridge objects are preparation boundaries only.
- It does not claim verification or outcome execution behavior as implemented today; those bridge objects are preparation boundaries only.
- It does not claim evidence or gate execution behavior as implemented today; those bridge objects are preparation boundaries only.
- It does not claim audit or closure execution behavior as implemented today; those bridge objects are preparation boundaries only.
- New architecture decisions are outside this foundation description.
