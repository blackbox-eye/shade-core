# shade-core

`shade-core` er et build-, contract- og QA-lag med en minimal Python-kerne.

## Status

- Repositoryet samler foundation-dokumentation, governance og en lille inspectable Python-package.
- Python-kernen dækker kontraktmodeller, et minimalt runtime-beslutningssnit, evaluation og serialisering.
- Build-gaten validerer både baseline-filer og lokale pytest-checks.

## Rammer

- Ingen deploy.
- Ingen VPS.
- Ingen secrets.
- Ingen produktion eller integration.

## Arbejdsform

- `main` er protected.
- Merge til `main` sker kun via pull request.
- Signed commits er obligatoriske.
- Historikken holdes lineær.
- Arbejd lokalt i VS Code og PowerShell.
- Copilot bruges som assistent, ikke autoritet.

## Python-kerne

- Package-navn er `shade_core`.
- Kernen er bevidst lille og uden IO, persistence eller netværk.
- Interfaces holdes testbare og inspectable.
