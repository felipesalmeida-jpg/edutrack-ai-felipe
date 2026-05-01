// Search subjects by name for the authenticated user
query subjects_search verb=GET {
  api_group = "Authentication"
  auth = "user"

  input {
    text search
  }

  stack {
    // Regra de Ouro: Garante que a busca só retorne dados do usuário logado
    db.query subjects {
      where = "user_id = ${auth.id} AND name LIKE %${input.search}%" == true
      return = {type: "list"}
    } as $model
  }

  response = $model
}