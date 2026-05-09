// Edit subjects record
query "subjects/{subjects_id}" verb=PATCH {
  api_group = "Authentication"
  auth = "user"

  input {
    int subjects_id? filters=min:1
    dblink {
      table = "subjects"
    }
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
  
    util.get_raw_input {
      encoding = "json"
      exclude_middleware = false
    } as $raw_input
  
    db.patch subjects {
      field_name = "id"
      field_value = $input.subjects_id
      data = `$input|pick:($raw_input|keys)`|filter_null|filter_empty_text
    } as $subjects
  }

  response = $subjects
}