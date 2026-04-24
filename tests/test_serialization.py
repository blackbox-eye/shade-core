from shade_core import (  # noqa: E402
    MetaAuditEvent,
    RuntimeDecision,
    serialize_evaluation_result,
    serialize_meta_audit_event,
    serialize_runtime_decision,
)
from shade_core.models import ArtifactHandoff, TaskRoute, WorkerResult, WorkerTask
from shade_core.serialization import (
    serialize_artifact_handoff,
    serialize_task_route,
    serialize_worker_result,
    serialize_worker_task,
)


def test_serialize_runtime_decision() -> None:
    decision = RuntimeDecision(
        decision="accept",
        reason="clear",
        next_step="continue",
    )

    assert serialize_runtime_decision(decision) == {
        "decision": "accept",
        "reason": "clear",
        "next_step": "continue",
    }


def test_serialize_artifact_handoff() -> None:
    handoff = ArtifactHandoff(
        artifact_ref="artifact-1",
        source_lane="analysis-lane",
        target_lane="review-lane",
    )

    assert serialize_artifact_handoff(handoff) == {
        "artifact_ref": "artifact-1",
        "source_lane": "analysis-lane",
        "target_lane": "review-lane",
    }


def test_serialize_meta_audit_event() -> None:
    event = MetaAuditEvent(
        event_type="runtime_decision",
        message="accept: clear",
        severity="info",
        reference="ref-1",
        run_id="run-1",
    )

    assert serialize_meta_audit_event(event) == {
        "event_type": "runtime_decision",
        "message": "accept: clear",
        "severity": "info",
        "reference": "ref-1",
        "run_id": "run-1",
    }


def test_serialize_evaluation_result() -> None:
    assert serialize_evaluation_result("review") == {"result": "review"}


def test_serialize_worker_task() -> None:
    task = WorkerTask(
        task_id="task-1",
        worker_role="analysis",
        input_ref="artifact-1",
        task_status="pending",
    )

    assert serialize_worker_task(task) == {
        "task_id": "task-1",
        "worker_role": "analysis",
        "input_ref": "artifact-1",
        "task_status": "pending",
    }


def test_serialize_worker_result() -> None:
    result = WorkerResult(
        task_id="task-1",
        worker_role="analysis",
        output_ref="output-1",
        result_status="complete",
    )

    assert serialize_worker_result(result) == {
        "task_id": "task-1",
        "worker_role": "analysis",
        "output_ref": "output-1",
        "result_status": "complete",
    }


def test_serialize_task_route() -> None:
    route = TaskRoute(
        task_id="task-1",
        source_role="analysis",
        target_role="review",
        route_ref="route-1",
    )

    assert serialize_task_route(route) == {
        "task_id": "task-1",
        "source_role": "analysis",
        "target_role": "review",
        "route_ref": "route-1",
    }
