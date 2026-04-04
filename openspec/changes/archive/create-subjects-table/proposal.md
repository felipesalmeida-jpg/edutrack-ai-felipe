# Proposal: Create Subjects Table

## Why
Academic management systems require structured organization of disciplines.
Currently, there is no way to register, associate, or manage academic subjects
per user, which blocks access control and future automations.

## What Changes
- Create the `subjects` table with full ownership model
- Associate subjects with authenticated users via foreign key
- Enforce data validation at the schema level

## Impact
- New table `subjects` added to the database
- Direct relationship between `subjects` and `users`
- Foundation for future APIs, filters, and automations

## Capabilities
- Users can create academic subjects with a name and description
- Users can list only their own subjects (ownership enforced)
- Users can update subject details
- Users can soft-delete subjects (is_active flag)
- System can filter subjects by status and user

## Out of Scope
- Subject sharing between users (future)
- Subject categories or tags (future)
- Enrollment or student association (future)