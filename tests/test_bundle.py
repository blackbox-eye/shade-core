from dataclasses import replace
from pathlib import Path
import sys

import shade_core.bundle as bundle_module
import shade_core.evaluation_gate as evaluation_gate_module


src_path = Path(__file__).resolve().parents[1] / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from shade_core import (  # noqa: E402
    ConfidenceRecord,
    EvaluationGateResult,
    MetaAuditEvent,
    RunState,
    RuntimeDecision,
    SelfModel,
    WorkerRegistry,
    build_bundle,
)
from shade_core.bundle import _build_audit_closure_snapshot  # noqa: E402
from shade_core.bundle import _build_checkpoint_junction_snapshot  # noqa: E402
from shade_core.bundle import _build_evidence_gate_snapshot  # noqa: E402
from shade_core.bundle import _guard_prepared_runtime_evaluation_fabric  # noqa: E402
from shade_core.bundle import _guard_runtime_evaluation_fabric_snapshot  # noqa: E402
from shade_core.bundle import _build_lineage_manifest_snapshot  # noqa: E402
from shade_core.bundle import _build_review_assertion_snapshot  # noqa: E402
from shade_core.bundle import _build_publication_release_view_snapshot  # noqa: E402
from shade_core.bundle import _prepare_runtime_evaluation_fabric  # noqa: E402
from shade_core.bundle import _build_runtime_contract_integration_snapshot  # noqa: E402
from shade_core.bundle import _build_runtime_evaluation_gate_integration_snapshot  # noqa: E402
from shade_core.bundle import _build_orchestration_contract_snapshot, _build_runtime_fabric_snapshot, _build_state_transition_snapshot  # noqa: E402
from shade_core.bundle import _build_verification_outcome_snapshot  # noqa: E402
from shade_core.models import (  # noqa: E402
    OrchestrationAssertion,
    OrchestrationAudit,
    OrchestrationClosure,
    OrchestrationCheckpoint,
    OrchestrationEvidence,
    OrchestrationGate,
    OrchestrationJunction,
    OrchestrationLineage,
    OrchestrationManifest,
    OrchestrationOutcome,
    OrchestrationPublication,
    OrchestrationReleaseView,
    OrchestrationReview,
    OrchestrationVerification,
    RunTransition,
    TaskRoute,
    TaskTransition,
    WorkerResult,
    WorkerTask,
)


def test_build_bundle_returns_expected_structure() -> None:
    decision = RuntimeDecision(
        decision="accept",
        reason="Confidence 0.90 meets threshold",
        next_step="continue",
    )
    event = MetaAuditEvent(
        event_type="runtime_decision",
        message="accept: Confidence 0.90 meets threshold",
        severity="info",
        reference="ref-1",
        run_id="run-1",
    )

    assert build_bundle(decision, event, "pass") == {
        "decision": {
            "decision": "accept",
            "reason": "Confidence 0.90 meets threshold",
            "next_step": "continue",
        },
        "audit_event": {
            "event_type": "runtime_decision",
            "message": "accept: Confidence 0.90 meets threshold",
            "severity": "info",
            "reference": "ref-1",
            "run_id": "run-1",
        },
        "evaluation": {
            "result": "pass",
        },
    }


def test_build_runtime_fabric_snapshot_returns_expected_structure() -> None:
    state = RunState(
        run_id="run-1",
        worker_role="control",
        decision_class="accept",
        verification_state="verified",
        artifact_ref="artifact-1",
        source_lane="analysis-lane",
        target_lane="review-lane",
    )
    decision = RuntimeDecision(
        decision="accept",
        reason="Confidence 0.90 meets threshold",
        next_step="continue",
    )
    event = MetaAuditEvent(
        event_type="runtime_decision",
        message="accept: Confidence 0.90 meets threshold",
        severity="info",
        reference="ref-1",
        run_id="run-1",
    )
    evaluation_gate_result = EvaluationGateResult(
        result="pass",
        contract_valid=True,
        errors=(),
    )

    assert _build_runtime_fabric_snapshot(
        state,
        decision,
        event,
        evaluation_gate_result,
    ) == {
        "run_state": {
            "run_id": "run-1",
            "worker_role": "control",
            "decision_class": "accept",
            "verification_state": "verified",
            "artifact_ref": "artifact-1",
            "source_lane": "analysis-lane",
            "target_lane": "review-lane",
        },
        "artifact_handoff": {
            "artifact_ref": "artifact-1",
            "source_lane": "analysis-lane",
            "target_lane": "review-lane",
        },
        "decision": {
            "decision": "accept",
            "reason": "Confidence 0.90 meets threshold",
            "next_step": "continue",
        },
        "audit_event": {
            "event_type": "runtime_decision",
            "message": "accept: Confidence 0.90 meets threshold",
            "severity": "info",
            "reference": "ref-1",
            "run_id": "run-1",
        },
        "evaluation_gate": {
            "result": "pass",
            "contract_valid": True,
            "errors": (),
        },
    }


def test_prepare_runtime_evaluation_fabric_evaluates_once_and_reuses_raw_result(
    monkeypatch,
) -> None:
    self_model = SelfModel(agent_id="shade-v1", role="control", state="idle")
    registry = WorkerRegistry()
    registry.register(name="control-worker", role="control", status="active")
    confidence = ConfidenceRecord(0.9, "local", "clear", "ref-accept")
    state = RunState(
        run_id="run-1",
        worker_role="control",
        decision_class="accept",
        verification_state="verified",
        artifact_ref="artifact-1",
        source_lane="analysis-lane",
        target_lane="review-lane",
    )
    call_counts = {"bundle": 0, "gate": 0}
    original_bundle_evaluate = bundle_module.evaluate
    original_gate_evaluate = evaluation_gate_module.evaluate

    def counted_bundle_evaluate(decision, event):
        call_counts["bundle"] += 1
        return original_bundle_evaluate(decision, event)

    def counted_gate_evaluate(decision, event):
        call_counts["gate"] += 1
        return original_gate_evaluate(decision, event)

    monkeypatch.setattr(bundle_module, "evaluate", counted_bundle_evaluate)
    monkeypatch.setattr(
        evaluation_gate_module,
        "evaluate",
        counted_gate_evaluate,
    )

    prepared_fabric = _prepare_runtime_evaluation_fabric(
        self_model,
        registry,
        confidence,
        state,
    )

    assert call_counts == {"bundle": 1, "gate": 0}
    assert prepared_fabric.aggregated_contract_result.is_valid is True
    assert prepared_fabric.raw_evaluation_result == "pass"
    assert prepared_fabric.evaluation_gate_result == EvaluationGateResult(
        result="pass",
        contract_valid=True,
        errors=(),
    )


