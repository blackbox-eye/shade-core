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
from shade_core.bundle import _build_audit_closure_snapshot  # noqa: E402
from shade_core.bundle import _build_checkpoint_junction_snapshot  # noqa: E402
from shade_core.bundle import _build_evidence_gate_snapshot  # noqa: E402
from shade_core.bundle import _build_lineage_manifest_snapshot  # noqa: E402
from shade_core.bundle import _build_review_assertion_snapshot  # noqa: E402
from shade_core.bundle import _build_publication_release_view_snapshot  # noqa: E402
from shade_core.bundle import _build_orchestration_contract_snapshot, _build_runtime_fabric_snapshot, _build_state_transition_snapshot  # noqa: E402
from shade_core.bundle import _build_verification_outcome_snapshot  # noqa: E402
from shade_core.models import (  # noqa: E402
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
    RunTransition,
    TaskRoute,
    TaskTransition,
    WorkerResult,
    WorkerTask,
)


def test_build_bundle_returns_expected_structure() -> None:
    decision = RuntimeDecision(
        decision="accept",
        reason="Confidence 0.90 meets threshold",
        next_step="continue",
    )
    event = MetaAuditEvent(
        event_type="runtime_decision",
        message="accept: Confidence 0.90 meets threshold",
        severity="info",
        reference="ref-1",
        run_id="run-1",
    )

    assert build_bundle(decision, event, "pass") == {
        "decision": {
            "decision": "accept",
            "reason": "Confidence 0.90 meets threshold",
            "next_step": "continue",
        },
        "audit_event": {
            "event_type": "runtime_decision",
            "message": "accept: Confidence 0.90 meets threshold",
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
        reason="Confidence 0.90 meets threshold",
        next_step="continue",
    )
    event = MetaAuditEvent(
        event_type="runtime_decision",
        message="accept: Confidence 0.90 meets threshold",
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
            "reason": "Confidence 0.90 meets threshold",
            "next_step": "continue",
        },
        "audit_event": {
            "event_type": "runtime_decision",
            "message": "accept: Confidence 0.90 meets threshold",
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


def test_build_state_transition_snapshot_returns_expected_structure() -> None:
    task_transition = TaskTransition(
        task_id="task-1",
        from_status="pending",
        to_status="running",
        transition_ref="tr-1",
    )
    run_transition = RunTransition(
        run_id="run-1",
        from_step="ingest",
        to_step="evaluate",
        transition_ref="tr-2",
    )

    assert _build_state_transition_snapshot(task_transition, run_transition) == {
        "task_transition": {
            "task_id": "task-1",
            "from_status": "pending",
            "to_status": "running",
            "transition_ref": "tr-1",
        },
        "run_transition": {
            "run_id": "run-1",
            "from_step": "ingest",
            "to_step": "evaluate",
            "transition_ref": "tr-2",
        },
    }


def test_build_checkpoint_junction_snapshot_returns_expected_structure() -> None:
    checkpoint = OrchestrationCheckpoint(
        task_id="task-1",
        output_ref="output-1",
        route_ref="route-1",
        checkpoint_ref="checkpoint-1",
    )
    junction = OrchestrationJunction(
        route_ref="route-1",
        task_transition_ref="task-transition-1",
        run_transition_ref="run-transition-1",
        junction_ref="junction-1",
    )

    assert _build_checkpoint_junction_snapshot(checkpoint, junction) == {
        "orchestration_checkpoint": {
            "task_id": "task-1",
            "output_ref": "output-1",
            "route_ref": "route-1",
            "checkpoint_ref": "checkpoint-1",
        },
        "orchestration_junction": {
            "route_ref": "route-1",
            "task_transition_ref": "task-transition-1",
            "run_transition_ref": "run-transition-1",
            "junction_ref": "junction-1",
        },
    }


def test_build_verification_outcome_snapshot_returns_expected_structure() -> None:
    verification = OrchestrationVerification(
        checkpoint_ref="checkpoint-1",
        junction_ref="junction-1",
        task_transition_ref="task-transition-1",
        verification_ref="verification-1",
    )
    outcome = OrchestrationOutcome(
        verification_ref="verification-1",
        decision_ref="decision-1",
        evaluation_ref="evaluation-1",
        outcome_ref="outcome-1",
    )

    assert _build_verification_outcome_snapshot(verification, outcome) == {
        "orchestration_verification": {
            "checkpoint_ref": "checkpoint-1",
            "junction_ref": "junction-1",
            "task_transition_ref": "task-transition-1",
            "verification_ref": "verification-1",
        },
        "orchestration_outcome": {
            "verification_ref": "verification-1",
            "decision_ref": "decision-1",
            "evaluation_ref": "evaluation-1",
            "outcome_ref": "outcome-1",
        },
    }


def test_build_evidence_gate_snapshot_returns_expected_structure() -> None:
    evidence = OrchestrationEvidence(
        verification_ref="verification-1",
        outcome_ref="outcome-1",
        evaluation_ref="evaluation-1",
        evidence_ref="evidence-1",
    )
    gate = OrchestrationGate(
        evidence_ref="evidence-1",
        evaluation_gate_ref="evaluation-gate-1",
        audit_ref="audit-1",
        gate_ref="gate-1",
    )

    assert _build_evidence_gate_snapshot(evidence, gate) == {
        "orchestration_evidence": {
            "verification_ref": "verification-1",
            "outcome_ref": "outcome-1",
            "evaluation_ref": "evaluation-1",
            "evidence_ref": "evidence-1",
        },
        "orchestration_gate": {
            "evidence_ref": "evidence-1",
            "evaluation_gate_ref": "evaluation-gate-1",
            "audit_ref": "audit-1",
            "gate_ref": "gate-1",
        },
    }


def test_build_audit_closure_snapshot_returns_expected_structure() -> None:
    audit = OrchestrationAudit(
        gate_ref="gate-1",
        evaluation_gate_ref="evaluation-gate-1",
        audit_event_ref="audit-event-1",
        audit_ref="audit-1",
    )
    closure = OrchestrationClosure(
        audit_ref="audit-1",
        decision_ref="decision-1",
        evaluation_ref="evaluation-1",
        closure_ref="closure-1",
    )

    assert _build_audit_closure_snapshot(audit, closure) == {
        "orchestration_audit": {
            "gate_ref": "gate-1",
            "evaluation_gate_ref": "evaluation-gate-1",
            "audit_event_ref": "audit-event-1",
            "audit_ref": "audit-1",
        },
        "orchestration_closure": {
            "audit_ref": "audit-1",
            "decision_ref": "decision-1",
            "evaluation_ref": "evaluation-1",
            "closure_ref": "closure-1",
        },
    }


def test_build_lineage_manifest_snapshot_returns_expected_structure() -> None:
    lineage = OrchestrationLineage(
        closure_ref="closure-1",
        audit_ref="audit-1",
        outcome_ref="outcome-1",
        lineage_ref="lineage-1",
    )
    manifest = OrchestrationManifest(
        lineage_ref="lineage-1",
        closure_ref="closure-1",
        evidence_ref="evidence-1",
        manifest_ref="manifest-1",
    )

    assert _build_lineage_manifest_snapshot(lineage, manifest) == {
        "orchestration_lineage": {
            "closure_ref": "closure-1",
            "audit_ref": "audit-1",
            "outcome_ref": "outcome-1",
            "lineage_ref": "lineage-1",
        },
        "orchestration_manifest": {
            "lineage_ref": "lineage-1",
            "closure_ref": "closure-1",
            "evidence_ref": "evidence-1",
            "manifest_ref": "manifest-1",
        },
    }


def test_build_review_assertion_snapshot_returns_expected_structure() -> None:
    review = OrchestrationReview(
        manifest_ref="manifest-1",
        lineage_ref="lineage-1",
        closure_ref="closure-1",
        review_ref="review-1",
    )
    assertion = OrchestrationAssertion(
        review_ref="review-1",
        manifest_ref="manifest-1",
        lineage_ref="lineage-1",
        assertion_ref="assertion-1",
    )

    assert _build_review_assertion_snapshot(review, assertion) == {
        "orchestration_review": {
            "manifest_ref": "manifest-1",
            "lineage_ref": "lineage-1",
            "closure_ref": "closure-1",
            "review_ref": "review-1",
        },
        "orchestration_assertion": {
            "review_ref": "review-1",
            "manifest_ref": "manifest-1",
            "lineage_ref": "lineage-1",
            "assertion_ref": "assertion-1",
        },
    }


def test_build_publication_release_view_snapshot_returns_expected_structure() -> None:
    publication = OrchestrationPublication(
        assertion_ref="assertion-1",
        review_ref="review-1",
        manifest_ref="manifest-1",
        publication_ref="publication-1",
    )
    release_view = OrchestrationReleaseView(
        publication_ref="publication-1",
        assertion_ref="assertion-1",
        review_ref="review-1",
        release_view_ref="release-view-1",
    )

    assert _build_publication_release_view_snapshot(publication, release_view) == {
        "orchestration_publication": {
            "assertion_ref": "assertion-1",
            "review_ref": "review-1",
            "manifest_ref": "manifest-1",
            "publication_ref": "publication-1",
        },
        "orchestration_release_view": {
            "publication_ref": "publication-1",
            "assertion_ref": "assertion-1",
            "review_ref": "review-1",
            "release_view_ref": "release-view-1",
        },
    }
