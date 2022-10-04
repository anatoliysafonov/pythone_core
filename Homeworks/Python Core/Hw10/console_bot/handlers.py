from decorator import input_error
from classes import AdressBook, MESSAGE_HELP
from os import system as _system


PHONEBOOK = AdressBook()
NEW_LINE  = '\n'
SEPARATOR = ', '

@input_error
def add(args: list = None) -> str:
    """
    Adds a new entry to the phonebook
    :param args:
    :return:
    """
    if not args:
        raise IndexError(f"-- Enter the user's name and phone number --")
    if len(args) < 2:
        raise IndexError(f'-- You have not entered a phone number --')
    user_name, *number = args
    return PHONEBOOK.add_record(user_name, number)


@input_error
def change(*args) -> str:
    """
    Changes the phone number of an existing entry in the phone book
    :param args:
    :return:
    """
    if not args or len(args[0]) < 3:
        raise IndexError(
            "-- The name and also the phone number are not correct --")
    user_name, old_number, new_number = args[0]
    try:
        record = PHONEBOOK.data[user_name]
    except KeyError:
        raise KeyError('-- User not found --')
    else:
        return record.change_number(user_name, old_number, new_number)


@input_error
def delete(*args) -> str:
    if not args:
        raise IndexError(
            f"-- Enter the user's name and phone number to delete --")
    user_name, *numbers = args[0]
    record = PHONEBOOK.data[user_name]
    return record.delete_number(numbers)


@input_error
def contact_delete(*args):
    user_name = args[0][0]
    return PHONEBOOK.del_record(user_name)


@input_error
def name(*args) -> str:
    """
    Searches for a record by phone number. Return name of contact : numbers
    :param args:
    :return:
    """
    if not args:
        raise IndexError('-- Enter a phone number to search --')
    number = args[0][0]
    for name, record in PHONEBOOK.data.items():
        phones = [item.value for item in record.phones]
        if number in phones:
            return f'{name} : {SEPARATOR.join(phones)}'
    return f'-- Contact not fount --'


@input_error
def phone(*args) -> str:
    """
    Searches for a record by name and return  name : numbers
    :param args:
    :return:
    """
    if not args:
        raise IndexError('-- Enter a name  to search --')
    user_name = args[0][0]
    if user_name not in PHONEBOOK.data:
        raise KeyError(f'-- User {user_name} non exists in phonebook --')
    record = PHONEBOOK.data[user_name]
    return record.out_info()


def hello() -> str:
    """
    print some text
    :return:
    """
    return '-- How can I help you? --'


def show_all() -> str:
    """
    prints all entries in the phone book
    :return:
    """
    string = ''
    if not PHONEBOOK.data:
        return '-- PhoneBook is empty. Add some contact --'
    print(NEW_LINE)
    for key, value in PHONEBOOK.data.items():
        numbers = SEPARATOR.join([item.value for item in value.show_numbers()])
        print(f'{key} : {numbers}')
    print(f'-- Total records: {len(PHONEBOOK)} --')
    return string[:-1]


def stop() -> str:
    """
    exit script
    :return:
    """
    return '-- Good by! --'


def out_help():
    print(MESSAGE_HELP)


def console_clear():
    _system('clear')


FUNCTIONS = {
    'add': add,
    'change ': change,
    'delete': delete,
    'contact delete': contact_delete,
    'name': name,
    'phone': phone,
    'hello': hello,
    'show all': show_all,
    'close': stop,
    'exit': stop,
    'good by': stop,
    'help': out_help,
    'cls': console_clear
}


def parse_string(string: str) -> tuple:

    func = None
    args = None

    strings = string.strip()
    strings_lower = string.strip().lower()

    for key in FUNCTIONS:
        if strings_lower.startswith(key):
            func = key
            args = strings.replace(strings[:len(key)], '').strip().split()
            return FUNCTIONS[func], args
    return func, args
