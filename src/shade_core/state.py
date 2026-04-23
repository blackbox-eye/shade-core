from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

DecisionClass = Literal["accept", "reject", "needs_review"]
VerificationState = Literal["pending", "verified", "failed"]


@dataclass(slots=True)
class RunState:
    run_id: str
    worker_role: str
    decision_class: DecisionClass
    verification_state: VerificationState
    artifact_ref: str
    source_lane: str
    target_lane: str