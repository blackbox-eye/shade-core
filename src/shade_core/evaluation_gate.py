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


def run_evaluation_gate(
    contract_result: ContractGateResult,
    decision: RuntimeDecision,
    event: MetaAuditEvent,
) -> EvaluationGateResult:
    if not contract_result.is_valid:
        return EvaluationGateResult(
            result="fail",
            contract_valid=False,
            errors=contract_result.errors,
        )

    return EvaluationGateResult(
        result=evaluate(decision, event),
        contract_valid=True,
        errors=(),
    )


def _run_runtime_evaluation_gate(
    self_model_result: ContractGateResult,
    worker_registry_result: ContractGateResult,
    confidence_record_result: ContractGateResult,
    state_contract_result: ContractGateResult,
    decision: RuntimeDecision,
    event: MetaAuditEvent,
) -> EvaluationGateResult:
    contract_results = (
        self_model_result,
        worker_registry_result,
        confidence_record_result,
        state_contract_result,
    )
    aggregated_contract_result = ContractGateResult(
        is_valid=all(result.is_valid for result in contract_results),
        errors=tuple(
            error
            for result in contract_results
            for error in result.errors
        ),
    )

    return run_evaluation_gate(aggregated_contract_result, decision, event)
