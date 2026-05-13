# PR command bundles

## Purpose

- Keep common PR operations copy/paste-ready in PowerShell.
- Use these bundles with [PR workflow SOP](pr-workflow-sop.md).

## Pre-implementation state gate

- Start from a clean working tree and a current local `main`.
- Stop if `git status -sb` shows unrelated changes before branch creation.

```powershell
git status -sb
git switch main
git pull --ff-only
git switch -c feature/<short-name>
git status -sb
```

## Validation gate

- Run before commit and before major PR updates.

```powershell
git diff --stat
git diff -- <relevant-path>
python -m pytest -q
git status -sb
```

## Commit gate

- Stage only the locked scope.
- Review the staged diff before signing.

```powershell
git add <allowed-paths>
git diff --cached --stat
git diff --cached -- <relevant-path>
git commit -S -m "<message>"
git status -sb
```

## Push and PR creation with body file

- Use the PR template fields in the body file.
- If GitHub CLI cannot request Copilot review, request Copilot in the GitHub UI after PR creation.

```powershell
@'
Purpose:
- <why>

Scope:
- Bundle type: <docs|test|code|governance|checkpoint|review-fix|other>
- Required changes in this bundle: <2-4 items>
- Included: <in scope>
- Out of scope: <out of scope>
- Changed files or areas: <paths>
- Micro-PR justification if applicable: <n/a or reason>

Validation:
- Command: python -m pytest -q
- Result: <result>
'@ | Set-Content -Path .\pr-body.md

git push -u origin feature/<short-name>
gh pr create --base main --title "<title>" --body-file .\pr-body.md
```

## Post-merge sync and cleanup

- Run after merge before starting new work.

```powershell
git switch main
git pull --ff-only
git branch -d feature/<short-name>
python -m pytest -q
git status -sb
```

## GitHub CLI auth check and recovery

- Run `gh auth status` before PR creation when auth is uncertain.
- Use `gh auth login` if there is no active GitHub CLI session.

```powershell
gh auth status
gh auth refresh -h github.com -s repo
gh auth status
```

## Branch cleanup

- Use for merged or abandoned local branches after operator approval.

```powershell
git fetch --prune
git branch --merged
git branch -d feature/<short-name>
git status -sb
```

## Failed test stop gate

- Do not commit, push, or open a PR while pytest is failing.

```powershell
python -m pytest -q
if ($LASTEXITCODE -ne 0) {
    git status -sb
    throw "Stop: pytest failed. Fix the failure or relock scope before continuing."
}
```

## Stale local main recovery

- Use when local `main` is behind `origin/main`.
- If `git pull --ff-only` fails, stop and ask ChatGPT/tovholder before rewriting or merging local `main`.

```powershell
git fetch origin
git switch main
git pull --ff-only
git status -sb
```