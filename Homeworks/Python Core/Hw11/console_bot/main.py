from handlers import parse_string
import data



def main():
    data.start_message()
    while True:
        command_line = input(data.INPUT)
        func, arguments = parse_string(command_line)
        if not func:
            print(data.COMMAND_NOT_FOUND)
            continue

        if not arguments: text = func()
        else: text = func(*arguments)
        
        if text:
            print(text)

        if text == data.EXIT:
            break


if __name__ == '__main__':
    main()
