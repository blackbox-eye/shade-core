from __future__ import annotations

from .models import (
    ConfidenceRecord,
    MetaAuditEvent,
    RuntimeDecision,
    SelfModel,
    WorkerRegistry,
)

CONFIDENCE_THRESHOLD = 0.7


def decide(
    self_model: SelfModel,
    registry: WorkerRegistry,
    confidence: ConfidenceRecord,
) -> RuntimeDecision:
    if not _has_active_worker(registry):
        return RuntimeDecision(
            decision="reject",
            reason=f"Ingen aktiv worker for {self_model.role}",
            next_step="stop",
        )

    if confidence.score >= CONFIDENCE_THRESHOLD:
        return RuntimeDecision(
            decision="accept",
            reason=f"Confidence {confidence.score:.2f} er høj nok",
            next_step="continue",
        )

    return RuntimeDecision(
        decision="needs_review",
        reason=f"Confidence {confidence.score:.2f} kræver review",
        next_step="review",
    )


def audit_decision(
    self_model: SelfModel,
    decision: RuntimeDecision,
    confidence: ConfidenceRecord,
) -> MetaAuditEvent:
    severity = "info" if decision.decision == "accept" else "warning"
    if decision.decision == "reject":
        severity = "error"

    return MetaAuditEvent(
        event_type="runtime_decision",
        message=f"{decision.decision}: {decision.reason}",
        severity=severity,
        reference=confidence.reference,
        run_id=self_model.agent_id,
    )


def _has_active_worker(registry: WorkerRegistry) -> bool:
    return any(status == "active" for _, status in registry.workers.values())