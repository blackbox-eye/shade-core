# Test strategy

## Formål

Denne strategi definerer en kort, lokal baseline for kvalitetssikring i repositoryet.

## Principper

- Test og review udføres før pull request merge.
- `main` er protected og modtager kun ændringer via pull request.
- Signed commits og linear history er obligatoriske.

## Lokal kvalitetssikring

- Brug VS Code til at gennemgå ændringer og markdown-indhold.
- Brug PowerShell til lokale Git-kommandoer og enkle valideringer.
- Hold ændringer små, afgrænsede og lette at reviewe.

## Minimum før PR

- Indhold er læst igennem lokalt.
- Ændringen er sporbar i én eller få signerede commits.
- Pull request beskriver formål og omfang kort.

## Ikke omfattet

- Deploy-validering.
- VPS-test eller driftstjek.
- Håndtering af secrets.

