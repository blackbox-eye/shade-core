from shade_core import (  # noqa: E402
    MetaAuditEvent,
    RuntimeDecision,
    serialize_evaluation_result,
    serialize_meta_audit_event,
    serialize_runtime_decision,
)


def test_serialize_runtime_decision() -> None:
    decision = RuntimeDecision(
        decision="accept",
        reason="klar",
        next_step="continue",
    )

    assert serialize_runtime_decision(decision) == {
        "decision": "accept",
        "reason": "klar",
        "next_step": "continue",
    }


def test_serialize_meta_audit_event() -> None:
    event = MetaAuditEvent(
        event_type="runtime_decision",
        message="accept: klar",
        severity="info",
        reference="ref-1",
        run_id="run-1",
    )

    assert serialize_meta_audit_event(event) == {
        "event_type": "runtime_decision",
        "message": "accept: klar",
        "severity": "info",
        "reference": "ref-1",
        "run_id": "run-1",
    }


def test_serialize_evaluation_result() -> None:
    assert serialize_evaluation_result("review") == {"result": "review"}