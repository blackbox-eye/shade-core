# Architecture

This folder describes the overall structure and boundaries of the repository.

## Content

- Use the documents here for short, maintainable architecture overviews.
- Use [current runtime slice](current-runtime-slice.md) as the source of truth for what is implemented now versus target-only.
- Use [next contract slice options](next-contract-slice-options.md) for the Cycle 9.2 comparison and recommendation.
- Keep focus on structure, responsibilities, and documentation boundaries.
- Exclude deploy-, VPS-, and secrets-related content.

## Working mode

- Changes are made locally in VS Code.
- Git workflow runs through PowerShell.
- Changes are merged through pull request to protected `main`.
- Commits must be signed, and history must stay linear.
