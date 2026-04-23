"""Minimal package for shade-core."""

from .bundle import build_bundle
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

__all__ = [
    "__version__",
    "ConfidenceRecord",
    "MetaAuditEvent",
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
]

__version__ = "0.1.0"