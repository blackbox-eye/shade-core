"""Minimal package for shade-core."""

from .evaluation import evaluate
from .models import (
	ConfidenceRecord,
	MetaAuditEvent,
	RuntimeDecision,
	SelfModel,
	WorkerRegistry,
)
from .runtime_loop import audit_decision, decide

__all__ = [
	"__version__",
	"ConfidenceRecord",
	"MetaAuditEvent",
	"RuntimeDecision",
	"SelfModel",
	"WorkerRegistry",
	"evaluate",
	"audit_decision",
	"decide",
]

__version__ = "0.1.0"