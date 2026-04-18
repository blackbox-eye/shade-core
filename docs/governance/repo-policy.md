# Repo policy

## Formål

Denne policy fastlægger minimumskrav for ændringer i `shade-core`.

## Branch-regler

- `main` er protected.
- Direkte pushes til `main` er ikke tilladt.
- Ændringer merges kun via pull request.
- Repositoryet bruger linear history.

## Commit-krav

- Alle commits skal være signed commits.
- Historik skal holdes ren og sporbar.
- Små, afgrænsede ændringer foretrækkes.

## Review og merge

- Hver ændring skal have en pull request med tydeligt formål.
- Feedback håndteres i pull requesten før merge.
- Merge må ikke omgå branch protection.

## Sikkerhedsgrænser

- Secrets må ikke committes.
- Repositoryet bruges ikke til deploy-konfiguration.
- VPS-specifik drift dokumenteres ikke her.
