# Data models

## Purpose

This file locks the central contract objects and their fields for V1.
The current code implements only a smaller typed subset through `src/shade_core/models.py` and `src/shade_core/state.py`.
The current public package surface exposes only the implemented subset through the root `shade_core` import path.

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
