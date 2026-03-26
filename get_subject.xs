query "subject/{id}" verb=GET {
  api_group = "subject"
  description = "Obtém os detalhes de uma disciplina específica, validando a propriedade do usuário logado."
  auth = "user"

  input {
    int id {
      description = "ID da disciplina"
    }
  }

  stack {
    db.query subject {
      where = $db.subject.id == $input.id && $db.subject.user_id == $auth.id
      return = {type: "single"}
      mock = {
        "deve retornar a disciplina com sucesso": {id: 1, user_id: 10, name: "Matemática"}
        "deve falhar se a disciplina nao existir ou for de outro usuario": null
      }
    } as $subject

    precondition ($subject != null) {
      error_type = "notfound"
      error = "Disciplina não encontrada ou sem permissão de acesso."
    }
  }

  response = $subject

  test "deve retornar a disciplina com sucesso" {
    input = {id: 1}
    expect.to_equal ($response.name) { value = "Matemática" }
  }

  test "deve falhar se a disciplina nao existir ou for de outro usuario" {
    input = {id: 99}
    expect.to_throw
  }
}