def test_prepare_runtime_evaluation_fabric_returns_fail_gate_for_invalid_contract() -> None:
    self_model = SelfModel(agent_id="shade-v1", role="control", state="idle")
    registry = WorkerRegistry()
    registry.register(name="control-worker", role="control", status="active")
    confidence = ConfidenceRecord(0.9, "local", "clear", "ref-invalid")
    state = RunState(
        run_id="",
        worker_role="control",
        decision_class="accept",
        verification_state="verified",
        artifact_ref="artifact-1",
        source_lane="",
        target_lane="review-lane",
    )

    prepared_fabric = _prepare_runtime_evaluation_fabric(
        self_model,
        registry,
        confidence,
        state,
    )

    assert prepared_fabric.aggregated_contract_result.is_valid is False
    assert prepared_fabric.aggregated_contract_result.errors == (
        "run_id is required",
        "source_lane is required",
    )
    assert prepared_fabric.raw_evaluation_result == "pass"
    assert prepared_fabric.evaluation_gate_result == EvaluationGateResult(
        result="fail",
        contract_valid=False,
        errors=("run_id is required", "source_lane is required"),
    )


def test_build_runtime_contract_integration_snapshot_accepts_valid_runtime_inputs() -> None:
    self_model = SelfModel(agent_id="shade-v1", role="control", state="idle")
    registry = WorkerRegistry()
    registry.register(name="control-worker", role="control", status="active")
    confidence = ConfidenceRecord(0.9, "local", "clear", "ref-accept")
    state = RunState(
        run_id="run-1",
        worker_role="control",
        decision_class="accept",
        verification_state="verified",
        artifact_ref="artifact-1",
        source_lane="analysis-lane",
        target_lane="review-lane",
    )
    prepared_fabric = _prepare_runtime_evaluation_fabric(
        self_model,
        registry,
        confidence,
        state,
    )

    assert _build_runtime_contract_integration_snapshot(
        state,
        prepared_fabric,
    ) == {
        "contract_gate": {
            "self_model": {"is_valid": True, "errors": ()},
            "worker_registry": {"is_valid": True, "errors": ()},
            "confidence_record": {"is_valid": True, "errors": ()},
            "state_contract": {"is_valid": True, "errors": ()},
        },
        "runtime_fabric": {
            "run_state": {
                "run_id": "run-1",
                "worker_role": "control",
                "decision_class": "accept",
                "verification_state": "verified",
                "artifact_ref": "artifact-1",
                "source_lane": "analysis-lane",
                "target_lane": "review-lane",
            },
            "artifact_handoff": {
                "artifact_ref": "artifact-1",
                "source_lane": "analysis-lane",
                "target_lane": "review-lane",
            },
            "decision": {
                "decision": "accept",
                "reason": "Confidence 0.90 meets threshold",
                "next_step": "continue",
            },
            "audit_event": {
                "event_type": "runtime_decision",
                "message": "accept: Confidence 0.90 meets threshold",
                "severity": "info",
                "reference": "ref-accept",
                "run_id": "shade-v1",
            },
            "evaluation_gate": {
                "result": "pass",
                "contract_valid": True,
                "errors": (),
            },
        },
    }


def test_build_runtime_contract_integration_snapshot_rejects_without_active_worker() -> None:
    self_model = SelfModel(agent_id="shade-v1", role="control", state="idle")
    registry = WorkerRegistry()
    registry.register(name="analysis-worker", role="analysis", status="active")
    confidence = ConfidenceRecord(0.9, "local", "clear", "ref-reject")
    state = RunState(
        run_id="run-1",
        worker_role="control",
        decision_class="reject",
        verification_state="pending",
        artifact_ref="artifact-1",
        source_lane="analysis-lane",
        target_lane="review-lane",
    )
    prepared_fabric = _prepare_runtime_evaluation_fabric(
        self_model,
        registry,
        confidence,
        state,
    )

    assert _build_runtime_contract_integration_snapshot(
        state,
        prepared_fabric,
    ) == {
        "contract_gate": {
            "self_model": {"is_valid": True, "errors": ()},
            "worker_registry": {"is_valid": True, "errors": ()},
            "confidence_record": {"is_valid": True, "errors": ()},
            "state_contract": {"is_valid": True, "errors": ()},
        },
        "runtime_fabric": {
            "run_state": {
                "run_id": "run-1",
                "worker_role": "control",
                "decision_class": "reject",
                "verification_state": "pending",
                "artifact_ref": "artifact-1",
                "source_lane": "analysis-lane",
                "target_lane": "review-lane",
            },
            "artifact_handoff": {
                "artifact_ref": "artifact-1",
                "source_lane": "analysis-lane",
                "target_lane": "review-lane",
            },
            "decision": {
                "decision": "reject",
                "reason": "No active worker for control",
                "next_step": "stop",
            },
            "audit_event": {
                "event_type": "runtime_decision",
                "message": "reject: No active worker for control",
                "severity": "error",
                "reference": "ref-reject",
                "run_id": "shade-v1",
            },
            "evaluation_gate": {
                    "result": "fail",
                "contract_valid": True,
                "errors": (),
            },
        },
    }


