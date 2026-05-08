// Update academic_tasks record.
query "academic_tasks/{academic_tasks_id}" verb=PATCH {
  api_group = "academic_tasks"
  auth = "user"

  input {
    int academic_tasks_id? filters=min:1
    dblink {
      table = "academic_tasks"
    }
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
    
    util.get_raw_input {
      encoding = "json"
      exclude_middleware = false
    } as $raw_input
  
    db.patch academic_tasks {
      field_name = "id"
      field_value = $input.academic_tasks_id
      data = `$input|pick:($raw_input|keys)`|filter_null|filter_empty_text
    } as $academic_tasks_updated_record
  }

  response = $academic_tasks_updated_record
}