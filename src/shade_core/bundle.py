from __future__ import annotations

from .evaluation import EvaluationResult
from .models import MetaAuditEvent, RuntimeDecision
from .serialization import (
    serialize_evaluation_result,
    serialize_meta_audit_event,
    serialize_runtime_decision,
)


def build_bundle(
    decision: RuntimeDecision,
    audit_event: MetaAuditEvent,
    evaluation_result: EvaluationResult,
) -> dict[str, dict[str, str]]:
    return {
        "decision": serialize_runtime_decision(decision),
        "audit_event": serialize_meta_audit_event(audit_event),
        "evaluation": serialize_evaluation_result(evaluation_result),
    }