def test_build_runtime_contract_integration_snapshot_skips_top_level_serializers(
    monkeypatch,
) -> None:
    self_model = SelfModel(agent_id="shade-v1", role="control", state="idle")
    registry = WorkerRegistry()
    registry.register(name="control-worker", role="control", status="active")
    confidence = ConfidenceRecord(0.9, "local", "clear", "ref-minimal")
    state = RunState(
        run_id="run-1",
        worker_role="control",
        decision_class="accept",
        verification_state="verified",
        artifact_ref="artifact-1",
        source_lane="analysis-lane",
        target_lane="review-lane",
    )
    prepared_fabric = _prepare_runtime_evaluation_fabric(
        self_model,
        registry,
        confidence,
        state,
    )
    captured = {"evaluation_gate_arg": None}

    def fail_aggregated_serializer(*_args, **_kwargs):
        raise AssertionError("aggregated contract gate should not serialize")

    def fail_raw_evaluation_serializer(*_args, **_kwargs):
        raise AssertionError("raw evaluation should not serialize")

    def fail_top_level_evaluation_gate_serializer(*_args, **_kwargs):
        raise AssertionError("top-level evaluation gate should not serialize")

    def fake_runtime_contract_gate(*_args, **_kwargs):
        return {"contract_gate": "sentinel"}

    def fake_runtime_fabric(state_arg, decision_arg, audit_event_arg, evaluation_gate_arg):
        captured["evaluation_gate_arg"] = evaluation_gate_arg
        assert state_arg is state
        assert decision_arg is prepared_fabric.decision
        assert audit_event_arg is prepared_fabric.audit_event
        return {"runtime_fabric": "sentinel"}

    monkeypatch.setattr(
        bundle_module,
        "_serialize_aggregated_runtime_contract_gate",
        fail_aggregated_serializer,
    )
    monkeypatch.setattr(
        bundle_module,
        "serialize_evaluation_result",
        fail_raw_evaluation_serializer,
    )
    monkeypatch.setattr(
        bundle_module,
        "serialize_evaluation_gate_result",
        fail_top_level_evaluation_gate_serializer,
    )
    monkeypatch.setattr(
        bundle_module,
        "serialize_runtime_contract_gate",
        fake_runtime_contract_gate,
    )
    monkeypatch.setattr(
        bundle_module,
        "_build_runtime_fabric_snapshot",
        fake_runtime_fabric,
    )

    assert _build_runtime_contract_integration_snapshot(
        state,
        prepared_fabric,
    ) == {
        "contract_gate": {"contract_gate": "sentinel"},
        "runtime_fabric": {"runtime_fabric": "sentinel"},
    }
    assert captured["evaluation_gate_arg"] is prepared_fabric.evaluation_gate_result


def test_build_runtime_evaluation_gate_integration_snapshot_accepts_valid_runtime_inputs() -> None:
    self_model = SelfModel(agent_id="shade-v1", role="control", state="idle")
    registry = WorkerRegistry()
    registry.register(name="control-worker", role="control", status="active")
    confidence = ConfidenceRecord(0.9, "local", "clear", "ref-accept")
    state = RunState(
        run_id="run-1",
        worker_role="control",
        decision_class="accept",
        verification_state="verified",
        artifact_ref="artifact-1",
        source_lane="analysis-lane",
        target_lane="review-lane",
    )

    assert _build_runtime_evaluation_gate_integration_snapshot(
        self_model,
        registry,
        confidence,
        state,
    ) == {
        "runtime_contract_integration": {
            "contract_gate": {
                "self_model": {"is_valid": True, "errors": ()},
                "worker_registry": {"is_valid": True, "errors": ()},
                "confidence_record": {"is_valid": True, "errors": ()},
                "state_contract": {"is_valid": True, "errors": ()},
            },
            "runtime_fabric": {
                "run_state": {
                    "run_id": "run-1",
                    "worker_role": "control",
                    "decision_class": "accept",
                    "verification_state": "verified",
                    "artifact_ref": "artifact-1",
                    "source_lane": "analysis-lane",
                    "target_lane": "review-lane",
                },
                "artifact_handoff": {
                    "artifact_ref": "artifact-1",
                    "source_lane": "analysis-lane",
                    "target_lane": "review-lane",
                },
                "decision": {
                    "decision": "accept",
                    "reason": "Confidence 0.90 meets threshold",
                    "next_step": "continue",
                },
                "audit_event": {
                    "event_type": "runtime_decision",
                    "message": "accept: Confidence 0.90 meets threshold",
                    "severity": "info",
                    "reference": "ref-accept",
                    "run_id": "shade-v1",
                },
                "evaluation_gate": {
                    "result": "pass",
                    "contract_valid": True,
                    "errors": (),
                },
            },
        },
        "aggregated_contract_gate": {"is_valid": True, "errors": ()},
        "raw_evaluation": {"result": "pass"},
        "evaluation_gate": {
            "result": "pass",
            "contract_valid": True,
            "errors": (),
        },
    }


def test_build_runtime_evaluation_gate_integration_snapshot_returns_review_path() -> None:
    self_model = SelfModel(agent_id="shade-v1", role="control", state="idle")
    registry = WorkerRegistry()
    registry.register(name="control-worker", role="control", status="active")
    confidence = ConfidenceRecord(0.4, "local", "unclear", "ref-review")
    state = RunState(
        run_id="run-1",
        worker_role="control",
        decision_class="needs_review",
        verification_state="pending",
        artifact_ref="artifact-1",
        source_lane="analysis-lane",
        target_lane="review-lane",
    )

    assert _build_runtime_evaluation_gate_integration_snapshot(
        self_model,
        registry,
        confidence,
        state,
    ) == {
        "runtime_contract_integration": {
            "contract_gate": {
                "self_model": {"is_valid": True, "errors": ()},
                "worker_registry": {"is_valid": True, "errors": ()},
                "confidence_record": {"is_valid": True, "errors": ()},
                "state_contract": {"is_valid": True, "errors": ()},
            },
            "runtime_fabric": {
                "run_state": {
                    "run_id": "run-1",
                    "worker_role": "control",
                    "decision_class": "needs_review",
                    "verification_state": "pending",
                    "artifact_ref": "artifact-1",
                    "source_lane": "analysis-lane",
                    "target_lane": "review-lane",
                },
                "artifact_handoff": {
                    "artifact_ref": "artifact-1",
                    "source_lane": "analysis-lane",
                    "target_lane": "review-lane",
                },
                "decision": {
                    "decision": "needs_review",
                    "reason": "Confidence 0.40 requires review",
                    "next_step": "review",
                },
                "audit_event": {
                    "event_type": "runtime_decision",
                    "message": "needs_review: Confidence 0.40 requires review",
                    "severity": "warning",
                    "reference": "ref-review",
                    "run_id": "shade-v1",
                },
                "evaluation_gate": {
                    "result": "review",
                    "contract_valid": True,
                    "errors": (),
                },
            },
        },
        "aggregated_contract_gate": {"is_valid": True, "errors": ()},
        "raw_evaluation": {"result": "review"},
        "evaluation_gate": {
            "result": "review",
            "contract_valid": True,
            "errors": (),
        },
    }


