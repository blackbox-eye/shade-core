from shade_core import (  # noqa: E402
    MetaAuditEvent,
    RuntimeDecision,
    serialize_evaluation_result,
    serialize_meta_audit_event,
    serialize_runtime_decision,
)
from shade_core.models import (
    ArtifactHandoff,
    OrchestrationCheckpoint,
    OrchestrationJunction,
    OrchestrationOutcome,
    OrchestrationVerification,
    RunTransition,
    TaskRoute,
    TaskTransition,
    WorkerResult,
    WorkerTask,
)
from shade_core.serialization import (
    serialize_artifact_handoff,
    serialize_orchestration_checkpoint,
    serialize_orchestration_junction,
    serialize_orchestration_outcome,
    serialize_orchestration_verification,
    serialize_run_transition,
    serialize_task_route,
    serialize_task_transition,
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


def test_serialize_orchestration_checkpoint() -> None:
    checkpoint = OrchestrationCheckpoint(
        task_id="task-1",
        output_ref="output-1",
        route_ref="route-1",
        checkpoint_ref="checkpoint-1",
    )

    assert serialize_orchestration_checkpoint(checkpoint) == {
        "task_id": "task-1",
        "output_ref": "output-1",
        "route_ref": "route-1",
        "checkpoint_ref": "checkpoint-1",
    }


def test_serialize_orchestration_junction() -> None:
    junction = OrchestrationJunction(
        route_ref="route-1",
        task_transition_ref="task-transition-1",
        run_transition_ref="run-transition-1",
        junction_ref="junction-1",
    )

    assert serialize_orchestration_junction(junction) == {
        "route_ref": "route-1",
        "task_transition_ref": "task-transition-1",
        "run_transition_ref": "run-transition-1",
        "junction_ref": "junction-1",
    }


def test_serialize_orchestration_verification() -> None:
    verification = OrchestrationVerification(
        checkpoint_ref="checkpoint-1",
        junction_ref="junction-1",
        task_transition_ref="task-transition-1",
        verification_ref="verification-1",
    )

    assert serialize_orchestration_verification(verification) == {
        "checkpoint_ref": "checkpoint-1",
        "junction_ref": "junction-1",
        "task_transition_ref": "task-transition-1",
        "verification_ref": "verification-1",
    }


def test_serialize_orchestration_outcome() -> None:
    outcome = OrchestrationOutcome(
        verification_ref="verification-1",
        decision_ref="decision-1",
        evaluation_ref="evaluation-1",
        outcome_ref="outcome-1",
    )

    assert serialize_orchestration_outcome(outcome) == {
        "verification_ref": "verification-1",
        "decision_ref": "decision-1",
        "evaluation_ref": "evaluation-1",
        "outcome_ref": "outcome-1",
    }


def test_serialize_task_transition() -> None:
    transition = TaskTransition(
        task_id="task-1",
        from_status="pending",
        to_status="running",
        transition_ref="tr-1",
    )

    assert serialize_task_transition(transition) == {
        "task_id": "task-1",
        "from_status": "pending",
        "to_status": "running",
        "transition_ref": "tr-1",
    }


def test_serialize_run_transition() -> None:
    transition = RunTransition(
        run_id="run-1",
        from_step="ingest",
        to_step="evaluate",
        transition_ref="tr-2",
    )

    assert serialize_run_transition(transition) == {
        "run_id": "run-1",
        "from_step": "ingest",
        "to_step": "evaluate",
        "transition_ref": "tr-2",
    }
