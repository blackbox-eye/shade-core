# shade-core

`shade-core` is a repository-local contract, verification, serialization, and QA fabric for the current runtime-facing `shade` work.
It combines a small inspectable Python package with tests and repository documentation so runtime-facing changes can be assembled, validated, serialized, and reviewed against explicit internal contracts.
The repository is not a production runtime, does not deploy anything, and does not yet include production integration layers.

## Current scope

- The repository currently ships a minimal Python contract core under `src/shade_core/`, repository tests under `tests/`, and supporting architecture, governance, QA, onboarding, and release documentation under `docs/`.
- The implemented Python surface is intentionally narrow and reviewable; it does not claim full runtime orchestration, deploy infrastructure, or production integration.
- The current baseline after post-foundation cycle 6 is `202 passed` from `python -m pytest`.
- The broader V1 architecture documents remain target-boundary references beyond the currently implemented runtime slice.

## Current Python core

- Contract models: internal typed dataclasses define the current runtime and orchestration-facing contract boundaries.
- Run state: one internal run-state contract supports runtime/evaluation snapshot assembly.
- Contract validation: contract-gate validators check current runtime inputs and state contracts.
- Runtime decision slice: the implemented decision path produces deterministic accept, needs_review, and reject decisions plus audit events.
- Runtime/evaluation fabric: internal helpers prepare the runtime evaluation fabric once and reuse the computed decision, audit, contract, and evaluation values across snapshots.
- Evaluation results: `raw_evaluation` and `evaluation_gate` remain explicit internal surfaces, with the gate failing closed when contract inputs are invalid.
- Runtime contract aggregation: `aggregated_contract_gate` captures the ordered contract result implied by the nested runtime contract entries.
- Runtime integration snapshot: `runtime_contract_integration` composes nested contract validation output with the runtime fabric snapshot.
- Runtime fabric consistency guards: internal guards validate prepared runtime fabric state and serialized runtime/evaluation snapshots without changing those snapshot keys.
- Guard verification snapshot: an internal verification surface composes `runtime_evaluation`, `prepared_fabric_guard`, and `serialized_snapshot_guard` in parallel.
- Verification summary: `verification_summary` records deterministic alignment semantics across guard validity, aggregated contract alignment, and raw-vs-gated evaluation behavior.
- Verification contract: `verification_contract` validates the verification surface itself, including malformed guard mappings and malformed runtime-evaluation structure.
- Verification snapshot validation: contract-gate validation now covers the verification snapshot as an internal contract boundary.
- Serialization: internal serializers convert current contracts, verification surfaces, and results into plain inspectable dictionaries.
- Bundle snapshots: internal bundle helpers expose current runtime and orchestration snapshot views.

## Out of scope / non-goals

- No deploy.
- No VPS.
- No secrets.
- No production integration.
- No adapters, providers, or memory layer yet.

## Repository layout

- `src/shade_core/` - current Python core.
- `tests/` - executable contract, runtime, serialization, bundle, and repo-consistency tests.
- `docs/architecture/` - system and boundary documentation.
- `docs/governance/` - branch, PR, and repository policy documents.
- `docs/qa/` - traceability, evaluation, and test-strategy documentation.
- `docs/releases/` - checkpoint and release-process documents.

## Local validation

- `python -m pytest`

## Working mode

- `main` is protected.
- Merge to `main` happens only through pull request.
- Signed commits are required.
- Copilot is used as an assistant, not an authority.
- PR review fixes are applied through local signed commits only.

## Checkpoints

- Foundation bundles: [docs/releases/checkpoint-foundation-bundles.md](docs/releases/checkpoint-foundation-bundles.md)
- Post-foundation cycle 1: [docs/releases/checkpoint-post-foundation-cycle-1.md](docs/releases/checkpoint-post-foundation-cycle-1.md)
- Post-foundation cycle 2: [docs/releases/checkpoint-post-foundation-cycle-2.md](docs/releases/checkpoint-post-foundation-cycle-2.md)
- Post-foundation cycle 3: [docs/releases/checkpoint-post-foundation-cycle-3.md](docs/releases/checkpoint-post-foundation-cycle-3.md)
- Post-foundation cycle 4: [docs/releases/checkpoint-post-foundation-cycle-4.md](docs/releases/checkpoint-post-foundation-cycle-4.md)
- Post-foundation cycle 5: [docs/releases/checkpoint-post-foundation-cycle-5.md](docs/releases/checkpoint-post-foundation-cycle-5.md)
- Post-foundation cycle 6: [docs/releases/checkpoint-post-foundation-cycle-6.md](docs/releases/checkpoint-post-foundation-cycle-6.md)

Current checkpoint: [docs/releases/checkpoint-post-foundation-cycle-6.md](docs/releases/checkpoint-post-foundation-cycle-6.md)
