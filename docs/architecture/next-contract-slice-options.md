# Next contract slice options

## Purpose

This file compares the safe Cycle 9.2 contract-slice options from the current runtime slice and recommends one next step.

## Selection rule

- Prefer the next slice that extends the current implemented contract-prep chain.
- Do not imply runtime execution, deploy, provider wiring, memory behavior, or production integration.
- Keep the next slice small enough to stay reviewable and explicit.

## Candidate options

### Worker orchestration contract prep

- Fit: closest to the current implemented worker-task, worker-result, task-route, checkpoint, junction, and transition prep seam.
- Benefit: extends the earliest orchestration-facing contract boundary without claiming execution behavior.
- Risk: low, because it stays inside internal contract objects, validation, serialization, and snapshot composition.

### A-to-O runtime loop contract prep

- Fit: aligned with the documented V1 target loop.
- Benefit: would clarify the full target chain end to end.
- Risk: too broad for the next slice because it spans the full target loop and can blur target docs with current implementation.

### Verification and manifest hardening

- Fit: aligned with already implemented downstream bridge objects.
- Benefit: would strengthen terminal verification, lineage, and manifest seams.
- Risk: better deferred until the earlier worker-orchestration seam is more explicit, so downstream hardening does not outrun upstream contract clarity.

### Adapter boundary prep

- Fit: only partial today through the neutral artifact handoff boundary.
- Benefit: could make future external boundary assumptions more explicit.
- Risk: too close to provider and integration concerns for the safest next slice.

## Recommended Cycle 9.2 slice

- Recommend `worker orchestration contract prep`.
- Reason: it is the closest safe extension of the currently implemented contract-prep chain and keeps the repo in a contract-first, non-runtime-execution mode.
- Scope shape: continue from worker task, worker result, task route, checkpoint, junction, and transition prep before pushing further into wider loop or integration-facing work.

## Deferred options

- Defer `A-to-O runtime loop contract prep` because it is too broad for the next repo-local slice.
- Defer `verification and manifest hardening` until the upstream worker-orchestration seam is firmer.
- Defer `adapter boundary prep` until contract prep needs more than the current neutral handoff boundary.