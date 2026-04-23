from __future__ import annotations

from collections.abc import Mapping

from .evaluation import EvaluationResult
from .evaluation_gate import EvaluationGateResult
from .models import ArtifactHandoff, MetaAuditEvent, RuntimeDecision
from .state import RunState
from .serialization import (
    serialize_artifact_handoff,
    serialize_evaluation_gate_result,
    serialize_evaluation_result,
    serialize_meta_audit_event,
    serialize_run_state,
    serialize_runtime_decision,
)


def _build_runtime_fabric_snapshot(
    state: RunState,
    decision: RuntimeDecision,
    audit_event: MetaAuditEvent,
    evaluation_gate_result: EvaluationGateResult,
) -> Mapping[str, Mapping[str, object]]:
    handoff = ArtifactHandoff(
        artifact_ref=state.artifact_ref,
        source_lane=state.source_lane,
        target_lane=state.target_lane,
    )

    return {
        "run_state": serialize_run_state(state),
        "artifact_handoff": serialize_artifact_handoff(handoff),
        "decision": serialize_runtime_decision(decision),
        "audit_event": serialize_meta_audit_event(audit_event),
        "evaluation_gate": serialize_evaluation_gate_result(
            evaluation_gate_result,
        ),
    }


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