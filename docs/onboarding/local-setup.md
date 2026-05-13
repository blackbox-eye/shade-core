# Local setup

## Purpose

This guide covers only local working mode in VS Code and PowerShell.

## Prerequisites

- Git is installed locally.
- PowerShell is used as the shell.
- The repository is opened in VS Code.

## Local working mode

- Follow the [PR workflow SOP](../governance/pr-workflow-sop.md) for scope lock, bundle sizing, validation, PR creation, review, merge, and cleanup.
- Use [PR command bundles](../governance/pr-command-bundles.md) for copy/paste-ready PowerShell command sets.
- Use [Copilot bundle prompts](../governance/copilot-bundle-prompts.md) when shaping a larger Copilot bundle.
- Use [Copilot instructions](../../.github/copilot-instructions.md) when asking Copilot to implement a bundle.
- Use one feature branch per cohesive bundle.
- Keep Copilot work inside the locked scope and repository hard bounds.

```powershell
git switch -c feature/<short-name>
git add .
git commit -S -m "Short message"
git push -u origin feature/<short-name>
gh pr create --base main --title "<title>" --body "<body>"
```

- Make changes locally in VS Code after the scope is locked.
- Use PowerShell for Git commands.
- Use the SOP validation bundle before `git add` and commit.
- Use GitHub CLI for PR creation when authenticated.
- Use the PR template fields for bundle type, changed files, micro-PR justification when used, and validation.
- If GitHub CLI cannot request Copilot review, create the PR with CLI and request Copilot in the GitHub UI.
- Copilot is a reviewer and assistant, not merge authority.

## Post-merge cleanup

- Use the SOP post-merge cleanup bundle after the PR is merged.

## Boundaries

This guide does not cover deploy, VPS, or secrets.
