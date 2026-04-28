from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
import math

from .models import (
    ArtifactHandoff,
    ConfidenceRecord,
    MetaAuditEvent,
    OrchestrationAudit,
    OrchestrationAssertion,
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
from .state import RunState

_DECISION_CLASSES = {"accept", "reject", "needs_review"}
_VERIFICATION_STATES = {"pending", "verified", "failed"}
_VERIFICATION_ALIGNMENTS = {"aligned", "fail_closed", "drifted"}
_VERIFICATION_SUMMARY_STATUSES = {"verified", "failed"}
_RUNTIME_CONTRACT_GATE_KEYS = (
    "self_model",
    "worker_registry",
    "confidence_record",
    "state_contract",
)


@dataclass(slots=True)
class ContractGateResult:
    is_valid: bool
    errors: tuple[str, ...]


def validate_artifact_handoff(handoff: ArtifactHandoff) -> ContractGateResult:
    errors: list[str] = []

    if not handoff.artifact_ref:
        errors.append("artifact_ref is required")
    if not handoff.source_lane:
        errors.append("source_lane is required")
    if not handoff.target_lane:
        errors.append("target_lane is required")

    return ContractGateResult(is_valid=not errors, errors=tuple(errors))


def validate_state_contract(state: RunState) -> ContractGateResult:
    errors: list[str] = []

    if not state.run_id:
        errors.append("run_id is required")
    if not state.worker_role:
        errors.append("worker_role is required")
    if state.decision_class not in _DECISION_CLASSES:
        errors.append("decision_class is invalid")
    if state.verification_state not in _VERIFICATION_STATES:
        errors.append("verification_state is invalid")
    if not state.artifact_ref:
        errors.append("artifact_ref is required")
    if not state.source_lane:
        errors.append("source_lane is required")
    if not state.target_lane:
        errors.append("target_lane is required")

    return ContractGateResult(is_valid=not errors, errors=tuple(errors))


def validate_self_model(self_model: SelfModel) -> ContractGateResult:
    errors: list[str] = []

    if not self_model.agent_id:
        errors.append("agent_id is required")
    if not self_model.role:
        errors.append("role is required")
    if not self_model.state:
        errors.append("state is required")

    return ContractGateResult(is_valid=not errors, errors=tuple(errors))


def validate_worker_registry(registry: WorkerRegistry) -> ContractGateResult:
    errors: list[str] = []

    for name, worker in registry.workers.items():
        if not name:
            errors.append("worker name is required")

        if not isinstance(worker, tuple) or len(worker) != 2:
            worker_name = name or "<unnamed>"
            errors.append(
                f"worker entry for {worker_name} must contain role and status",
            )
            continue

        worker_role, status = worker
        if not worker_role:
            errors.append(f"worker role is required for {name or '<unnamed>'}")
        if not status:
            errors.append(f"worker status is required for {name or '<unnamed>'}")

    return ContractGateResult(is_valid=not errors, errors=tuple(errors))


def validate_confidence_record(
    confidence: ConfidenceRecord,
) -> ContractGateResult:
    errors: list[str] = []

    if not math.isfinite(confidence.score) or not 0.0 <= confidence.score <= 1.0:
        errors.append("score must be finite and between 0.0 and 1.0 inclusive")
    if not confidence.source:
        errors.append("source is required")
    if not confidence.reason:
        errors.append("reason is required")
    if not confidence.reference:
        errors.append("reference is required")

    return ContractGateResult(is_valid=not errors, errors=tuple(errors))


def validate_meta_audit_event(event: MetaAuditEvent) -> ContractGateResult:
    errors: list[str] = []

    if not event.event_type:
        errors.append("event_type is required")
    if not event.message:
        errors.append("message is required")
    if not event.severity:
        errors.append("severity is required")
    if not event.reference:
        errors.append("reference is required")
    if not event.run_id:
        errors.append("run_id is required")

    return ContractGateResult(is_valid=not errors, errors=tuple(errors))


def validate_runtime_decision(
    decision: RuntimeDecision,
) -> ContractGateResult:
    errors: list[str] = []

    if decision.decision not in _DECISION_CLASSES:
        errors.append("decision is invalid")
    if not decision.reason:
        errors.append("reason is required")
    if not decision.next_step:
        errors.append("next_step is required")

    return ContractGateResult(is_valid=not errors, errors=tuple(errors))


def _normalize_runtime_verification_errors(
    value: object,
) -> tuple[object, ...]:
    if isinstance(value, tuple):
        return value
    if isinstance(value, list):
        return tuple(value)
    if value is None:
        return ()

    return ()


def _normalize_runtime_verification_contract_result_mapping(
    value: object,
) -> dict[str, object]:
    if not isinstance(value, Mapping):
        return {}

    return {
        "is_valid": value.get("is_valid") is True,
        "errors": _normalize_runtime_verification_errors(value.get("errors")),
    }


def _normalize_runtime_verification_evaluation_gate_mapping(
    value: object,
) -> dict[str, object]:
    if not isinstance(value, Mapping):
        return {}

    return {
        "result": value.get("result"),
        "contract_valid": value.get("contract_valid"),
        "errors": _normalize_runtime_verification_errors(value.get("errors")),
    }


def _serialize_runtime_contract_gate_from_mapping(
    contract_gate: Mapping[str, object],
) -> dict[str, object]:
    return {
        "is_valid": all(
            _normalize_runtime_verification_contract_result_mapping(
                contract_gate.get(key),
            ).get("is_valid")
            is True
            for key in _RUNTIME_CONTRACT_GATE_KEYS
        ),
        "errors": tuple(
            error
            for key in _RUNTIME_CONTRACT_GATE_KEYS
            for error in _normalize_runtime_verification_contract_result_mapping(
                contract_gate.get(key),
            ).get("errors", ())
            if isinstance(error, str)
        ),
    }


def _summarize_runtime_verification_evaluation_gate_alignment(
    aggregated_contract_gate: Mapping[str, object],
    raw_evaluation: Mapping[str, object],
    evaluation_gate: Mapping[str, object],
) -> str:
    normalized_aggregated_contract_gate = (
        _normalize_runtime_verification_contract_result_mapping(
            aggregated_contract_gate,
        )
    )
    normalized_evaluation_gate = _normalize_runtime_verification_evaluation_gate_mapping(
        evaluation_gate,
    )

    contract_is_valid = normalized_aggregated_contract_gate.get("is_valid") is True
    expected_errors = (
        ()
        if contract_is_valid
        else normalized_aggregated_contract_gate.get("errors", ())
    )
    raw_result = raw_evaluation.get("result") if isinstance(raw_evaluation, Mapping) else None

    if contract_is_valid:
        if (
            normalized_evaluation_gate.get("result") == raw_result
            and normalized_evaluation_gate.get("contract_valid") is True
            and normalized_evaluation_gate.get("errors") == ()
        ):
            return "aligned"

        return "drifted"

    if (
        normalized_evaluation_gate.get("result") == "fail"
        and normalized_evaluation_gate.get("contract_valid") is False
        and normalized_evaluation_gate.get("errors") == expected_errors
    ):
        return "fail_closed"

    return "drifted"


def _summarize_runtime_evaluation_verification_snapshot(
    runtime_evaluation_snapshot: Mapping[str, object],
    prepared_fabric_guard: Mapping[str, object],
    serialized_snapshot_guard: Mapping[str, object],
) -> dict[str, object]:
    runtime_contract_integration = runtime_evaluation_snapshot.get(
        "runtime_contract_integration",
    )
    if not isinstance(runtime_contract_integration, Mapping):
        runtime_contract_integration = {}

    contract_gate = runtime_contract_integration.get("contract_gate")
    if not isinstance(contract_gate, Mapping):
        contract_gate = {}

    runtime_fabric = runtime_contract_integration.get("runtime_fabric")
    if not isinstance(runtime_fabric, Mapping):
        runtime_fabric = {}

    aggregated_contract_gate = runtime_evaluation_snapshot.get(
        "aggregated_contract_gate",
    )
    if not isinstance(aggregated_contract_gate, Mapping):
        aggregated_contract_gate = {}

    raw_evaluation = runtime_evaluation_snapshot.get("raw_evaluation")
    if not isinstance(raw_evaluation, Mapping):
        raw_evaluation = {}

    evaluation_gate = runtime_evaluation_snapshot.get("evaluation_gate")
    if not isinstance(evaluation_gate, Mapping):
        evaluation_gate = {}

    nested_evaluation_gate = runtime_fabric.get("evaluation_gate")
    if not isinstance(nested_evaluation_gate, Mapping):
        nested_evaluation_gate = {}

    normalized_aggregated_contract_gate = (
        _normalize_runtime_verification_contract_result_mapping(
            aggregated_contract_gate,
        )
    )
    normalized_top_level_evaluation_gate = (
        _normalize_runtime_verification_evaluation_gate_mapping(evaluation_gate)
    )
    normalized_nested_evaluation_gate = (
        _normalize_runtime_verification_evaluation_gate_mapping(
            nested_evaluation_gate,
        )
    )
    expected_aggregated_contract_gate = _serialize_runtime_contract_gate_from_mapping(
        contract_gate,
    )
    evaluation_gate_alignment = _summarize_runtime_verification_evaluation_gate_alignment(
        normalized_aggregated_contract_gate,
        raw_evaluation,
        normalized_top_level_evaluation_gate,
    )
    aggregated_contract_gate_aligned = (
        normalized_aggregated_contract_gate == expected_aggregated_contract_gate
    )
    nested_evaluation_gate_aligned = (
        normalized_nested_evaluation_gate == normalized_top_level_evaluation_gate
    )
    runtime_evaluation_consistent = (
        aggregated_contract_gate_aligned
        and nested_evaluation_gate_aligned
        and evaluation_gate_alignment != "drifted"
    )
    prepared_fabric_guard_valid = (
        isinstance(prepared_fabric_guard, Mapping)
        and prepared_fabric_guard.get("is_valid") is True
    )
    serialized_snapshot_guard_valid = (
        isinstance(serialized_snapshot_guard, Mapping)
        and serialized_snapshot_guard.get("is_valid") is True
    )

    return {
        "prepared_fabric_guard_valid": prepared_fabric_guard_valid,
        "serialized_snapshot_guard_valid": serialized_snapshot_guard_valid,
        "runtime_evaluation_consistent": runtime_evaluation_consistent,
        "runtime_contract_valid": normalized_aggregated_contract_gate.get("is_valid")
        is True,
        "evaluation_gate_alignment": evaluation_gate_alignment,
        "aggregated_contract_gate_aligned": aggregated_contract_gate_aligned,
        "nested_evaluation_gate_aligned": nested_evaluation_gate_aligned,
        "verification_status": (
            "verified"
            if prepared_fabric_guard_valid
            and serialized_snapshot_guard_valid
            and runtime_evaluation_consistent
            else "failed"
        ),
    }


def _collect_runtime_verification_contract_result_errors(
    value: object,
    path: str,
    errors: list[str],
) -> None:
    if not isinstance(value, Mapping):
        errors.append(f"{path} must be a mapping")
        return

    if not isinstance(value.get("is_valid"), bool):
        errors.append(f"{path}.is_valid must be a bool")

    normalized_errors = value.get("errors")
    if not (
        isinstance(normalized_errors, tuple)
        or isinstance(normalized_errors, list)
        or normalized_errors is None
    ):
        errors.append(f"{path}.errors must be a tuple, list, or None")


def _collect_runtime_verification_evaluation_gate_errors(
    value: object,
    path: str,
    errors: list[str],
) -> None:
    if not isinstance(value, Mapping):
        errors.append(f"{path} must be a mapping")
        return

    if not isinstance(value.get("contract_valid"), bool):
        errors.append(f"{path}.contract_valid must be a bool")

    normalized_errors = value.get("errors")
    if not (
        isinstance(normalized_errors, tuple)
        or isinstance(normalized_errors, list)
        or normalized_errors is None
    ):
        errors.append(f"{path}.errors must be a tuple, list, or None")


def validate_runtime_evaluation_guard_verification_snapshot(
    snapshot: Mapping[str, object],
) -> ContractGateResult:
    if not isinstance(snapshot, Mapping):
        return ContractGateResult(
            is_valid=False,
            errors=("verification_snapshot must be a mapping",),
        )

    errors: list[str] = []
    runtime_evaluation = snapshot.get("runtime_evaluation")
    prepared_fabric_guard = snapshot.get("prepared_fabric_guard")
    serialized_snapshot_guard = snapshot.get("serialized_snapshot_guard")
    verification_summary = snapshot.get("verification_summary")

    if not isinstance(runtime_evaluation, Mapping):
        errors.append("verification_snapshot.runtime_evaluation must be a mapping")
        runtime_evaluation = {}
    else:
        runtime_contract_integration = runtime_evaluation.get(
            "runtime_contract_integration",
        )
        if not isinstance(runtime_contract_integration, Mapping):
            errors.append(
                "verification_snapshot.runtime_evaluation.runtime_contract_integration must be a mapping",
            )
            runtime_contract_integration = {}

        contract_gate = runtime_contract_integration.get("contract_gate")
        if not isinstance(contract_gate, Mapping):
            errors.append(
                "verification_snapshot.runtime_evaluation.runtime_contract_integration.contract_gate must be a mapping",
            )
            contract_gate = {}

        for key in _RUNTIME_CONTRACT_GATE_KEYS:
            _collect_runtime_verification_contract_result_errors(
                contract_gate.get(key),
                (
                    "verification_snapshot.runtime_evaluation."
                    f"runtime_contract_integration.contract_gate.{key}"
                ),
                errors,
            )

        runtime_fabric = runtime_contract_integration.get("runtime_fabric")
        if not isinstance(runtime_fabric, Mapping):
            errors.append(
                "verification_snapshot.runtime_evaluation.runtime_contract_integration.runtime_fabric must be a mapping",
            )
            runtime_fabric = {}

        _collect_runtime_verification_evaluation_gate_errors(
            runtime_fabric.get("evaluation_gate"),
            (
                "verification_snapshot.runtime_evaluation.runtime_contract_integration."
                "runtime_fabric.evaluation_gate"
            ),
            errors,
        )
        _collect_runtime_verification_contract_result_errors(
            runtime_evaluation.get("aggregated_contract_gate"),
            "verification_snapshot.runtime_evaluation.aggregated_contract_gate",
            errors,
        )

        raw_evaluation = runtime_evaluation.get("raw_evaluation")
        if not isinstance(raw_evaluation, Mapping):
            errors.append(
                "verification_snapshot.runtime_evaluation.raw_evaluation must be a mapping",
            )

        _collect_runtime_verification_evaluation_gate_errors(
            runtime_evaluation.get("evaluation_gate"),
            "verification_snapshot.runtime_evaluation.evaluation_gate",
            errors,
        )

    _collect_runtime_verification_contract_result_errors(
        prepared_fabric_guard,
        "verification_snapshot.prepared_fabric_guard",
        errors,
    )
    _collect_runtime_verification_contract_result_errors(
        serialized_snapshot_guard,
        "verification_snapshot.serialized_snapshot_guard",
        errors,
    )

    if not isinstance(verification_summary, Mapping):
        errors.append("verification_snapshot.verification_summary must be a mapping")
        verification_summary = None
    else:
        for key in (
            "prepared_fabric_guard_valid",
            "serialized_snapshot_guard_valid",
            "runtime_evaluation_consistent",
            "runtime_contract_valid",
            "aggregated_contract_gate_aligned",
            "nested_evaluation_gate_aligned",
        ):
            if not isinstance(verification_summary.get(key), bool):
                errors.append(
                    f"verification_snapshot.verification_summary.{key} must be a bool",
                )

        if verification_summary.get("evaluation_gate_alignment") not in _VERIFICATION_ALIGNMENTS:
            errors.append(
                "verification_snapshot.verification_summary.evaluation_gate_alignment must be aligned, fail_closed, or drifted",
            )

        if verification_summary.get("verification_status") not in _VERIFICATION_SUMMARY_STATUSES:
            errors.append(
                "verification_snapshot.verification_summary.verification_status must be verified or failed",
            )

    expected_summary = _summarize_runtime_evaluation_verification_snapshot(
        runtime_evaluation,
        prepared_fabric_guard if isinstance(prepared_fabric_guard, Mapping) else {},
        (
            serialized_snapshot_guard
            if isinstance(serialized_snapshot_guard, Mapping)
            else {}
        ),
    )

    if isinstance(verification_summary, Mapping):
        summary_mismatch_messages = {
            "prepared_fabric_guard_valid": (
                "verification_snapshot.verification_summary.prepared_fabric_guard_valid must match verification_snapshot.prepared_fabric_guard.is_valid"
            ),
            "serialized_snapshot_guard_valid": (
                "verification_snapshot.verification_summary.serialized_snapshot_guard_valid must match verification_snapshot.serialized_snapshot_guard.is_valid"
            ),
            "runtime_evaluation_consistent": (
                "verification_snapshot.verification_summary.runtime_evaluation_consistent must reflect aggregated contract, evaluation gate, and nested alignment semantics"
            ),
            "runtime_contract_valid": (
                "verification_snapshot.verification_summary.runtime_contract_valid must match verification_snapshot.runtime_evaluation.aggregated_contract_gate.is_valid"
            ),
            "evaluation_gate_alignment": (
                "verification_snapshot.verification_summary.evaluation_gate_alignment must match the runtime evaluation gate alignment"
            ),
            "aggregated_contract_gate_aligned": (
                "verification_snapshot.verification_summary.aggregated_contract_gate_aligned must match verification_snapshot.runtime_evaluation aggregated contract alignment"
            ),
            "nested_evaluation_gate_aligned": (
                "verification_snapshot.verification_summary.nested_evaluation_gate_aligned must match verification_snapshot.runtime_evaluation evaluation gate alignment"
            ),
            "verification_status": (
                "verification_snapshot.verification_summary.verification_status must match the derived verification status"
            ),
        }

        for key, message in summary_mismatch_messages.items():
            if verification_summary.get(key) != expected_summary[key]:
                errors.append(message)

    return ContractGateResult(is_valid=not errors, errors=tuple(errors))


def validate_worker_task(task: WorkerTask) -> ContractGateResult:
    errors: list[str] = []

    if not task.task_id:
        errors.append("task_id is required")
    if not task.worker_role:
        errors.append("worker_role is required")
    if not task.input_ref:
        errors.append("input_ref is required")
    if not task.task_status:
        errors.append("task_status is required")

    return ContractGateResult(is_valid=not errors, errors=tuple(errors))


def validate_worker_result(result: WorkerResult) -> ContractGateResult:
    errors: list[str] = []

    if not result.task_id:
        errors.append("task_id is required")
    if not result.worker_role:
        errors.append("worker_role is required")
    if not result.output_ref:
        errors.append("output_ref is required")
    if not result.result_status:
        errors.append("result_status is required")

    return ContractGateResult(is_valid=not errors, errors=tuple(errors))


def validate_task_transition(transition: TaskTransition) -> ContractGateResult:
    errors: list[str] = []

    if not transition.task_id:
        errors.append("task_id is required")
    if not transition.from_status:
        errors.append("from_status is required")
    if not transition.to_status:
        errors.append("to_status is required")
    if not transition.transition_ref:
        errors.append("transition_ref is required")

    return ContractGateResult(is_valid=not errors, errors=tuple(errors))


def validate_run_transition(transition: RunTransition) -> ContractGateResult:
    errors: list[str] = []

    if not transition.run_id:
        errors.append("run_id is required")
    if not transition.from_step:
        errors.append("from_step is required")
    if not transition.to_step:
        errors.append("to_step is required")
    if not transition.transition_ref:
        errors.append("transition_ref is required")

    return ContractGateResult(is_valid=not errors, errors=tuple(errors))


def validate_task_route(route: TaskRoute) -> ContractGateResult:
    errors: list[str] = []

    if not route.task_id:
        errors.append("task_id is required")
    if not route.source_role:
        errors.append("source_role is required")
    if not route.target_role:
        errors.append("target_role is required")
    if not route.route_ref:
        errors.append("route_ref is required")

    return ContractGateResult(is_valid=not errors, errors=tuple(errors))


def validate_orchestration_checkpoint(
    checkpoint: OrchestrationCheckpoint,
) -> ContractGateResult:
    errors: list[str] = []

    if not checkpoint.task_id:
        errors.append("task_id is required")
    if not checkpoint.output_ref:
        errors.append("output_ref is required")
    if not checkpoint.route_ref:
        errors.append("route_ref is required")
    if not checkpoint.checkpoint_ref:
        errors.append("checkpoint_ref is required")

    return ContractGateResult(is_valid=not errors, errors=tuple(errors))


def validate_orchestration_junction(
    junction: OrchestrationJunction,
) -> ContractGateResult:
    errors: list[str] = []

    if not junction.route_ref:
        errors.append("route_ref is required")
    if not junction.task_transition_ref:
        errors.append("task_transition_ref is required")
    if not junction.run_transition_ref:
        errors.append("run_transition_ref is required")
    if not junction.junction_ref:
        errors.append("junction_ref is required")

    return ContractGateResult(is_valid=not errors, errors=tuple(errors))


def validate_orchestration_verification(
    verification: OrchestrationVerification,
) -> ContractGateResult:
    errors: list[str] = []

    if not verification.checkpoint_ref:
        errors.append("checkpoint_ref is required")
    if not verification.junction_ref:
        errors.append("junction_ref is required")
    if not verification.task_transition_ref:
        errors.append("task_transition_ref is required")
    if not verification.verification_ref:
        errors.append("verification_ref is required")

    return ContractGateResult(is_valid=not errors, errors=tuple(errors))


def validate_orchestration_outcome(
    outcome: OrchestrationOutcome,
) -> ContractGateResult:
    errors: list[str] = []

    if not outcome.verification_ref:
        errors.append("verification_ref is required")
    if not outcome.decision_ref:
        errors.append("decision_ref is required")
    if not outcome.evaluation_ref:
        errors.append("evaluation_ref is required")
    if not outcome.outcome_ref:
        errors.append("outcome_ref is required")

    return ContractGateResult(is_valid=not errors, errors=tuple(errors))


def validate_orchestration_evidence(
    evidence: OrchestrationEvidence,
) -> ContractGateResult:
    errors: list[str] = []

    if not evidence.verification_ref:
        errors.append("verification_ref is required")
    if not evidence.outcome_ref:
        errors.append("outcome_ref is required")
    if not evidence.evaluation_ref:
        errors.append("evaluation_ref is required")
    if not evidence.evidence_ref:
        errors.append("evidence_ref is required")

    return ContractGateResult(is_valid=not errors, errors=tuple(errors))


def validate_orchestration_gate(
    gate: OrchestrationGate,
) -> ContractGateResult:
    errors: list[str] = []

    if not gate.evidence_ref:
        errors.append("evidence_ref is required")
    if not gate.evaluation_gate_ref:
        errors.append("evaluation_gate_ref is required")
    if not gate.audit_ref:
        errors.append("audit_ref is required")
    if not gate.gate_ref:
        errors.append("gate_ref is required")

    return ContractGateResult(is_valid=not errors, errors=tuple(errors))


def validate_orchestration_audit(
    audit: OrchestrationAudit,
) -> ContractGateResult:
    errors: list[str] = []

    if not audit.gate_ref:
        errors.append("gate_ref is required")
    if not audit.evaluation_gate_ref:
        errors.append("evaluation_gate_ref is required")
    if not audit.audit_event_ref:
        errors.append("audit_event_ref is required")
    if not audit.audit_ref:
        errors.append("audit_ref is required")

    return ContractGateResult(is_valid=not errors, errors=tuple(errors))


def validate_orchestration_closure(
    closure: OrchestrationClosure,
) -> ContractGateResult:
    errors: list[str] = []

    if not closure.audit_ref:
        errors.append("audit_ref is required")
    if not closure.decision_ref:
        errors.append("decision_ref is required")
    if not closure.evaluation_ref:
        errors.append("evaluation_ref is required")
    if not closure.closure_ref:
        errors.append("closure_ref is required")

    return ContractGateResult(is_valid=not errors, errors=tuple(errors))


def validate_orchestration_lineage(
    lineage: OrchestrationLineage,
) -> ContractGateResult:
    errors: list[str] = []

    if not lineage.closure_ref:
        errors.append("closure_ref is required")
    if not lineage.audit_ref:
        errors.append("audit_ref is required")
    if not lineage.outcome_ref:
        errors.append("outcome_ref is required")
    if not lineage.lineage_ref:
        errors.append("lineage_ref is required")

    return ContractGateResult(is_valid=not errors, errors=tuple(errors))


def validate_orchestration_manifest(
    manifest: OrchestrationManifest,
) -> ContractGateResult:
    errors: list[str] = []

    if not manifest.lineage_ref:
        errors.append("lineage_ref is required")
    if not manifest.closure_ref:
        errors.append("closure_ref is required")
    if not manifest.evidence_ref:
        errors.append("evidence_ref is required")
    if not manifest.manifest_ref:
        errors.append("manifest_ref is required")

    return ContractGateResult(is_valid=not errors, errors=tuple(errors))


def validate_orchestration_review(
    review: OrchestrationReview,
) -> ContractGateResult:
    errors: list[str] = []

    if not review.manifest_ref:
        errors.append("manifest_ref is required")
    if not review.lineage_ref:
        errors.append("lineage_ref is required")
    if not review.closure_ref:
        errors.append("closure_ref is required")
    if not review.review_ref:
        errors.append("review_ref is required")

    return ContractGateResult(is_valid=not errors, errors=tuple(errors))


def validate_orchestration_publication(
    publication: OrchestrationPublication,
) -> ContractGateResult:
    errors: list[str] = []

    if not publication.assertion_ref:
        errors.append("assertion_ref is required")
    if not publication.review_ref:
        errors.append("review_ref is required")
    if not publication.manifest_ref:
        errors.append("manifest_ref is required")
    if not publication.publication_ref:
        errors.append("publication_ref is required")

    return ContractGateResult(is_valid=not errors, errors=tuple(errors))


def validate_orchestration_release_view(
    release_view: OrchestrationReleaseView,
) -> ContractGateResult:
    errors: list[str] = []

    if not release_view.publication_ref:
        errors.append("publication_ref is required")
    if not release_view.assertion_ref:
        errors.append("assertion_ref is required")
    if not release_view.review_ref:
        errors.append("review_ref is required")
    if not release_view.release_view_ref:
        errors.append("release_view_ref is required")

    return ContractGateResult(is_valid=not errors, errors=tuple(errors))


def validate_orchestration_assertion(
    assertion: OrchestrationAssertion,
) -> ContractGateResult:
    errors: list[str] = []

    if not assertion.review_ref:
        errors.append("review_ref is required")
    if not assertion.manifest_ref:
        errors.append("manifest_ref is required")
    if not assertion.lineage_ref:
        errors.append("lineage_ref is required")
    if not assertion.assertion_ref:
        errors.append("assertion_ref is required")

    return ContractGateResult(is_valid=not errors, errors=tuple(errors))
