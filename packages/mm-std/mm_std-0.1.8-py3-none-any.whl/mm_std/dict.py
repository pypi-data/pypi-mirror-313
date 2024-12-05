def replace_empty_values(data: dict[object, object], defaults: dict[object, object]) -> None:
    for k, v in defaults.items():
        if not data.get(k):
            data[k] = v
