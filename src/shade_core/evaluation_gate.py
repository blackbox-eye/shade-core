from __future__ import annotations

from dataclasses import dataclass

from .contract_gate import ContractGateResult
from .evaluation import EvaluationResult, evaluate
from .models import MetaAuditEvent, RuntimeDecision


@dataclass(slots=True)
class EvaluationGateResult:
    result: EvaluationResult
    contract_valid: bool
    errors: tuple[str, ...]


def _build_evaluation_gate_result_from_raw_result(
    contract_result: ContractGateResult,
    raw_result: EvaluationResult,
) -> EvaluationGateResult:
    if not contract_result.is_valid:
        return EvaluationGateResult(
            result="fail",
            contract_valid=False,
            errors=contract_result.errors,
        )

    return EvaluationGateResult(
        result=raw_result,
        contract_valid=True,
        errors=(),
    )


def _guard_evaluation_gate_result_from_raw_result(
    contract_result: ContractGateResult,
    raw_result: EvaluationResult,
    evaluation_gate_result: EvaluationGateResult,
) -> tuple[str, ...]:
    alignment_summary = _summarize_evaluation_gate_alignment(
        contract_result,
        raw_result,
        evaluation_gate_result,
    )
    errors: list[str] = []

    if contract_result.is_valid:
        if not alignment_summary["raw_evaluation_matches_gate"]:
            errors.append(
                "valid contracts must keep the evaluation gate result aligned with the raw result",
            )
        if not alignment_summary["contract_valid_matches_contract"]:
            errors.append(
                "valid contracts must mark the evaluation gate result as contract-valid",
            )
        if not alignment_summary["errors_match_contract"]:
            errors.append(
                "valid contracts must keep evaluation gate errors empty",
            )
    else:
        if evaluation_gate_result.result != "fail":
            errors.append(
                "invalid contracts must force the evaluation gate result to fail",
            )
        if not alignment_summary["contract_valid_matches_contract"]:
            errors.append(
                "invalid contracts must mark the evaluation gate result as contract-invalid",
            )
        if not alignment_summary["errors_match_contract"]:
            errors.append(
                "invalid contracts must preserve contract errors in the evaluation gate result",
            )

    return tuple(errors)


def _summarize_evaluation_gate_alignment(
    contract_result: ContractGateResult,
    raw_result: EvaluationResult,
    evaluation_gate_result: EvaluationGateResult,
) -> dict[str, object]:
    raw_evaluation_matches_gate = evaluation_gate_result.result == raw_result
    contract_valid_matches_contract = (
        evaluation_gate_result.contract_valid is contract_result.is_valid
    )
    expected_errors = () if contract_result.is_valid else contract_result.errors
    errors_match_contract = evaluation_gate_result.errors == expected_errors

    if contract_result.is_valid:
        alignment = (
            "aligned"
            if raw_evaluation_matches_gate
            and contract_valid_matches_contract
            and errors_match_contract
            else "drifted"
        )
    else:
        alignment = (
            "fail_closed"
            if evaluation_gate_result.result == "fail"
            and contract_valid_matches_contract
            and errors_match_contract
            else "drifted"
        )

    return {
        "alignment": alignment,
        "raw_evaluation_matches_gate": raw_evaluation_matches_gate,
        "contract_valid_matches_contract": contract_valid_matches_contract,
        "errors_match_contract": errors_match_contract,
    }


def run_evaluation_gate(
    contract_result: ContractGateResult,
    decision: RuntimeDecision,
    event: MetaAuditEvent,
) -> EvaluationGateResult:
    if not contract_result.is_valid:
        return _build_evaluation_gate_result_from_raw_result(
            contract_result,
            "fail",
        )

    return _build_evaluation_gate_result_from_raw_result(
        contract_result,
        evaluate(decision, event),
    )


def _aggregate_runtime_contract_result(
    self_model_result: ContractGateResult,
    worker_registry_result: ContractGateResult,
    confidence_record_result: ContractGateResult,
    state_contract_result: ContractGateResult,
) -> ContractGateResult:
    contract_results = (
        self_model_result,
        worker_registry_result,
        confidence_record_result,
        state_contract_result,
    )

    return ContractGateResult(
        is_valid=all(result.is_valid for result in contract_results),
        errors=tuple(
            error
            for result in contract_results
            for error in result.errors
        ),
    )


def _run_runtime_evaluation_gate(
    self_model_result: ContractGateResult,
    worker_registry_result: ContractGateResult,
    confidence_record_result: ContractGateResult,
    state_contract_result: ContractGateResult,
    decision: RuntimeDecision,
    event: MetaAuditEvent,
) -> EvaluationGateResult:
    aggregated_contract_result = _aggregate_runtime_contract_result(
        self_model_result,
        worker_registry_result,
        confidence_record_result,
        state_contract_result,
    )

    return run_evaluation_gate(aggregated_contract_result, decision, event)
