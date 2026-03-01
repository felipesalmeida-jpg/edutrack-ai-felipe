// Add edutrack record
query edutrack verb=POST {
  api_group = "Edutrack AI Felipe"

  input {
    dblink {
      table = "edutrack"
    }
  }

  stack {
    db.add edutrack {
      data = {created_at: "now"}
    } as $edutrack
  }

  response = $edutrack
}