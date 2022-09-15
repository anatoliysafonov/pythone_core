def to_indexed(source_file, output_file):
    with open(source_file, 'r') as file:
        data = file.readlines()
    print(data)
    with open(output_file, 'w') as file:
        for num, st in enumerate(data):
            file.write(': '.join((str(num), st)))
