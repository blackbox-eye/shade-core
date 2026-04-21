# Runtime loop A to O

## Formål

Denne fil låser det sekventielle beslutnings- og kontrolflow for V1.

## Sekvens

- A: modtag input og opret et forløb.
- B: valider input mod kontrakterne.
- C: fastlæg aktivt mål og tilladt scope.
- D: vælg relevant worker-type.
- E: klargør worker-opgave.
- F: udfør et enkelt worker-trin.
- G: registrér output og status.
- H: kontroller output mod kontrakterne.
- I: vurder om næste trin er nødvendigt.
- J: stop ved brud, uklarhed eller manglende evidens.
- K: send videre til næste worker, hvis kontrakten tillader det.
- L: saml samlet tilstand for forløbet.
- M: kør evaluering mod V1-målepunkter.
- N: markér resultat som accept, afvisning eller behov for review.
- O: afslut forløbet med inspectable slutstatus.

## Arbejdsregler

- Kontrakter kommer før runtime-adfærd.
- Hvert trin skal kunne inspiceres bagefter.
- Hvert skifte mellem trin skal kunne testes som interface.
- Copilot er assistent for arbejdet, ikke beslutningsmyndighed.
