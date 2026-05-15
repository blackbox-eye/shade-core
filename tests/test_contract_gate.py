from dataclasses import replace as dc_replace
from shade_core import (
    ConfidenceRecord,
    MetaAuditEvent,
    RunState,
    RuntimeDecision,
    SelfModel,
    WorkerRegistry,
    validate_state_contract,
)
from shade_core.contract_gate import (
    validate_artifact_handoff,
    validate_confidence_record,
    validate_meta_audit_event,
    validate_orchestration_assertion,
    validate_orchestration_audit,
    validate_orchestration_closure,
    validate_orchestration_checkpoint,
    validate_orchestration_evidence,
    validate_orchestration_gate,
    validate_orchestration_junction,
    validate_orchestration_lineage,
    validate_orchestration_manifest,
    validate_orchestration_manifest_chain,
    validate_orchestration_outcome,
    validate_orchestration_publication,
    _collect_publication_release_view_consistency_errors,
    validate_orchestration_publication_release_view_consistency,
    validate_orchestration_release_view,
    validate_orchestration_review,
    validate_orchestration_verification,
    validate_run_transition,
    validate_runtime_evaluation_guard_verification_snapshot,
    validate_runtime_decision,
    validate_self_model,
    validate_task_route,
    validate_task_transition,
    validate_worker_orchestration_handoff,
    validate_worker_orchestration_plan,
    validate_worker_orchestration_review,
    validate_worker_orchestration_status,
    validate_worker_orchestration_step,
    validate_worker_orchestration_summary,
    validate_worker_registry,
    validate_worker_result,
    validate_worker_task,
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
    WorkerOrchestrationHandoff,
    WorkerOrchestrationPlan,
    WorkerOrchestrationReview,
    WorkerOrchestrationStatus,
    WorkerOrchestrationStep,
    WorkerOrchestrationSummary,
    WorkerResult,
    WorkerTask,
)


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


def test_validate_self_model_passes_for_valid_self_model() -> None:
    self_model = SelfModel(agent_id="shade-v1", role="control", state="idle")

    result = validate_self_model(self_model)

    assert result.is_valid is True
    assert result.errors == ()


def test_validate_self_model_fails_for_invalid_self_model() -> None:
    self_model = SelfModel(agent_id="", role="", state="")

    result = validate_self_model(self_model)

    assert result.is_valid is False
    assert result.errors == (
        "agent_id is required",
        "role is required",
        "state is required",
    )


def test_validate_worker_registry_passes_for_empty_registry() -> None:
    registry = WorkerRegistry()

    result = validate_worker_registry(registry)

    assert result.is_valid is True
    assert result.errors == ()


def test_validate_worker_registry_fails_for_invalid_registry_entries() -> None:
    registry = WorkerRegistry(
        workers={
            "": ("control", "active"),
            "shape-bad": ("control",),
            "role-bad": ("", "active"),
            "status-bad": ("control", ""),
        },
    )

    result = validate_worker_registry(registry)

    assert result.is_valid is False
    assert result.errors == (
        "worker name is required",
        "worker entry for shape-bad must contain role and status",
        "worker role is required for role-bad",
        "worker status is required for status-bad",
    )


def test_validate_confidence_record_passes_for_valid_confidence_record() -> None:
    confidence = ConfidenceRecord(
        score=0.9,
        source="local",
        reason="clear",
        reference="ref-1",
    )

    result = validate_confidence_record(confidence)

    assert result.is_valid is True
    assert result.errors == ()


def test_validate_confidence_record_fails_for_invalid_confidence_record() -> None:
    confidence = ConfidenceRecord(
        score=0.9,
        source="",
        reason="",
        reference="",
    )

    result = validate_confidence_record(confidence)

    assert result.is_valid is False
    assert result.errors == (
        "source is required",
        "reason is required",
        "reference is required",
    )


def test_validate_confidence_record_fails_for_invalid_score() -> None:
    confidence = ConfidenceRecord(
        score=float("inf"),
        source="local",
        reason="clear",
        reference="ref-1",
    )

    result = validate_confidence_record(confidence)

    assert result.is_valid is False
    assert result.errors == (
        "score must be finite and between 0.0 and 1.0 inclusive",
    )


def test_validate_meta_audit_event_passes_for_valid_meta_audit_event() -> None:
    event = MetaAuditEvent(
        event_type="runtime_decision",
        message="accepted",
        severity="info",
        reference="ref-1",
        run_id="run-1",
    )

    result = validate_meta_audit_event(event)

    assert result.is_valid is True
    assert result.errors == ()


def test_validate_meta_audit_event_fails_for_invalid_meta_audit_event() -> None:
    event = MetaAuditEvent(
        event_type="",
        message="",
        severity="",
        reference="",
        run_id="",
    )

    result = validate_meta_audit_event(event)

    assert result.is_valid is False
    assert result.errors == (
        "event_type is required",
        "message is required",
        "severity is required",
        "reference is required",
        "run_id is required",
    )


def test_validate_runtime_decision_passes_for_valid_runtime_decision() -> None:
    decision = RuntimeDecision(
        decision="needs_review",
        reason="needs inspection",
        next_step="review",
    )

    result = validate_runtime_decision(decision)

    assert result.is_valid is True
    assert result.errors == ()


