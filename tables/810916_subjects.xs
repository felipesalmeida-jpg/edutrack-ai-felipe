table subjects {
  auth = false

  schema {
    int id
    timestamp created_at?=now {
      visibility = "private"
    }
  
    int user_id? {
      table = "user"
    }
  
    text name? filters=trim
    text professor? filters=trim
    text day_of_week? filters=trim
    text semester? filters=trim {
      description = "Semestre/Período da disciplina (ex: 2024.1, 2024.2)"
    }
    text status?=active {
      description = "Status da disciplina: active ou archived"
    }
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
  ]
}