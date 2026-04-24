from __future__ import annotations

from .evaluation import EvaluationResult
from .evaluation_gate import EvaluationGateResult
from .models import ArtifactHandoff, MetaAuditEvent, RuntimeDecision, RunTransition, TaskRoute, TaskTransition, WorkerResult, WorkerTask
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
