# Test strategy

## Formål

Denne fil dækker kun lokal repo-baseline, PR-baseline og senere testretning.

## Nuværende baseline

- Lokale ændringer gennemlæses i VS Code.
- Enkle repository- og filchecks kan køres lokalt i PowerShell.
- Pull request er den faste kvalitetssluse før merge.

## Før pull request

- Indhold er læst igennem lokalt.
- Ændringen er lille nok til hurtigt review.
- Baseline-checks er gennemført.

## Senere retning

- Testdækning kan udvides, når kode og moduler vokser.
- Nye tests skal følge repositoryets enkle foundation-ramme.

## Afgrænsning

Denne strategi dækker ikke deploy, VPS, produktion eller integration.
