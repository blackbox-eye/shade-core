# Local setup

## Purpose

This guide covers only local working mode in VS Code and PowerShell.

## Prerequisites

- Git is installed locally.
- PowerShell is used as the shell.
- The repository is opened in VS Code.

## Local working mode

```powershell
git switch -c feature/<short-name>
git status
git add .
git commit -S -m "Short message"
git push -u origin feature/<short-name>
```

- Make changes locally in VS Code.
- Use PowerShell for Git commands.
- Open a pull request when the change is ready.

## Boundaries

This guide does not cover deploy, VPS, or secrets.
