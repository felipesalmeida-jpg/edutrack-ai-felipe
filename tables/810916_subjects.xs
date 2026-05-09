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
  
    // Semestre/Período da disciplina (ex: 2024.1, 2024.2)
    text semester? filters=trim
  
    // Sala da disciplina (ex: Sala 101, Laboratório 2)
    text room? filters=trim
  
    // Horário da disciplina (ex: 08:00-10:00, 14:00-16:00)
    text schedule? filters=trim
  
    // Status da disciplina: active ou archived
    text status?=active
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
  ]
}