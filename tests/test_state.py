from shade_core import RunState


def test_run_state_creation() -> None:
    state = RunState(
        run_id="run-1",
        worker_role="analysis",
        decision_class="needs_review",
        verification_state="pending",
        artifact_ref="artifact-1",
        source_lane="adapter-a",
        target_lane="adapter-b",
    )

    assert state.run_id == "run-1"
    assert state.worker_role == "analysis"
    assert state.decision_class == "needs_review"
    assert state.verification_state == "pending"
    assert state.artifact_ref == "artifact-1"
    assert state.source_lane == "adapter-a"
    assert state.target_lane == "adapter-b"