from shade_core import RunState, validate_state_contract
from shade_core.contract_gate import validate_artifact_handoff
from shade_core.models import ArtifactHandoff


def test_validate_state_contract_passes_for_valid_state() -> None:
    state = RunState(
        run_id="run-1",
        worker_role="analysis",
        decision_class="accept",
        verification_state="verified",
        artifact_ref="artifact-1",
        source_lane="adapter-a",
        target_lane="adapter-b",
    )

    result = validate_state_contract(state)

    assert result.is_valid is True
    assert result.errors == ()


def test_validate_state_contract_fails_for_invalid_state() -> None:
    state = RunState(
        run_id="",
        worker_role="",
        decision_class="accept",
        verification_state="pending",
        artifact_ref="",
        source_lane="",
        target_lane="adapter-b",
    )

    result = validate_state_contract(state)

    assert result.is_valid is False
    assert result.errors == (
        "run_id is required",
        "worker_role is required",
        "artifact_ref is required",
        "source_lane is required",
    )


def test_validate_artifact_handoff_passes_for_valid_handoff() -> None:
    handoff = ArtifactHandoff(
        artifact_ref="artifact-1",
        source_lane="analysis-lane",
        target_lane="review-lane",
    )

    result = validate_artifact_handoff(handoff)

    assert result.is_valid is True
    assert result.errors == ()


def test_validate_artifact_handoff_fails_for_invalid_handoff() -> None:
    handoff = ArtifactHandoff(
        artifact_ref="",
        source_lane="",
        target_lane="",
    )

    result = validate_artifact_handoff(handoff)

    assert result.is_valid is False
    assert result.errors == (
        "artifact_ref is required",
        "source_lane is required",
        "target_lane is required",
    )
