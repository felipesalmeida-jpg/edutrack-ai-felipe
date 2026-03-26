query "subjects" verb=GET {
  api_group = "subject"
  description = "Lista todas as disciplinas cadastradas pelo usuário logado, com filtro opcional de status."
  auth = "user"

  input {
    text status? filters=trim|lower {
      description = "Filtro opcional pelo estado da disciplina (ex: active, completed, dropped)"
    }
  }

  stack {
    db.query subject {
      description = "Busca as disciplinas pertencentes ao usuário com ordenação pelas mais recentes"
      where = $db.subject.user_id == $auth.id && $db.subject.status ==? $input.status
      sort = {subject.created_at: "desc"}
      return = {type: "list"}
      mock = {
        "deve retornar a lista de disciplinas do usuario": [
          {id: 1, name: "Matemática", status: "active"},
          {id: 2, name: "Física", status: "active"}
        ]
      }
    } as $subjects
  }

  response = $subjects

  test "deve retornar a lista de disciplinas do usuario" {
    input = {}
    expect.to_be_greater_than ($response|count) { value = 0 }
  }
}