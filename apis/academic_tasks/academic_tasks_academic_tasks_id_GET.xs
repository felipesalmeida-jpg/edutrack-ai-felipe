// Read academic_tasks record.
query "academic_tasks/{academic_tasks_id}" verb=GET {
  api_group = "academic_tasks"

  input {
    int academic_tasks_id? filters=min:1
  }

  stack {
    db.get academic_tasks {
      field_name = "id"
      field_value = $input.academic_tasks_id
    } as $record
  }

  response = $record
}