// Delete a subject for the authenticated user
query subjects verb=DELETE {
  api_group = "Authentication"
  auth = true
  input {
    int id
  }
  stack {
    db.delete subjects {
      where {
        id == .id
        user_id == .id
      }
    }
  }
  response = {deleted: true}
}
