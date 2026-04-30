// Query all edutrack records
query edutrack verb=GET {
  api_group = "Edutrack AI Felipe"

  input {
  }

  stack {
    db.query edutrack {
      return = {type: "list"}
    } as $edutrack
  }

  response = $edutrack
}