table subjects {
  auth = false

  schema {
    int id
    timestamp created_at?=now {
      visibility = "private"
    }
  
    // The name of the subject.
    text name? filters=trim
  
    // A brief description of the subject.
    text description? filters=trim
  
    // The name of the professor teaching the subject.
    text professor? filters=trim
  
    // Reference to the user responsible for this subject.
    int user? {
      table = "user"
    }
  
    // Indicates if the subject is currently active.
    bool is_active?
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
  ]
}