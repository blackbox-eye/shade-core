# QA

This folder describes the local baseline for quality assurance in the repository.

## Focus

- Simple, local checks before pull request.
- Reviewable documentation and small changes.
- Traceable quality without environment-specific operations.
- The existing pytest path includes one narrow automated repo consistency check for stable workflow and path drift.

## Working frame

- Review changes in VS Code.
- Use PowerShell for local Git commands.
- Merge happens only through pull request to protected `main`.
- Signed commits and linear history are a fixed part of the process.
- Use [PR workflow SOP](../governance/pr-workflow-sop.md) for validation and cleanup gates.
- Use [test strategy](test-strategy.md) for the local QA baseline and PR reporting expectations.
- Use [PR QA gates](pr-qa-gates.md) for PR-type evidence and stop conditions.
- No deploy-, VPS-, or secrets-scope.
