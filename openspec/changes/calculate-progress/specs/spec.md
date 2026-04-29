# calculate-progress Specification

## Purpose
Define a Python script that calculates the progress percentage of academic
tasks for a given subject in EduTrack AI.

## ADDED Requirements

### Requirement: Calculate task progress
The system SHALL calculate the percentage of completed tasks over total tasks.

#### Scenario: Tasks exist and some are completed
- **WHEN** a list of tasks is provided with some marked as completed
- **THEN** system returns a JSON with the percentage of completed tasks

### Requirement: Handle division by zero
The system SHALL return zero percent when no tasks exist.

#### Scenario: No tasks exist
- **WHEN** the task list is empty
- **THEN** system returns JSON with percentage equal to 0