def test_build_runtime_evaluation_gate_integration_snapshot_returns_reject_path() -> None:
    self_model = SelfModel(agent_id="shade-v1", role="control", state="idle")
    registry = WorkerRegistry()
    registry.register(name="analysis-worker", role="analysis", status="active")
    confidence = ConfidenceRecord(0.9, "local", "clear", "ref-reject")
    state = RunState(
        run_id="run-1",
        worker_role="control",
        decision_class="reject",
        verification_state="pending",
        artifact_ref="artifact-1",
        source_lane="analysis-lane",
        target_lane="review-lane",
    )

    assert _build_runtime_evaluation_gate_integration_snapshot(
        self_model,
        registry,
        confidence,
        state,
    ) == {
        "runtime_contract_integration": {
            "contract_gate": {
                "self_model": {"is_valid": True, "errors": ()},
                "worker_registry": {"is_valid": True, "errors": ()},
                "confidence_record": {"is_valid": True, "errors": ()},
                "state_contract": {"is_valid": True, "errors": ()},
            },
            "runtime_fabric": {
                "run_state": {
                    "run_id": "run-1",
                    "worker_role": "control",
                    "decision_class": "reject",
                    "verification_state": "pending",
                    "artifact_ref": "artifact-1",
                    "source_lane": "analysis-lane",
                    "target_lane": "review-lane",
                },
                "artifact_handoff": {
                    "artifact_ref": "artifact-1",
                    "source_lane": "analysis-lane",
                    "target_lane": "review-lane",
                },
                "decision": {
                    "decision": "reject",
                    "reason": "No active worker for control",
                    "next_step": "stop",
                },
                "audit_event": {
                    "event_type": "runtime_decision",
                    "message": "reject: No active worker for control",
                    "severity": "error",
                    "reference": "ref-reject",
                    "run_id": "shade-v1",
                },
                "evaluation_gate": {
                    "result": "fail",
                    "contract_valid": True,
                    "errors": (),
                },
            },
        },
        "aggregated_contract_gate": {"is_valid": True, "errors": ()},
        "raw_evaluation": {"result": "fail"},
        "evaluation_gate": {
            "result": "fail",
            "contract_valid": True,
            "errors": (),
        },
    }


def test_build_runtime_evaluation_gate_integration_snapshot_fails_for_invalid_contract() -> None:
    self_model = SelfModel(agent_id="shade-v1", role="control", state="idle")
    registry = WorkerRegistry()
    registry.register(name="control-worker", role="control", status="active")
    confidence = ConfidenceRecord(0.9, "local", "clear", "ref-invalid")
    state = RunState(
        run_id="",
        worker_role="control",
        decision_class="accept",
        verification_state="verified",
        artifact_ref="artifact-1",
        source_lane="",
        target_lane="review-lane",
    )

    assert _build_runtime_evaluation_gate_integration_snapshot(
        self_model,
        registry,
        confidence,
        state,
    ) == {
        "runtime_contract_integration": {
            "contract_gate": {
                "self_model": {"is_valid": True, "errors": ()},
                "worker_registry": {"is_valid": True, "errors": ()},
                "confidence_record": {"is_valid": True, "errors": ()},
                "state_contract": {
                    "is_valid": False,
                    "errors": ("run_id is required", "source_lane is required"),
                },
            },
            "runtime_fabric": {
                "run_state": {
                    "run_id": "",
                    "worker_role": "control",
                    "decision_class": "accept",
                    "verification_state": "verified",
                    "artifact_ref": "artifact-1",
                    "source_lane": "",
                    "target_lane": "review-lane",
                },
                "artifact_handoff": {
                    "artifact_ref": "artifact-1",
                    "source_lane": "",
                    "target_lane": "review-lane",
                },
                "decision": {
                    "decision": "accept",
                    "reason": "Confidence 0.90 meets threshold",
                    "next_step": "continue",
                },
                "audit_event": {
                    "event_type": "runtime_decision",
                    "message": "accept: Confidence 0.90 meets threshold",
                    "severity": "info",
                    "reference": "ref-invalid",
                    "run_id": "shade-v1",
                },
                "evaluation_gate": {
                    "result": "fail",
                    "contract_valid": False,
                    "errors": ("run_id is required", "source_lane is required"),
                },
            },
        },
        "aggregated_contract_gate": {
            "is_valid": False,
            "errors": ("run_id is required", "source_lane is required"),
        },
        "raw_evaluation": {"result": "pass"},
        "evaluation_gate": {
            "result": "fail",
            "contract_valid": False,
            "errors": ("run_id is required", "source_lane is required"),
        },
    }


def test_build_runtime_evaluation_gate_integration_snapshot_keeps_valid_results_in_sync() -> None:
    self_model = SelfModel(agent_id="shade-v1", role="control", state="idle")
    valid_scenarios = (
        (
            ("control-worker", "control", "active"),
            ConfidenceRecord(0.9, "local", "clear", "ref-pass"),
            RunState(
                run_id="run-pass",
                worker_role="control",
                decision_class="accept",
                verification_state="verified",
                artifact_ref="artifact-1",
                source_lane="analysis-lane",
                target_lane="review-lane",
            ),
            "pass",
        ),
        (
            ("control-worker", "control", "active"),
            ConfidenceRecord(0.4, "local", "unclear", "ref-review"),
            RunState(
                run_id="run-review",
                worker_role="control",
                decision_class="needs_review",
                verification_state="pending",
                artifact_ref="artifact-1",
                source_lane="analysis-lane",
                target_lane="review-lane",
            ),
            "review",
        ),
        (
            ("analysis-worker", "analysis", "active"),
            ConfidenceRecord(0.9, "local", "clear", "ref-fail"),
            RunState(
                run_id="run-fail",
                worker_role="control",
                decision_class="reject",
                verification_state="pending",
                artifact_ref="artifact-1",
                source_lane="analysis-lane",
                target_lane="review-lane",
            ),
            "fail",
        ),
    )

    for worker_entry, confidence, state, expected_result in valid_scenarios:
        registry = WorkerRegistry()
        registry.register(
            name=worker_entry[0],
            role=worker_entry[1],
            status=worker_entry[2],
        )

        snapshot = _build_runtime_evaluation_gate_integration_snapshot(
            self_model,
            registry,
            confidence,
            state,
        )

        assert snapshot["aggregated_contract_gate"] == {
            "is_valid": True,
            "errors": (),
        }
        assert snapshot["runtime_contract_integration"]["runtime_fabric"][
            "evaluation_gate"
        ] == snapshot["evaluation_gate"]
        assert snapshot["raw_evaluation"]["result"] == expected_result
        assert snapshot["evaluation_gate"]["result"] == expected_result


