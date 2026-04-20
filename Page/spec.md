# activity_grades Specification

## Purpose
Define the data structure and behavior for assigning and storing academic activity grades within EduTrack AI.

## Requirements

### Requirement: Create activity_grades table
The system SHALL provide a database table to store grades assigned to specific activities.

#### Scenario: Record a new grade
- **WHEN** a professor assigns a grade to an activity
- **THEN** the system SHALL store the grade securely, linking it to the authenticated `user_id` to ensure data segregation.

### Requirement: Submit activity grades via API
The system MUST provide a secure REST API endpoint to submit new grades.

#### Scenario: API grade submission
- **WHEN** the frontend sends a POST request to `/activity_grades` with valid grade data
- **THEN** the system MUST create a new grade record associated with the authenticated user.
### Requirement: Submit activity grades via API
The system MUST provide a secure REST API endpoint to submit new grades.

#### Scenario: API grade submission
- **WHEN** the frontend sends a POST request to `/activity_grades` with valid grade data
- **THEN** the system MUST create a new grade record associated with the authenticated user.
