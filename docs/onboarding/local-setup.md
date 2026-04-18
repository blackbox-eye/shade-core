# Local setup

## Formål

Denne guide beskriver et enkelt lokalt workflow med PowerShell og VS Code.

## Forudsætninger

- Git installeret lokalt.
- PowerShell som standard shell.
- VS Code med adgang til repositoryet.

## Klargøring

```powershell
git clone <repo-url>
cd shade-core
code .
```

## Dagligt workflow

```powershell
git switch -c feature/<kort-navn>
git status
git add .
git commit -S -m "Kort, præcis besked"
git push -u origin feature/<kort-navn>
```

## Arbejdsform

- Lav ændringer lokalt i VS Code.
- Brug PowerShell til Git-kommandoer.
- Opret pull request for at få ændringer ind på `main`.
- Hold historikken lineær og commits signerede.

## Ikke omfattet

- Deploy-trin.
- VPS-opsætning.
- Deling eller lagring af secrets.
