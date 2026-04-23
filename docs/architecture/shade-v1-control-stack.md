# Shade V1 control stack

## Purpose

This file locks the V1 control stack before runtime.

## Core modules

- `control-plane` defines rules, ordering, and stop conditions.
- `state-store` holds the inspectable work status for a single run.
- `worker-registry` describes which workers exist and what they may do.
- `contract-gate` rejects input or output that breaks the contracts.
- `evaluation-gate` gathers QA signals before a run can be accepted.

## Responsibilities

- Each module has one clear responsibility.
- Modules must be inspectable through clear input, output, and status.
- Interfaces must be testable without runtime extensions.
- Copilot is an assistant in the work, not an authority over the contracts.

## Boundaries

- This contract does not describe code, deploy, VPS, workflows, or operations.
- Production, integration, or secrets are not introduced in V1.
