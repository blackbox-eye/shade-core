# Branch and PR rules

## Main

- `main` er protected.
- Direkte push til `main` er ikke tilladt.
- Merge til `main` sker kun via pull request.

## Merge-krav

- Signed commits er obligatoriske.
- Historikken holdes lineær.
- Ændringer holdes små og reviewbare.
- Lokal gennemgang sker i VS Code før PR.
- Git-workflow køres lokalt via PowerShell.

## PR-flow

- Opret en lokal branch.
- Commit med signering.
- Push branch og åbn pull request mod `main`.
- Copilot kan assistere med tekst og udkast, men review og beslutning er manuel.

## Ikke omfattet

- Deploy.
- VPS.
- Secrets.
