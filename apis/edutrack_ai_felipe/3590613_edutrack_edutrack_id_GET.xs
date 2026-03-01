// Get edutrack record
query "edutrack/{edutrack_id}" verb=GET {
  api_group = "Edutrack AI Felipe"

  input {
    int edutrack_id? filters=min:1
  }

  stack {
    db.get edutrack {
      field_name = "id"
      field_value = $input.edutrack_id
    } as $edutrack
  
    precondition ($edutrack != null) {
      error_type = "notfound"
      error = "Not Found."
    }
  }

  response = $edutrack
}