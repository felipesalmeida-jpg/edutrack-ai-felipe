// Edit edutrack record
query "edutrack/{edutrack_id}" verb=PATCH {
  api_group = "Edutrack AI Felipe"

  input {
    int edutrack_id? filters=min:1
    dblink {
      table = "edutrack"
    }
  }

  stack {
    util.get_raw_input {
      encoding = "json"
      exclude_middleware = false
    } as $raw_input
  
    db.patch edutrack {
      field_name = "id"
      field_value = $input.edutrack_id
      data = `$input|pick:($raw_input|keys)`|filter_null|filter_empty_text
    } as $edutrack
  }

  response = $edutrack
}