def test_build_runtime_evaluation_gate_integration_snapshot_uses_stable_invalid_aggregation() -> None:
    self_model = SelfModel(agent_id="", role="control", state="idle")
    registry = WorkerRegistry()
    registry.register(name="control-worker", role="control", status="active")
    confidence = ConfidenceRecord(0.9, "local", "clear", "")
    state = RunState(
        run_id="",
        worker_role="control",
        decision_class="accept",
        verification_state="verified",
        artifact_ref="artifact-1",
        source_lane="",
        target_lane="review-lane",
    )

    snapshot = _build_runtime_evaluation_gate_integration_snapshot(
        self_model,
        registry,
        confidence,
        state,
    )
    nested_contract_gate = snapshot["runtime_contract_integration"][
        "contract_gate"
    ]

    assert snapshot["runtime_contract_integration"]["runtime_fabric"][
        "evaluation_gate"
    ] == snapshot["evaluation_gate"]
    assert snapshot["aggregated_contract_gate"] == {
        "is_valid": False,
        "errors": (
            *nested_contract_gate["self_model"]["errors"],
            *nested_contract_gate["worker_registry"]["errors"],
            *nested_contract_gate["confidence_record"]["errors"],
            *nested_contract_gate["state_contract"]["errors"],
        ),
    }
    assert snapshot["aggregated_contract_gate"]["errors"] == (
        "agent_id is required",
        "reference is required",
        "run_id is required",
        "source_lane is required",
    )
    assert snapshot["raw_evaluation"] == {"result": "pass"}
    assert snapshot["evaluation_gate"] == {
        "result": "fail",
        "contract_valid": False,
        "errors": (
            "agent_id is required",
            "reference is required",
            "run_id is required",
            "source_lane is required",
        ),
    }


def test_build_runtime_evaluation_gate_integration_snapshot_serializes_shared_fragments_once(
    monkeypatch,
) -> None:
    self_model = SelfModel(agent_id="shade-v1", role="control", state="idle")
    registry = WorkerRegistry()
    registry.register(name="control-worker", role="control", status="active")
    confidence = ConfidenceRecord(0.9, "local", "clear", "ref-once")
    state = RunState(
        run_id="run-1",
        worker_role="control",
        decision_class="accept",
        verification_state="verified",
        artifact_ref="artifact-1",
        source_lane="analysis-lane",
        target_lane="review-lane",
    )
    call_counts = {"evaluation_gate": 0, "contract_gate": 0}
    original_evaluation_gate_serializer = bundle_module.serialize_evaluation_gate_result
    original_contract_gate_serializer = bundle_module.serialize_runtime_contract_gate

    def counted_evaluation_gate_serializer(result):
        call_counts["evaluation_gate"] += 1
        return original_evaluation_gate_serializer(result)

    def counted_contract_gate_serializer(
        self_model_result,
        worker_registry_result,
        confidence_record_result,
        state_contract_result,
    ):
        call_counts["contract_gate"] += 1
        return original_contract_gate_serializer(
            self_model_result,
            worker_registry_result,
            confidence_record_result,
            state_contract_result,
        )

    monkeypatch.setattr(
        bundle_module,
        "serialize_evaluation_gate_result",
        counted_evaluation_gate_serializer,
    )
    monkeypatch.setattr(
        bundle_module,
        "serialize_runtime_contract_gate",
        counted_contract_gate_serializer,
    )

    snapshot = _build_runtime_evaluation_gate_integration_snapshot(
        self_model,
        registry,
        confidence,
        state,
    )

    assert call_counts == {"evaluation_gate": 1, "contract_gate": 1}
    assert snapshot["runtime_contract_integration"]["runtime_fabric"][
        "evaluation_gate"
    ] == snapshot["evaluation_gate"]


def test_guard_prepared_runtime_evaluation_fabric_returns_no_errors_for_consistent_paths() -> None:
    self_model = SelfModel(agent_id="shade-v1", role="control", state="idle")
    scenarios = (
        (
            ("control-worker", "control", "active"),
            ConfidenceRecord(0.9, "local", "clear", "ref-pass"),
            RunState(
                run_id="run-pass",
                worker_role="control",
                decision_class="accept",
                verification_state="verified",
                artifact_ref="artifact-1",
                source_lane="analysis-lane",
                target_lane="review-lane",
            ),
        ),
        (
            ("control-worker", "control", "active"),
            ConfidenceRecord(0.4, "local", "unclear", "ref-review"),
            RunState(
                run_id="run-review",
                worker_role="control",
                decision_class="needs_review",
                verification_state="pending",
                artifact_ref="artifact-1",
                source_lane="analysis-lane",
                target_lane="review-lane",
            ),
        ),
        (
            ("analysis-worker", "analysis", "active"),
            ConfidenceRecord(0.9, "local", "clear", "ref-reject"),
            RunState(
                run_id="run-reject",
                worker_role="control",
                decision_class="reject",
                verification_state="pending",
                artifact_ref="artifact-1",
                source_lane="analysis-lane",
                target_lane="review-lane",
            ),
        ),
        (
            ("control-worker", "control", "active"),
            ConfidenceRecord(0.9, "local", "clear", ""),
            RunState(
                run_id="",
                worker_role="control",
                decision_class="accept",
                verification_state="verified",
                artifact_ref="artifact-1",
                source_lane="",
                target_lane="review-lane",
            ),
        ),
    )

    for worker_entry, confidence, state in scenarios:
        registry = WorkerRegistry()
        registry.register(
            name=worker_entry[0],
            role=worker_entry[1],
            status=worker_entry[2],
        )

        prepared_fabric = _prepare_runtime_evaluation_fabric(
            self_model,
            registry,
            confidence,
            state,
        )

        assert _guard_prepared_runtime_evaluation_fabric(prepared_fabric) == ()


