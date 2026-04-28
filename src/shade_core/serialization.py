from __future__ import annotations

from .contract_gate import ContractGateResult
from .evaluation import EvaluationResult
from .evaluation_gate import EvaluationGateResult
from .models import (
    ArtifactHandoff,
    MetaAuditEvent,
    OrchestrationAssertion,
    OrchestrationAudit,
    OrchestrationClosure,
    OrchestrationCheckpoint,
    OrchestrationEvidence,
    OrchestrationGate,
    OrchestrationJunction,
    OrchestrationLineage,
    OrchestrationManifest,
    OrchestrationOutcome,
    OrchestrationPublication,
    OrchestrationReleaseView,
    OrchestrationReview,
    OrchestrationVerification,
    RuntimeDecision,
    RunTransition,
    TaskRoute,
    TaskTransition,
    WorkerResult,
    WorkerTask,
)
from .state import RunState


def serialize_runtime_decision(decision: RuntimeDecision) -> dict[str, str]:
    return {
        "decision": decision.decision,
        "reason": decision.reason,
        "next_step": decision.next_step,
    }


def serialize_run_state(state: RunState) -> dict[str, str]:
    return {
        "run_id": state.run_id,
        "worker_role": state.worker_role,
        "decision_class": state.decision_class,
        "verification_state": state.verification_state,
        "artifact_ref": state.artifact_ref,
        "source_lane": state.source_lane,
        "target_lane": state.target_lane,
    }


def serialize_artifact_handoff(handoff: ArtifactHandoff) -> dict[str, str]:
    return {
        "artifact_ref": handoff.artifact_ref,
        "source_lane": handoff.source_lane,
        "target_lane": handoff.target_lane,
    }


def serialize_meta_audit_event(event: MetaAuditEvent) -> dict[str, str]:
    return {
        "event_type": event.event_type,
        "message": event.message,
        "severity": event.severity,
        "reference": event.reference,
        "run_id": event.run_id,
    }


def serialize_evaluation_result(result: EvaluationResult) -> dict[str, str]:
    return {"result": result}


def serialize_contract_gate_result(
    result: ContractGateResult,
) -> dict[str, object]:
    return {
        "is_valid": result.is_valid,
        "errors": result.errors,
    }


def serialize_runtime_contract_gate(
    self_model_result: ContractGateResult,
    worker_registry_result: ContractGateResult,
    confidence_record_result: ContractGateResult,
    state_contract_result: ContractGateResult,
) -> dict[str, dict[str, object]]:
    return {
        "self_model": serialize_contract_gate_result(self_model_result),
        "worker_registry": serialize_contract_gate_result(
            worker_registry_result,
        ),
        "confidence_record": serialize_contract_gate_result(
            confidence_record_result,
        ),
        "state_contract": serialize_contract_gate_result(
            state_contract_result,
        ),
    }


def serialize_evaluation_gate_result(
    result: EvaluationGateResult,
) -> dict[str, object]:
    return {
        "result": result.result,
        "contract_valid": result.contract_valid,
        "errors": result.errors,
    }


def serialize_worker_task(task: WorkerTask) -> dict[str, str]:
    return {
        "task_id": task.task_id,
        "worker_role": task.worker_role,
        "input_ref": task.input_ref,
        "task_status": task.task_status,
    }


def serialize_worker_result(result: WorkerResult) -> dict[str, str]:
    return {
        "task_id": result.task_id,
        "worker_role": result.worker_role,
        "output_ref": result.output_ref,
        "result_status": result.result_status,
    }


def serialize_task_route(route: TaskRoute) -> dict[str, str]:
    return {
        "task_id": route.task_id,
        "source_role": route.source_role,
        "target_role": route.target_role,
        "route_ref": route.route_ref,
    }


def serialize_orchestration_checkpoint(
    checkpoint: OrchestrationCheckpoint,
) -> dict[str, str]:
    return {
        "task_id": checkpoint.task_id,
        "output_ref": checkpoint.output_ref,
        "route_ref": checkpoint.route_ref,
        "checkpoint_ref": checkpoint.checkpoint_ref,
    }


def serialize_orchestration_junction(
    junction: OrchestrationJunction,
) -> dict[str, str]:
    return {
        "route_ref": junction.route_ref,
        "task_transition_ref": junction.task_transition_ref,
        "run_transition_ref": junction.run_transition_ref,
        "junction_ref": junction.junction_ref,
    }


