from decorator import input_error
from os import system as _system
import data


PHONEBOOK = data.AdressBook()
NEW_LINE = '\n'
SEPARATOR = ', '


@input_error
def add(*args ) -> str:
    """  Adds a new entry to the phonebook """

    if not args     : raise IndexError(data.ENTER_NAME_NUMBER)
    if len(args) < 2: raise IndexError(data.NUMBER_NOT_FOUND)

    user_name, *numbers = args
    record = data.Record(user_name, numbers)
    return PHONEBOOK.add_record(record)



@input_error
def change(*args) -> str:
    """ Changes the phone number of an existing entry in the phone book """
    
    if not args or len(args) < 3: raise IndexError(data.NAME_NUMBER_NOT_CORRECT)
    user_name, old_number, new_number = args
    try:
        record = PHONEBOOK.data[user_name]
    except KeyError:
        raise KeyError(data.CONTACT_NOT_FOUND)
    else:
        return record.change_number(user_name, old_number, new_number)



@input_error
def delete(*args) -> str:
    """ Delete the phone number of an existing entry in the phone book """

    if not args: raise IndexError(data.ENTER_NAME_NUMBER)
    user_name, *numbers = args
    record = PHONEBOOK.data[user_name]
    return record.delete_number(numbers)



@input_error
def contact_delete(*args):
    """ Delete entire record from phonebook """

    if not args: raise ValueError(data.ENTER_NAME_NUMBER)
    user_name, *_ = args
    return PHONEBOOK.del_record(user_name)



@input_error
def name(*args) -> str:
    """ Searches for a record by phone number. Return name of contact : numbers """

    if not args: raise IndexError(data.NUMBER_NOT_FOUND)
    return_message = data.CONTACT_NOT_FOUND
    number, *_ = args
    for name, record in PHONEBOOK.data.items():
        phones = [item.value for item in record.phones]
        if number in phones:
            print (f'{name} : {SEPARATOR.join(phones)}')
            return_message = '... Done ...'
    
    return return_message



@input_error
def phone(*args) -> str:
    """ Searches for a record by name and return  name : numbers """
    if not args: raise IndexError('-- Enter a name  to search --')
    user_name, *_ = args
    if user_name not in PHONEBOOK.data: raise KeyError(data.CONTACT_NOT_FOUND)
    record = PHONEBOOK.data[user_name]
    return record.out_info()



def hello() -> str:
    """ print some text """
    return '-- How can I help you? --'


def show_all() -> str:
    """ prints all entries in the phone book """
    if not PHONEBOOK.data: return data.PHONEBOOK_IS_EMPTY
    for key, value in PHONEBOOK.data.items():
        string = SEPARATOR.join(
            [phone.value for phone in value.get_numbers()])
        print(f'{key} : {string}')
    print(f'total contacts : {PHONEBOOK.total_records}')


def stop() -> str:
    """ exit script """
    return '-- Good by! --'


def out_help():
    """ Print out the help message """
    print(NEW_LINE)
    print('{:^20}{:^39}{:^60}'.format(
        data.MESSAGE_DATA[0][0], data.MESSAGE_DATA[0][1], data.MESSAGE_DATA[0][2]))
    print('{:-^128}'.format(''))
    for i in range(1, len(data.MESSAGE_DATA)):
        string = '{:>20} {:.<39} -> {:<60}'.format(
            data.MESSAGE_DATA[i][0], data.MESSAGE_DATA[i][1], data.MESSAGE_DATA[i][2])
        print(string)
    print(NEW_LINE)


def console_clear():
    """ clear consol """
    _system('clear')


FUNCTIONS = {
    'add': add,
    'change': change,
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
