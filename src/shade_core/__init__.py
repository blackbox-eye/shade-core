"""Minimal package for shade-core."""

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
	"audit_decision",
	"decide",
]

__version__ = "0.1.0"