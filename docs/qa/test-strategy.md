# Test strategy

## Purpose

This file covers only local repo baseline, PR baseline, and later test direction.

## Current baseline

- Local changes are reviewed in VS Code.
- Simple repository and file checks can be run locally in PowerShell.
- The current pytest suite covers the implemented minimal Python core.
- The current pytest suite also includes one narrow repo consistency check for stable workflow and documented path drift.
- Pull request is the fixed quality gate before merge.
- The `pr-baseline` workflow verifies baseline files and runs `python -m pytest`.

## Before pull request

- Content has been read through locally.
- The change is small enough for fast review.
- Baseline checks have been completed.

## Later direction

- Test coverage can expand as code and modules grow.
- New tests must follow the repository's simple foundation frame.
- Docs-to-code alignment is tracked in `docs/qa/docs-to-code-traceability.md`.

## Boundaries

This strategy does not cover deploy, VPS, production, or integration.