def test_guard_prepared_runtime_evaluation_fabric_detects_mutated_contract_alignment() -> None:
    self_model = SelfModel(agent_id="shade-v1", role="control", state="idle")
    registry = WorkerRegistry()
    registry.register(name="control-worker", role="control", status="active")
    confidence = ConfidenceRecord(0.9, "local", "clear", "ref-mutate")
    state = RunState(
        run_id="run-1",
        worker_role="control",
        decision_class="accept",
        verification_state="verified",
        artifact_ref="artifact-1",
        source_lane="analysis-lane",
        target_lane="review-lane",
    )
    prepared_fabric = _prepare_runtime_evaluation_fabric(
        self_model,
        registry,
        confidence,
        state,
    )
    mutated_prepared_fabric = replace(
        prepared_fabric,
        aggregated_contract_result=bundle_module.ContractGateResult(
            is_valid=False,
            errors=("agent_id is required",),
        ),
    )

    assert _guard_prepared_runtime_evaluation_fabric(
        mutated_prepared_fabric,
    ) == (
        "prepared_fabric.aggregated_contract_result must equal the aggregated component contract results",
        "prepared_fabric.evaluation_gate_result must match the aggregated contract result and raw evaluation result",
        "prepared_fabric.invalid contracts must force the gated evaluation result to fail",
        "prepared_fabric.invalid contracts must preserve aggregated contract errors in the gated evaluation result",
    )


def test_guard_prepared_runtime_evaluation_fabric_detects_invalid_decision_and_audit() -> None:
    self_model = SelfModel(agent_id="shade-v1", role="control", state="idle")
    registry = WorkerRegistry()
    registry.register(name="control-worker", role="control", status="active")
    confidence = ConfidenceRecord(0.9, "local", "clear", "ref-invalid")
    state = RunState(
        run_id="run-1",
        worker_role="control",
        decision_class="accept",
        verification_state="verified",
        artifact_ref="artifact-1",
        source_lane="analysis-lane",
        target_lane="review-lane",
    )
    prepared_fabric = _prepare_runtime_evaluation_fabric(
        self_model,
        registry,
        confidence,
        state,
    )
    mutated_prepared_fabric = replace(
        prepared_fabric,
        decision=RuntimeDecision(decision="hold", reason="", next_step=""),
        audit_event=MetaAuditEvent(
            event_type="",
            message="",
            severity="",
            reference="",
            run_id="",
        ),
    )

    assert _guard_prepared_runtime_evaluation_fabric(
        mutated_prepared_fabric,
    ) == (
        "prepared_fabric.decision must satisfy the runtime decision contract",
        "prepared_fabric.audit_event must satisfy the meta audit contract",
    )


def test_guard_runtime_evaluation_fabric_snapshot_returns_no_errors_for_consistent_paths() -> None:
    self_model = SelfModel(agent_id="shade-v1", role="control", state="idle")
    scenarios = (
        (
            ("control-worker", "control", "active"),
            ConfidenceRecord(0.9, "local", "clear", "ref-pass"),
            RunState(
                run_id="run-pass",
                worker_role="control",
                decision_class="accept",
                verification_state="verified",
                artifact_ref="artifact-1",
                source_lane="analysis-lane",
                target_lane="review-lane",
            ),
        ),
        (
            ("control-worker", "control", "active"),
            ConfidenceRecord(0.4, "local", "unclear", "ref-review"),
            RunState(
                run_id="run-review",
                worker_role="control",
                decision_class="needs_review",
                verification_state="pending",
                artifact_ref="artifact-1",
                source_lane="analysis-lane",
                target_lane="review-lane",
            ),
        ),
        (
            ("analysis-worker", "analysis", "active"),
            ConfidenceRecord(0.9, "local", "clear", "ref-reject"),
            RunState(
                run_id="run-reject",
                worker_role="control",
                decision_class="reject",
                verification_state="pending",
                artifact_ref="artifact-1",
                source_lane="analysis-lane",
                target_lane="review-lane",
            ),
        ),
        (
            ("control-worker", "control", "active"),
            ConfidenceRecord(0.9, "local", "clear", ""),
            RunState(
                run_id="",
                worker_role="control",
                decision_class="accept",
                verification_state="verified",
                artifact_ref="artifact-1",
                source_lane="",
                target_lane="review-lane",
            ),
        ),
    )

    for worker_entry, confidence, state in scenarios:
        registry = WorkerRegistry()
        registry.register(
            name=worker_entry[0],
            role=worker_entry[1],
            status=worker_entry[2],
        )

        snapshot = _build_runtime_evaluation_gate_integration_snapshot(
            self_model,
            registry,
            confidence,
            state,
        )

        assert _guard_runtime_evaluation_fabric_snapshot(snapshot) == ()


def test_guard_runtime_evaluation_fabric_snapshot_detects_synthetic_inconsistencies() -> None:
    self_model = SelfModel(agent_id="shade-v1", role="control", state="idle")
    registry = WorkerRegistry()
    registry.register(name="control-worker", role="control", status="active")
    confidence = ConfidenceRecord(0.9, "local", "clear", "")
    state = RunState(
        run_id="",
        worker_role="control",
        decision_class="accept",
        verification_state="verified",
        artifact_ref="artifact-1",
        source_lane="",
        target_lane="review-lane",
    )
    snapshot = _build_runtime_evaluation_gate_integration_snapshot(
        self_model,
        registry,
        confidence,
        state,
    )
    mutated_snapshot = {
        **snapshot,
        "aggregated_contract_gate": {
            "is_valid": False,
            "errors": (
                "source_lane is required",
                "run_id is required",
            ),
        },
        "evaluation_gate": {
            "result": "pass",
            "contract_valid": True,
            "errors": (),
        },
    }

    assert _guard_runtime_evaluation_fabric_snapshot(mutated_snapshot) == (
        "snapshot.runtime_contract_integration.runtime_fabric.evaluation_gate must equal snapshot.evaluation_gate",
        "snapshot.aggregated_contract_gate must equal the aggregation implied by nested contract_gate entries",
        "snapshot.invalid contracts must force evaluation_gate.result to fail",
        "snapshot.invalid contracts must mark evaluation_gate.contract_valid as false",
        "snapshot.invalid contracts must preserve aggregated_contract_gate.errors in evaluation_gate.errors",
    )


def test_guard_runtime_evaluation_fabric_snapshot_reports_mapping_errors_without_raising() -> None:
    assert _guard_runtime_evaluation_fabric_snapshot(
        {"runtime_contract_integration": "invalid"},
    ) == (
        "snapshot.runtime_contract_integration must be a mapping",
    )


