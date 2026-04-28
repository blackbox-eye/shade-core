from shade_core.contract_gate import ContractGateResult
from shade_core.evaluation_gate import (
    _aggregate_runtime_contract_result,
    _build_evaluation_gate_result_from_raw_result,
    _guard_evaluation_gate_result_from_raw_result,
    _run_runtime_evaluation_gate,
)
from shade_core import (
    EvaluationGateResult,
    MetaAuditEvent,
    RuntimeDecision,
    evaluate,
    run_evaluation_gate,
)


def test_evaluation_gate_fails_when_contract_gate_fails() -> None:
    contract_result = ContractGateResult(
        is_valid=False,
        errors=("run_id is required",),
    )
    decision = RuntimeDecision(decision="accept", reason="ok", next_step="continue")
    event = MetaAuditEvent(
        event_type="runtime_decision",
        message="accept",
        severity="info",
        reference="ref-1",
        run_id="run-1",
    )

    result = run_evaluation_gate(contract_result, decision, event)

    assert result == EvaluationGateResult(
        result="fail",
        contract_valid=False,
        errors=("run_id is required",),
    )


def test_evaluation_gate_passes_through_pass_result() -> None:
    contract_result = ContractGateResult(is_valid=True, errors=())
    decision = RuntimeDecision(decision="accept", reason="ok", next_step="continue")
    event = MetaAuditEvent(
        event_type="runtime_decision",
        message="accept",
        severity="info",
        reference="ref-pass",
        run_id="run-1",
    )

    result = run_evaluation_gate(contract_result, decision, event)

    assert result == EvaluationGateResult(
        result="pass",
        contract_valid=True,
        errors=(),
    )


def test_evaluation_gate_passes_through_review_result() -> None:
    contract_result = ContractGateResult(is_valid=True, errors=())
    decision = RuntimeDecision(
        decision="needs_review",
        reason="check",
        next_step="review",
    )
    event = MetaAuditEvent(
        event_type="runtime_decision",
        message="warning",
        severity="warning",
        reference="ref-review",
        run_id="run-1",
    )

    result = run_evaluation_gate(contract_result, decision, event)

    assert result == EvaluationGateResult(
        result="review",
        contract_valid=True,
        errors=(),
    )


def test_build_evaluation_gate_result_from_raw_result_preserves_valid_result() -> None:
    assert _build_evaluation_gate_result_from_raw_result(
        ContractGateResult(is_valid=True, errors=()),
        "review",
    ) == EvaluationGateResult(
        result="review",
        contract_valid=True,
        errors=(),
    )


def test_build_evaluation_gate_result_from_raw_result_fails_closed_for_invalid_contract() -> None:
    assert _build_evaluation_gate_result_from_raw_result(
        ContractGateResult(
            is_valid=False,
            errors=("run_id is required", "source_lane is required"),
        ),
        "pass",
    ) == EvaluationGateResult(
        result="fail",
        contract_valid=False,
        errors=("run_id is required", "source_lane is required"),
    )


def test_run_evaluation_gate_matches_internal_raw_result_builder() -> None:
    valid_contract_result = ContractGateResult(is_valid=True, errors=())
    invalid_contract_result = ContractGateResult(
        is_valid=False,
        errors=("run_id is required",),
    )
    decision = RuntimeDecision(decision="accept", reason="ok", next_step="continue")
    event = MetaAuditEvent(
        event_type="runtime_decision",
        message="accept",
        severity="info",
        reference="ref-compare",
        run_id="run-1",
    )

    assert run_evaluation_gate(
        valid_contract_result,
        decision,
        event,
    ) == _build_evaluation_gate_result_from_raw_result(
        valid_contract_result,
        evaluate(decision, event),
    )
    assert run_evaluation_gate(
        invalid_contract_result,
        decision,
        event,
    ) == _build_evaluation_gate_result_from_raw_result(
        invalid_contract_result,
        "fail",
    )


def test_guard_evaluation_gate_result_from_raw_result_returns_no_errors_for_consistent_result() -> None:
    contract_result = ContractGateResult(is_valid=True, errors=())

    assert _guard_evaluation_gate_result_from_raw_result(
        contract_result,
        "review",
        EvaluationGateResult(result="review", contract_valid=True, errors=()),
    ) == ()


def test_guard_evaluation_gate_result_from_raw_result_reports_invalid_contract_drift() -> None:
    contract_result = ContractGateResult(
        is_valid=False,
        errors=("run_id is required",),
    )

    assert _guard_evaluation_gate_result_from_raw_result(
        contract_result,
        "pass",
        EvaluationGateResult(result="review", contract_valid=True, errors=()),
    ) == (
        "invalid contracts must force the evaluation gate result to fail",
        "invalid contracts must mark the evaluation gate result as contract-invalid",
        "invalid contracts must preserve contract errors in the evaluation gate result",
    )


def test_aggregate_runtime_contract_result_returns_valid_result_when_all_valid() -> None:
    result = _aggregate_runtime_contract_result(
        ContractGateResult(is_valid=True, errors=()),
        ContractGateResult(is_valid=True, errors=()),
        ContractGateResult(is_valid=True, errors=()),
        ContractGateResult(is_valid=True, errors=()),
    )

    assert result == ContractGateResult(is_valid=True, errors=())


def test_aggregate_runtime_contract_result_preserves_stable_error_order() -> None:
    result = _aggregate_runtime_contract_result(
        ContractGateResult(is_valid=False, errors=("agent_id is required",)),
        ContractGateResult(
            is_valid=False,
            errors=("worker name is required", "worker status is required for x"),
        ),
        ContractGateResult(is_valid=True, errors=()),
        ContractGateResult(is_valid=False, errors=("run_id is required",)),
    )

    assert result == ContractGateResult(
        is_valid=False,
        errors=(
            "agent_id is required",
            "worker name is required",
            "worker status is required for x",
            "run_id is required",
        ),
    )


