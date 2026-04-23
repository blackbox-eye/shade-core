# Docs-to-code traceability

## Purpose

This file maps documented `shade-core` components to the current code surface and existing tests.

## Traceability

| Component | Code file | Current implementation status | Relevant tests |
| --- | --- | --- | --- |
| Root package API | `src/shade_core/__init__.py` | Implemented, stable public import surface | `tests/test_import.py` |
| Contract models | `src/shade_core/models.py` | Implemented, internal module and re-exported through the root package | `tests/test_models.py` |
| Run state | `src/shade_core/state.py` | Implemented, internal module and re-exported through the root package | `tests/test_state.py` |
| Contract gate | `src/shade_core/contract_gate.py` | Implemented, internal module and re-exported through the root package | `tests/test_contract_gate.py` |
| Runtime decision slice | `src/shade_core/runtime_loop.py` | Implemented, internal module and re-exported through the root package | `tests/test_runtime_loop.py` |
| Evaluation | `src/shade_core/evaluation.py` | Implemented, internal module and re-exported through the root package | `tests/test_evaluation.py` |
| Evaluation gate | `src/shade_core/evaluation_gate.py` | Implemented, internal module and re-exported through the root package | `tests/test_evaluation_gate.py` |
| Serialization | `src/shade_core/serialization.py` | Implemented, internal module and re-exported through the root package | `tests/test_serialization.py` |
| Bundle output | `src/shade_core/bundle.py` | Implemented, internal module and re-exported through the root package | `tests/test_bundle.py` |
| Full A-to-O runtime loop | No current code file | Documented target only; not implemented as orchestration | None |
| Worker orchestration | No current code file | Documented target only; role vocabulary only in current code | None |
