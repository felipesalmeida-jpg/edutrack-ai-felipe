# hybrid-search Specification

## Purpose
Define a hybrid search feature that filters subjects by name or by overdue
tasks, combining Xano database queries with Python processing logic.

## ADDED Requirements

### Requirement: Search subjects by name
The system SHALL filter subjects by name using a search term.

#### Scenario: User searches by name
- **WHEN** authenticated user calls GET /subjects/search with a name parameter
- **THEN** system returns subjects where name contains the search term

### Requirement: Filter overdue tasks
The system SHALL identify tasks past their due date using Python logic.

#### Scenario: User requests overdue tasks
- **WHEN** a list of tasks is provided to the Python script
- **THEN** system returns only tasks where due_date is before today
