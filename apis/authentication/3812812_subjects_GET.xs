// Query all subjects records filtered by authenticated user
query subjects verb=GET {
  api_group = "Authentication"
  auth = true
  input {
  }
  stack {
    db.query subjects {
      return = {type: "list"}
      where {
        user_id == .id
      }
    } as 
  }
  response = 
}
