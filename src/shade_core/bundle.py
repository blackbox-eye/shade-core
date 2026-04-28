from __future__ import annotations

from dataclasses import dataclass
from collections.abc import Mapping

from .contract_gate import (
    ContractGateResult,
    validate_confidence_record,
    validate_self_model,
    validate_state_contract,
    validate_worker_registry,
)
from .evaluation import EvaluationResult, evaluate
from .evaluation_gate import (
    EvaluationGateResult,
    _aggregate_runtime_contract_result,
)
from .models import (
    ArtifactHandoff,
    ConfidenceRecord,
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
    SelfModel,
    RunTransition,
    TaskRoute,
    TaskTransition,
    WorkerRegistry,
    WorkerResult,
    WorkerTask,
)
from .runtime_loop import audit_decision, decide
from .state import RunState
from .serialization import (
    serialize_artifact_handoff,
    serialize_contract_gate_result,
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
    serialize_orchestration_assertion,
    serialize_orchestration_review,
    serialize_orchestration_publication,
    serialize_orchestration_release_view,
    serialize_orchestration_outcome,
    serialize_orchestration_verification,
    serialize_run_state,
    serialize_run_transition,
    serialize_runtime_contract_gate,
    serialize_runtime_decision,
    serialize_task_route,
    serialize_task_transition,
    serialize_worker_result,
    serialize_worker_task,
)


@dataclass(slots=True)
class _PreparedRuntimeEvaluationFabric:
    self_model_result: ContractGateResult
    worker_registry_result: ContractGateResult
    confidence_record_result: ContractGateResult
    state_contract_result: ContractGateResult
    aggregated_contract_result: ContractGateResult
    decision: RuntimeDecision
    audit_event: MetaAuditEvent
    raw_evaluation_result: EvaluationResult
    evaluation_gate_result: EvaluationGateResult


def _build_runtime_fabric_snapshot(
    state: RunState,
    decision: RuntimeDecision,
    audit_event: MetaAuditEvent,
    evaluation_gate_result: EvaluationGateResult | Mapping[str, object],
) -> Mapping[str, Mapping[str, object]]:
    if isinstance(evaluation_gate_result, EvaluationGateResult):
        serialized_evaluation_gate = serialize_evaluation_gate_result(
            evaluation_gate_result,
        )
    else:
        serialized_evaluation_gate = dict(evaluation_gate_result)

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
        "evaluation_gate": serialized_evaluation_gate,
    }


def _serialize_runtime_evaluation_fabric_fragments(
    state: RunState,
    prepared_fabric: _PreparedRuntimeEvaluationFabric,
) -> Mapping[str, object]:
    serialized_evaluation_gate = serialize_evaluation_gate_result(
        prepared_fabric.evaluation_gate_result,
    )

    return {
        "contract_gate": serialize_runtime_contract_gate(
            prepared_fabric.self_model_result,
            prepared_fabric.worker_registry_result,
            prepared_fabric.confidence_record_result,
            prepared_fabric.state_contract_result,
        ),
        "runtime_fabric": _build_runtime_fabric_snapshot(
            state,
            prepared_fabric.decision,
            prepared_fabric.audit_event,
            serialized_evaluation_gate,
        ),
        "aggregated_contract_gate": serialize_contract_gate_result(
            prepared_fabric.aggregated_contract_result,
        ),
        "raw_evaluation": serialize_evaluation_result(
            prepared_fabric.raw_evaluation_result,
        ),
        "evaluation_gate": serialized_evaluation_gate,
    }


