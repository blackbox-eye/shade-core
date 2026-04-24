from shade_core import RunState, validate_state_contract
from shade_core.contract_gate import (
    validate_artifact_handoff,
    validate_task_route,
    validate_worker_result,
    validate_worker_task,
)
from shade_core.models import ArtifactHandoff, TaskRoute, WorkerResult, WorkerTask


def test_validate_state_contract_passes_for_valid_state() -> None:
    state = RunState(
        run_id="run-1",
        worker_role="analysis",
        decision_class="accept",
        verification_state="verified",
        artifact_ref="artifact-1",
        source_lane="adapter-a",
        target_lane="adapter-b",
    )

    result = validate_state_contract(state)

    assert result.is_valid is True
    assert result.errors == ()


def test_validate_state_contract_fails_for_invalid_state() -> None:
    state = RunState(
        run_id="",
        worker_role="",
        decision_class="accept",
        verification_state="pending",
        artifact_ref="",
        source_lane="",
        target_lane="adapter-b",
    )

    result = validate_state_contract(state)

    assert result.is_valid is False
    assert result.errors == (
        "run_id is required",
        "worker_role is required",
        "artifact_ref is required",
        "source_lane is required",
    )


def test_validate_artifact_handoff_passes_for_valid_handoff() -> None:
    handoff = ArtifactHandoff(
        artifact_ref="artifact-1",
        source_lane="analysis-lane",
        target_lane="review-lane",
    )

    result = validate_artifact_handoff(handoff)

    assert result.is_valid is True
    assert result.errors == ()


def test_validate_artifact_handoff_fails_for_invalid_handoff() -> None:
    handoff = ArtifactHandoff(
        artifact_ref="",
        source_lane="",
        target_lane="",
    )

    result = validate_artifact_handoff(handoff)

    assert result.is_valid is False
    assert result.errors == (
        "artifact_ref is required",
        "source_lane is required",
        "target_lane is required",
    )


def test_validate_worker_task_passes_for_valid_task() -> None:
    task = WorkerTask(
        task_id="task-1",
        worker_role="analysis",
        input_ref="artifact-1",
        task_status="pending",
    )

    result = validate_worker_task(task)

    assert result.is_valid is True
    assert result.errors == ()


def test_validate_worker_task_fails_for_invalid_task() -> None:
    task = WorkerTask(
        task_id="",
        worker_role="",
        input_ref="",
        task_status="",
    )

    result = validate_worker_task(task)

    assert result.is_valid is False
    assert result.errors == (
        "task_id is required",
        "worker_role is required",
        "input_ref is required",
        "task_status is required",
    )


def test_validate_worker_result_passes_for_valid_result() -> None:
    worker_result = WorkerResult(
        task_id="task-1",
        worker_role="analysis",
        output_ref="output-1",
        result_status="complete",
    )

    result = validate_worker_result(worker_result)

    assert result.is_valid is True
    assert result.errors == ()


def test_validate_worker_result_fails_for_invalid_result() -> None:
    worker_result = WorkerResult(
        task_id="",
        worker_role="",
        output_ref="",
        result_status="",
    )

    result = validate_worker_result(worker_result)

    assert result.is_valid is False
    assert result.errors == (
        "task_id is required",
        "worker_role is required",
        "output_ref is required",
        "result_status is required",
    )


def test_validate_task_route_passes_for_valid_route() -> None:
    route = TaskRoute(
        task_id="task-1",
        source_role="analysis",
        target_role="review",
        route_ref="route-1",
    )

    result = validate_task_route(route)

    assert result.is_valid is True
    assert result.errors == ()


def test_validate_task_route_fails_for_invalid_route() -> None:
    route = TaskRoute(
        task_id="",
        source_role="",
        target_role="",
        route_ref="",
    )

    result = validate_task_route(route)

    assert result.is_valid is False
    assert result.errors == (
        "task_id is required",
        "source_role is required",
        "target_role is required",
        "route_ref is required",
    )
