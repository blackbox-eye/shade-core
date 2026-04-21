# Worker ontology

## Formål

Denne fil låser worker-typer, roller, ansvar og grænser for V1.

## Worker-typer

- `intake-worker` afklarer input, mål og scope.
- `analysis-worker` vurderer materiale mod aktive kontrakter.
- `control-worker` beslutter næste tilladte trin i loopet.
- `evaluation-worker` måler output mod QA-matrixen.

## Roller og ansvar

- Hver worker løser én afgrænset opgave ad gangen.
- En worker må kun arbejde inden for deklareret scope.
- En worker skal aflevere inspectable output og status.
- En worker må ikke omskrive kontrakterne.

## Grænser

- Workers er ikke autoriteter; de udfører kontraktstyret arbejde.
- Copilot er assistent til forslag og formulering, ikke beslutningstager.
- Workers må ikke indføre deploy, VPS, secrets, produktion eller integration.
- Workers må ikke springe kontrol- eller evalueringsled over.
