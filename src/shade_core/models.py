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


@dataclass(slots=True)
class WorkerTask:
    task_id: str
    worker_role: str
    input_ref: str
    task_status: str


@dataclass(slots=True)
class WorkerResult:
    task_id: str
    worker_role: str
    output_ref: str
    result_status: str


@dataclass(slots=True)
class TaskRoute:
    task_id: str
    source_role: str
    target_role: str
    route_ref: str


@dataclass(slots=True)
class OrchestrationCheckpoint:
    task_id: str
    output_ref: str
    route_ref: str
    checkpoint_ref: str


@dataclass(slots=True)
class OrchestrationJunction:
    route_ref: str
    task_transition_ref: str
    run_transition_ref: str
    junction_ref: str


@dataclass(slots=True)
class OrchestrationVerification:
    checkpoint_ref: str
    junction_ref: str
    task_transition_ref: str
    verification_ref: str


@dataclass(slots=True)
class OrchestrationOutcome:
    verification_ref: str
    decision_ref: str
    evaluation_ref: str
    outcome_ref: str


@dataclass(slots=True)
class OrchestrationEvidence:
    verification_ref: str
    outcome_ref: str
    evaluation_ref: str
    evidence_ref: str


@dataclass(slots=True)
class OrchestrationGate:
    evidence_ref: str
    evaluation_gate_ref: str
    audit_ref: str
    gate_ref: str


@dataclass(slots=True)
class OrchestrationAudit:
    gate_ref: str
    evaluation_gate_ref: str
    audit_event_ref: str
    audit_ref: str


@dataclass(slots=True)
class OrchestrationClosure:
    audit_ref: str
    decision_ref: str
    evaluation_ref: str
    closure_ref: str


@dataclass(slots=True)
class TaskTransition:
    task_id: str
    from_status: str
    to_status: str
    transition_ref: str


@dataclass(slots=True)
class RunTransition:
    run_id: str
    from_step: str
    to_step: str
    transition_ref: str
