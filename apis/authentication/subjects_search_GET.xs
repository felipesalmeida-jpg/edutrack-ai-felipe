<<<<<<<
=======
// Search subjects by name for the authenticated user
query subjects_search verb=GET {
  api_group = "Authentication"
  auth = "user"
>>>>>>>

<<<<<<<
=======
  input {
    text search
  }

  stack {
    db.query subjects {
      where = $db.subjects.user_id == $auth.id && $db.subjects.name includes $input.search
      return = {type: "list"}
    } as $model
  }

  response = $model
}
>>>>>>>