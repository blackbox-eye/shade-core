from pathlib import Path
import sys

import pytest


src_path = Path(__file__).resolve().parents[1] / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from shade_core import MetaAuditEvent, RuntimeDecision, evaluate  # noqa: E402


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