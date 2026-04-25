from __future__ import annotations

from dataclasses import dataclass

from .models import (
    ArtifactHandoff,
    OrchestrationCheckpoint,
    OrchestrationJunction,
    RunTransition,
    TaskRoute,
    TaskTransition,
    WorkerResult,
    WorkerTask,
)
from .state import RunState

_DECISION_CLASSES = {"accept", "reject", "needs_review"}
_VERIFICATION_STATES = {"pending", "verified", "failed"}


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
