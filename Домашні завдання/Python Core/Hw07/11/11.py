def sequence_buttons(string):
    BUTTONS = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    SYMBOLS = ['.,?!:', 'ABC', 'DEF', 'GHI',
               'JKL', 'MNO', 'PQRS', 'TUV', 'WXYZ', ' ']
    output = ''
    string = string.upper()
    dict = list(zip(BUTTONS, SYMBOLS))
    for char in string:
        for k, v in dict:
            if char in v:
                output += k*(v.index(char)+1)
    return output
