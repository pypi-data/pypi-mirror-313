def build_alias_map(response_class: type) -> dict:
    return {field: field for field in response_class.__fields__.keys()}
