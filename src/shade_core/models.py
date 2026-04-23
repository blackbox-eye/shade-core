from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

DecisionValue = Literal["accept", "reject", "needs_review"]


@dataclass(slots=True)
class SelfModel:
    agent_id: str
    role: str
    state: str


@dataclass(slots=True)
class WorkerRegistry:
    workers: dict[str, tuple[str, str]] = field(default_factory=dict)

    def register(self, name: str, role: str, status: str) -> None:
        self.workers[name] = (role, status)


@dataclass(slots=True)
class ConfidenceRecord:
    score: float
    source: str
    reason: str
    reference: str


@dataclass(slots=True)
class MetaAuditEvent:
    event_type: str
    message: str
    severity: str
    reference: str
    run_id: str


@dataclass(slots=True)
class RuntimeDecision:
    decision: DecisionValue
    reason: str
    next_step: str


@dataclass(slots=True)
class ArtifactHandoff:
    artifact_ref: str
    source_lane: str
    target_lane: str
