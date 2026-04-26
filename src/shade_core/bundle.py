from __future__ import annotations

from collections.abc import Mapping

from .evaluation import EvaluationResult
from .evaluation_gate import EvaluationGateResult
from .models import (
    ArtifactHandoff,
    MetaAuditEvent,
    OrchestrationAudit,
    OrchestrationClosure,
    OrchestrationCheckpoint,
    OrchestrationEvidence,
    OrchestrationGate,
    OrchestrationJunction,
    OrchestrationLineage,
    OrchestrationManifest,
    OrchestrationOutcome,
    OrchestrationVerification,
    RuntimeDecision,
    RunTransition,
    TaskRoute,
    TaskTransition,
    WorkerResult,
    WorkerTask,
)
from .state import RunState
from .serialization import (
    serialize_artifact_handoff,
    serialize_evaluation_gate_result,
    serialize_evaluation_result,
    serialize_meta_audit_event,
    serialize_orchestration_audit,
    serialize_orchestration_closure,
    serialize_orchestration_checkpoint,
    serialize_orchestration_evidence,
    serialize_orchestration_gate,
    serialize_orchestration_junction,
    serialize_orchestration_lineage,
    serialize_orchestration_manifest,
    serialize_orchestration_outcome,
    serialize_orchestration_verification,
    serialize_run_state,
    serialize_run_transition,
    serialize_runtime_decision,
    serialize_task_route,
    serialize_task_transition,
    serialize_worker_result,
    serialize_worker_task,
)


def _build_runtime_fabric_snapshot(
    state: RunState,
    decision: RuntimeDecision,
    audit_event: MetaAuditEvent,
    evaluation_gate_result: EvaluationGateResult,
) -> Mapping[str, Mapping[str, object]]:
    handoff = ArtifactHandoff(
        artifact_ref=state.artifact_ref,
        source_lane=state.source_lane,
        target_lane=state.target_lane,
    )

    return {
        "run_state": serialize_run_state(state),
        "artifact_handoff": serialize_artifact_handoff(handoff),
        "decision": serialize_runtime_decision(decision),
        "audit_event": serialize_meta_audit_event(audit_event),
        "evaluation_gate": serialize_evaluation_gate_result(
            evaluation_gate_result,
        ),
    }


def build_bundle(
    decision: RuntimeDecision,
    audit_event: MetaAuditEvent,
    evaluation_result: EvaluationResult,
) -> dict[str, dict[str, str]]:
    return {
        "decision": serialize_runtime_decision(decision),
        "audit_event": serialize_meta_audit_event(audit_event),
        "evaluation": serialize_evaluation_result(evaluation_result),
    }


def _build_orchestration_contract_snapshot(
    task: WorkerTask,
    result: WorkerResult,
    route: TaskRoute,
) -> Mapping[str, Mapping[str, str]]:
    return {
        "worker_task": serialize_worker_task(task),
        "worker_result": serialize_worker_result(result),
        "task_route": serialize_task_route(route),
    }


def _build_state_transition_snapshot(
    task_transition: TaskTransition,
    run_transition: RunTransition,
) -> Mapping[str, Mapping[str, str]]:
    return {
        "task_transition": serialize_task_transition(task_transition),
        "run_transition": serialize_run_transition(run_transition),
    }


def _build_checkpoint_junction_snapshot(
    checkpoint: OrchestrationCheckpoint,
    junction: OrchestrationJunction,
) -> Mapping[str, Mapping[str, str]]:
    return {
        "orchestration_checkpoint": serialize_orchestration_checkpoint(
            checkpoint,
        ),
        "orchestration_junction": serialize_orchestration_junction(
            junction,
        ),
    }


def _build_verification_outcome_snapshot(
    verification: OrchestrationVerification,
    outcome: OrchestrationOutcome,
) -> Mapping[str, Mapping[str, str]]:
    return {
        "orchestration_verification": serialize_orchestration_verification(
            verification,
        ),
        "orchestration_outcome": serialize_orchestration_outcome(
            outcome,
        ),
    }


def _build_evidence_gate_snapshot(
    evidence: OrchestrationEvidence,
    gate: OrchestrationGate,
) -> Mapping[str, Mapping[str, str]]:
    return {
        "orchestration_evidence": serialize_orchestration_evidence(
            evidence,
        ),
        "orchestration_gate": serialize_orchestration_gate(
            gate,
        ),
    }


def _build_audit_closure_snapshot(
    audit: OrchestrationAudit,
    closure: OrchestrationClosure,
) -> Mapping[str, Mapping[str, str]]:
    return {
        "orchestration_audit": serialize_orchestration_audit(
            audit,
        ),
        "orchestration_closure": serialize_orchestration_closure(
            closure,
        ),
    }


def _build_lineage_manifest_snapshot(
    lineage: OrchestrationLineage,
    manifest: OrchestrationManifest,
) -> Mapping[str, Mapping[str, str]]:
    return {
        "orchestration_lineage": serialize_orchestration_lineage(
            lineage,
        ),
        "orchestration_manifest": serialize_orchestration_manifest(
            manifest,
        ),
    }
