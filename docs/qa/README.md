# QA

This folder describes the local baseline for quality assurance in the repository.

## Focus

- Simple, local checks before pull request.
- Reviewable documentation and small changes.
- Traceable quality without environment-specific operations.

## Working frame

- Review changes in VS Code.
- Use PowerShell for local Git commands.
- Merge happens only through pull request to protected `main`.
- Signed commits and linear history are a fixed part of the process.
- No deploy-, VPS-, or secrets-scope.
