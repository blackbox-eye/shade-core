# shade-core

`shade-core` is a repository-local build, contract, and QA core for the current `shade` work.
It combines a small inspectable Python package with tests and repo-facing documentation so runtime-facing contract changes can be reviewed against explicit boundaries instead of informal notes.

## Current scope

- The repository currently ships a minimal Python contract core under `src/shade_core/`, repository tests under `tests/`, and supporting architecture, governance, QA, onboarding, and release documentation under `docs/`.
- The implemented Python surface is intentionally narrow and reviewable; it does not claim full runtime orchestration or production integration.
- The current baseline after post-foundation cycle 5 is `157 passed` from `python -m pytest`.
- The broader V1 architecture documents remain target-boundary references beyond the currently implemented runtime slice.

## Current Python core

- Contract models: internal typed dataclasses define the current runtime and orchestration-facing contract boundaries.
- Run state: one internal run-state contract supports runtime/evaluation snapshot assembly.
- Contract validation: contract-gate validators check current runtime inputs and state contracts.
- Runtime decision slice: the implemented decision path produces deterministic accept, needs_review, and reject decisions plus audit events.
- Evaluation: raw evaluation derives a result from the runtime decision and audit severity.
- Evaluation gate: contract-aware gating keeps valid raw evaluation results and fails closed when contract inputs are invalid.
- Serialization: internal serializers convert current contracts and results into plain inspectable dictionaries.
- Bundle snapshots: internal bundle helpers expose current runtime and orchestration snapshot views.
- Runtime/evaluation fabric snapshots: internal helpers prepare, serialize, and reuse runtime/evaluation fabric values consistently across contract-integration and evaluation-gate snapshots.

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
