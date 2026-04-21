# academic_tasks Specification

## Purpose
Define the data structure for managing academic obligations tied to subjects within EduTrack AI.

## ADDED Requirements

### Requirement: Create academic_tasks table
The system SHALL provide a database table to store academic tasks such as lessons, exams, and assignments linked to a specific subject.

#### Scenario: Registering a new academic task
- **WHEN** a user creates a new task for a subject
- **THEN** the system SHALL securely store the task with its respective `title`, `description`, `due_date`, `status`, and `subject_id`.