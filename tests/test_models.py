from shade_core import (  # noqa: E402
    ConfidenceRecord,
    MetaAuditEvent,
    RuntimeDecision,
    SelfModel,
    WorkerRegistry,
)


def test_model_instantiation_smoke() -> None:
    self_model = SelfModel(agent_id="shade-v1", role="control", state="idle")
    registry = WorkerRegistry()
    registry.register(name="analysis-worker", role="analysis", status="ready")
    confidence = ConfidenceRecord(
        score=0.8,
        source="local-review",
        reason="Kort og inspectable",
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
        reason="Mangler manuel accept",
        next_step="review",
    )

    assert self_model.agent_id == "shade-v1"
    assert registry.workers["analysis-worker"] == ("analysis", "ready")
    assert confidence.reference == "ref-1"
    assert event.run_id == "run-1"
    assert decision.decision == "needs_review"