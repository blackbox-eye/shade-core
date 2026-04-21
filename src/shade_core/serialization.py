from __future__ import annotations

from .evaluation import EvaluationResult
from .models import MetaAuditEvent, RuntimeDecision


def serialize_runtime_decision(decision: RuntimeDecision) -> dict[str, str]:
    return {
        "decision": decision.decision,
        "reason": decision.reason,
        "next_step": decision.next_step,
    }


def serialize_meta_audit_event(event: MetaAuditEvent) -> dict[str, str]:
    return {
        "event_type": event.event_type,
        "message": event.message,
        "severity": event.severity,
        "reference": event.reference,
        "run_id": event.run_id,
    }


def serialize_evaluation_result(result: EvaluationResult) -> dict[str, str]:
    return {"result": result}