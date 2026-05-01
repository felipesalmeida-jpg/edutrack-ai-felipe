table academic_tasks {
  auth = false

  schema {
    int id
    timestamp created_at?=now {
      visibility = "private"
    }
  
    text title? filters=trim
    text description? filters=trim
    timestamp due_date?
    text status?=pending
    int subject_id? {
      table = "subjects"
    }
  }

  index = [{type: "primary", field: [{name: "id"}]}]
}