def token_parser(s):
    import re
    s = s.replace(' ', '')
    results = re.finditer(r'((\(|\)|\*|\/|\+|\-){1})|(\d+)', s)
    return ([item[0] for item in results])
