def value_by_key_prefix(d: dict, partial: str):
    matches = [val for key, val in d.items() if key.startswith(partial)]
    if not matches:
        raise KeyError(partial)
    if len(matches) > 1:
        raise ValueError(f"{partial} matches more than one key")
    return matches[0]
