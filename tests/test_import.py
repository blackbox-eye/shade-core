import importlib


def test_import_smoke() -> None:
    module = importlib.import_module("shade_core")

    assert module.__version__ == "0.1.0"
    assert module.__all__ == [
        "__version__",
        "ContractGateResult",
        "ConfidenceRecord",
        "EvaluationGateResult",
        "MetaAuditEvent",
        "RunState",
        "RuntimeDecision",
        "SelfModel",
        "WorkerRegistry",
        "build_bundle",
        "evaluate",
        "run_evaluation_gate",
        "audit_decision",
        "decide",
        "serialize_evaluation_result",
        "serialize_meta_audit_event",
        "serialize_runtime_decision",
        "validate_state_contract",
    ]
