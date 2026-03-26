## Why

Users need a way to register and manage their academic subjects. This creates a foundation for subject-specific features, access control, and future automations.

## What Changes

- A new `subjects` table will be added to the database.
- The table will store subject details and a reference to the user who owns it.

## Capabilities

### New Capabilities
- `subjects-db`: Defines the schema and storage for academic subjects.

### Modified Capabilities


## Impact

- A new table will be added to the Xano database schema.
- This change is foundational and will likely require new API endpoints for subject management in the future.