def _prepare_runtime_evaluation_fabric(
    self_model: SelfModel,
    registry: WorkerRegistry,
    confidence: ConfidenceRecord,
    state: RunState,
) -> _PreparedRuntimeEvaluationFabric:
    self_model_result = validate_self_model(self_model)
    worker_registry_result = validate_worker_registry(registry)
    confidence_record_result = validate_confidence_record(confidence)
    state_contract_result = validate_state_contract(state)
    aggregated_contract_result = _aggregate_runtime_contract_result(
        self_model_result,
        worker_registry_result,
        confidence_record_result,
        state_contract_result,
    )
    decision = decide(self_model, registry, confidence)
    audit_event = audit_decision(self_model, decision, confidence)
    raw_evaluation_result = evaluate(decision, audit_event)
    if aggregated_contract_result.is_valid:
        evaluation_gate_result = EvaluationGateResult(
            result=raw_evaluation_result,
            contract_valid=True,
            errors=(),
        )
    else:
        evaluation_gate_result = EvaluationGateResult(
            result="fail",
            contract_valid=False,
            errors=aggregated_contract_result.errors,
        )

    return _PreparedRuntimeEvaluationFabric(
        self_model_result=self_model_result,
        worker_registry_result=worker_registry_result,
        confidence_record_result=confidence_record_result,
        state_contract_result=state_contract_result,
        aggregated_contract_result=aggregated_contract_result,
        decision=decision,
        audit_event=audit_event,
        raw_evaluation_result=raw_evaluation_result,
        evaluation_gate_result=evaluation_gate_result,
    )


def _build_runtime_contract_integration_snapshot(
    state: RunState,
    prepared_fabric: _PreparedRuntimeEvaluationFabric,
    serialized_fragments: Mapping[str, object] | None = None,
) -> Mapping[str, Mapping[str, Mapping[str, object]]]:
    if serialized_fragments is None:
        serialized_fragments = _serialize_runtime_evaluation_fabric_fragments(
            state,
            prepared_fabric,
        )

    return {
        "contract_gate": serialized_fragments["contract_gate"],
        "runtime_fabric": serialized_fragments["runtime_fabric"],
    }


def _build_runtime_evaluation_gate_integration_snapshot(
    self_model: SelfModel,
    registry: WorkerRegistry,
    confidence: ConfidenceRecord,
    state: RunState,
) -> Mapping[str, object]:
    prepared_fabric = _prepare_runtime_evaluation_fabric(
        self_model,
        registry,
        confidence,
        state,
    )
    serialized_fragments = _serialize_runtime_evaluation_fabric_fragments(
        state,
        prepared_fabric,
    )

    return {
        "runtime_contract_integration": _build_runtime_contract_integration_snapshot(
            state,
            prepared_fabric,
            serialized_fragments,
        ),
        "aggregated_contract_gate": serialized_fragments[
            "aggregated_contract_gate"
        ],
        "raw_evaluation": serialized_fragments["raw_evaluation"],
        "evaluation_gate": serialized_fragments["evaluation_gate"],
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
        "orchestration_outcome": serialize_orchestration_outcome(outcome),
    }


def _build_evidence_gate_snapshot(
    evidence: OrchestrationEvidence,
    gate: OrchestrationGate,
) -> Mapping[str, Mapping[str, str]]:
    return {
        "orchestration_evidence": serialize_orchestration_evidence(
            evidence,
        ),
        "orchestration_gate": serialize_orchestration_gate(gate),
    }


def _build_audit_closure_snapshot(
    audit: OrchestrationAudit,
    closure: OrchestrationClosure,
) -> Mapping[str, Mapping[str, str]]:
    return {
        "orchestration_audit": serialize_orchestration_audit(audit),
        "orchestration_closure": serialize_orchestration_closure(closure),
    }


def _build_lineage_manifest_snapshot(
    lineage: OrchestrationLineage,
    manifest: OrchestrationManifest,
) -> Mapping[str, Mapping[str, str]]:
    return {
        "orchestration_lineage": serialize_orchestration_lineage(
            lineage,
        ),
        "orchestration_manifest": serialize_orchestration_manifest(manifest),
    }


def _build_review_assertion_snapshot(
    review: OrchestrationReview,
    assertion: OrchestrationAssertion,
) -> Mapping[str, Mapping[str, str]]:
    return {
        "orchestration_review": serialize_orchestration_review(review),
        "orchestration_assertion": serialize_orchestration_assertion(
            assertion,
        ),
    }


def _build_publication_release_view_snapshot(
    publication: OrchestrationPublication,
    release_view: OrchestrationReleaseView,
) -> Mapping[str, Mapping[str, str]]:
    return {
        "orchestration_publication": serialize_orchestration_publication(
            publication,
        ),
        "orchestration_release_view": serialize_orchestration_release_view(
            release_view,
        ),
    }
