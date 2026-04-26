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
| Orchestration checkpoint contract | `src/shade_core/models.py`   | Implemented as one internal typed bridge object; not re-exported      | `tests/test_models.py`          |
| Orchestration junction contract | `src/shade_core/models.py`    | Implemented as one internal typed bridge object; not re-exported      | `tests/test_models.py`          |
| Orchestration checkpoint validation | `src/shade_core/contract_gate.py` | Implemented as one internal validator for checkpoint bridge fields | `tests/test_contract_gate.py`   |
| Orchestration junction validation | `src/shade_core/contract_gate.py` | Implemented as one internal validator for junction bridge fields   | `tests/test_contract_gate.py`   |
| Orchestration checkpoint serial. | `src/shade_core/serialization.py` | Implemented as one internal serializer for checkpoint bridge fields | `tests/test_serialization.py`   |
| Orchestration junction serial. | `src/shade_core/serialization.py`  | Implemented as one internal serializer for junction bridge fields  | `tests/test_serialization.py`   |
| Checkpoint junction snapshot | `src/shade_core/bundle.py`         | Implemented as one internal helper for the checkpoint/junction bridge view | `tests/test_bundle.py`      |
| Task transition contract  | `src/shade_core/models.py`          | Implemented as one internal typed boundary object; not re-exported    | `tests/test_models.py`          |
| Run transition contract   | `src/shade_core/models.py`          | Implemented as one internal typed boundary object; not re-exported    | `tests/test_models.py`          |
| Task transition validation | `src/shade_core/contract_gate.py`  | Implemented as one internal validator for task transition fields      | `tests/test_contract_gate.py`   |
| Run transition validation | `src/shade_core/contract_gate.py`   | Implemented as one internal validator for run transition fields       | `tests/test_contract_gate.py`   |
| Task transition serial.   | `src/shade_core/serialization.py`   | Implemented as one internal serializer for task transition fields     | `tests/test_serialization.py`   |
| Run transition serial.    | `src/shade_core/serialization.py`   | Implemented as one internal serializer for run transition fields      | `tests/test_serialization.py`   |
| State transition snapshot | `src/shade_core/bundle.py`          | Implemented as one internal helper for task/run transition view       | `tests/test_bundle.py`          |
| Orchestration verification contract | `src/shade_core/models.py` | Implemented as one internal typed bridge object; not re-exported      | `tests/test_models.py`          |
| Orchestration outcome contract | `src/shade_core/models.py`      | Implemented as one internal typed bridge object; not re-exported      | `tests/test_models.py`          |
| Orchestration verification validation | `src/shade_core/contract_gate.py` | Implemented as one internal validator for verification bridge fields | `tests/test_contract_gate.py` |
| Orchestration outcome validation | `src/shade_core/contract_gate.py` | Implemented as one internal validator for outcome bridge fields     | `tests/test_contract_gate.py`   |
| Orchestration verification serial. | `src/shade_core/serialization.py` | Implemented as one internal serializer for verification bridge fields | `tests/test_serialization.py` |
| Orchestration outcome serial. | `src/shade_core/serialization.py` | Implemented as one internal serializer for outcome bridge fields     | `tests/test_serialization.py`   |
| Verification outcome snapshot | `src/shade_core/bundle.py`      | Implemented as one internal helper for the verification/outcome bridge view | `tests/test_bundle.py`    |
| Orchestration evidence contract | `src/shade_core/models.py`     | Implemented as one internal typed bridge object; not re-exported      | `tests/test_models.py`          |
| Orchestration gate contract | `src/shade_core/models.py`         | Implemented as one internal typed bridge object; not re-exported      | `tests/test_models.py`          |
| Orchestration evidence validation | `src/shade_core/contract_gate.py` | Implemented as one internal validator for evidence bridge fields   | `tests/test_contract_gate.py`   |
| Orchestration gate validation | `src/shade_core/contract_gate.py` | Implemented as one internal validator for gate bridge fields         | `tests/test_contract_gate.py`   |
| Orchestration evidence serial. | `src/shade_core/serialization.py` | Implemented as one internal serializer for evidence bridge fields   | `tests/test_serialization.py`   |
| Orchestration gate serial. | `src/shade_core/serialization.py`   | Implemented as one internal serializer for gate bridge fields       | `tests/test_serialization.py`   |
| Evidence gate snapshot | `src/shade_core/bundle.py`            | Implemented as one internal helper for the evidence/gate bridge view | `tests/test_bundle.py`          |
| Orchestration audit contract | `src/shade_core/models.py` | Implemented as one internal typed bridge object; not re-exported | `tests/test_models.py` |
| Orchestration closure contract | `src/shade_core/models.py` | Implemented as one internal typed bridge object; not re-exported | `tests/test_models.py` |
| Orchestration audit validation | `src/shade_core/contract_gate.py` | Implemented as one internal validator for audit bridge fields | `tests/test_contract_gate.py` |
| Orchestration closure validation | `src/shade_core/contract_gate.py` | Implemented as one internal validator for closure bridge fields | `tests/test_contract_gate.py` |
| Orchestration audit serial. | `src/shade_core/serialization.py` | Implemented as one internal serializer for audit bridge fields | `tests/test_serialization.py` |
| Orchestration closure serial. | `src/shade_core/serialization.py` | Implemented as one internal serializer for closure bridge fields | `tests/test_serialization.py` |
| Audit closure snapshot | `src/shade_core/bundle.py` | Implemented as one internal helper for the audit/closure bridge view | `tests/test_bundle.py` |
| Orchestration lineage contract | `src/shade_core/models.py` | Implemented as one internal typed bridge object; not re-exported | `tests/test_models.py` |
| Orchestration manifest contract | `src/shade_core/models.py` | Implemented as one internal typed bridge object; not re-exported | `tests/test_models.py` |
| Orchestration lineage validation | `src/shade_core/contract_gate.py` | Implemented as one internal validator for lineage bridge fields | `tests/test_contract_gate.py` |
| Orchestration manifest validation | `src/shade_core/contract_gate.py` | Implemented as one internal validator for manifest bridge fields | `tests/test_contract_gate.py` |
| Orchestration lineage serial. | `src/shade_core/serialization.py` | Implemented as one internal serializer for lineage bridge fields | `tests/test_serialization.py` |
| Orchestration manifest serial. | `src/shade_core/serialization.py` | Implemented as one internal serializer for manifest bridge fields | `tests/test_serialization.py` |
| Lineage manifest snapshot | `src/shade_core/bundle.py` | Implemented as one internal helper for the lineage/manifest bridge view | `tests/test_bundle.py` |
| Full A-to-O runtime loop  | No current code file                | Documented target only; not implemented as orchestration              | None                            |
| Worker orchestration      | No current code file                | Documented target only; role vocabulary only in current code          | None                            |
