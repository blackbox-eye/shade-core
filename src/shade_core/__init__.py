"""Minimal package for shade-core."""

from .models import (
	ConfidenceRecord,
	MetaAuditEvent,
	RuntimeDecision,
	SelfModel,
	WorkerRegistry,
)

__all__ = [
	"__version__",
	"ConfidenceRecord",
	"MetaAuditEvent",
	"RuntimeDecision",
	"SelfModel",
	"WorkerRegistry",
]

__version__ = "0.1.0"