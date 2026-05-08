table academic_tasks {
  auth = false

  schema {
    int id
    timestamp created_at?=now {
      visibility = "private"
    }
  
    int user_id? {
      table = "user"
    }
    text title? filters=trim
    text description? filters=trim
    timestamp due_date?
    text status?=pending
    text priority?=medium {
      description = "Prioridade da tarefa: low, medium, high"
    }
    int subject_id? {
      table = "subjects"
    }
  }

  index = [{type: "primary", field: [{name: "id"}]}]
}