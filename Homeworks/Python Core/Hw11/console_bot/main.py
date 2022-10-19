import handlers
from message import INPUT, COMMAND_NOT_FOUND, EXIT
import data



def main():
    data.start_message()
    while True:
        command_line = input(INPUT)
        func, arguments = handlers.parse_string(command_line)
        # if not func:
        #     print(COMMAND_NOT_FOUND)
        #     continue

        if not arguments: text = func()
        else: text = func(*arguments)
        
        if text:
            print(text)
        elif text is None:
            print(COMMAND_NOT_FOUND)

        if text == EXIT:
            
            break


if __name__ == '__main__':
    main()
