def map_dict(data: dict, key_func, value_func):
    """
    Apply key_func to keys, value_func to values.
    Return a new dictionary.
    """
    if not isinstance(data, dict):
        raise TypeError("Expected a dictionary.")

    return {key_func(k): value_func(v) for k, v in data.items()}
