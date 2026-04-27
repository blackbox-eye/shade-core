from shade_core import (  # noqa: E402
    ConfidenceRecord,
    MetaAuditEvent,
    RuntimeDecision,
    SelfModel,
    WorkerRegistry,
)
from shade_core.models import (
    ArtifactHandoff,
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


def test_model_instantiation_smoke() -> None:
    self_model = SelfModel(agent_id="shade-v1", role="control", state="idle")
    registry = WorkerRegistry()
    registry.register(name="analysis-worker", role="analysis", status="ready")
    confidence = ConfidenceRecord(
        score=0.8,
        source="local-review",
        reason="Short and inspectable",
        reference="ref-1",
    )
    event = MetaAuditEvent(
        event_type="contract_check",
        message="OK",
        severity="info",
        reference="ref-1",
        run_id="run-1",
    )
    decision = RuntimeDecision(
        decision="needs_review",
        reason="Needs manual approval",
        next_step="review",
    )

    assert self_model.agent_id == "shade-v1"
    assert registry.workers["analysis-worker"] == ("analysis", "ready")
    assert confidence.reference == "ref-1"
    assert event.run_id == "run-1"
    assert decision.decision == "needs_review"


def test_artifact_handoff_retains_fields() -> None:
    handoff = ArtifactHandoff(
        artifact_ref="artifact-1",
        source_lane="analysis-lane",
        target_lane="review-lane",
    )

    assert handoff.artifact_ref == "artifact-1"
    assert handoff.source_lane == "analysis-lane"
    assert handoff.target_lane == "review-lane"


def test_worker_task_retains_fields() -> None:
    task = WorkerTask(
        task_id="task-1",
        worker_role="analysis",
        input_ref="artifact-1",
        task_status="pending",
    )

    assert task.task_id == "task-1"
    assert task.worker_role == "analysis"
    assert task.input_ref == "artifact-1"
    assert task.task_status == "pending"


def test_worker_result_retains_fields() -> None:
    result = WorkerResult(
        task_id="task-1",
        worker_role="analysis",
        output_ref="output-1",
        result_status="complete",
    )

    assert result.task_id == "task-1"
    assert result.worker_role == "analysis"
    assert result.output_ref == "output-1"
    assert result.result_status == "complete"


def test_task_route_retains_fields() -> None:
    route = TaskRoute(
        task_id="task-1",
        source_role="analysis",
        target_role="review",
        route_ref="route-1",
    )

    assert route.task_id == "task-1"
    assert route.source_role == "analysis"
    assert route.target_role == "review"
    assert route.route_ref == "route-1"


def test_orchestration_checkpoint_retains_fields() -> None:
    checkpoint = OrchestrationCheckpoint(
        task_id="task-1",
        output_ref="output-1",
        route_ref="route-1",
        checkpoint_ref="checkpoint-1",
    )

    assert checkpoint.task_id == "task-1"
    assert checkpoint.output_ref == "output-1"
    assert checkpoint.route_ref == "route-1"
    assert checkpoint.checkpoint_ref == "checkpoint-1"


def test_orchestration_junction_retains_fields() -> None:
    junction = OrchestrationJunction(
        route_ref="route-1",
        task_transition_ref="task-transition-1",
        run_transition_ref="run-transition-1",
        junction_ref="junction-1",
    )

    assert junction.route_ref == "route-1"
    assert junction.task_transition_ref == "task-transition-1"
    assert junction.run_transition_ref == "run-transition-1"
    assert junction.junction_ref == "junction-1"


def test_orchestration_verification_retains_fields() -> None:
    verification = OrchestrationVerification(
        checkpoint_ref="checkpoint-1",
        junction_ref="junction-1",
        task_transition_ref="task-transition-1",
        verification_ref="verification-1",
    )

    assert verification.checkpoint_ref == "checkpoint-1"
    assert verification.junction_ref == "junction-1"
    assert verification.task_transition_ref == "task-transition-1"
    assert verification.verification_ref == "verification-1"


def test_orchestration_outcome_retains_fields() -> None:
    outcome = OrchestrationOutcome(
        verification_ref="verification-1",
        decision_ref="decision-1",
        evaluation_ref="evaluation-1",
        outcome_ref="outcome-1",
    )

    assert outcome.verification_ref == "verification-1"
    assert outcome.decision_ref == "decision-1"
    assert outcome.evaluation_ref == "evaluation-1"
    assert outcome.outcome_ref == "outcome-1"


def test_orchestration_evidence_retains_fields() -> None:
    evidence = OrchestrationEvidence(
        verification_ref="verification-1",
        outcome_ref="outcome-1",
        evaluation_ref="evaluation-1",
        evidence_ref="evidence-1",
    )

    assert evidence.verification_ref == "verification-1"
    assert evidence.outcome_ref == "outcome-1"
    assert evidence.evaluation_ref == "evaluation-1"
    assert evidence.evidence_ref == "evidence-1"


def test_orchestration_gate_retains_fields() -> None:
    gate = OrchestrationGate(
        evidence_ref="evidence-1",
        evaluation_gate_ref="evaluation-gate-1",
        audit_ref="audit-1",
        gate_ref="gate-1",
    )

    assert gate.evidence_ref == "evidence-1"
    assert gate.evaluation_gate_ref == "evaluation-gate-1"
    assert gate.audit_ref == "audit-1"
    assert gate.gate_ref == "gate-1"


def test_orchestration_audit_retains_fields() -> None:
    audit = OrchestrationAudit(
        gate_ref="gate-1",
        evaluation_gate_ref="evaluation-gate-1",
        audit_event_ref="audit-event-1",
        audit_ref="audit-1",
    )

    assert audit.gate_ref == "gate-1"
    assert audit.evaluation_gate_ref == "evaluation-gate-1"
    assert audit.audit_event_ref == "audit-event-1"
    assert audit.audit_ref == "audit-1"


def test_orchestration_closure_retains_fields() -> None:
    closure = OrchestrationClosure(
        audit_ref="audit-1",
        decision_ref="decision-1",
        evaluation_ref="evaluation-1",
        closure_ref="closure-1",
    )

    assert closure.audit_ref == "audit-1"
    assert closure.decision_ref == "decision-1"
    assert closure.evaluation_ref == "evaluation-1"
    assert closure.closure_ref == "closure-1"


def test_task_transition_retains_fields() -> None:
    transition = TaskTransition(
        task_id="task-1",
        from_status="pending",
        to_status="running",
        transition_ref="tr-1",
    )

    assert transition.task_id == "task-1"
    assert transition.from_status == "pending"
    assert transition.to_status == "running"
    assert transition.transition_ref == "tr-1"


def test_run_transition_retains_fields() -> None:
    transition = RunTransition(
        run_id="run-1",
        from_step="ingest",
        to_step="evaluate",
        transition_ref="tr-2",
    )

    assert transition.run_id == "run-1"
    assert transition.from_step == "ingest"
    assert transition.to_step == "evaluate"
    assert transition.transition_ref == "tr-2"


def test_orchestration_lineage_retains_fields() -> None:
    lineage = OrchestrationLineage(
        closure_ref="closure-1",
        audit_ref="audit-1",
        outcome_ref="outcome-1",
        lineage_ref="lineage-1",
    )

    assert lineage.closure_ref == "closure-1"
    assert lineage.audit_ref == "audit-1"
    assert lineage.outcome_ref == "outcome-1"
    assert lineage.lineage_ref == "lineage-1"


def test_orchestration_manifest_retains_fields() -> None:
    manifest = OrchestrationManifest(
        lineage_ref="lineage-1",
        closure_ref="closure-1",
        evidence_ref="evidence-1",
        manifest_ref="manifest-1",
    )

    assert manifest.lineage_ref == "lineage-1"
    assert manifest.closure_ref == "closure-1"
    assert manifest.evidence_ref == "evidence-1"
    assert manifest.manifest_ref == "manifest-1"


def test_orchestration_review_retains_fields() -> None:
    review = OrchestrationReview(
        manifest_ref="manifest-1",
        lineage_ref="lineage-1",
        closure_ref="closure-1",
        review_ref="review-1",
    )

    assert review.manifest_ref == "manifest-1"
    assert review.lineage_ref == "lineage-1"
    assert review.closure_ref == "closure-1"
    assert review.review_ref == "review-1"


def test_orchestration_assertion_retains_fields() -> None:
    assertion = OrchestrationAssertion(
        review_ref="review-1",
        manifest_ref="manifest-1",
        lineage_ref="lineage-1",
        assertion_ref="assertion-1",
    )

    assert assertion.review_ref == "review-1"
    assert assertion.manifest_ref == "manifest-1"
    assert assertion.lineage_ref == "lineage-1"
    assert assertion.assertion_ref == "assertion-1"


def test_orchestration_publication_retains_fields() -> None:
    publication = OrchestrationPublication(
        assertion_ref="assertion-1",
        review_ref="review-1",
        manifest_ref="manifest-1",
        publication_ref="publication-1",
    )

    assert publication.assertion_ref == "assertion-1"
    assert publication.review_ref == "review-1"
    assert publication.manifest_ref == "manifest-1"
    assert publication.publication_ref == "publication-1"


def test_orchestration_release_view_retains_fields() -> None:
    release_view = OrchestrationReleaseView(
        publication_ref="publication-1",
        assertion_ref="assertion-1",
        review_ref="review-1",
        release_view_ref="release-view-1",
    )

    assert release_view.publication_ref == "publication-1"
    assert release_view.assertion_ref == "assertion-1"
    assert release_view.review_ref == "review-1"
    assert release_view.release_view_ref == "release-view-1"
