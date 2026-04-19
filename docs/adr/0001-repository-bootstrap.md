# ADR-0001 Repository Bootstrap

Status: Accepted

## Context

Repositoryet havde behov for en enkel, lokal ramme for dokumentation og ændringskontrol i opstartsfasen.

## Decision

`shade-core` etableres som et letvægts repository med dokumentation, governance og lokalt workflow via VS Code og PowerShell.

## Consequences

- `main` beskyttes med PR-only merge.
- Signed commits og linear history er faste krav.
- Repositoryet omfatter ikke deploy, VPS eller secrets.

