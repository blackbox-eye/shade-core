# Data models

## Formål

Denne fil låser de centrale kontraktobjekter og deres felter for V1.

## Contract object: Run

- `run_id`: entydig identitet for et forløb.
- `goal`: aktivt mål for forløbet.
- `scope`: tilladt arbejdsramme.
- `status`: nuværende tilstand.
- `current_step`: aktuelt trin i loopet.
- `result`: slutresultat eller mellemresultat.

## Contract object: Worker task

- `task_id`: entydig identitet for opgaven.
- `worker_type`: valgt worker-type.
- `input_ref`: reference til det input, der arbejdes på.
- `expected_output`: det forventede outputformat.
- `constraints`: aktive grænser for opgaven.
- `task_status`: opgavens tilstand.

## Contract object: Evaluation record

- `evaluation_id`: entydig identitet for målingen.
- `run_id`: reference til forløbet.
- `checks`: hvilke checks der er kørt.
- `findings`: observerede afvigelser.
- `decision`: accept, afvisning eller review.
- `notes`: korte operationelle noter.

## Feltregler

- Felter skal være entydige og inspectable.
- Objekter skal kunne testes via deres input og output.
- V1 holder kun de felter, som styrer kontrol, status og evaluering.
