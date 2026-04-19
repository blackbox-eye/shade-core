# Local setup

## Formål

Denne guide dækker kun lokal arbejdsform i VS Code og PowerShell.

## Forudsætninger

- Git er installeret lokalt.
- PowerShell bruges som shell.
- Repositoryet er åbnet i VS Code.

## Lokal arbejdsform

```powershell
git switch -c feature/<kort-navn>
git status
git add .
git commit -S -m "Kort besked"
git push -u origin feature/<kort-navn>
```

- Lav ændringer lokalt i VS Code.
- Brug PowerShell til Git-kommandoer.
- Åbn pull request, når ændringen er klar.

## Afgrænsning

Denne guide dækker ikke deploy, VPS eller secrets.
