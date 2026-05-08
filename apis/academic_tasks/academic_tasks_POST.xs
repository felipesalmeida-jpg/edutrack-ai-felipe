// Create a new academic task
query academic_tasks verb=POST {
  api_group = "academic_tasks"
  auth = "user"

  input {
    text title
    text description?
    timestamp due_date?
    text status?
    text priority?
    int subject_id?
  }

  stack {
    db.add academic_tasks {
      data = {
        user_id    : $auth.id
        title      : $input.title
        description: $input.description
        due_date   : $input.due_date
        status     : $input.status || "pending"
        priority   : $input.priority || "medium"
        subject_id : $input.subject_id
      }
    } as $model
  }

  response = $model
}