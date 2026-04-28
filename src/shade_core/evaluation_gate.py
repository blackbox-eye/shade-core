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
    errors: list[str] = []

    if contract_result.is_valid:
        if evaluation_gate_result.result != raw_result:
            errors.append(
                "valid contracts must keep the evaluation gate result aligned with the raw result",
            )
        if evaluation_gate_result.contract_valid is not True:
            errors.append(
                "valid contracts must mark the evaluation gate result as contract-valid",
            )
        if evaluation_gate_result.errors != ():
            errors.append(
                "valid contracts must keep evaluation gate errors empty",
            )
    else:
        if evaluation_gate_result.result != "fail":
            errors.append(
                "invalid contracts must force the evaluation gate result to fail",
            )
        if evaluation_gate_result.contract_valid is not False:
            errors.append(
                "invalid contracts must mark the evaluation gate result as contract-invalid",
            )
        if evaluation_gate_result.errors != contract_result.errors:
            errors.append(
                "invalid contracts must preserve contract errors in the evaluation gate result",
            )

    return tuple(errors)


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
