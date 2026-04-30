// Delete edutrack record.
query "edutrack/{edutrack_id}" verb=DELETE {
  api_group = "Edutrack AI Felipe"

  input {
    int edutrack_id? filters=min:1
  }

  stack {
    db.del edutrack {
      field_name = "id"
      field_value = $input.edutrack_id
    }
  }

  response = null
}