// Delete subjects record.
query "subjects/{subjects_id}" verb=DELETE {
  api_group = "Authentication"
  auth = "user"

  input {
    int subjects_id? filters=min:1
  }

  stack {
    // Security check: verify user owns this subject
    db.query subjects {
      where = $db.subjects.id == $input.subjects_id && $db.subjects.user_id == $auth.id
      return = {type: "single"}
    } as $subject_check
    
    precondition ($subject_check.id != null) {
      error_type = "accessdenied"
    }
    
    db.del subjects {
      field_name = "id"
      field_value = $input.subjects_id
    }
  }

  response = null
}