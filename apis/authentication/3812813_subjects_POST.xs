// Add subjects record
query subjects verb=POST {
  api_group = "Authentication"

  input {
    dblink {
      table = "subjects"
    }
    text name
    text professor?
    text day_of_week?
  }

  stack {
    db.add subjects {
      data = {
        user_id: $user.id
        name: $input.name
        professor: $input.professor
        day_of_week: $input.day_of_week
        created_at: "now"
      }
    } as $subjects
  }

  response = $subjects
}