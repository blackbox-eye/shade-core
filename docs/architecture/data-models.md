# Data models

## Purpose

This file locks the central contract objects and their fields for V1.
The current code implements only a smaller typed subset through `src/shade_core/models.py` and `src/shade_core/state.py`.
The current public package surface exposes only the implemented subset through the root `shade_core` import path.
The current internal model set also includes one neutral handoff object for future adapter preparation without adding adapters now, three neutral worker-task/orchestration contract objects that prepare internal boundaries without implementing orchestration, and two neutral state-transition contract objects that prepare step-junction boundaries without implementing step transitions.
The current internal model set also includes two neutral checkpoint/junction bridge objects that connect the existing worker-result and route layer to the existing transition-prep layer without executing orchestration or routing behavior.
The current internal model set also includes two neutral verification/outcome bridge objects that connect the existing checkpoint/junction and transition-prep layers to the decision/evaluation side without executing verification, evaluation, or decision behavior.

## Current internal object: Artifact handoff

- `artifact_ref`: reference to the artifact being handed off.
- `source_lane`: neutral source lane label for the handoff.
- `target_lane`: neutral target lane label for the handoff.

This object is an internal preparation boundary only. It is not a new public package export and does not add provider-specific fields or runtime behavior.

## Current internal object: Worker task

- `task_id`: unique identity for this task.
- `worker_role`: which role executes this task.
- `input_ref`: reference to the input for this task.
- `task_status`: current state of the task.

This object is an internal contract boundary only. It is not a public package export and does not add orchestration behavior.

## Current internal object: Worker result

- `task_id`: matches the task this result belongs to.
- `worker_role`: which role produced this result.
- `output_ref`: reference to the output produced.
- `result_status`: state or disposition of the result.

This object is an internal contract boundary only. It is not a public package export.

## Current internal object: Task route

- `task_id`: which task is being routed.
- `source_role`: neutral source role label.
- `target_role`: neutral target role label.
- `route_ref`: reference key for this route.

This object is an internal contract boundary only. It is not a public package export.

## Current internal object: Orchestration checkpoint

- `task_id`: which task reached the checkpoint.
- `output_ref`: reference to the current worker result output.
- `route_ref`: reference to the route already associated with this checkpoint.
- `checkpoint_ref`: reference key for this checkpoint event.

This object is a neutral internal bridge contract only. It connects current result and route preparation to later transition preparation without executing orchestration behavior. It is not a public package export.

## Current internal object: Orchestration junction

- `route_ref`: reference to the route being joined to transition preparation.
- `task_transition_ref`: reference to the prepared task transition.
- `run_transition_ref`: reference to the prepared run transition.
- `junction_ref`: reference key for this junction event.

This object is a neutral internal bridge contract only. It connects current result and route preparation to later transition preparation without executing orchestration behavior. It is not a public package export.

## Current internal object: Task transition

- `task_id`: which task is transitioning.
- `from_status`: the status the task is transitioning from.
- `to_status`: the status the task is transitioning to.
- `transition_ref`: reference key for this transition event.

This object is an internal contract boundary only. It is not a public package export.

## Current internal object: Run transition

- `run_id`: which run is transitioning.
- `from_step`: the step the run is transitioning from.
- `to_step`: the step the run is transitioning to.
- `transition_ref`: reference key for this transition event.

This object is an internal contract boundary only. It is not a public package export.

## Current internal object: Orchestration verification

- `checkpoint_ref`: reference to the checkpoint being verified.
- `junction_ref`: reference to the junction being carried into verification prep.
- `task_transition_ref`: reference to the prepared task transition carried into verification prep.
- `verification_ref`: reference key for this verification boundary.

This object is a neutral internal bridge contract only. It connects current checkpoint/junction and transition preparation to the decision/evaluation side without executing verification behavior. It is not a public package export.

## Current internal object: Orchestration outcome

- `verification_ref`: reference to the prepared verification boundary.
- `decision_ref`: reference to the related decision-side boundary.
- `evaluation_ref`: reference to the related evaluation-side boundary.
- `outcome_ref`: reference key for this outcome boundary.

This object is a neutral internal bridge contract only. It connects current verification preparation to the decision/evaluation side without executing evaluation or decision behavior. It is not a public package export.

## Contract object: Run

- `run_id`: unique identity for a run.
- `goal`: active goal for the run.
- `scope`: allowed working scope.
- `status`: current state.
- `current_step`: current step in the loop.
- `result`: final result or intermediate result.

## Contract object: Worker task

- `task_id`: unique identity for the task.
- `worker_type`: selected worker type.
- `input_ref`: reference to the input being worked on.
- `expected_output`: the expected output format.
- `constraints`: active boundaries for the task.
- `task_status`: task state.

## Contract object: Evaluation record

- `evaluation_id`: unique identity for the evaluation.
- `run_id`: reference to the run.
- `checks`: which checks have been run.
- `findings`: observed deviations.
- `decision`: acceptance, rejection, or review.
- `notes`: short operational notes.

## Field rules

- Fields must be unambiguous and inspectable.
- Objects must be testable through their input and output.
- V1 keeps only the fields that drive control, status, and evaluation.
- This document remains broader than the current public API where V1 contract objects are still documented targets rather than implemented exports.
