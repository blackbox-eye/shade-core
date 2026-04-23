# Runtime loop A to O

## Purpose

This file locks the sequential decision and control flow for V1.

## Sequence

- A: receive input and create a run.
- B: validate input against the contracts.
- C: determine the active goal and allowed scope.
- D: select the relevant worker type.
- E: prepare the worker task.
- F: execute a single worker step.
- G: record output and status.
- H: check output against the contracts.
- I: assess whether the next step is required.
- J: stop on violation, uncertainty, or missing evidence.
- K: pass onward to the next worker if the contract allows it.
- L: collect the full state for the run.
- M: run evaluation against the V1 metrics.
- N: mark the result as acceptance, rejection, or need for review.
- O: end the run with inspectable final status.

## Working rules

- Contracts come before runtime behavior.
- Each step must be inspectable afterwards.
- Each transition between steps must be testable as an interface.
- Copilot is an assistant for the work, not a decision authority.
