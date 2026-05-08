// Get subjects record
query "subjects/{subjects_id}" verb=GET {
  api_group = "Authentication"
  auth = "user"

  input {
    int subjects_id? filters=min:1
  }

  stack {
    db.query subjects {
      where = $db.subjects.id == $input.subjects_id && $db.subjects.user_id == $auth.id
      return = {type: "single"}
    } as $subjects
  }

  response = $subjects
}