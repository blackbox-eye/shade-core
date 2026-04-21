from __future__ import annotations

from typing import Literal

from .models import MetaAuditEvent, RuntimeDecision

EvaluationResult = Literal["pass", "review", "fail"]

_DECISION_LEVELS = {
    "accept": 0,
    "needs_review": 1,
    "reject": 2,
}

_SEVERITY_LEVELS = {
    "info": 0,
    "warning": 1,
    "error": 2,
}

_RESULT_BY_LEVEL = {
    0: "pass",
    1: "review",
    2: "fail",
}


def evaluate(decision: RuntimeDecision, event: MetaAuditEvent) -> EvaluationResult:
    try:
        decision_level = _DECISION_LEVELS[decision.decision]
    except KeyError as exc:
        raise ValueError(f"Unknown decision: {decision.decision}") from exc

    try:
        severity_level = _SEVERITY_LEVELS[event.severity]
    except KeyError as exc:
        raise ValueError(f"Unknown severity: {event.severity}") from exc

    level = max(decision_level, severity_level)
    return _RESULT_BY_LEVEL[level]