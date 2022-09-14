def make_request(keys, values):
    json = {}
    if len(keys) != len(values):
        return json
    for k, v in zip(keys, values):
        json[k] = v
    return json
