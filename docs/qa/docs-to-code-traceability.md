# Docs-to-code traceability

## Purpose

This file maps documented `shade-core` components to the current code surface and existing tests.
Concrete code and test paths in the table are kept machine-checkable through one narrow repo consistency pytest check.

## Traceability

| Component                 | Code file                           | Current implementation status                                         | Relevant tests                  |
| ------------------------- | ----------------------------------- | --------------------------------------------------------------------- | ------------------------------- |
| Root package API          | `src/shade_core/__init__.py`        | Implemented, stable public import path                                | `tests/test_import.py`          |
| Contract models           | `src/shade_core/models.py`          | Implemented, internal module; only a subset of model types is re-exported through the stable root package surface; transition and route-related objects are not re-exported | `tests/test_models.py`          |
| Artifact handoff boundary | `src/shade_core/models.py`          | Implemented as one internal typed handoff object; not re-exported     | `tests/test_models.py`          |
| Run state                 | `src/shade_core/state.py`           | Implemented, internal module and re-exported through the root package | `tests/test_state.py`           |
| Contract gate             | `src/shade_core/contract_gate.py`   | Implemented, internal module and re-exported through the root package | `tests/test_contract_gate.py`   |
| Handoff validation        | `src/shade_core/contract_gate.py`   | Implemented as one internal validator for the neutral handoff fields  | `tests/test_contract_gate.py`   |
| Runtime decision slice    | `src/shade_core/runtime_loop.py`    | Implemented, internal module and re-exported through the root package | `tests/test_runtime_loop.py`    |
| Evaluation                | `src/shade_core/evaluation.py`      | Implemented, internal module and re-exported through the root package | `tests/test_evaluation.py`      |
| Evaluation gate           | `src/shade_core/evaluation_gate.py` | Implemented, internal module and re-exported through the root package | `tests/test_evaluation_gate.py` |
| Serialization             | `src/shade_core/serialization.py`   | Implemented, internal module and re-exported through the root package | `tests/test_serialization.py`   |
| Handoff serialization     | `src/shade_core/serialization.py`   | Implemented as one internal serializer for the neutral handoff fields | `tests/test_serialization.py`   |
| State serialization       | `src/shade_core/serialization.py`   | Implemented as one internal serializer for current run state          | `tests/test_bundle.py`          |
| Evaluation gate snapshot  | `src/shade_core/serialization.py`   | Implemented as one internal serializer for evaluation gate results    | `tests/test_bundle.py`          |
| Bundle output             | `src/shade_core/bundle.py`          | Implemented, internal module and re-exported through the root package | `tests/test_bundle.py`          |
| Runtime fabric snapshot   | `src/shade_core/bundle.py`          | Implemented as one internal helper for a consolidated runtime view    | `tests/test_bundle.py`          |
| Worker task contract      | `src/shade_core/models.py`          | Implemented as one internal typed boundary object; not re-exported    | `tests/test_models.py`          |
| Worker result contract    | `src/shade_core/models.py`          | Implemented as one internal typed boundary object; not re-exported    | `tests/test_models.py`          |
| Task route contract       | `src/shade_core/models.py`          | Implemented as one internal typed boundary object; not re-exported    | `tests/test_models.py`          |
| Worker task validation    | `src/shade_core/contract_gate.py`   | Implemented as one internal validator for worker task fields          | `tests/test_contract_gate.py`   |
| Worker result validation  | `src/shade_core/contract_gate.py`   | Implemented as one internal validator for worker result fields        | `tests/test_contract_gate.py`   |
| Task route validation     | `src/shade_core/contract_gate.py`   | Implemented as one internal validator for task route fields           | `tests/test_contract_gate.py`   |
| Worker task serialization | `src/shade_core/serialization.py`   | Implemented as one internal serializer for worker task fields         | `tests/test_serialization.py`   |
| Worker result serial.     | `src/shade_core/serialization.py`   | Implemented as one internal serializer for worker result fields       | `tests/test_serialization.py`   |
| Task route serialization  | `src/shade_core/serialization.py`   | Implemented as one internal serializer for task route fields          | `tests/test_serialization.py`   |
| Orchestration contract snapshot | `src/shade_core/bundle.py`    | Implemented as one internal helper for task/result/route view         | `tests/test_bundle.py`          |
| Task transition contract  | `src/shade_core/models.py`          | Implemented as one internal typed boundary object; not re-exported    | `tests/test_models.py`          |
| Run transition contract   | `src/shade_core/models.py`          | Implemented as one internal typed boundary object; not re-exported    | `tests/test_models.py`          |
| Task transition validation | `src/shade_core/contract_gate.py`  | Implemented as one internal validator for task transition fields      | `tests/test_contract_gate.py`   |
| Run transition validation | `src/shade_core/contract_gate.py`   | Implemented as one internal validator for run transition fields       | `tests/test_contract_gate.py`   |
| Task transition serial.   | `src/shade_core/serialization.py`   | Implemented as one internal serializer for task transition fields     | `tests/test_serialization.py`   |
| Run transition serial.    | `src/shade_core/serialization.py`   | Implemented as one internal serializer for run transition fields      | `tests/test_serialization.py`   |
| State transition snapshot | `src/shade_core/bundle.py`          | Implemented as one internal helper for task/run transition view       | `tests/test_bundle.py`          |
| Full A-to-O runtime loop  | No current code file                | Documented target only; not implemented as orchestration              | None                            |
| Worker orchestration      | No current code file                | Documented target only; role vocabulary only in current code          | None                            |