def test_aggregate_runtime_contract_result_returns_all_invalid_errors() -> None:
    result = _aggregate_runtime_contract_result(
        ContractGateResult(is_valid=False, errors=("agent_id is required",)),
        ContractGateResult(is_valid=False, errors=("worker name is required",)),
        ContractGateResult(is_valid=False, errors=("reference is required",)),
        ContractGateResult(is_valid=False, errors=("run_id is required",)),
    )

    assert result == ContractGateResult(
        is_valid=False,
        errors=(
            "agent_id is required",
            "worker name is required",
            "reference is required",
            "run_id is required",
        ),
    )


def test_run_runtime_evaluation_gate_accepts_valid_runtime_contracts() -> None:
    decision = RuntimeDecision(
        decision="accept",
        reason="Confidence 0.90 meets threshold",
        next_step="continue",
    )
    event = MetaAuditEvent(
        event_type="runtime_decision",
        message="accept: Confidence 0.90 meets threshold",
        severity="info",
        reference="ref-accept",
        run_id="shade-v1",
    )

    result = _run_runtime_evaluation_gate(
        ContractGateResult(is_valid=True, errors=()),
        ContractGateResult(is_valid=True, errors=()),
        ContractGateResult(is_valid=True, errors=()),
        ContractGateResult(is_valid=True, errors=()),
        decision,
        event,
    )

    assert result == EvaluationGateResult(
        result="pass",
        contract_valid=True,
        errors=(),
    )


def test_run_runtime_evaluation_gate_returns_review_for_needs_review_path() -> None:
    decision = RuntimeDecision(
        decision="needs_review",
        reason="Confidence 0.40 requires review",
        next_step="review",
    )
    event = MetaAuditEvent(
        event_type="runtime_decision",
        message="needs_review: Confidence 0.40 requires review",
        severity="warning",
        reference="ref-review",
        run_id="shade-v1",
    )

    result = _run_runtime_evaluation_gate(
        ContractGateResult(is_valid=True, errors=()),
        ContractGateResult(is_valid=True, errors=()),
        ContractGateResult(is_valid=True, errors=()),
        ContractGateResult(is_valid=True, errors=()),
        decision,
        event,
    )

    assert result == EvaluationGateResult(
        result="review",
        contract_valid=True,
        errors=(),
    )


def test_run_runtime_evaluation_gate_returns_fail_for_reject_path() -> None:
    decision = RuntimeDecision(
        decision="reject",
        reason="No active worker for control",
        next_step="stop",
    )
    event = MetaAuditEvent(
        event_type="runtime_decision",
        message="reject: No active worker for control",
        severity="error",
        reference="ref-reject",
        run_id="shade-v1",
    )

    result = _run_runtime_evaluation_gate(
        ContractGateResult(is_valid=True, errors=()),
        ContractGateResult(is_valid=True, errors=()),
        ContractGateResult(is_valid=True, errors=()),
        ContractGateResult(is_valid=True, errors=()),
        decision,
        event,
    )

    assert result == EvaluationGateResult(
        result="fail",
        contract_valid=True,
        errors=(),
    )


def test_run_runtime_evaluation_gate_matches_raw_evaluate_for_valid_contracts() -> None:
    valid_scenarios = (
        (
            RuntimeDecision(
                decision="accept",
                reason="Confidence 0.90 meets threshold",
                next_step="continue",
            ),
            MetaAuditEvent(
                event_type="runtime_decision",
                message="accept: Confidence 0.90 meets threshold",
                severity="info",
                reference="ref-pass",
                run_id="shade-v1",
            ),
        ),
        (
            RuntimeDecision(
                decision="needs_review",
                reason="Confidence 0.40 requires review",
                next_step="review",
            ),
            MetaAuditEvent(
                event_type="runtime_decision",
                message="needs_review: Confidence 0.40 requires review",
                severity="warning",
                reference="ref-review",
                run_id="shade-v1",
            ),
        ),
        (
            RuntimeDecision(
                decision="reject",
                reason="No active worker for control",
                next_step="stop",
            ),
            MetaAuditEvent(
                event_type="runtime_decision",
                message="reject: No active worker for control",
                severity="error",
                reference="ref-reject",
                run_id="shade-v1",
            ),
        ),
    )

    for decision, event in valid_scenarios:
        result = _run_runtime_evaluation_gate(
            ContractGateResult(is_valid=True, errors=()),
            ContractGateResult(is_valid=True, errors=()),
            ContractGateResult(is_valid=True, errors=()),
            ContractGateResult(is_valid=True, errors=()),
            decision,
            event,
        )

        assert result.result == evaluate(decision, event)
        assert result.contract_valid is True
        assert result.errors == ()


def test_run_runtime_evaluation_gate_fails_for_invalid_contracts() -> None:
    decision = RuntimeDecision(
        decision="accept",
        reason="Confidence 0.90 meets threshold",
        next_step="continue",
    )
    event = MetaAuditEvent(
        event_type="runtime_decision",
        message="accept: Confidence 0.90 meets threshold",
        severity="info",
        reference="ref-invalid",
        run_id="shade-v1",
    )

    result = _run_runtime_evaluation_gate(
        ContractGateResult(is_valid=False, errors=("agent_id is required",)),
        ContractGateResult(is_valid=True, errors=()),
        ContractGateResult(is_valid=True, errors=()),
        ContractGateResult(is_valid=False, errors=("run_id is required",)),
        decision,
        event,
    )

    assert result == EvaluationGateResult(
        result="fail",
        contract_valid=False,
        errors=("agent_id is required", "run_id is required"),
    )