def test_guard_runtime_evaluation_fabric_snapshot_handles_malformed_nested_contract_gate_entries() -> None:
    self_model = SelfModel(agent_id="shade-v1", role="control", state="idle")
    registry = WorkerRegistry()
    registry.register(name="control-worker", role="control", status="active")
    confidence = ConfidenceRecord(0.9, "local", "clear", "ref-malformed")
    state = RunState(
        run_id="run-1",
        worker_role="control",
        decision_class="accept",
        verification_state="verified",
        artifact_ref="artifact-1",
        source_lane="analysis-lane",
        target_lane="review-lane",
    )
    snapshot = _build_runtime_evaluation_gate_integration_snapshot(
        self_model,
        registry,
        confidence,
        state,
    )
    snapshot["runtime_contract_integration"]["contract_gate"] = {
        "self_model": 7,
        "worker_registry": {"is_valid": True, "errors": ()},
        "confidence_record": "invalid",
        "state_contract": None,
    }

    assert _guard_runtime_evaluation_fabric_snapshot(snapshot) == (
        "snapshot.runtime_contract_integration.contract_gate.self_model must be a mapping",
        "snapshot.runtime_contract_integration.contract_gate.confidence_record must be a mapping",
        "snapshot.runtime_contract_integration.contract_gate.state_contract must be a mapping",
        "snapshot.aggregated_contract_gate must equal the aggregation implied by nested contract_gate entries",
    )


def test_guard_runtime_evaluation_fabric_snapshot_compares_list_errors_by_content() -> None:
    self_model = SelfModel(agent_id="shade-v1", role="control", state="idle")
    registry = WorkerRegistry()
    registry.register(name="control-worker", role="control", status="active")
    confidence = ConfidenceRecord(0.9, "local", "clear", "ref-list")
    state = RunState(
        run_id="",
        worker_role="control",
        decision_class="accept",
        verification_state="verified",
        artifact_ref="artifact-1",
        source_lane="",
        target_lane="review-lane",
    )
    snapshot = _build_runtime_evaluation_gate_integration_snapshot(
        self_model,
        registry,
        confidence,
        state,
    )
    list_errors = ["run_id is required", "source_lane is required"]
    snapshot["aggregated_contract_gate"] = {
        "is_valid": False,
        "errors": list_errors,
    }
    snapshot["evaluation_gate"] = {
        "result": "fail",
        "contract_valid": False,
        "errors": list_errors,
    }
    snapshot["runtime_contract_integration"]["runtime_fabric"]["evaluation_gate"] = {
        "result": "fail",
        "contract_valid": False,
        "errors": ["run_id is required", "source_lane is required"],
    }

    assert _guard_runtime_evaluation_fabric_snapshot(snapshot) == ()


def test_guard_runtime_evaluation_fabric_snapshot_reports_invalid_non_sequence_errors() -> None:
    self_model = SelfModel(agent_id="shade-v1", role="control", state="idle")
    registry = WorkerRegistry()
    registry.register(name="control-worker", role="control", status="active")
    confidence = ConfidenceRecord(0.9, "local", "clear", "")
    state = RunState(
        run_id="",
        worker_role="control",
        decision_class="accept",
        verification_state="verified",
        artifact_ref="artifact-1",
        source_lane="",
        target_lane="review-lane",
    )
    snapshot = _build_runtime_evaluation_gate_integration_snapshot(
        self_model,
        registry,
        confidence,
        state,
    )
    snapshot["aggregated_contract_gate"] = {
        "is_valid": False,
        "errors": 7,
    }
    snapshot["evaluation_gate"] = {
        "result": "fail",
        "contract_valid": False,
        "errors": 9,
    }
    snapshot["runtime_contract_integration"]["runtime_fabric"]["evaluation_gate"] = {
        "result": "fail",
        "contract_valid": False,
        "errors": 9,
    }

    assert _guard_runtime_evaluation_fabric_snapshot(snapshot) == (
        "snapshot.aggregated_contract_gate.errors must be a tuple, list, or None",
        "snapshot.evaluation_gate.errors must be a tuple, list, or None",
        "snapshot.runtime_contract_integration.runtime_fabric.evaluation_gate.errors must be a tuple, list, or None",
        "snapshot.aggregated_contract_gate must equal the aggregation implied by nested contract_gate entries",
    )


def test_build_orchestration_contract_snapshot_returns_expected_structure() -> None:
    task = WorkerTask(
        task_id="task-1",
        worker_role="analysis",
        input_ref="artifact-1",
        task_status="pending",
    )
    result = WorkerResult(
        task_id="task-1",
        worker_role="analysis",
        output_ref="output-1",
        result_status="complete",
    )
    route = TaskRoute(
        task_id="task-1",
        source_role="analysis",
        target_role="review",
        route_ref="route-1",
    )

    assert _build_orchestration_contract_snapshot(task, result, route) == {
        "worker_task": {
            "task_id": "task-1",
            "worker_role": "analysis",
            "input_ref": "artifact-1",
            "task_status": "pending",
        },
        "worker_result": {
            "task_id": "task-1",
            "worker_role": "analysis",
            "output_ref": "output-1",
            "result_status": "complete",
        },
        "task_route": {
            "task_id": "task-1",
            "source_role": "analysis",
            "target_role": "review",
            "route_ref": "route-1",
        },
    }


def test_build_state_transition_snapshot_returns_expected_structure() -> None:
    task_transition = TaskTransition(
        task_id="task-1",
        from_status="pending",
        to_status="running",
        transition_ref="tr-1",
    )
    run_transition = RunTransition(
        run_id="run-1",
        from_step="ingest",
        to_step="evaluate",
        transition_ref="tr-2",
    )

    assert _build_state_transition_snapshot(task_transition, run_transition) == {
        "task_transition": {
            "task_id": "task-1",
            "from_status": "pending",
            "to_status": "running",
            "transition_ref": "tr-1",
        },
        "run_transition": {
            "run_id": "run-1",
            "from_step": "ingest",
            "to_step": "evaluate",
            "transition_ref": "tr-2",
        },
    }


