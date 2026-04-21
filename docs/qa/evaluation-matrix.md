# Evaluation matrix

## Formål

Denne fil låser hvad der måles i V1, og hvordan vi QA'er før runtime udvides.

## Målepunkter

- Kontraktklarhed: er ansvar, felter og grænser tydelige.
- Sekvensklarhed: kan loopet følges trin for trin.
- Interface-testbarhed: kan input og output vurderes entydigt.
- Inspectability: kan status og beslutninger læses bagefter.
- Scope-disciplin: holder materialet sig uden for deploy, VPS, secrets, produktion og integration.

## QA-form

- Hvert dokument læses som kontrakt, ikke som idéoplæg.
- Hvert modul vurderes for tydeligt ansvar og tydelige grænser.
- Hvert interface vurderes for testbarhed uden ekstra antagelser.
- Afvigelser markeres som blocker, hvis de svækker kontrakt eller kontrolflow.

## V1-beslutning

- V1 er klar, når kontrakterne er korte, stabile og sammenhængende.
- V1 er ikke klar, hvis hype, uklare roller eller skjult runtime-adfærd sniger sig ind.
- Copilot kan hjælpe med formulering og review, men er ikke autoritet for accept.
