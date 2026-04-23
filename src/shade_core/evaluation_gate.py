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