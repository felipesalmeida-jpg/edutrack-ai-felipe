// Add subjects record
query subjects verb=POST {
  api_group = "Authentication"
  auth = "user"

  input {
    text name
    text professor?
    text day_of_week?
    text semester?
  }

  stack {
    db.add subjects {
      data = {
        user_id    : $auth.id
        name       : $input.name
        professor  : $input.professor
        day_of_week: $input.day_of_week
        semester   : $input.semester
        created_at : "now"
      }
    } as $subjects
  }

  response = $subjects
}