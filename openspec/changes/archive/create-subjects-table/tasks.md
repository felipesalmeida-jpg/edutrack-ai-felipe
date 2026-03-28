# Tasks: Create Subjects Table

## Database
- [x] Create subjects table
- [x] Add id field (primary key, auto increment)
- [x] Add user_id field (integer, required, foreign key)
- [x] Add name field (text, required, max 100 chars)
- [x] Add description field (text, optional)
- [x] Add is_active field (boolean, default true)
- [x] Add created_at field (timestamp, auto)
- [x] Add updated_at field (timestamp, auto)

## Relationships
- [x] Create foreign key: subjects.user_id → users.id

## Indexes
- [x] Add index on user_id
- [x] Add index on is_active

## Validation
- [x] Ensure name is required and non-empty
- [x] Ensure user_id references a valid user
- [x] Ensure is_active defaults to true

## Future (Out of Scope)
- [x] Add subject categories
- [x] Enable subject sharing between users
- [x] Add enrollment model