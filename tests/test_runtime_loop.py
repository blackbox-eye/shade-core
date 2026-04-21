from pathlib import Path
import sys


src_path = Path(__file__).resolve().parents[1] / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from shade_core import (  # noqa: E402
    ConfidenceRecord,
    SelfModel,
    WorkerRegistry,
    audit_decision,
    decide,
)


def test_decide_accept() -> None:
    self_model = SelfModel(agent_id="shade-v1", role="control", state="idle")
    registry = WorkerRegistry()
    registry.register(name="control-worker", role="control", status="active")
    confidence = ConfidenceRecord(0.9, "local", "klar", "ref-accept")

    decision = decide(self_model, registry, confidence)

    assert decision.decision == "accept"
    assert decision.next_step == "continue"


def test_decide_needs_review() -> None:
    self_model = SelfModel(agent_id="shade-v1", role="control", state="idle")
    registry = WorkerRegistry()
    registry.register(name="control-worker", role="control", status="active")
    confidence = ConfidenceRecord(0.4, "local", "uklar", "ref-review")

    decision = decide(self_model, registry, confidence)

    assert decision.decision == "needs_review"
    assert decision.next_step == "review"


def test_decide_reject_without_active_worker_and_create_audit() -> None:
    self_model = SelfModel(agent_id="shade-v1", role="control", state="idle")
    registry = WorkerRegistry()
    registry.register(name="control-worker", role="control", status="idle")
    confidence = ConfidenceRecord(0.9, "local", "klar", "ref-reject")

    decision = decide(self_model, registry, confidence)
    event = audit_decision(self_model, decision, confidence)

    assert decision.decision == "reject"
    assert decision.next_step == "stop"
    assert event.event_type == "runtime_decision"
    assert event.reference == "ref-reject"
    assert event.run_id == "shade-v1"


def test_decide_reject_with_active_worker_for_other_role() -> None:
    self_model = SelfModel(agent_id="shade-v1", role="control", state="idle")
    registry = WorkerRegistry()
    registry.register(name="analysis-worker", role="analysis", status="active")
    confidence = ConfidenceRecord(0.9, "local", "klar", "ref-other-role")

    decision = decide(self_model, registry, confidence)

    assert decision.decision == "reject"
    assert decision.next_step == "stop"