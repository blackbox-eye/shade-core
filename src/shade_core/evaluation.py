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
    level = max(
        _DECISION_LEVELS.get(decision.decision, 2),
        _SEVERITY_LEVELS.get(event.severity, 2),
    )
    return _RESULT_BY_LEVEL[level]