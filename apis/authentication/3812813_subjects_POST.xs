// Add subjects record
query subjects verb=POST {
  api_group = "Authentication"
  auth = "user"

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
        user_id    : $auth.id
        name       : $input.name
        professor  : $input.professor
        day_of_week: $input.day_of_week
        created_at : "now"
      }
    } as $subjects
  }

  response = $subjects
}