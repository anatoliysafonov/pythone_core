def all_sub_lists(data):
    output = [[]]
    for i in range(len(data)):
        for j in range(i+1, len(data)+1):
            output.append(data[i:j])
    return sorted(output, key=lambda x: len(x))
