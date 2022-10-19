from decorator import input_error
from os import system as _system
import pickle
import message 
import data
import re

PHONEBOOK = data.AdressBook()

NEW_LINE = '\n'
SEPARATOR = ', '
LINE = '+'+'-'*20+'+'+'-'*50+'+'+'-'*20+"+"
HEADER = '{}|{:^20}|{:^50}|{:^20}|{}'.format(LINE+'\n','N A M E', 'P H O N E S', 'B I R T H D A Y','\n'+LINE)

def is_date(date):
    resault = re.search(r'^\d{2}/\d{2}/\d{4}$', str(date))
    return resault is not None

def is_phone(phone):
    result = re.search(r'^\d{10}$', phone)
    return result is not None

def table_build (records:list) ->str:
    string = HEADER
    for record in records:
        current_record = PHONEBOOK[record]
        string += NEW_LINE + str(current_record) + NEW_LINE + LINE
    return string


def footer_build(start:int, end:int, page:int,total:int)->str:
    if total == page:
        right = ''
    else:
        right = 'page {} from {}'.format(page, total)
    if start == end:
        left = '{}th record'.format(end)
    else:    
        left = '1 ◀ {}..{} ▶ {} (records)'.format(start, end, len(PHONEBOOK))
    
    footer = '{}{:>15}'.format(left, right)
    return NEW_LINE + footer

@input_error
def add(*args ) -> str:
    """  Adds a new entry to the phonebook """
    if not args     : raise IndexError(message.ENTER_NAME_USER)
    if len(args) < 2: raise IndexError(message.ENTER_PHONE_NUMBER)
    if len(args) > 3: raise IndexError(message.TOO_MUCH_ARGS)
    user_name, number, *birthday = args
    record = data.Record(user_name, number, *birthday)
    return PHONEBOOK + record



@input_error
def change(*args) -> str:
    """ Changes the phone number of an existing entry in the phone book """
    
    if not args or len(args) < 3: raise IndexError(message.NAME_NUMBER_NOT_CORRECT)
    user, old, new, *_ = args
    if user not in PHONEBOOK: raise ValueError(message.CONTACT_NOT_FOUND)
    record = PHONEBOOK.data[user]
    return record.change(user, old, new)


@input_error
def delete(*args) -> str:
    """ Delete the phone number of an existing entry in the phone book """

    if not args or len(args) < 2: raise IndexError(message.ENTER_NAME_NUMBER)
    user_name, number, *_ = args
    record = PHONEBOOK.data[user_name]
    return record.delete(number)



@input_error
def contact_delete(*args):
    """ Delete entire record from phonebook """

    if not args: raise ValueError(message.ENTER_NAME_NUMBER)
    user, *_ = args
    result =  PHONEBOOK - user
    data.AdressBook.total_records -= 1
    return result




@input_error
def name(*args) -> str:
    """ Searches for a record by phone number or by date of birth. Return name of contact : numbers """

    if not args: raise IndexError(message.NUMBER_NOT_FOUND)
    return_message = message.CONTACT_NOT_FOUND
    string, *_ = args
    records = []
    if is_phone(string):
        for name, record in PHONEBOOK.data.items():
            phones = [item.value for item in record.phones]
            if string in phones:
                records.append(name)
        
    if is_date(string):
        for record in PHONEBOOK.values():
            if string == record.birthday.value:
                records.append(record.name.value)

    if not records: raise ValueError (message.CONTACT_NOT_FOUND)
    return_message = table_build(records)
    return return_message



@input_error
def phone(*args) -> str:
    """ Searches for a record by name and return  name : numbers """

    if not args: raise ValueError(message.ENTER_USER_NAME)
    user_name, *_ = args
    if user_name not in PHONEBOOK.data: raise KeyError(message.CONTACT_NOT_FOUND)
    message_out = table_build([user_name])
    return message_out



def hello(*args) -> str:
    """ print some text """
    return '-- How can I help you? --'


def show_all (*args):
    """
    Виводить в консоль усі записи в телефонній книзі
    Якщо книга велика, інформація виводиться меньшими порціями
    """
    MAX_SIZE = 5
    total_records = len(PHONEBOOK.data)
    keys = list(PHONEBOOK.data)
    pages = total_records // MAX_SIZE
    pages = pages if total_records % MAX_SIZE == 0 else pages + 1

    if not PHONEBOOK.data: 
        return message.PHONEBOOK_IS_EMPTY
    number_rows = total_records 
    if number_rows > MAX_SIZE:
        number_rows = MAX_SIZE
    generator = PHONEBOOK.iterator(number_rows, pages)
    current_page = 0
    for records in generator:
        current_page += 1
        start_index = keys.index(records[0]) +1
        stop_index  = keys.index(records[-1])+1
        table_string  = table_build(records)
        table_string += footer_build(start_index, stop_index,current_page, pages)
        print(table_string)
        if stop_index == total_records:
            break
        char = input('press "C" to escape or any key to continue : ')
        if char == 'c' or char == "C":
            break
    return message.DONE

@input_error
def find(*args):
    if not args:
        raise ValueError(message.FIND_ARG_NOT_VALID)
    value, *_ = args
    finded_users = []
    table = None
    for user in PHONEBOOK.data.values():
        name = user.name.value
        phones = ', '.join([ phone.value for phone in user.phones])
        if user.birthday:
            bd = user.birthday.value
        else:
            bd = '--'
        if value in name or value in phones or value in bd:
            finded_users.append(name)
    if finded_users:
        table = table_build(finded_users)
    return table


def stop(*args) -> str:
    """ exit script """
    if PHONEBOOK:
        with open (message.FILE_NAME, 'wb') as fh:
            pickle.dump(PHONEBOOK.data, fh)
    return '-- Good by! --'



@input_error
def set_birthday(*args):
    if not args or len(args) < 2:
        raise ValueError (message.VALID_DATA)
    name , date, *_ = args
    if name in PHONEBOOK.data:
        PHONEBOOK.data[name].birthday = date
    else:
        return message.CONTACT_NOT_FOUND
    return message.DONE


@input_error
def days(*args):
    if not args:
        raise ValueError(message.CONTACT_NOT_FOUND)
    name, *_ = args
    if name not in PHONEBOOK:
        raise ValueError(message.CONTACT_NOT_FOUND)  
    return 'To next birthday(days):{}'.format(PHONEBOOK[name].days())
    


def console_clear(*args):
    """ clear consol """
    _system('clear')
    return ''
    


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
    'cls': console_clear,
    'birthday': phone,
    'set birthday': set_birthday,
    'days':days,
    'find': find,
}


def parse_string(command: str) -> tuple:

    func = None
    arguments = None 
    command = command.strip()
    command_lower = command.lower().strip()
    for comm in FUNCTIONS:
        if command_lower.startswith(comm.lower()):
            arguments = command.replace(comm, '')
            if arguments and arguments[0] != ' ':
                first_space = arguments.find(' ')
                arguments = arguments[first_space:]
            func = FUNCTIONS[comm]
            if func is None:
                func = FUNCTIONS['find']
                arguments = [command]
            else:
                arguments = arguments.strip().split()
            break
    if func is None:
         func = FUNCTIONS['find']
         arguments = [command]
    return func, arguments
