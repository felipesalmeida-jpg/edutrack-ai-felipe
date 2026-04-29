query "subject/{id}" verb=PATCH {
  api_group = "subject"
  description = "Atualiza informações de uma disciplina existente."
  auth = "user"

  input {
    int id {
      description = "ID da disciplina a ser atualizada"
    }
    text name? filters=trim
    text description? filters=trim
    text semester? filters=trim
    int credits? filters=min:0
    text status? filters=trim|lower
  }

  stack {
    db.query subject {
      description = "Verifica se a disciplina existe e pertence ao usuário"
      where = $db.subject.id == $input.id && $db.subject.user_id == $auth.id
      return = {type: "single"}
      mock = {
        "deve atualizar a disciplina com sucesso": {id: 1, user_id: 10, name: "Antiga", status: "active"}
        "deve falhar ao atualizar disciplina inexistente": null
      }
    } as $existing_subject

    precondition ($existing_subject != null) {
      error_type = "notfound"
      error = "Disciplina não encontrada ou sem permissão de acesso."
    }

    db.update subject {
      description = "Aplica a atualização mesclando os valores enviados com os dados atuais"
      id = $input.id
      data = {
        name: ($input.name != null) ? $input.name : $existing_subject.name
        description: ($input.description != null) ? $input.description : $existing_subject.description
        semester: ($input.semester != null) ? $input.semester : $existing_subject.semester
        credits: ($input.credits != null) ? $input.credits : $existing_subject.credits
        status: ($input.status != null) ? $input.status : $existing_subject.status
      }
      mock = {
        "deve atualizar a disciplina com sucesso": {id: 1, user_id: 10, name: "Nova Disciplina", status: "active"}
      }
    } as $updated_subject
  }

  response = $updated_subject

  test "deve atualizar a disciplina com sucesso" {
    input = {id: 1, name: "Nova Disciplina"}
    expect.to_equal ($response.name) { value = "Nova Disciplina" }
  }

  test "deve falhar ao atualizar disciplina inexistente" {
    input = {id: 99, name: "Nova Disciplina"}
    expect.to_throw
  }
}