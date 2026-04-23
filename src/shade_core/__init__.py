"""Minimal package for shade-core."""

from .bundle import build_bundle
from .contract_gate import ContractGateResult, validate_state_contract
from .evaluation import evaluate
from .models import (
    ConfidenceRecord,
    MetaAuditEvent,
    RuntimeDecision,
    SelfModel,
    WorkerRegistry,
)
from .runtime_loop import audit_decision, decide
from .serialization import (
    serialize_evaluation_result,
    serialize_meta_audit_event,
    serialize_runtime_decision,
)
from .state import RunState

__all__ = [
    "__version__",
    "ContractGateResult",
    "ConfidenceRecord",
    "MetaAuditEvent",
    "RunState",
    "RuntimeDecision",
    "SelfModel",
    "WorkerRegistry",
    "build_bundle",
    "evaluate",
    "audit_decision",
    "decide",
    "serialize_evaluation_result",
    "serialize_meta_audit_event",
    "serialize_runtime_decision",
    "validate_state_contract",
]

__version__ = "0.1.0"