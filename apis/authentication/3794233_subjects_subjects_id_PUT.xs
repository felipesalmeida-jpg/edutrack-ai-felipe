// Update subjects record
query "subjects/{subjects_id}" verb=PUT {
  api_group = "Authentication"

  input {
    int subjects_id? filters=min:1
    dblink {
      table = "subjects"
    }
  }

  stack {
    db.edit subjects {
      field_name = "id"
      field_value = $input.subjects_id
      data = {
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