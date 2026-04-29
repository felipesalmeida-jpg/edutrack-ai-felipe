// Get a single subject for the authenticated user
query subjects verb=GET {
  api_group = "Authentication"
  auth = true
  input {
    int id
  }
  stack {
    db.query subjects {
      return = {type: "first"}
      where {
        id == .id
        user_id == .id
      }
    } as 
  }
  response = 
}
