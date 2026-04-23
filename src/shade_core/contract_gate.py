from __future__ import annotations

from dataclasses import dataclass

from .state import RunState

_DECISION_CLASSES = {"accept", "reject", "needs_review"}
_VERIFICATION_STATES = {"pending", "verified", "failed"}


@dataclass(slots=True)
class ContractGateResult:
    is_valid: bool
    errors: tuple[str, ...]


def validate_state_contract(state: RunState) -> ContractGateResult:
    errors: list[str] = []

    if not state.run_id:
        errors.append("run_id is required")
    if not state.worker_role:
        errors.append("worker_role is required")
    if state.decision_class not in _DECISION_CLASSES:
        errors.append("decision_class is invalid")
    if state.verification_state not in _VERIFICATION_STATES:
        errors.append("verification_state is invalid")
    if not state.artifact_ref:
        errors.append("artifact_ref is required")
    if not state.source_lane:
        errors.append("source_lane is required")
    if not state.target_lane:
        errors.append("target_lane is required")

    return ContractGateResult(is_valid=not errors, errors=tuple(errors))