// Search subjects by name for the authenticated user
query subjects_search verb=GET {
  api_group = "Authentication"
  auth = "user"

  input {
    text search
  }

  stack {
    // Query all subjects for authenticated user, filtering by name via db
    db.query subjects {
      where = $db.subjects.user_id == $auth.id
      return = {type: "list"}
    } as $subjects
  }

  response = $subjects
}