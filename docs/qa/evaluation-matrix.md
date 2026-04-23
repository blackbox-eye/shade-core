# Evaluation matrix

## Purpose

This file locks what is measured in V1 and how we perform QA before runtime is extended.

## Metrics

- Contract clarity: are responsibilities, fields, and boundaries clear.
- Sequence clarity: can the loop be followed step by step.
- Interface testability: can input and output be assessed unambiguously.
- Inspectability: can status and decisions be read afterwards.
- Scope discipline: does the material stay outside deploy, VPS, secrets, production, and integration.

## QA form

- Each document is read as a contract, not as an idea draft.
- Each module is assessed for clear responsibility and clear boundaries.
- Each interface is assessed for testability without extra assumptions.
- Deviations are marked as blockers if they weaken contract or control flow.

## V1 decision

- V1 is ready when the contracts are short, stable, and coherent.
- V1 is not ready if hype, unclear roles, or hidden runtime behavior creep in.
- Copilot can help with wording and review, but is not an authority for acceptance.
