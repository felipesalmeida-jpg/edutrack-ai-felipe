// Query all academic_tasks records
query academic_tasks verb=GET {
  api_group = "academic_tasks"
  auth = "user"

  input {
    int page?
  }

  stack {
    db.query academic_tasks {
      where = $db.academic_tasks.user_id == $auth.id
      return = {type: "list", paging: {page: $input.page, per_page: 30}}
    } as $academic_tasks_records
  }

  response = $academic_tasks_records
}