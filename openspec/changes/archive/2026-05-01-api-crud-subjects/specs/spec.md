# api-crud-subjects Specification

## Purpose
Define the CRUD API endpoints for managing academic subjects in EduTrack AI,
ensuring users can only access their own data.

## ADDED Requirements

### Requirement: List subjects filtered by user
The system SHALL return only subjects belonging to the authenticated user.

#### Scenario: User requests their subjects
- **WHEN** authenticated user calls GET /subjects
- **THEN** system returns only subjects where user_id matches auth.id

### Requirement: Create subject linked to user
The system SHALL create a subject associated with the authenticated user.

#### Scenario: User creates a new subject
- **WHEN** authenticated user calls POST /subjects
- **THEN** system stores subject with user_id from auth.id

### Requirement: Update own subject only
The system SHALL allow updating only subjects owned by the authenticated user.

#### Scenario: User updates their subject
- **WHEN** authenticated user calls PATCH /subjects/{id}
- **THEN** system updates subject only if user_id matches auth.id

### Requirement: Delete own subject only
The system SHALL allow deleting only subjects owned by the authenticated user.

#### Scenario: User deletes their subject
- **WHEN** authenticated user calls DELETE /subjects/{id}
- **THEN** system deletes subject only if user_id matches auth.id