def test_build_checkpoint_junction_snapshot_returns_expected_structure() -> None:
    checkpoint = OrchestrationCheckpoint(
        task_id="task-1",
        output_ref="output-1",
        route_ref="route-1",
        checkpoint_ref="checkpoint-1",
    )
    junction = OrchestrationJunction(
        route_ref="route-1",
        task_transition_ref="task-transition-1",
        run_transition_ref="run-transition-1",
        junction_ref="junction-1",
    )

    assert _build_checkpoint_junction_snapshot(checkpoint, junction) == {
        "orchestration_checkpoint": {
            "task_id": "task-1",
            "output_ref": "output-1",
            "route_ref": "route-1",
            "checkpoint_ref": "checkpoint-1",
        },
        "orchestration_junction": {
            "route_ref": "route-1",
            "task_transition_ref": "task-transition-1",
            "run_transition_ref": "run-transition-1",
            "junction_ref": "junction-1",
        },
    }


def test_build_verification_outcome_snapshot_returns_expected_structure() -> None:
    verification = OrchestrationVerification(
        checkpoint_ref="checkpoint-1",
        junction_ref="junction-1",
        task_transition_ref="task-transition-1",
        verification_ref="verification-1",
    )
    outcome = OrchestrationOutcome(
        verification_ref="verification-1",
        decision_ref="decision-1",
        evaluation_ref="evaluation-1",
        outcome_ref="outcome-1",
    )

    assert _build_verification_outcome_snapshot(verification, outcome) == {
        "orchestration_verification": {
            "checkpoint_ref": "checkpoint-1",
            "junction_ref": "junction-1",
            "task_transition_ref": "task-transition-1",
            "verification_ref": "verification-1",
        },
        "orchestration_outcome": {
            "verification_ref": "verification-1",
            "decision_ref": "decision-1",
            "evaluation_ref": "evaluation-1",
            "outcome_ref": "outcome-1",
        },
    }


def test_build_evidence_gate_snapshot_returns_expected_structure() -> None:
    evidence = OrchestrationEvidence(
        verification_ref="verification-1",
        outcome_ref="outcome-1",
        evaluation_ref="evaluation-1",
        evidence_ref="evidence-1",
    )
    gate = OrchestrationGate(
        evidence_ref="evidence-1",
        evaluation_gate_ref="evaluation-gate-1",
        audit_ref="audit-1",
        gate_ref="gate-1",
    )

    assert _build_evidence_gate_snapshot(evidence, gate) == {
        "orchestration_evidence": {
            "verification_ref": "verification-1",
            "outcome_ref": "outcome-1",
            "evaluation_ref": "evaluation-1",
            "evidence_ref": "evidence-1",
        },
        "orchestration_gate": {
            "evidence_ref": "evidence-1",
            "evaluation_gate_ref": "evaluation-gate-1",
            "audit_ref": "audit-1",
            "gate_ref": "gate-1",
        },
    }


def test_build_audit_closure_snapshot_returns_expected_structure() -> None:
    audit = OrchestrationAudit(
        gate_ref="gate-1",
        evaluation_gate_ref="evaluation-gate-1",
        audit_event_ref="audit-event-1",
        audit_ref="audit-1",
    )
    closure = OrchestrationClosure(
        audit_ref="audit-1",
        decision_ref="decision-1",
        evaluation_ref="evaluation-1",
        closure_ref="closure-1",
    )

    assert _build_audit_closure_snapshot(audit, closure) == {
        "orchestration_audit": {
            "gate_ref": "gate-1",
            "evaluation_gate_ref": "evaluation-gate-1",
            "audit_event_ref": "audit-event-1",
            "audit_ref": "audit-1",
        },
        "orchestration_closure": {
            "audit_ref": "audit-1",
            "decision_ref": "decision-1",
            "evaluation_ref": "evaluation-1",
            "closure_ref": "closure-1",
        },
    }


def test_build_lineage_manifest_snapshot_returns_expected_structure() -> None:
    lineage = OrchestrationLineage(
        closure_ref="closure-1",
        audit_ref="audit-1",
        outcome_ref="outcome-1",
        lineage_ref="lineage-1",
    )
    manifest = OrchestrationManifest(
        lineage_ref="lineage-1",
        closure_ref="closure-1",
        evidence_ref="evidence-1",
        manifest_ref="manifest-1",
    )

    assert _build_lineage_manifest_snapshot(lineage, manifest) == {
        "orchestration_lineage": {
            "closure_ref": "closure-1",
            "audit_ref": "audit-1",
            "outcome_ref": "outcome-1",
            "lineage_ref": "lineage-1",
        },
        "orchestration_manifest": {
            "lineage_ref": "lineage-1",
            "closure_ref": "closure-1",
            "evidence_ref": "evidence-1",
            "manifest_ref": "manifest-1",
        },
    }


def test_build_review_assertion_snapshot_returns_expected_structure() -> None:
    review = OrchestrationReview(
        manifest_ref="manifest-1",
        lineage_ref="lineage-1",
        closure_ref="closure-1",
        review_ref="review-1",
    )
    assertion = OrchestrationAssertion(
        review_ref="review-1",
        manifest_ref="manifest-1",
        lineage_ref="lineage-1",
        assertion_ref="assertion-1",
    )

    assert _build_review_assertion_snapshot(review, assertion) == {
        "orchestration_review": {
            "manifest_ref": "manifest-1",
            "lineage_ref": "lineage-1",
            "closure_ref": "closure-1",
            "review_ref": "review-1",
        },
        "orchestration_assertion": {
            "review_ref": "review-1",
            "manifest_ref": "manifest-1",
            "lineage_ref": "lineage-1",
            "assertion_ref": "assertion-1",
        },
    }


def test_build_publication_release_view_snapshot_returns_expected_structure() -> None:
    publication = OrchestrationPublication(
        assertion_ref="assertion-1",
        review_ref="review-1",
        manifest_ref="manifest-1",
        publication_ref="publication-1",
    )
    release_view = OrchestrationReleaseView(
        publication_ref="publication-1",
        assertion_ref="assertion-1",
        review_ref="review-1",
        release_view_ref="release-view-1",
    )

    assert _build_publication_release_view_snapshot(publication, release_view) == {
        "orchestration_publication": {
            "assertion_ref": "assertion-1",
            "review_ref": "review-1",
            "manifest_ref": "manifest-1",
            "publication_ref": "publication-1",
        },
        "orchestration_release_view": {
            "publication_ref": "publication-1",
            "assertion_ref": "assertion-1",
            "review_ref": "review-1",
            "release_view_ref": "release-view-1",
        },
    }
