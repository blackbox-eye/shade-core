from pathlib import Path
import sys


src_path = Path(__file__).resolve().parents[1] / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from shade_core import MetaAuditEvent, RuntimeDecision, build_bundle  # noqa: E402


def test_build_bundle_returns_expected_structure() -> None:
    decision = RuntimeDecision(
        decision="accept",
        reason="klar",
        next_step="continue",
    )
    event = MetaAuditEvent(
        event_type="runtime_decision",
        message="accept: klar",
        severity="info",
        reference="ref-1",
        run_id="run-1",
    )

    assert build_bundle(decision, event, "pass") == {
        "decision": {
            "decision": "accept",
            "reason": "klar",
            "next_step": "continue",
        },
        "audit_event": {
            "event_type": "runtime_decision",
            "message": "accept: klar",
            "severity": "info",
            "reference": "ref-1",
            "run_id": "run-1",
        },
        "evaluation": {
            "result": "pass",
        },
    }