from shade_core import (
    ContractGateResult,
    EvaluationGateResult,
    MetaAuditEvent,
    RuntimeDecision,
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