def test_validate_runtime_decision_fails_for_invalid_runtime_decision() -> None:
    decision = RuntimeDecision(
        decision="pause",
        reason="",
        next_step="",
    )

    result = validate_runtime_decision(decision)

    assert result.is_valid is False
    assert result.errors == (
        "decision is invalid",
        "reason is required",
        "next_step is required",
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


def test_validate_worker_orchestration_plan_passes_for_valid_plan() -> None:
    plan = WorkerOrchestrationPlan(
        task_id="task-1",
        route_ref="route-1",
        plan_status="prepared",
        plan_ref="plan-1",
    )

    result = validate_worker_orchestration_plan(plan)

    assert result.is_valid is True
    assert result.errors == ()


def test_validate_worker_orchestration_plan_fails_for_invalid_plan() -> None:
    plan = WorkerOrchestrationPlan(
        task_id="",
        route_ref="",
        plan_status="stale",
        plan_ref="",
    )

    result = validate_worker_orchestration_plan(plan)

    assert result.is_valid is False
    assert result.errors == (
        "task_id is required",
        "route_ref is required",
        "plan_status is invalid",
        "plan_ref is required",
    )


def test_validate_worker_orchestration_step_passes_for_valid_step() -> None:
    step = WorkerOrchestrationStep(
        plan_ref="plan-1",
        task_transition_ref="task-transition-1",
        step_status="prepared",
        step_ref="step-1",
    )

    result = validate_worker_orchestration_step(step)

    assert result.is_valid is True
    assert result.errors == ()


def test_validate_worker_orchestration_step_fails_for_invalid_step() -> None:
    step = WorkerOrchestrationStep(
        plan_ref="",
        task_transition_ref="",
        step_status="stale",
        step_ref="",
    )

    result = validate_worker_orchestration_step(step)

    assert result.is_valid is False
    assert result.errors == (
        "plan_ref is required",
        "task_transition_ref is required",
        "step_status is invalid",
        "step_ref is required",
    )


def test_validate_worker_orchestration_handoff_passes_for_valid_handoff() -> None:
    handoff = WorkerOrchestrationHandoff(
        step_ref="step-1",
        output_ref="output-1",
        checkpoint_ref="checkpoint-1",
        handoff_ref="handoff-1",
    )

    result = validate_worker_orchestration_handoff(handoff)

    assert result.is_valid is True
    assert result.errors == ()


def test_validate_worker_orchestration_handoff_fails_for_invalid_handoff() -> None:
    handoff = WorkerOrchestrationHandoff(
        step_ref="",
        output_ref="",
        checkpoint_ref="",
        handoff_ref="",
    )

    result = validate_worker_orchestration_handoff(handoff)

    assert result.is_valid is False
    assert result.errors == (
        "step_ref is required",
        "output_ref is required",
        "checkpoint_ref is required",
        "handoff_ref is required",
    )


def test_validate_worker_orchestration_status_passes_for_valid_status() -> None:
    status = WorkerOrchestrationStatus(
        handoff_ref="handoff-1",
        junction_ref="junction-1",
        status_value="pending",
        status_ref="status-1",
    )

    result = validate_worker_orchestration_status(status)

    assert result.is_valid is True
    assert result.errors == ()


def test_validate_worker_orchestration_status_fails_for_invalid_status() -> None:
    status = WorkerOrchestrationStatus(
        handoff_ref="",
        junction_ref="",
        status_value="stale",
        status_ref="",
    )

    result = validate_worker_orchestration_status(status)

    assert result.is_valid is False
    assert result.errors == (
        "handoff_ref is required",
        "junction_ref is required",
        "status_value is invalid",
        "status_ref is required",
    )


def test_validate_worker_orchestration_summary_passes_for_valid_summary() -> None:
    summary = WorkerOrchestrationSummary(
        plan_ref="plan-1",
        status_ref="status-1",
        summary_status="aligned",
        summary_ref="summary-1",
    )

    result = validate_worker_orchestration_summary(summary)

    assert result.is_valid is True
    assert result.errors == ()


def test_validate_worker_orchestration_summary_fails_for_invalid_summary() -> None:
    summary = WorkerOrchestrationSummary(
        plan_ref="",
        status_ref="",
        summary_status="stale",
        summary_ref="",
    )

    result = validate_worker_orchestration_summary(summary)

    assert result.is_valid is False
    assert result.errors == (
        "plan_ref is required",
        "status_ref is required",
        "summary_status is invalid",
        "summary_ref is required",
    )


def test_validate_worker_orchestration_review_passes_for_valid_review() -> None:
    review = WorkerOrchestrationReview(
        summary_ref="summary-1",
        status_ref="status-1",
        review_status="pending",
        review_ref="worker-review-1",
    )

    result = validate_worker_orchestration_review(review)

    assert result.is_valid is True
    assert result.errors == ()


def test_validate_worker_orchestration_review_fails_for_invalid_review() -> None:
    review = WorkerOrchestrationReview(
        summary_ref="",
        status_ref="",
        review_status="stale",
        review_ref="",
    )

    result = validate_worker_orchestration_review(review)

    assert result.is_valid is False
    assert result.errors == (
        "summary_ref is required",
        "status_ref is required",
        "review_status is invalid",
        "review_ref is required",
    )


def test_validate_orchestration_checkpoint_passes_for_valid_checkpoint() -> None:
    checkpoint = OrchestrationCheckpoint(
        task_id="task-1",
        output_ref="output-1",
        route_ref="route-1",
        checkpoint_ref="checkpoint-1",
    )

    result = validate_orchestration_checkpoint(checkpoint)

    assert result.is_valid is True
    assert result.errors == ()


def test_validate_orchestration_checkpoint_fails_for_invalid_checkpoint() -> None:
    checkpoint = OrchestrationCheckpoint(
        task_id="",
        output_ref="",
        route_ref="",
        checkpoint_ref="",
    )

    result = validate_orchestration_checkpoint(checkpoint)

    assert result.is_valid is False
    assert result.errors == (
        "task_id is required",
        "output_ref is required",
        "route_ref is required",
        "checkpoint_ref is required",
    )


def test_validate_orchestration_junction_passes_for_valid_junction() -> None:
    junction = OrchestrationJunction(
        route_ref="route-1",
        task_transition_ref="task-transition-1",
        run_transition_ref="run-transition-1",
        junction_ref="junction-1",
    )

    result = validate_orchestration_junction(junction)

    assert result.is_valid is True
    assert result.errors == ()


def test_validate_orchestration_junction_fails_for_invalid_junction() -> None:
    junction = OrchestrationJunction(
        route_ref="",
        task_transition_ref="",
        run_transition_ref="",
        junction_ref="",
    )

    result = validate_orchestration_junction(junction)

    assert result.is_valid is False
    assert result.errors == (
        "route_ref is required",
        "task_transition_ref is required",
        "run_transition_ref is required",
        "junction_ref is required",
    )


def test_validate_orchestration_verification_passes_for_valid_verification() -> None:
    verification = OrchestrationVerification(
        checkpoint_ref="checkpoint-1",
        junction_ref="junction-1",
        task_transition_ref="task-transition-1",
        verification_ref="verification-1",
    )

    result = validate_orchestration_verification(verification)

    assert result.is_valid is True
    assert result.errors == ()


def test_validate_orchestration_verification_fails_for_invalid_verification() -> None:
    verification = OrchestrationVerification(
        checkpoint_ref="",
        junction_ref="",
        task_transition_ref="",
        verification_ref="",
    )

    result = validate_orchestration_verification(verification)

    assert result.is_valid is False
    assert result.errors == (
        "checkpoint_ref is required",
        "junction_ref is required",
        "task_transition_ref is required",
        "verification_ref is required",
    )


def test_validate_orchestration_outcome_passes_for_valid_outcome() -> None:
    outcome = OrchestrationOutcome(
        verification_ref="verification-1",
        decision_ref="decision-1",
        evaluation_ref="evaluation-1",
        outcome_ref="outcome-1",
    )

    result = validate_orchestration_outcome(outcome)

    assert result.is_valid is True
    assert result.errors == ()


def test_validate_orchestration_outcome_fails_for_invalid_outcome() -> None:
    outcome = OrchestrationOutcome(
        verification_ref="",
        decision_ref="",
        evaluation_ref="",
        outcome_ref="",
    )

    result = validate_orchestration_outcome(outcome)

    assert result.is_valid is False
    assert result.errors == (
        "verification_ref is required",
        "decision_ref is required",
        "evaluation_ref is required",
        "outcome_ref is required",
    )


def test_validate_orchestration_evidence_passes_for_valid_evidence() -> None:
    evidence = OrchestrationEvidence(
        verification_ref="verification-1",
        outcome_ref="outcome-1",
        evaluation_ref="evaluation-1",
        evidence_ref="evidence-1",
    )

    result = validate_orchestration_evidence(evidence)

    assert result.is_valid is True
    assert result.errors == ()


def test_validate_orchestration_evidence_fails_for_invalid_evidence() -> None:
    evidence = OrchestrationEvidence(
        verification_ref="",
        outcome_ref="",
        evaluation_ref="",
        evidence_ref="",
    )

    result = validate_orchestration_evidence(evidence)

    assert result.is_valid is False
    assert result.errors == (
        "verification_ref is required",
        "outcome_ref is required",
        "evaluation_ref is required",
        "evidence_ref is required",
    )


def test_validate_orchestration_gate_passes_for_valid_gate() -> None:
    gate = OrchestrationGate(
        evidence_ref="evidence-1",
        evaluation_gate_ref="evaluation-gate-1",
        audit_ref="audit-1",
        gate_ref="gate-1",
    )

    result = validate_orchestration_gate(gate)

    assert result.is_valid is True
    assert result.errors == ()


def test_validate_orchestration_gate_fails_for_invalid_gate() -> None:
    gate = OrchestrationGate(
        evidence_ref="",
        evaluation_gate_ref="",
        audit_ref="",
        gate_ref="",
    )

    result = validate_orchestration_gate(gate)

    assert result.is_valid is False
    assert result.errors == (
        "evidence_ref is required",
        "evaluation_gate_ref is required",
        "audit_ref is required",
        "gate_ref is required",
    )


def test_validate_orchestration_audit_passes_for_valid_audit() -> None:
    audit = OrchestrationAudit(
        gate_ref="gate-1",
        evaluation_gate_ref="evaluation-gate-1",
        audit_event_ref="audit-event-1",
        audit_ref="audit-1",
    )

    result = validate_orchestration_audit(audit)

    assert result.is_valid is True
    assert result.errors == ()


def test_validate_orchestration_audit_fails_for_invalid_audit() -> None:
    audit = OrchestrationAudit(
        gate_ref="",
        evaluation_gate_ref="",
        audit_event_ref="",
        audit_ref="",
    )

    result = validate_orchestration_audit(audit)

    assert result.is_valid is False
    assert result.errors == (
        "gate_ref is required",
        "evaluation_gate_ref is required",
        "audit_event_ref is required",
        "audit_ref is required",
    )


def test_validate_orchestration_closure_passes_for_valid_closure() -> None:
    closure = OrchestrationClosure(
        audit_ref="audit-1",
        decision_ref="decision-1",
        evaluation_ref="evaluation-1",
        closure_ref="closure-1",
    )

    result = validate_orchestration_closure(closure)

    assert result.is_valid is True
    assert result.errors == ()


def test_validate_orchestration_closure_fails_for_invalid_closure() -> None:
    closure = OrchestrationClosure(
        audit_ref="",
        decision_ref="",
        evaluation_ref="",
        closure_ref="",
    )

    result = validate_orchestration_closure(closure)

    assert result.is_valid is False
    assert result.errors == (
        "audit_ref is required",
        "decision_ref is required",
        "evaluation_ref is required",
        "closure_ref is required",
    )


def test_validate_task_transition_passes_for_valid_transition() -> None:
    transition = TaskTransition(
        task_id="task-1",
        from_status="pending",
        to_status="running",
        transition_ref="tr-1",
    )

    result = validate_task_transition(transition)

    assert result.is_valid is True
    assert result.errors == ()


def test_validate_task_transition_fails_for_invalid_transition() -> None:
    transition = TaskTransition(
        task_id="",
        from_status="",
        to_status="",
        transition_ref="",
    )

    result = validate_task_transition(transition)

    assert result.is_valid is False
    assert result.errors == (
        "task_id is required",
        "from_status is required",
        "to_status is required",
        "transition_ref is required",
    )


def test_validate_run_transition_passes_for_valid_transition() -> None:
    transition = RunTransition(
        run_id="run-1",
        from_step="ingest",
        to_step="evaluate",
        transition_ref="tr-2",
    )

    result = validate_run_transition(transition)

    assert result.is_valid is True
    assert result.errors == ()


def test_validate_run_transition_fails_for_invalid_transition() -> None:
    transition = RunTransition(
        run_id="",
        from_step="",
        to_step="",
        transition_ref="",
    )

    result = validate_run_transition(transition)

    assert result.is_valid is False
    assert result.errors == (
        "run_id is required",
        "from_step is required",
        "to_step is required",
        "transition_ref is required",
    )


def test_validate_orchestration_lineage_passes_for_valid_lineage() -> None:
    lineage = OrchestrationLineage(
        closure_ref="closure-1",
        audit_ref="audit-1",
        outcome_ref="outcome-1",
        lineage_ref="lineage-1",
    )

    result = validate_orchestration_lineage(lineage)

    assert result.is_valid is True
    assert result.errors == ()


def test_validate_orchestration_lineage_fails_for_invalid_lineage() -> None:
    lineage = OrchestrationLineage(
        closure_ref="",
        audit_ref="",
        outcome_ref="",
        lineage_ref="",
    )

    result = validate_orchestration_lineage(lineage)

    assert result.is_valid is False
    assert result.errors == (
        "closure_ref is required",
        "audit_ref is required",
        "outcome_ref is required",
        "lineage_ref is required",
    )


def test_validate_orchestration_manifest_passes_for_valid_manifest() -> None:
    manifest = OrchestrationManifest(
        lineage_ref="lineage-1",
        closure_ref="closure-1",
        evidence_ref="evidence-1",
        manifest_ref="manifest-1",
    )

    result = validate_orchestration_manifest(manifest)

    assert result.is_valid is True
    assert result.errors == ()


def test_validate_orchestration_manifest_fails_for_invalid_manifest() -> None:
    manifest = OrchestrationManifest(
        lineage_ref="",
        closure_ref="",
        evidence_ref="",
        manifest_ref="",
    )

    result = validate_orchestration_manifest(manifest)

    assert result.is_valid is False
    assert result.errors == (
        "lineage_ref is required",
        "closure_ref is required",
        "evidence_ref is required",
        "manifest_ref is required",
    )


def test_validate_orchestration_review_passes_for_valid_review() -> None:
    review = OrchestrationReview(
        manifest_ref="manifest-1",
        lineage_ref="lineage-1",
        closure_ref="closure-1",
        review_ref="review-1",
    )

    result = validate_orchestration_review(review)

    assert result.is_valid is True
    assert result.errors == ()


def test_validate_orchestration_review_fails_for_invalid_review() -> None:
    review = OrchestrationReview(
        manifest_ref="",
        lineage_ref="",
        closure_ref="",
        review_ref="",
    )

    result = validate_orchestration_review(review)

    assert result.is_valid is False
    assert result.errors == (
        "manifest_ref is required",
        "lineage_ref is required",
        "closure_ref is required",
        "review_ref is required",
    )


def test_validate_orchestration_assertion_passes_for_valid_assertion() -> None:
    assertion = OrchestrationAssertion(
        review_ref="review-1",
        manifest_ref="manifest-1",
        lineage_ref="lineage-1",
        assertion_ref="assertion-1",
    )

    result = validate_orchestration_assertion(assertion)

    assert result.is_valid is True
    assert result.errors == ()


def test_validate_orchestration_assertion_fails_for_invalid_assertion() -> None:
    assertion = OrchestrationAssertion(
        review_ref="",
        manifest_ref="",
        lineage_ref="",
        assertion_ref="",
    )

    result = validate_orchestration_assertion(assertion)

    assert result.is_valid is False
    assert result.errors == (
        "review_ref is required",
        "manifest_ref is required",
        "lineage_ref is required",
        "assertion_ref is required",
    )


def test_validate_orchestration_publication_passes_for_valid_publication() -> None:
    publication = OrchestrationPublication(
        assertion_ref="assertion-1",
        review_ref="review-1",
        manifest_ref="manifest-1",
        publication_ref="publication-1",
    )

    result = validate_orchestration_publication(publication)

    assert result.is_valid is True
    assert result.errors == ()


def test_validate_orchestration_publication_fails_for_invalid_publication() -> None:
    publication = OrchestrationPublication(
        assertion_ref="",
        review_ref="",
        manifest_ref="",
        publication_ref="",
    )

    result = validate_orchestration_publication(publication)

    assert result.is_valid is False
    assert result.errors == (
        "assertion_ref is required",
        "review_ref is required",
        "manifest_ref is required",
        "publication_ref is required",
    )


def test_validate_orchestration_release_view_passes_for_valid_release_view() -> None:
    release_view = OrchestrationReleaseView(
        publication_ref="publication-1",
        assertion_ref="assertion-1",
        review_ref="review-1",
        release_view_ref="release-view-1",
    )

    result = validate_orchestration_release_view(release_view)

    assert result.is_valid is True
    assert result.errors == ()


def test_validate_orchestration_release_view_fails_for_invalid_release_view() -> None:
    release_view = OrchestrationReleaseView(
        publication_ref="",
        assertion_ref="",
        review_ref="",
        release_view_ref="",
    )

    result = validate_orchestration_release_view(release_view)

    assert result.is_valid is False
    assert result.errors == (
        "publication_ref is required",
        "assertion_ref is required",
        "review_ref is required",
        "release_view_ref is required",
    )


def _valid_publication_release_view_consistency_objects(
) -> tuple[OrchestrationPublication, OrchestrationReleaseView]:
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

    return publication, release_view


def test_validate_orchestration_publication_release_view_consistency_passes_for_valid_objects() -> None:
    publication, release_view = _valid_publication_release_view_consistency_objects()

    result = validate_orchestration_publication_release_view_consistency(
        publication,
        release_view,
    )

    assert result.is_valid is True
    assert result.errors == ()


def test_validate_orchestration_publication_release_view_consistency_fails_for_invalid_individual_objects() -> None:
    publication = OrchestrationPublication(
        assertion_ref="",
        review_ref="",
        manifest_ref="",
        publication_ref="",
    )
    release_view = OrchestrationReleaseView(
        publication_ref="",
        assertion_ref="",
        review_ref="",
        release_view_ref="",
    )

    result = validate_orchestration_publication_release_view_consistency(
        publication,
        release_view,
    )

    assert result.is_valid is False
    assert result.errors == (
        "publication.assertion_ref is required",
        "publication.review_ref is required",
        "publication.manifest_ref is required",
        "publication.publication_ref is required",
        "release_view.publication_ref is required",
        "release_view.assertion_ref is required",
        "release_view.review_ref is required",
        "release_view.release_view_ref is required",
    )


def test_validate_orchestration_publication_release_view_consistency_fails_for_publication_ref_mismatch() -> None:
    publication, release_view = _valid_publication_release_view_consistency_objects()
    release_view = dc_replace(release_view, publication_ref="wrong-publication")

    result = validate_orchestration_publication_release_view_consistency(
        publication,
        release_view,
    )

    assert result.is_valid is False
    assert result.errors == (
        "release_view.publication_ref must equal publication.publication_ref",
    )


def test_validate_orchestration_publication_release_view_consistency_fails_for_assertion_ref_mismatch() -> None:
    publication, release_view = _valid_publication_release_view_consistency_objects()
    release_view = dc_replace(release_view, assertion_ref="wrong-assertion")

    result = validate_orchestration_publication_release_view_consistency(
        publication,
        release_view,
    )

    assert result.is_valid is False
    assert result.errors == (
        "release_view.assertion_ref must equal publication.assertion_ref",
    )


def test_validate_orchestration_publication_release_view_consistency_fails_for_review_ref_mismatch() -> None:
    publication, release_view = _valid_publication_release_view_consistency_objects()
    release_view = dc_replace(release_view, review_ref="wrong-review")

    result = validate_orchestration_publication_release_view_consistency(
        publication,
        release_view,
    )

    assert result.is_valid is False
    assert result.errors == (
        "release_view.review_ref must equal publication.review_ref",
    )


def test_collect_publication_release_view_consistency_errors_returns_same_errors_as_both_validators() -> None:
    publication, release_view = _valid_publication_release_view_consistency_objects()
    mismatched_release_view = dc_replace(
        release_view,
        publication_ref="wrong-pub",
        assertion_ref="wrong-assert",
        review_ref="wrong-review",
    )

    shared_errors = _collect_publication_release_view_consistency_errors(
        publication,
        mismatched_release_view,
    )

    standalone_result = validate_orchestration_publication_release_view_consistency(
        publication,
        mismatched_release_view,
    )
    chain_objects = _valid_manifest_chain_objects()
    chain_publication = chain_objects[4]
    chain_release_view = dc_replace(
        chain_objects[5],
        publication_ref="wrong-pub",
        assertion_ref="wrong-assert",
        review_ref="wrong-review",
    )
    manifest_chain_result = validate_orchestration_manifest_chain(
        chain_objects[0],
        chain_objects[1],
        chain_objects[2],
        chain_objects[3],
        chain_publication,
        chain_release_view,
    )

    assert shared_errors == (
        "release_view.publication_ref must equal publication.publication_ref",
        "release_view.assertion_ref must equal publication.assertion_ref",
        "release_view.review_ref must equal publication.review_ref",
    )
    assert all(e in standalone_result.errors for e in shared_errors)
    assert all(e in manifest_chain_result.errors for e in shared_errors)


def test_validate_runtime_evaluation_guard_verification_snapshot_passes_for_valid_snapshot() -> None:
    snapshot = {
        "runtime_evaluation": {
            "runtime_contract_integration": {
                "contract_gate": {
                    "self_model": {"is_valid": True, "errors": ()},
                    "worker_registry": {"is_valid": True, "errors": ()},
                    "confidence_record": {"is_valid": True, "errors": ()},
                    "state_contract": {"is_valid": True, "errors": ()},
                },
                "runtime_fabric": {
                    "evaluation_gate": {
                        "result": "pass",
                        "contract_valid": True,
                        "errors": (),
                    },
                },
            },
            "aggregated_contract_gate": {"is_valid": True, "errors": ()},
            "raw_evaluation": {"result": "pass"},
            "evaluation_gate": {
                "result": "pass",
                "contract_valid": True,
                "errors": (),
            },
        },
        "prepared_fabric_guard": {"is_valid": True, "errors": ()},
        "serialized_snapshot_guard": {"is_valid": True, "errors": ()},
        "verification_summary": {
            "prepared_fabric_guard_valid": True,
            "serialized_snapshot_guard_valid": True,
            "runtime_evaluation_consistent": True,
            "runtime_contract_valid": True,
            "evaluation_gate_alignment": "aligned",
            "aggregated_contract_gate_aligned": True,
            "nested_evaluation_gate_aligned": True,
            "verification_status": "verified",
        },
    }

    result = validate_runtime_evaluation_guard_verification_snapshot(snapshot)

    assert result.is_valid is True
    assert result.errors == ()


def test_validate_runtime_evaluation_guard_verification_snapshot_fails_for_malformed_top_level_mapping() -> None:
    result = validate_runtime_evaluation_guard_verification_snapshot("invalid")

    assert result.is_valid is False
    assert result.errors == (
        "verification_snapshot must be a mapping",
    )


def test_validate_runtime_evaluation_guard_verification_snapshot_fails_for_malformed_guard_result_mapping() -> None:
    snapshot = {
        "runtime_evaluation": {
            "runtime_contract_integration": {
                "contract_gate": {
                    "self_model": {"is_valid": True, "errors": ()},
                    "worker_registry": {"is_valid": True, "errors": ()},
                    "confidence_record": {"is_valid": True, "errors": ()},
                    "state_contract": {"is_valid": True, "errors": ()},
                },
                "runtime_fabric": {
                    "evaluation_gate": {
                        "result": "pass",
                        "contract_valid": True,
                        "errors": (),
                    },
                },
            },
            "aggregated_contract_gate": {"is_valid": True, "errors": ()},
            "raw_evaluation": {"result": "pass"},
            "evaluation_gate": {
                "result": "pass",
                "contract_valid": True,
                "errors": (),
            },
        },
        "prepared_fabric_guard": {"is_valid": "invalid", "errors": 9},
        "serialized_snapshot_guard": {"is_valid": True, "errors": ()},
        "verification_summary": {
            "prepared_fabric_guard_valid": False,
            "serialized_snapshot_guard_valid": True,
            "runtime_evaluation_consistent": True,
            "runtime_contract_valid": True,
            "evaluation_gate_alignment": "aligned",
            "aggregated_contract_gate_aligned": True,
            "nested_evaluation_gate_aligned": True,
            "verification_status": "failed",
        },
    }

    result = validate_runtime_evaluation_guard_verification_snapshot(snapshot)

    assert result.is_valid is False
    assert result.errors == (
        "verification_snapshot.prepared_fabric_guard.is_valid must be a bool",
        "verification_snapshot.prepared_fabric_guard.errors must be a tuple, list, or None",
    )


def test_validate_runtime_evaluation_guard_verification_snapshot_fails_for_malformed_summary_mapping() -> None:
    snapshot = {
        "runtime_evaluation": {
            "runtime_contract_integration": {
                "contract_gate": {
                    "self_model": {"is_valid": True, "errors": ()},
                    "worker_registry": {"is_valid": True, "errors": ()},
                    "confidence_record": {"is_valid": True, "errors": ()},
                    "state_contract": {"is_valid": True, "errors": ()},
                },
                "runtime_fabric": {
                    "evaluation_gate": {
                        "result": "pass",
                        "contract_valid": True,
                        "errors": (),
                    },
                },
            },
            "aggregated_contract_gate": {"is_valid": True, "errors": ()},
            "raw_evaluation": {"result": "pass"},
            "evaluation_gate": {
                "result": "pass",
                "contract_valid": True,
                "errors": (),
            },
        },
        "prepared_fabric_guard": {"is_valid": True, "errors": ()},
        "serialized_snapshot_guard": {"is_valid": True, "errors": ()},
        "verification_summary": "invalid",
    }

    result = validate_runtime_evaluation_guard_verification_snapshot(snapshot)

    assert result.is_valid is False
    assert result.errors == (
        "verification_snapshot.verification_summary must be a mapping",
    )


def test_validate_runtime_evaluation_guard_verification_snapshot_fails_for_inconsistent_summary_flags() -> None:
    snapshot = {
        "runtime_evaluation": {
            "runtime_contract_integration": {
                "contract_gate": {
                    "self_model": {"is_valid": True, "errors": ()},
                    "worker_registry": {"is_valid": True, "errors": ()},
                    "confidence_record": {"is_valid": True, "errors": ()},
                    "state_contract": {"is_valid": True, "errors": ()},
                },
                "runtime_fabric": {
                    "evaluation_gate": {
                        "result": "pass",
                        "contract_valid": True,
                        "errors": (),
                    },
                },
            },
            "aggregated_contract_gate": {"is_valid": True, "errors": ()},
            "raw_evaluation": {"result": "pass"},
            "evaluation_gate": {
                "result": "pass",
                "contract_valid": True,
                "errors": (),
            },
        },
        "prepared_fabric_guard": {"is_valid": True, "errors": ()},
        "serialized_snapshot_guard": {"is_valid": True, "errors": ()},
        "verification_summary": {
            "prepared_fabric_guard_valid": True,
            "serialized_snapshot_guard_valid": True,
            "runtime_evaluation_consistent": False,
            "runtime_contract_valid": True,
            "evaluation_gate_alignment": "aligned",
            "aggregated_contract_gate_aligned": True,
            "nested_evaluation_gate_aligned": True,
            "verification_status": "failed",
        },
    }

    result = validate_runtime_evaluation_guard_verification_snapshot(snapshot)

    assert result.is_valid is False
    assert result.errors == (
        "verification_snapshot.verification_summary.runtime_evaluation_consistent must reflect aggregated contract, evaluation gate, and nested alignment semantics",
        "verification_snapshot.verification_summary.verification_status must match the derived verification status",
    )


def test_validate_runtime_evaluation_guard_verification_snapshot_fails_for_rephrased_alignment_messages() -> None:
    snapshot = {
        "runtime_evaluation": {
            "runtime_contract_integration": {
                "contract_gate": {
                    "self_model": {"is_valid": True, "errors": ()},
                    "worker_registry": {"is_valid": True, "errors": ()},
                    "confidence_record": {"is_valid": True, "errors": ()},
                    "state_contract": {"is_valid": True, "errors": ()},
                },
                "runtime_fabric": {
                    "evaluation_gate": {
                        "result": "pass",
                        "contract_valid": True,
                        "errors": (),
                    },
                },
            },
            "aggregated_contract_gate": {"is_valid": True, "errors": ()},
            "raw_evaluation": {"result": "pass"},
            "evaluation_gate": {
                "result": "pass",
                "contract_valid": True,
                "errors": (),
            },
        },
        "prepared_fabric_guard": {"is_valid": True, "errors": ()},
        "serialized_snapshot_guard": {"is_valid": True, "errors": ()},
        "verification_summary": {
            "prepared_fabric_guard_valid": True,
            "serialized_snapshot_guard_valid": True,
            "runtime_evaluation_consistent": True,
            "runtime_contract_valid": True,
            "evaluation_gate_alignment": "aligned",
            "aggregated_contract_gate_aligned": False,
            "nested_evaluation_gate_aligned": False,
            "verification_status": "verified",
        },
    }

    result = validate_runtime_evaluation_guard_verification_snapshot(snapshot)

    assert result.is_valid is False
    assert result.errors == (
        "verification_snapshot.verification_summary.aggregated_contract_gate_aligned must match verification_snapshot.runtime_evaluation.aggregated_contract_gate",
        "verification_snapshot.verification_summary.nested_evaluation_gate_aligned must match verification_snapshot.runtime_evaluation.evaluation_gate == verification_snapshot.evaluation_gate",
    )


def test_validate_runtime_evaluation_guard_verification_snapshot_fails_for_malformed_runtime_evaluation_nested_structure() -> None:
    snapshot = {
        "runtime_evaluation": {
            "runtime_contract_integration": {
                "contract_gate": {
                    "self_model": {"is_valid": True, "errors": ()},
                    "worker_registry": {"is_valid": True, "errors": ()},
                    "confidence_record": {"is_valid": True, "errors": ()},
                    "state_contract": {"is_valid": True, "errors": ()},
                },
                "runtime_fabric": {
                    "evaluation_gate": "invalid",
                },
            },
            "aggregated_contract_gate": {"is_valid": True, "errors": ()},
            "raw_evaluation": {"result": "pass"},
            "evaluation_gate": {
                "result": "pass",
                "contract_valid": True,
                "errors": (),
            },
        },
        "prepared_fabric_guard": {"is_valid": True, "errors": ()},
        "serialized_snapshot_guard": {
            "is_valid": False,
            "errors": (
                "snapshot.runtime_contract_integration.runtime_fabric.evaluation_gate must be a mapping",
            ),
        },
        "verification_summary": {
            "prepared_fabric_guard_valid": True,
            "serialized_snapshot_guard_valid": False,
            "runtime_evaluation_consistent": False,
            "runtime_contract_valid": True,
            "evaluation_gate_alignment": "aligned",
            "aggregated_contract_gate_aligned": True,
            "nested_evaluation_gate_aligned": False,
            "verification_status": "failed",
        },
    }

    result = validate_runtime_evaluation_guard_verification_snapshot(snapshot)

    assert result.is_valid is False
    assert result.errors == (
        "verification_snapshot.runtime_evaluation.runtime_contract_integration.runtime_fabric.evaluation_gate must be a mapping",
    )


def _valid_manifest_chain_objects() -> tuple:
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
    return lineage, manifest, review, assertion, publication, release_view


def test_validate_orchestration_manifest_chain_passes_for_valid_chain() -> None:
    lineage, manifest, review, assertion, publication, release_view = (
        _valid_manifest_chain_objects()
    )

    result = validate_orchestration_manifest_chain(
        lineage, manifest, review, assertion, publication, release_view,
    )

    assert result.is_valid is True
    assert result.errors == ()


def test_validate_orchestration_manifest_chain_fails_for_invalid_individual_objects() -> None:
    lineage = OrchestrationLineage(
        closure_ref="",
        audit_ref="",
        outcome_ref="",
        lineage_ref="",
    )
    manifest = OrchestrationManifest(
        lineage_ref="",
        closure_ref="",
        evidence_ref="",
        manifest_ref="",
    )
    review = OrchestrationReview(
        manifest_ref="",
        lineage_ref="",
        closure_ref="",
        review_ref="",
    )
    assertion = OrchestrationAssertion(
        review_ref="",
        manifest_ref="",
        lineage_ref="",
        assertion_ref="",
    )
    publication = OrchestrationPublication(
        assertion_ref="",
        review_ref="",
        manifest_ref="",
        publication_ref="",
    )
    release_view = OrchestrationReleaseView(
        publication_ref="",
        assertion_ref="",
        review_ref="",
        release_view_ref="",
    )

    result = validate_orchestration_manifest_chain(
        lineage, manifest, review, assertion, publication, release_view,
    )

    assert result.is_valid is False
    assert result.errors == (
        "lineage.closure_ref is required",
        "lineage.audit_ref is required",
        "lineage.outcome_ref is required",
        "lineage.lineage_ref is required",
        "manifest.lineage_ref is required",
        "manifest.closure_ref is required",
        "manifest.evidence_ref is required",
        "manifest.manifest_ref is required",
        "review.manifest_ref is required",
        "review.lineage_ref is required",
        "review.closure_ref is required",
        "review.review_ref is required",
        "assertion.review_ref is required",
        "assertion.manifest_ref is required",
        "assertion.lineage_ref is required",
        "assertion.assertion_ref is required",
        "publication.assertion_ref is required",
        "publication.review_ref is required",
        "publication.manifest_ref is required",
        "publication.publication_ref is required",
        "release_view.publication_ref is required",
        "release_view.assertion_ref is required",
        "release_view.review_ref is required",
        "release_view.release_view_ref is required",
    )


def test_validate_orchestration_manifest_chain_fails_for_manifest_lineage_ref_mismatch() -> None:
    lineage, manifest, review, assertion, publication, release_view = (
        _valid_manifest_chain_objects()
    )
    manifest = dc_replace(manifest, lineage_ref="wrong-lineage")

    result = validate_orchestration_manifest_chain(
        lineage, manifest, review, assertion, publication, release_view,
    )

    assert result.is_valid is False
    assert "manifest.lineage_ref must equal lineage.lineage_ref" in result.errors


def test_validate_orchestration_manifest_chain_fails_for_manifest_closure_ref_mismatch() -> None:
    lineage, manifest, review, assertion, publication, release_view = (
        _valid_manifest_chain_objects()
    )
    manifest = dc_replace(manifest, closure_ref="wrong-closure")

    result = validate_orchestration_manifest_chain(
        lineage, manifest, review, assertion, publication, release_view,
    )

    assert result.is_valid is False
    assert "manifest.closure_ref must equal lineage.closure_ref" in result.errors


def test_validate_orchestration_manifest_chain_fails_for_review_manifest_ref_mismatch() -> None:
    lineage, manifest, review, assertion, publication, release_view = (
        _valid_manifest_chain_objects()
    )
    review = dc_replace(review, manifest_ref="wrong-manifest")

    result = validate_orchestration_manifest_chain(
        lineage, manifest, review, assertion, publication, release_view,
    )

    assert result.is_valid is False
    assert "review.manifest_ref must equal manifest.manifest_ref" in result.errors


def test_validate_orchestration_manifest_chain_fails_for_review_lineage_ref_mismatch() -> None:
    lineage, manifest, review, assertion, publication, release_view = (
        _valid_manifest_chain_objects()
    )
    review = dc_replace(review, lineage_ref="wrong-lineage")

    result = validate_orchestration_manifest_chain(
        lineage, manifest, review, assertion, publication, release_view,
    )

    assert result.is_valid is False
    assert "review.lineage_ref must equal manifest.lineage_ref" in result.errors


def test_validate_orchestration_manifest_chain_fails_for_review_closure_ref_mismatch() -> None:
    lineage, manifest, review, assertion, publication, release_view = (
        _valid_manifest_chain_objects()
    )
    review = dc_replace(review, closure_ref="wrong-closure")

    result = validate_orchestration_manifest_chain(
        lineage, manifest, review, assertion, publication, release_view,
    )

    assert result.is_valid is False
    assert "review.closure_ref must equal manifest.closure_ref" in result.errors


def test_validate_orchestration_manifest_chain_fails_for_assertion_review_ref_mismatch() -> None:
    lineage, manifest, review, assertion, publication, release_view = (
        _valid_manifest_chain_objects()
    )
    assertion = dc_replace(assertion, review_ref="wrong-review")

    result = validate_orchestration_manifest_chain(
        lineage, manifest, review, assertion, publication, release_view,
    )

    assert result.is_valid is False
    assert "assertion.review_ref must equal review.review_ref" in result.errors


def test_validate_orchestration_manifest_chain_fails_for_assertion_manifest_ref_mismatch() -> None:
    lineage, manifest, review, assertion, publication, release_view = (
        _valid_manifest_chain_objects()
    )
    assertion = dc_replace(assertion, manifest_ref="wrong-manifest")

    result = validate_orchestration_manifest_chain(
        lineage, manifest, review, assertion, publication, release_view,
    )

    assert result.is_valid is False
    assert "assertion.manifest_ref must equal review.manifest_ref" in result.errors


def test_validate_orchestration_manifest_chain_fails_for_assertion_lineage_ref_mismatch() -> None:
    lineage, manifest, review, assertion, publication, release_view = (
        _valid_manifest_chain_objects()
    )
    assertion = dc_replace(assertion, lineage_ref="wrong-lineage")

    result = validate_orchestration_manifest_chain(
        lineage, manifest, review, assertion, publication, release_view,
    )

    assert result.is_valid is False
    assert "assertion.lineage_ref must equal review.lineage_ref" in result.errors


def test_validate_orchestration_manifest_chain_fails_for_publication_assertion_ref_mismatch() -> None:
    lineage, manifest, review, assertion, publication, release_view = (
        _valid_manifest_chain_objects()
    )
    publication = dc_replace(publication, assertion_ref="wrong-assertion")

    result = validate_orchestration_manifest_chain(
        lineage, manifest, review, assertion, publication, release_view,
    )

    assert result.is_valid is False
    assert "publication.assertion_ref must equal assertion.assertion_ref" in result.errors


def test_validate_orchestration_manifest_chain_fails_for_publication_review_ref_mismatch() -> None:
    lineage, manifest, review, assertion, publication, release_view = (
        _valid_manifest_chain_objects()
    )
    publication = dc_replace(publication, review_ref="wrong-review")

    result = validate_orchestration_manifest_chain(
        lineage, manifest, review, assertion, publication, release_view,
    )

    assert result.is_valid is False
    assert "publication.review_ref must equal assertion.review_ref" in result.errors


def test_validate_orchestration_manifest_chain_fails_for_publication_manifest_ref_mismatch() -> None:
    lineage, manifest, review, assertion, publication, release_view = (
        _valid_manifest_chain_objects()
    )
    publication = dc_replace(publication, manifest_ref="wrong-manifest")

    result = validate_orchestration_manifest_chain(
        lineage, manifest, review, assertion, publication, release_view,
    )

    assert result.is_valid is False
    assert "publication.manifest_ref must equal assertion.manifest_ref" in result.errors


def test_validate_orchestration_manifest_chain_fails_for_release_view_publication_ref_mismatch() -> None:
    lineage, manifest, review, assertion, publication, release_view = (
        _valid_manifest_chain_objects()
    )
    release_view = dc_replace(release_view, publication_ref="wrong-publication")

    result = validate_orchestration_manifest_chain(
        lineage, manifest, review, assertion, publication, release_view,
    )

    assert result.is_valid is False
    assert "release_view.publication_ref must equal publication.publication_ref" in result.errors


def test_validate_orchestration_manifest_chain_fails_for_release_view_assertion_ref_mismatch() -> None:
    lineage, manifest, review, assertion, publication, release_view = (
        _valid_manifest_chain_objects()
    )
    release_view = dc_replace(release_view, assertion_ref="wrong-assertion")

    result = validate_orchestration_manifest_chain(
        lineage, manifest, review, assertion, publication, release_view,
    )

    assert result.is_valid is False
    assert "release_view.assertion_ref must equal publication.assertion_ref" in result.errors


def test_validate_orchestration_manifest_chain_fails_for_release_view_review_ref_mismatch() -> None:
    lineage, manifest, review, assertion, publication, release_view = (
        _valid_manifest_chain_objects()
    )
    release_view = dc_replace(release_view, review_ref="wrong-review")

    result = validate_orchestration_manifest_chain(
        lineage, manifest, review, assertion, publication, release_view,
    )

    assert result.is_valid is False
    assert "release_view.review_ref must equal publication.review_ref" in result.errors
