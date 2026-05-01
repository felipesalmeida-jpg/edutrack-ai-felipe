// Get subjects record (Filtrado por Usuário)
query "subjects/{subjects_id}" verb=GET {
  api_group = "Authentication"
  // Define que o usuário precisa estar autenticado
  auth = "user"

  input {
    int subjects_id? filters=min:1
  }

  stack {
    db.get subjects {
      field_name = "id"
      field_value = $input.subjects_id
      // Regra de Ouro: Filtro de segurança simplificado
      where = "user_id == $auth.id"
    } as $subjects
    // Filtro de segurança obrigatório para garantir que o usuário só acesse suas próprias disciplinas

    precondition ($subjects != null) {
      error_type = "notfound"
      error = "Disciplina não encontrada ou acesso negado."
    }
  }

  response = $subjects
}