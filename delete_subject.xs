query "subject/{id}" verb=DELETE {
  api_group = "subject"
  description = "Exclui permanentemente uma disciplina do usuário logado."
  auth = "user"

  input {
    int id
  }

  stack {
    db.query subject {
      where = $db.subject.id == $input.id && $db.subject.user_id == $auth.id
      return = {type: "single"}
      mock = {
        "deve deletar a disciplina com sucesso": {id: 1, user_id: 10}
        "deve falhar ao deletar disciplina inexistente": null
      }
    } as $existing_subject

    precondition ($existing_subject != null) {
      error_type = "notfound"
      error = "Disciplina não encontrada ou sem permissão de acesso."
    }

    db.delete subject {
      id = $input.id
      mock = {
        "deve deletar a disciplina com sucesso": true
      }
    } as $deleted
  }

  response = {
    success: true
  }

  test "deve deletar a disciplina com sucesso" {
    input = {id: 1}
    expect.to_be_true ($response.success)
  }

  test "deve falhar ao deletar disciplina inexistente" {
    input = {id: 99}
    expect.to_throw
  }
}