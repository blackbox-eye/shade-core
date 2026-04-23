# Worker ontology

## Purpose

This file locks worker types, roles, responsibilities, and boundaries for V1.
The current code uses role names and gate/state primitives, not worker orchestration.

## Worker types

- `intake-worker` clarifies input, goal, and scope.
- `analysis-worker` assesses material against active contracts.
- `control-worker` decides the next allowed step in the loop.
- `evaluation-worker` measures output against the QA matrix.

## Roles and responsibilities

- Each worker solves one scoped task at a time.
- A worker may only operate within declared scope.
- A worker must deliver inspectable output and status.
- A worker must not rewrite the contracts.

## Boundaries

- Workers are not authorities; they perform contract-driven work.
- Copilot is an assistant for suggestions and drafting, not a decision maker.
- Workers must not introduce deploy, VPS, secrets, production, or integration.
- Workers must not skip control or evaluation steps.
