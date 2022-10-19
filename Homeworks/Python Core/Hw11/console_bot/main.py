import handlers
from handlers import parse_string, PHONEBOOK
from message import INPUT, COMMAND_NOT_FOUND, EXIT
import data



def main():
    data.start_message()
    while True:
        command_line = input(INPUT)
        func, arguments = parse_string(command_line)

        if not arguments: text = func()
        else: text = func(*arguments)
        
        if text:
            print(text)
        elif text is None:
            print(COMMAND_NOT_FOUND)

        if text == EXIT:
            PHONEBOOK.save()
            break


if __name__ == '__main__':
    main()
