from decorator import input_error
import data
import re


PHONEBOOK = data.AdressBook()
NEW_LINE = '\n'
SEPARATOR = ', '
LINE = '+'+'-'*20+'+'+'-'*50+'+'+'-'*17+"+"
HEADER = '{}|{:^20}|{:^50}|{:^17}|{}'.format(LINE+'\n','N A M E', 'P H O N E S', 'B I R T H D A Y','\n'+LINE)

def is_date(date):
    resault = re.search(r'^\d{2}/\d{2}/\d{4}$', str(date))
    return resault != None

def is_phone(phone):
    result = re.search(r'^\d{10}$', phone)
    return result != None


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
        for name, record in PHONEBOOK.data.items():
            phones = [item.value for item in record.phones]
            if string in phones:
                print (f'{name} : {SEPARATOR.join(phones)}')
                return_message = '... Done ...'
    if is_date(string):
        for record in PHONEBOOK.values():
            if string == record.birthday.value:
                print (f'{record.name.value} : {string}')
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


def show_all ():
    """
    Виводить в консоль усі записи в телефонній книзі
    Якщо книга велика, інформація виводиться меньшими порціями
    """
    MAX_SIZE = 5
    if not PHONEBOOK.data: 
        return data.PHONEBOOK_IS_EMPTY
    size = number_rows = len(PHONEBOOK)
    if number_rows > MAX_SIZE:
        while True:
            try:
                print('PHONEBOOK ➜ {} records'.format(len(PHONEBOOK)))
                number_rows = int(input('PhobeBook is too large. Enter number of rows to output: '))
            except ValueError:    
                print('Must be a number!!!')
            else:
                if number_rows > len(PHONEBOOK):
                    continue
                break
    list_of_keys = list(PHONEBOOK)
    rene = PHONEBOOK.iterator(number_rows)
    for records in rene:
        print(HEADER)
        for record in records:
            current_record = PHONEBOOK[record]
            print(current_record)
            print(LINE)
        start_index = list_of_keys.index(records[0]) +1
        stop_index  = list_of_keys.index(records[-1])+1
        print('◀ {}..{} ▶ from {} records'.format(start_index, stop_index, len(PHONEBOOK)))
        if stop_index == size:
            break
        char = input('press "C" to escape or any key to continue : ')
        if char == 'c' or char == "C":
            break
    return "... Done ..."


def stop() -> str:
    """ exit script """
    return '-- Good by! --'


def out_help():
    """ Print out the help message """
    print(NEW_LINE)
    print('{:^20}{:^39}{:^62}'.format(
        data.MESSAGE_DATA[0][0], data.MESSAGE_DATA[0][1], data.MESSAGE_DATA[0][2]))
    print('{:-^130}'.format(''))
    for i in range(1, len(data.MESSAGE_DATA)):
        string = '{:·<20} ➜ {:·^40} ➜ {:·<60}'.format(
            data.MESSAGE_DATA[i][0], data.MESSAGE_DATA[i][1], data.MESSAGE_DATA[i][2])
        print(string)
    print(NEW_LINE)



@input_error
def show_birthday(*args):
    if not args:
        raise ValueError ('-- Input name show birthday -- ')
    name , *_ = args
    date = (PHONEBOOK.data[name].get_birthday())
    if not date:
        return '-- Birthday is not set. To set birthday select "set birthday" --'
    else:
        return '{} : {}'.format(name, date)


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
    
    print('To next birthday(days): {}'.format(PHONEBOOK[name].days_to_birthday()))
    


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
    'birthday': show_birthday,
    'set birthday': set_birthday,
    'days':days_to_birthday,
    #'show count':show
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
