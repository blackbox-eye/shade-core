from __future__ import annotations

from dataclasses import dataclass
from collections.abc import Mapping

from .contract_gate import (
    ContractGateResult,
    validate_confidence_record,
    validate_meta_audit_event,
    validate_self_model,
    validate_state_contract,
    validate_runtime_decision,
    validate_worker_registry,
)
from .evaluation import EvaluationResult, evaluate
from .evaluation_gate import (
    EvaluationGateResult,
    _aggregate_runtime_contract_result,
    _build_evaluation_gate_result_from_raw_result,
    _guard_evaluation_gate_result_from_raw_result,
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
    _serialize_runtime_fabric_guard_result,
    serialize_artifact_handoff,
    _serialize_aggregated_runtime_contract_gate,
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
    serialized_contract_gate = serialize_runtime_contract_gate(
        prepared_fabric.self_model_result,
        prepared_fabric.worker_registry_result,
        prepared_fabric.confidence_record_result,
        prepared_fabric.state_contract_result,
    )
    serialized_evaluation_gate = serialize_evaluation_gate_result(
        prepared_fabric.evaluation_gate_result,
    )

    return {
        "contract_gate": serialized_contract_gate,
        "runtime_fabric": _build_runtime_fabric_snapshot(
            state,
            prepared_fabric.decision,
            prepared_fabric.audit_event,
            serialized_evaluation_gate,
        ),
        "aggregated_contract_gate": _serialize_aggregated_runtime_contract_gate(
            serialized_contract_gate,
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
    evaluation_gate_result = _build_evaluation_gate_result_from_raw_result(
        aggregated_contract_result,
        raw_evaluation_result,
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


def _guard_prepared_runtime_evaluation_fabric(
    prepared_fabric: _PreparedRuntimeEvaluationFabric,
) -> tuple[str, ...]:
    errors: list[str] = []
    audit_event_inputs_are_valid = (
        prepared_fabric.self_model_result.is_valid
        and prepared_fabric.confidence_record_result.is_valid
    )

    if not validate_runtime_decision(prepared_fabric.decision).is_valid:
        errors.append(
            "prepared_fabric.decision must satisfy the runtime decision contract",
        )
    if (
        audit_event_inputs_are_valid
        and not validate_meta_audit_event(prepared_fabric.audit_event).is_valid
    ):
        errors.append(
            "prepared_fabric.audit_event must satisfy the meta audit contract",
        )

    expected_aggregated_contract_result = _aggregate_runtime_contract_result(
        prepared_fabric.self_model_result,
        prepared_fabric.worker_registry_result,
        prepared_fabric.confidence_record_result,
        prepared_fabric.state_contract_result,
    )
    if prepared_fabric.aggregated_contract_result != expected_aggregated_contract_result:
        errors.append(
            "prepared_fabric.aggregated_contract_result must equal the aggregated component contract results",
        )

    gate_errors = _guard_evaluation_gate_result_from_raw_result(
        prepared_fabric.aggregated_contract_result,
        prepared_fabric.raw_evaluation_result,
        prepared_fabric.evaluation_gate_result,
    )
    if gate_errors:
        errors.append(
            "prepared_fabric.evaluation_gate_result must match the aggregated contract result and raw evaluation result",
        )
        for gate_error in gate_errors:
            if gate_error == (
                "valid contracts must keep the evaluation gate result aligned with the raw result"
            ):
                errors.append(
                    "prepared_fabric.valid contracts must keep raw and gated evaluation results aligned",
                )
            elif gate_error == (
                "invalid contracts must force the evaluation gate result to fail"
            ):
                errors.append(
                    "prepared_fabric.invalid contracts must force the gated evaluation result to fail",
                )
            elif gate_error == (
                "invalid contracts must preserve contract errors in the evaluation gate result"
            ):
                errors.append(
                    "prepared_fabric.invalid contracts must preserve aggregated contract errors in the gated evaluation result",
                )

    return tuple(errors)


def _run_runtime_evaluation_fabric_guards(
    prepared_fabric: _PreparedRuntimeEvaluationFabric,
    runtime_evaluation_snapshot: Mapping[str, object],
) -> Mapping[str, tuple[str, ...]]:
    return {
        "prepared_fabric_guard": _guard_prepared_runtime_evaluation_fabric(
            prepared_fabric,
        ),
        "serialized_snapshot_guard": _guard_runtime_evaluation_fabric_snapshot(
            runtime_evaluation_snapshot,
        ),
    }


def _guard_runtime_evaluation_fabric_snapshot(
    snapshot: Mapping[str, object],
) -> tuple[str, ...]:
    errors: list[str] = []
    expected_contract_gate_keys = (
        "self_model",
        "worker_registry",
        "confidence_record",
        "state_contract",
    )

    def _normalize_errors_value(
        value: object,
        path: str,
    ) -> tuple[object, ...]:
        if isinstance(value, tuple):
            return value
        if isinstance(value, list):
            return tuple(value)
        if value is None:
            return ()

        errors.append(f"{path} must be a tuple, list, or None")
        return ()

    runtime_contract_integration = snapshot.get("runtime_contract_integration")
    if not isinstance(runtime_contract_integration, Mapping):
        return (
            "snapshot.runtime_contract_integration must be a mapping",
        )

    contract_gate = runtime_contract_integration.get("contract_gate")
    if not isinstance(contract_gate, Mapping):
        errors.append(
            "snapshot.runtime_contract_integration.contract_gate must be a mapping",
        )
        contract_gate = {}

    sanitized_contract_gate: dict[str, dict[str, object]] = {}
    for key in expected_contract_gate_keys:
        nested_entry = contract_gate.get(key)
        if not isinstance(nested_entry, Mapping):
            errors.append(
                f"snapshot.runtime_contract_integration.contract_gate.{key} must be a mapping",
            )
            sanitized_contract_gate[key] = {}
            continue

        sanitized_nested_entry = dict(nested_entry)
        sanitized_nested_entry["errors"] = _normalize_errors_value(
            sanitized_nested_entry.get("errors"),
            f"snapshot.runtime_contract_integration.contract_gate.{key}.errors",
        )
        sanitized_contract_gate[key] = sanitized_nested_entry

    runtime_fabric = runtime_contract_integration.get("runtime_fabric")
    if not isinstance(runtime_fabric, Mapping):
        errors.append(
            "snapshot.runtime_contract_integration.runtime_fabric must be a mapping",
        )
        runtime_fabric = {}

    aggregated_contract_gate = snapshot.get("aggregated_contract_gate")
    if not isinstance(aggregated_contract_gate, Mapping):
        errors.append("snapshot.aggregated_contract_gate must be a mapping")
        aggregated_contract_gate = {}
    else:
        aggregated_contract_gate = dict(aggregated_contract_gate)

    raw_evaluation = snapshot.get("raw_evaluation")
    if not isinstance(raw_evaluation, Mapping):
        errors.append("snapshot.raw_evaluation must be a mapping")
        raw_evaluation = {}

    evaluation_gate = snapshot.get("evaluation_gate")
    if not isinstance(evaluation_gate, Mapping):
        errors.append("snapshot.evaluation_gate must be a mapping")
        evaluation_gate = {}
    else:
        evaluation_gate = dict(evaluation_gate)

    nested_evaluation_gate = runtime_fabric.get("evaluation_gate")
    if not isinstance(nested_evaluation_gate, Mapping):
        errors.append(
            "snapshot.runtime_contract_integration.runtime_fabric.evaluation_gate must be a mapping",
        )
        nested_evaluation_gate = {}
    else:
        nested_evaluation_gate = dict(nested_evaluation_gate)

    aggregated_contract_gate["errors"] = _normalize_errors_value(
        aggregated_contract_gate.get("errors"),
        "snapshot.aggregated_contract_gate.errors",
    )
    evaluation_gate["errors"] = _normalize_errors_value(
        evaluation_gate.get("errors"),
        "snapshot.evaluation_gate.errors",
    )
    nested_evaluation_gate["errors"] = _normalize_errors_value(
        nested_evaluation_gate.get("errors"),
        "snapshot.runtime_contract_integration.runtime_fabric.evaluation_gate.errors",
    )

    if nested_evaluation_gate != evaluation_gate:
        errors.append(
            "snapshot.runtime_contract_integration.runtime_fabric.evaluation_gate must equal snapshot.evaluation_gate",
        )

    expected_aggregated_contract_gate = _serialize_aggregated_runtime_contract_gate(
        sanitized_contract_gate,
    )
    if aggregated_contract_gate != expected_aggregated_contract_gate:
        errors.append(
            "snapshot.aggregated_contract_gate must equal the aggregation implied by nested contract_gate entries",
        )

    aggregated_is_valid = aggregated_contract_gate.get("is_valid")
    evaluation_gate_errors = evaluation_gate.get("errors", ())
    aggregated_errors = aggregated_contract_gate.get("errors", ())

    if aggregated_is_valid is True:
        if raw_evaluation.get("result") != evaluation_gate.get("result"):
            errors.append(
                "snapshot.valid contracts must keep raw_evaluation.result aligned with evaluation_gate.result",
            )
        if evaluation_gate.get("contract_valid") is not True:
            errors.append(
                "snapshot.valid contracts must mark evaluation_gate.contract_valid as true",
            )
        if evaluation_gate_errors != ():
            errors.append(
                "snapshot.valid contracts must keep evaluation_gate.errors empty",
            )
    elif aggregated_is_valid is False:
        if evaluation_gate.get("result") != "fail":
            errors.append(
                "snapshot.invalid contracts must force evaluation_gate.result to fail",
            )
        if evaluation_gate.get("contract_valid") is not False:
            errors.append(
                "snapshot.invalid contracts must mark evaluation_gate.contract_valid as false",
            )
        if evaluation_gate_errors != aggregated_errors:
            errors.append(
                "snapshot.invalid contracts must preserve aggregated_contract_gate.errors in evaluation_gate.errors",
            )

    return tuple(errors)


def _build_runtime_contract_integration_snapshot(
    state: RunState,
    prepared_fabric: _PreparedRuntimeEvaluationFabric,
    serialized_fragments: Mapping[str, object] | None = None,
) -> Mapping[str, Mapping[str, Mapping[str, object]]]:
    if serialized_fragments is None:
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
                prepared_fabric.evaluation_gate_result,
            ),
        }

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


def _build_runtime_evaluation_guard_verification_snapshot(
    runtime_evaluation_snapshot: Mapping[str, object],
    prepared_fabric_guard_errors: tuple[str, ...],
    serialized_snapshot_guard_errors: tuple[str, ...],
) -> Mapping[str, object]:
    return {
        "runtime_evaluation": runtime_evaluation_snapshot,
        "prepared_fabric_guard": _serialize_runtime_fabric_guard_result(
            prepared_fabric_guard_errors,
        ),
        "serialized_snapshot_guard": _serialize_runtime_fabric_guard_result(
            serialized_snapshot_guard_errors,
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
