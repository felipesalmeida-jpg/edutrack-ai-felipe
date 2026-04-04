query "subject" verb=POST {
  api_group = "subject"
  description = "Cria uma nova disciplina vinculada ao usuário logado."
  auth = "user"

  input {
    text name filters=trim {
      description = "Nome da disciplina (Obrigatório)"
    }
    text description? filters=trim {
      description = "Descrição detalhada ou link para ementa"
    }
    text semester? filters=trim {
      description = "Semestre letivo (ex: 2024.1)"
    }
    int credits?=0 filters=min:0 {
      description = "Número de créditos ou carga horária"
    }
    text status?=active filters=trim|lower {
      description = "Estado da disciplina (active, completed, dropped)"
    }
  }

  stack {
    db.add subject {
      data = {
        user_id: $auth.id
        name: $input.name
        description: $input.description
        semester: $input.semester
        credits: $input.credits
        status: $input.status
      }
      mock = {
        "deve criar uma nova disciplina": {id: 1, user_id: 10, name: "Engenharia", status: "active"}
      }
    } as $new_subject
  }

  response = $new_subject

  test "deve criar uma nova disciplina" {
    input = {name: "Engenharia"}
    expect.to_equal ($response.name) { value = "Engenharia" }
  }
}