# ADR-0002 Cycle 9 Next Slice Selection

Status: Accepted

## Context

The current `shade-core` implementation is still a minimal public core plus an internal contract-prep chain. Full A-to-O runtime execution, worker orchestration, adapters/providers, memory, deploy, VPS, and production integration are not implemented.

## Decision

Cycle 9.2 selects `worker orchestration contract prep` as the next slice.
`A-to-O runtime loop contract prep`, `verification and manifest hardening`, and `adapter boundary prep` are deferred.

## Consequences

- The next slice stays close to the current worker-task, worker-result, task-route, checkpoint, junction, and transition prep seam.
- The repository continues to document broader target boundaries without claiming runtime orchestration as implemented.
- Adapter, provider, memory, deploy, VPS, and production integration work remain out of scope.