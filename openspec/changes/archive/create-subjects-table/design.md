# Design: Create Subjects Table

## Tables

### subjects
| Field       | Type      | Required | Description                        |
|-------------|-----------|----------|------------------------------------|
| id          | integer   | yes      | Primary key, auto increment        |
| user_id     | integer   | yes      | Foreign key referencing users.id   |
| name        | text      | yes      | Subject name (max 100 chars)       |
| description | text      | no       | Optional subject description       |
| is_active   | boolean   | yes      | Soft delete flag (default: true)   |
| created_at  | timestamp | yes      | Auto-generated on insert           |
| updated_at  | timestamp | yes      | Auto-updated on every change       |
| professor   | text      | no       | Professor responsible for subject  |

## Relationships
- `subjects.user_id` → `users.id` (many-to-one)
- Each subject belongs to exactly one user
- One user can own multiple subjects

## Indexes
- Index on `user_id` for fast user-based queries
- Index on `is_active` for filtering active subjects

## Structural Decisions
- `is_active` preferred over hard delete to preserve history
- `updated_at` enables cache invalidation and audit trails
- `description` is optional to keep creation flow simple
- All timestamps managed automatically by the database

## Constraints
- `name` cannot be null or empty
- `user_id` must reference a valid existing user
- `is_active` defaults to `true` on creation