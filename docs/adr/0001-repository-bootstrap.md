# ADR-0001 Repository Bootstrap

Status: Accepted

## Context

The repository needed a simple, local frame for documentation and change control in the bootstrap phase.

## Decision

`shade-core` is established as a lightweight repository with documentation, governance, and a local workflow through VS Code and PowerShell.

## Consequences

- `main` is protected with PR-only merge.
- Signed commits and linear history are fixed requirements.
- The repository does not include deploy, VPS, or secrets.
