# Shade V1 control stack

## Formål

Denne fil låser V1 control stack før runtime.

## Kerne-moduler

- `control-plane` fastlægger regler, rækkefølge og stopbetingelser.
- `state-store` holder den inspectable arbejdsstatus for et enkelt forløb.
- `worker-registry` beskriver hvilke workers der findes, og hvad de må.
- `contract-gate` afviser input eller output, der bryder kontrakterne.
- `evaluation-gate` samler QA-signaler før et forløb kan accepteres.

## Ansvar

- Hvert modul har ét klart ansvar.
- Moduler skal være inspectable via tydelige input, output og status.
- Interfaces skal være testbare uden runtime-udvidelser.
- Copilot er assistent i arbejdet, ikke autoritet i kontrakterne.

## Afgrænsning

- Denne kontrakt beskriver ikke kode, deploy, VPS, workflows eller drift.
- Der indføres ikke produktion, integration eller secrets i V1.
