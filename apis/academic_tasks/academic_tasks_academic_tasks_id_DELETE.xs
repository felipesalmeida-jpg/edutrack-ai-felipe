// Delete academic_tasks record.
query "academic_tasks/{academic_tasks_id}" verb=DELETE {
  api_group = "academic_tasks"
  auth = "user"

  input {
    int academic_tasks_id? filters=min:1
  }

  stack {
    // Security check: verify user owns this task
    db.query academic_tasks {
      where = $db.academic_tasks.id == $input.academic_tasks_id && $db.academic_tasks.user_id == $auth.id
      return = {type: "single"}
    } as $task_check
  
    precondition ($task_check.id != null) {
      error_type = "accessdenied"
    }
  
    db.del academic_tasks {
      field_name = "id"
      field_value = $input.academic_tasks_id
    }
  }

  response = null
}