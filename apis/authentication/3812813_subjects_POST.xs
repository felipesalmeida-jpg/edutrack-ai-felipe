// Create a new subject for the authenticated user
query subjects verb=POST {
  api_group = "Authentication"
  auth = true
  input {
    text name
    text description?
    text professor?
    bool is_active?=true
  }
  stack {
    db.create subjects {
      data {
        user_id = .id
        name = .name
        description = .description
        professor = .professor
        is_active = .is_active
      }
    } as 
  }
  response = 
}