def serialize_orchestration_verification(
    verification: OrchestrationVerification,
) -> dict[str, str]:
    return {
        "checkpoint_ref": verification.checkpoint_ref,
        "junction_ref": verification.junction_ref,
        "task_transition_ref": verification.task_transition_ref,
        "verification_ref": verification.verification_ref,
    }


def serialize_orchestration_outcome(
    outcome: OrchestrationOutcome,
) -> dict[str, str]:
    return {
        "verification_ref": outcome.verification_ref,
        "decision_ref": outcome.decision_ref,
        "evaluation_ref": outcome.evaluation_ref,
        "outcome_ref": outcome.outcome_ref,
    }


def serialize_orchestration_evidence(
    evidence: OrchestrationEvidence,
) -> dict[str, str]:
    return {
        "verification_ref": evidence.verification_ref,
        "outcome_ref": evidence.outcome_ref,
        "evaluation_ref": evidence.evaluation_ref,
        "evidence_ref": evidence.evidence_ref,
    }


def serialize_orchestration_gate(
    gate: OrchestrationGate,
) -> dict[str, str]:
    return {
        "evidence_ref": gate.evidence_ref,
        "evaluation_gate_ref": gate.evaluation_gate_ref,
        "audit_ref": gate.audit_ref,
        "gate_ref": gate.gate_ref,
    }


def serialize_orchestration_audit(
    audit: OrchestrationAudit,
) -> dict[str, str]:
    return {
        "gate_ref": audit.gate_ref,
        "evaluation_gate_ref": audit.evaluation_gate_ref,
        "audit_event_ref": audit.audit_event_ref,
        "audit_ref": audit.audit_ref,
    }


def serialize_orchestration_closure(
    closure: OrchestrationClosure,
) -> dict[str, str]:
    return {
        "audit_ref": closure.audit_ref,
        "decision_ref": closure.decision_ref,
        "evaluation_ref": closure.evaluation_ref,
        "closure_ref": closure.closure_ref,
    }


def serialize_task_transition(transition: TaskTransition) -> dict[str, str]:
    return {
        "task_id": transition.task_id,
        "from_status": transition.from_status,
        "to_status": transition.to_status,
        "transition_ref": transition.transition_ref,
    }


def serialize_run_transition(transition: RunTransition) -> dict[str, str]:
    return {
        "run_id": transition.run_id,
        "from_step": transition.from_step,
        "to_step": transition.to_step,
        "transition_ref": transition.transition_ref,
    }


def serialize_orchestration_lineage(
    lineage: OrchestrationLineage,
) -> dict[str, str]:
    return {
        "closure_ref": lineage.closure_ref,
        "audit_ref": lineage.audit_ref,
        "outcome_ref": lineage.outcome_ref,
        "lineage_ref": lineage.lineage_ref,
    }


def serialize_orchestration_manifest(
    manifest: OrchestrationManifest,
) -> dict[str, str]:
    return {
        "lineage_ref": manifest.lineage_ref,
        "closure_ref": manifest.closure_ref,
        "evidence_ref": manifest.evidence_ref,
        "manifest_ref": manifest.manifest_ref,
    }


def serialize_orchestration_review(
    review: OrchestrationReview,
) -> dict[str, str]:
    return {
        "manifest_ref": review.manifest_ref,
        "lineage_ref": review.lineage_ref,
        "closure_ref": review.closure_ref,
        "review_ref": review.review_ref,
    }


def serialize_orchestration_assertion(
    assertion: OrchestrationAssertion,
) -> dict[str, str]:
    return {
        "review_ref": assertion.review_ref,
        "manifest_ref": assertion.manifest_ref,
        "lineage_ref": assertion.lineage_ref,
        "assertion_ref": assertion.assertion_ref,
    }


def serialize_orchestration_publication(
    publication: OrchestrationPublication,
) -> dict[str, str]:
    return {
        "assertion_ref": publication.assertion_ref,
        "review_ref": publication.review_ref,
        "manifest_ref": publication.manifest_ref,
        "publication_ref": publication.publication_ref,
    }


def serialize_orchestration_release_view(
    release_view: OrchestrationReleaseView,
) -> dict[str, str]:
    return {
        "publication_ref": release_view.publication_ref,
        "assertion_ref": release_view.assertion_ref,
        "review_ref": release_view.review_ref,
        "release_view_ref": release_view.release_view_ref,
    }
