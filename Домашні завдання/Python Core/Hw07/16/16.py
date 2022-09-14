def decode(data):
    if not data:
        return []
    if len(data) == 2:
        return list(data[0]*data[1])
    return list(data[0]*data[1]) + decode(data[2:])
