from decorator import input_error
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
        left = '1 ◀ {}..{} ▶ {} records'.format(start, end, len(PHONEBOOK))
    
    footer = '{} {:>15}'.format(left, right)
    return NEW_LINE + footer

@input_error
def add(*args ) -> str:
    """  Adds a new entry to the phonebook """

    if not args     : raise IndexError(data.ENTER_NAME_NUMBER)
    if len(args) < 2: raise IndexError(data.NUMBER_NOT_FOUND)

    user_name, number, *birthday = args
    record = data.Record(user_name, number, *birthday)
    return PHONEBOOK.add_record(record)



@input_error
def change(*args) -> str:
    """ Changes the phone number of an existing entry in the phone book """
    
    if not args or len(args) < 3: raise IndexError(data.NAME_NUMBER_NOT_CORRECT)
    user_name, old_number, new_number, *_ = args
    try:
        record = PHONEBOOK.data[user_name]
    except KeyError:
        raise KeyError(data.CONTACT_NOT_FOUND)
    else:
        return record.change_number(user_name, old_number, new_number)



@input_error
def delete(*args) -> str:
    """ Delete the phone number of an existing entry in the phone book """

    if not args or len(args) < 2: raise IndexError(data.ENTER_NAME_NUMBER)
    user_name, number, *_ = args
    record = PHONEBOOK.data[user_name]
    return record.delete_number(number)



@input_error
def contact_delete(*args):
    """ Delete entire record from phonebook """

    if not args: raise ValueError(data.ENTER_NAME_NUMBER)
    user_name, *_ = args
    result =  PHONEBOOK.del_record(user_name)
    data.AdressBook.total_records -= 1
    return result




@input_error
def name(*args) -> str:
    """ Searches for a record by phone number or by date of birth. Return name of contact : numbers """

    if not args: raise IndexError(data.NUMBER_NOT_FOUND)
    return_message = data.CONTACT_NOT_FOUND
    string, *_ = args
    if is_phone(string):
        records = []
        for name, record in PHONEBOOK.data.items():
            phones = [item.value for item in record.phones]
            if string in phones:
                records.append(name)
        return_message = table_build(records)
        
    if is_date(string):
        records = []
        for record in PHONEBOOK.values():
            if string == record.birthday.value:
                records.append(record.name.value)
        return_message = table_build(records)
    return return_message



@input_error
def phone(*args) -> str:
    """ Searches for a record by name and return  name : numbers """

    if not args: raise IndexError('-- Enter a name  to search --')
    user_name, *_ = args
    if user_name not in PHONEBOOK.data: raise KeyError(data.CONTACT_NOT_FOUND)
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
    MAX_SIZE = 3
    total_records = len(PHONEBOOK)
    list_of_keys = list(PHONEBOOK)
    pages = total_records // MAX_SIZE
    pages = pages if total_records % MAX_SIZE == 0 else pages + 1

    if not PHONEBOOK.data: 
        return data.PHONEBOOK_IS_EMPTY
    number_rows = total_records 
    if number_rows > MAX_SIZE:
        number_rows = MAX_SIZE
    generator = PHONEBOOK.iterator(number_rows, pages)
    current_page = 0
    for records in generator:
        current_page += 1
        start_index = list_of_keys.index(records[0]) +1
        stop_index  = list_of_keys.index(records[-1])+1
        table_string  = table_build(records)
        table_string += footer_build(start_index, stop_index,current_page, pages)
        print(table_string)
        if stop_index == total_records:
            break
        char = input('press "C" to escape or any key to continue : ')
        if char == 'c' or char == "C":
            break
    return NEW_LINE


def stop(*args) -> str:
    """ exit script """
    return '-- Good by! --'


def out_help(*args):
    """ Print out the help message """
    message_out = ''
    hearder = '{}{:^20}{:^39}{:^62}{}'.format(NEW_LINE, data.MESSAGE_DATA[0][0],data.MESSAGE_DATA[0][1],data.MESSAGE_DATA[0][2],NEW_LINE)
    line = '-'*126 + NEW_LINE
    message_out = hearder + line
    for i in range(1, len(data.MESSAGE_DATA)):
        string = '{:·<20} ➜ {:·^40} ➜ {:·<60}{}'.format(data.MESSAGE_DATA[i][0],data.MESSAGE_DATA[i][1],data.MESSAGE_DATA[i][2],NEW_LINE)
        message_out += string
    return message_out


@input_error
def set_birthday(*args):
    if not args or len(args) < 2:
        raise ValueError ('-- Input name and date to set birthday -- ')
    name , date, *_ = args
    if name in PHONEBOOK.data:
        PHONEBOOK.data[name].set_birthday(date)
    else:
        return data.CONTACT_NOT_FOUND 
    return "... Done ..."


@input_error
def days_to_birthday(*args):
    if not args:
        raise ValueError(data.CONTACT_NOT_FOUND)
    name, *_ = args
    if name not in PHONEBOOK:
        raise ValueError(data.CONTACT_NOT_FOUND)  
    return 'To next birthday(days):{}'.format(PHONEBOOK[name].days_to_birthday())
    


def console_clear(*args):
    """ clear consol """
    data.start_message()


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
    'cls': console_clear,
    'birthday': phone,
    'set birthday': set_birthday,
    'days':days_to_birthday,
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
            arguments = arguments.strip().split()
            break
    return func, arguments
