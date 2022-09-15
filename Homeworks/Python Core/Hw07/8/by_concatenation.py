def token_parser(s):
    OPERANDS = '+-*/()'
    output = []
    digit = ''
    if s == '':
        return output
    for char in s:
        if char.isdigit():
            digit += char
            continue
        if char in OPERANDS:
            if digit:
                output.append(digit)
                digit = ''
            output.append(char)
    output.append(digit)
    return output
