# Release process

## Formål

Denne proces beskriver den minimale repository-del af en releaseforberedelse.

## Forudsætninger

- `main` er protected.
- Merge til `main` sker kun via pull request.
- Commits skal være signerede.
- Historik skal være lineær.

## Lokal arbejdsgang

```powershell
git switch -c release/<kort-navn>
git status
git add .
git commit -S -m "Forbered release-noter eller metadata"
git push -u origin release/<kort-navn>
```

## Klar til merge

- Ændringer er gennemgået i VS Code.
- Pull request beskriver release-omfang kort.
- Relevante lokale checks er gennemført.

## Ikke omfattet

- Deploy-trin.
- VPS-procedurer.
- Secrets eller miljøspecifik konfiguration.

