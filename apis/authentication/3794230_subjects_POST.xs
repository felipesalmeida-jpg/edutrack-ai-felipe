// Add subjects record
query subjects verb=POST {
  api_group = "Authentication"

  input {
    dblink {
      table = "subjects"
    }
  }

  stack {
    db.add subjects {
      data = {
        created_at : "now"
        name       : $input.name
        description: $input.description
        professor  : $input.professor
        user       : $input.user
        is_active  : $input.is_active
      }
    } as $model
  }

  response = $model
}