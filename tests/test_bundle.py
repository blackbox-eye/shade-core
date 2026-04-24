from pathlib import Path
import sys


src_path = Path(__file__).resolve().parents[1] / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from shade_core import (  # noqa: E402
    EvaluationGateResult,
    MetaAuditEvent,
    RunState,
    RuntimeDecision,
    build_bundle,
)
from shade_core.bundle import _build_orchestration_contract_snapshot, _build_runtime_fabric_snapshot  # noqa: E402
from shade_core.models import TaskRoute, WorkerResult, WorkerTask  # noqa: E402


def test_build_bundle_returns_expected_structure() -> None:
    decision = RuntimeDecision(
        decision="accept",
        reason="clear",
        next_step="continue",
    )
    event = MetaAuditEvent(
        event_type="runtime_decision",
        message="accept: clear",
        severity="info",
        reference="ref-1",
        run_id="run-1",
    )

    assert build_bundle(decision, event, "pass") == {
        "decision": {
            "decision": "accept",
            "reason": "clear",
            "next_step": "continue",
        },
        "audit_event": {
            "event_type": "runtime_decision",
            "message": "accept: clear",
            "severity": "info",
            "reference": "ref-1",
            "run_id": "run-1",
        },
        "evaluation": {
            "result": "pass",
        },
    }


def test_build_runtime_fabric_snapshot_returns_expected_structure() -> None:
    state = RunState(
        run_id="run-1",
        worker_role="control",
        decision_class="accept",
        verification_state="verified",
        artifact_ref="artifact-1",
        source_lane="analysis-lane",
        target_lane="review-lane",
    )
    decision = RuntimeDecision(
        decision="accept",
        reason="clear",
        next_step="continue",
    )
    event = MetaAuditEvent(
        event_type="runtime_decision",
        message="accept: clear",
        severity="info",
        reference="ref-1",
        run_id="run-1",
    )
    evaluation_gate_result = EvaluationGateResult(
        result="pass",
        contract_valid=True,
        errors=(),
    )

    assert _build_runtime_fabric_snapshot(
        state,
        decision,
        event,
        evaluation_gate_result,
    ) == {
        "run_state": {
            "run_id": "run-1",
            "worker_role": "control",
            "decision_class": "accept",
            "verification_state": "verified",
            "artifact_ref": "artifact-1",
            "source_lane": "analysis-lane",
            "target_lane": "review-lane",
        },
        "artifact_handoff": {
            "artifact_ref": "artifact-1",
            "source_lane": "analysis-lane",
            "target_lane": "review-lane",
        },
        "decision": {
            "decision": "accept",
            "reason": "clear",
            "next_step": "continue",
        },
        "audit_event": {
            "event_type": "runtime_decision",
            "message": "accept: clear",
            "severity": "info",
            "reference": "ref-1",
            "run_id": "run-1",
        },
        "evaluation_gate": {
            "result": "pass",
            "contract_valid": True,
            "errors": (),
        },
    }


def test_build_orchestration_contract_snapshot_returns_expected_structure() -> None:
    task = WorkerTask(
        task_id="task-1",
        worker_role="analysis",
        input_ref="artifact-1",
        task_status="pending",
    )
    result = WorkerResult(
        task_id="task-1",
        worker_role="analysis",
        output_ref="output-1",
        result_status="complete",
    )
    route = TaskRoute(
        task_id="task-1",
        source_role="analysis",
        target_role="review",
        route_ref="route-1",
    )

    assert _build_orchestration_contract_snapshot(task, result, route) == {
        "worker_task": {
            "task_id": "task-1",
            "worker_role": "analysis",
            "input_ref": "artifact-1",
            "task_status": "pending",
        },
        "worker_result": {
            "task_id": "task-1",
            "worker_role": "analysis",
            "output_ref": "output-1",
            "result_status": "complete",
        },
        "task_route": {
            "task_id": "task-1",
            "source_role": "analysis",
            "target_role": "review",
            "route_ref": "route-1",
        },
    }
