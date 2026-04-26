from shade_core import RunState, validate_state_contract
from shade_core.contract_gate import (
    validate_artifact_handoff,
    validate_orchestration_assertion,
    validate_orchestration_audit,
    validate_orchestration_closure,
    validate_orchestration_checkpoint,
    validate_orchestration_evidence,
    validate_orchestration_gate,
    validate_orchestration_junction,
    validate_orchestration_lineage,
    validate_orchestration_manifest,
    validate_orchestration_outcome,
    validate_orchestration_review,
    validate_orchestration_verification,
    validate_run_transition,
    validate_task_route,
    validate_task_transition,
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
    OrchestrationReview,
    OrchestrationVerification,
    RunTransition,
    TaskRoute,
    TaskTransition,
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
