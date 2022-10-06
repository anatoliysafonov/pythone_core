from handlers import parse_string


def main():
    print('\n👋 Hi. Type "help" for some help. Be sure that terminal has enoght width length')
    while True:

        command_line = input('Input command ▶ : ')
        func, arguments = parse_string(command_line)

        if not func:
            print('❗ command not valid ❗')
            continue

        if not arguments:
            text = func()
        else:
            text = func(*arguments)
        if text:
            print(text)

        if text == '-- Good by! --':
            break


if __name__ == '__main__':
    main()
