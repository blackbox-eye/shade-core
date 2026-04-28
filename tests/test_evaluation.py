import pytest

from shade_core import (  # noqa: E402
    ContractGateResult,
    MetaAuditEvent,
    RuntimeDecision,
    evaluate,
)


def test_evaluate_pass() -> None:
    decision = RuntimeDecision(decision="accept", reason="ok", next_step="continue")
    event = MetaAuditEvent(
        event_type="runtime_decision",
        message="accept",
        severity="info",
        reference="ref-pass",
        run_id="run-1",
    )

    assert evaluate(decision, event) == "pass"


def test_evaluate_review() -> None:
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

    assert evaluate(decision, event) == "review"


def test_evaluate_fail() -> None:
    decision = RuntimeDecision(decision="reject", reason="stop", next_step="stop")
    event = MetaAuditEvent(
        event_type="runtime_decision",
        message="error",
        severity="error",
        reference="ref-fail",
        run_id="run-1",
    )

    assert evaluate(decision, event) == "fail"


def test_evaluate_uses_strictest_result_on_conflict() -> None:
    decision = RuntimeDecision(decision="accept", reason="ok", next_step="continue")
    event = MetaAuditEvent(
        event_type="runtime_decision",
        message="warning",
        severity="warning",
        reference="ref-conflict",
        run_id="run-1",
    )

    assert evaluate(decision, event) == "review"


def test_evaluate_is_independent_of_contract_validity_context() -> None:
    contract_result = ContractGateResult(
        is_valid=False,
        errors=("run_id is required",),
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
        reference="ref-independent",
        run_id="run-1",
    )

    assert contract_result.is_valid is False
    assert evaluate(decision, event) == "pass"


def test_evaluate_raises_for_unknown_severity() -> None:
    decision = RuntimeDecision(decision="accept", reason="ok", next_step="continue")
    event = MetaAuditEvent(
        event_type="runtime_decision",
        message="unknown",
        severity="debug",
        reference="ref-unknown-severity",
        run_id="run-1",
    )

    with pytest.raises(ValueError, match="Unknown severity: debug"):
        evaluate(decision, event)


def test_evaluate_raises_for_unknown_decision() -> None:
    decision = RuntimeDecision(decision="hold", reason="ok", next_step="wait")
    event = MetaAuditEvent(
        event_type="runtime_decision",
        message="accept",
        severity="info",
        reference="ref-unknown-decision",
        run_id="run-1",
    )

    with pytest.raises(ValueError, match="Unknown decision: hold"):
        evaluate(decision, event)