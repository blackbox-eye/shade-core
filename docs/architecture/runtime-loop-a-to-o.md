# Runtime loop A to O

## Purpose

This file locks the sequential decision and control flow for V1.
The current codebase implements only minimal supporting slices and one internal runtime-fabric snapshot path, not full A-to-O orchestration.

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
- The current core can assemble run state, handoff, decision, audit event, and evaluation gate result into one inspectable internal snapshot.
- The current core also holds neutral internal contract objects for worker task, worker result, and task route. These are contract boundaries only; they do not execute steps D through K.
- The current core also holds neutral internal contract objects for task transition and run transition. These prepare step-junction verification without executing transitions.
- Each step must be inspectable afterwards.
- Each transition between steps must be testable as an interface.
- Copilot is an assistant for the work, not a decision authority.
