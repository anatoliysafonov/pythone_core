def encode(data):
    if not data:
        return []
    if len(data) == 1:
        return [data[0], 1]
    lst = encode(data[1:])
    if data[0] == lst[0]:
        lst[1] += 1
    else:
        lst = [data[0], 1]+lst
    return lst
