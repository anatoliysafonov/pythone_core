from handlers import parse_string

COMMAND_NOT_FOUND = "ā command not valid ā"
EXIT              = "-- Good by! --"
INPUT             = 'Input command ā¶ : '
START_MESSAGE     = '\nš Hi. Type "help" for some help. Be sure that terminal has enoght width length'


def main():
    print(START_MESSAGE)
    while True:

        command_line = input(INPUT)
        func, arguments = parse_string(command_line)

        if not func:
            print(COMMAND_NOT_FOUND)
            continue

        if not arguments: text = func()
        else: text = func(*arguments)
        
        if text:
            print(text)

        if text == EXIT:
            break


if __name__ == '__main__':
    main()
