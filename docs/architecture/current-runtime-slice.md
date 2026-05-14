# Current runtime slice

## Purpose

This file is the source-of-truth description of what `shade-core` implements now versus what remains target-only within the broader locked S1/S2 boundaries.

## Implemented now

- The stable public package surface is the root `shade_core` import path in `src/shade_core/__init__.py`.
- The implemented public slice is still small: run state, confidence and self-model records, worker registry, runtime decision and audit event records, contract-gate and evaluation-gate results, decision and audit helpers, evaluation helpers, serializers, `build_bundle`, and exported `validate_state_contract`.
- The current core also implements one neutral handoff seam through internal `ArtifactHandoff`, `validate_artifact_handoff`, `serialize_artifact_handoff`, and the `artifact_handoff` snapshot entry. This seam is a typed handoff boundary only, not adapter or provider integration.
- The current core implements one internal runtime/evaluation fabric path that prepares state validation, neutral handoff serialization, decision, audit, evaluation, evaluation gate, and inspectable snapshot output.
- The current core implements internal contract-prep objects, validators, serializers, and snapshot helpers for worker task, worker result, task route, checkpoint, junction, task transition, run transition, verification, outcome, evidence, gate, audit, closure, lineage, manifest, review, assertion, publication, and release-view seams.

## Runtime/evaluation fabric versus orchestration

- The runtime/evaluation fabric is implemented as an inspectable internal snapshot and guard-verification path.
- That implemented snapshot path already includes an `artifact_handoff` view, but only as the neutral handoff seam described above.
- That fabric is not a full runtime loop and not a worker execution engine.
- The worker, checkpoint, verification, evidence, audit, lineage, and publication objects currently exist as contract-prep boundaries only.
- These contract-prep boundaries do not execute worker selection, worker steps, routing, transitions, closure, publication, or release behavior.

## Target-only, not implemented

- Full A-to-O runtime loop execution.
- Worker orchestration behavior.
- Adapter or provider implementations.
- Memory layer behavior.
- Deploy or VPS behavior.
- Production integration.

## Safe reading rule

- Treat `docs/architecture/runtime-loop-a-to-o.md` and `docs/architecture/worker-ontology.md` as target-boundary references, not as claims of current runtime behavior.
- Treat this file as the current implementation truth layer when there is any ambiguity between implemented surfaces and broader target docs.
- Do not infer production safety, deployment readiness, or integrated orchestration from the current contract-prep chain.