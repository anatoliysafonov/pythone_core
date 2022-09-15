def get_employees_by_profession(path, profession):
    read_data = None
    output_data = []
    with open(path, 'r') as file:
        read_data = file.readlines()
    for item in range(len(read_data)):
        if read_data[item].find(profession) != -1:
            name = read_data[item].replace(profession, '')[:-1].strip()
            output_data.append(name)ß
    return ' '.join(output_data)
