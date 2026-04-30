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
      data = {created_at: "now"}
    } as $subjects
  }

  response = $subjects
}