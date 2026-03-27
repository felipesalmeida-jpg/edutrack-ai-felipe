## ADDED Requirements

### Requirement: `subjects` table schema
The system SHALL provide a table to store academic subjects with a specific schema. This ensures data integrity and consistency for all subject records.


### Scenario: Table structure verification

#### Scenario: Table structure verification

- **WHEN** the `subjects` table schema is inspected
- **THEN** it SHALL contain the following fields: `id` (integer), `created_at` (timestamp), `name` (text), `professor` (text), `description` (text), and `user_id` (integer, table reference to `user`).

### Requirement: User ownership of subjects
Every record in the `subjects` table SHALL be associated with a record in the `user` table. This is critical for access control and data segregation.

#### Scenario: Subject creation with user link
- **WHEN** a new subject record is created
- **THEN** its `user_id` field MUST NOT be null and MUST correspond to an existing `id` in the `user` table.
