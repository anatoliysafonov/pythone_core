from collections import UserDict
from datetime import datetime
from os import system as _system
import re

COMMAND_NOT_FOUND       = "❗ command not valid ❗"
EXIT                    = "-- Good by! --"
INPUT                   = 'Input command ▶ : '
START_MESSAGE           = '👋 Hi. Type "help" for some help. Be sure that terminal has enoght width length'
SEPARATOR               = ', '
CONTACT_NOT_FOUND       = '-- ❗ Contact not found --'
NUMBER_NOT_FOUND        = '-- ❗ Number not found --'
PHONEBOOK_IS_EMPTY      = '-- ❗ PhoneBook is empty. Add some contact --'
NAME_NUMBER_NOT_CORRECT = '-- ❗ The name and the phone number are not correct --'
ENTER_NAME_NUMBER       = "-- ❗ Enter the user's name and phone --"
MESSAGE_DATA            = [['C O M M A N D', 'A R G U M E N T S', 'A C T I O N'],
                           ['add', '[name][phone(1)][phone(2)]...[phone(N)]',
                           'create / add contact with phone numbers'],
                           ['change', '[name][old_phone][new_phone]',
                           "change contact's old phone number wuth new phone numbers"],
                           ['delete', '[name][phone(1)][phone(2)]...[phone(N)]',
                           "delete contact's phone number"],
                           ['name', '[phone_number] or [date of birth]', 'search contact by[phone_number] or by [date of birth]'],
                           ['phone', '[name]', "search phone number by contact's[name]"],
                           ['show all', '', 'display all contact in adressbook'],
                           ['contact delete', '[name]',
                           'delete contact with [name]from adressbook'],
                           ['birthday','[name]',"display contact's birthday"],
                           ['set birthday','[name] [date]',"change/set contact's birthday"],
                           ['days', '[name]',"print out days to the next contact's birthdate"],
                           ['cls', '', 'clear console'],
                           ['exit,close,good by', '', 'exit script']]


TITLE = """
 ######   #     #  #######  #     #  #######  ######   #######  #######  #    # 
 #     #  #     #  #     #  ##    #  #        #     #  #     #  #     #  #   #  
 #     #  #     #  #     #  # #   #  #        #     #  #     #  #     #  #  #   
 ######   #######  #     #  #  #  #  #####    ######   #     #  #     #  ###    
 #        #     #  #     #  #   # #  #        #     #  #     #  #     #  #  #   
 #        #     #  #     #  #    ##  #        #     #  #     #  #     #  #   #  
 #        #     #  #######  #     #  #######  ######   #######  #######  #    # 
                                                                                
"""
def start_message():
    _system('clear')
    print(TITLE)
    print(START_MESSAGE)


class Field:
    """ class Field """
    def __init__(self, value):
        self._value = None
        self.value = value

    @property
    def value (self) ->None:
        return self._value

    @value.setter
    def value(self, new_value:str) ->str:
        pass



class Phone(Field):
    """ class Phone """

    @Field.value.setter
    def value(self, new_value:str) -> None:
        normalize_new_value = re.sub(r'\(|\)|\.|,|-', '',new_value)
        if not normalize_new_value.isdigit() or len(normalize_new_value) != 10:
            raise ValueError('-- ❗ Phone number is invalid. Number cant containts "(", ")", "-", and have 10 digit\'s length--')
        self._value = normalize_new_value

    def __eq__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return self.value == other.value



class Name (Field):
    """ class Name """

    @Field.value.setter
    def value(self, new_value:str) -> None:
        if new_value[0].isdigit() or len(new_value) > 10:
            raise ValueError('-- ❗ Name format is invalid. Name must starts with letter and lenght must be less or equal 10 --')
        self._value = new_value


class Birthday(Field):


    @Field.value.setter
    def value (self, new_value) -> None:
        try:
            datetime.strptime(new_value, '%d/%m/%Y')
        except ValueError:
            raise ValueError("-- ❗ Incorrect data format, should be DD/MM/YYYY --")
        self._value = new_value



class Record:
    """ class Record  """
    def __init__(self, name: str, phone:str, birthday:str = None) -> None:
        if not name: raise ValueError(CONTACT_NOT_FOUND)
        self.name = Name(name)
        self.phones = [Phone(phone)]
        if birthday:
            self.birthday = Birthday(birthday)
        else:
            self.birthday = None


    def add_number(self, number) -> str:
        """ добавляє новий номсер телефона якщо його немає в списку """
        
        if number not in self.phones:
            self.phones.append(number)
        else:
            return (f'-- ❗ Phone number {number.value} exists already --')
        return '... Done ...'



    def change_number(self, name: str, old_number: str, new_number: str) -> str:
        """ міняє номер існуючого контакту з існуючим номером на новий номер """
        old_number = Phone(old_number)
        new_number = Phone(new_number)
        is_founded = False
        if old_number in self.phones:
            index = self.phones.index(old_number)
            self.phones[index] = new_number
            is_founded = True
        if not is_founded: raise ValueError(NUMBER_NOT_FOUND)
        return '... Changed ...'
        



    def out_info(self) -> str:
        """ Повертає інформацію про всі номера данного запису """
        numbers = [item.value for item in self.phones]
        numbers = SEPARATOR.join(numbers)
        return f'{self.name.value} : {numbers}'


    def get_numbers(self)->list:
        """ повертає список обʼєктів Phone """
        return self.phones


    def get_birthday(self)->str:
        """
        повертаємо дату народження
        якщо її немає, то повертаємо None
        """
        if self.birthday:
            return self.birthday.value
        else:
            return self.birthday


    def set_birthday(self, date:str) -> None:
        """
        встановлюємо дату народження
        якщо дата ще не встановлена, то ми добавляємо її в даний запис
        якщо дата є, то ми її міняємо 
        """
        if self.birthday:
            self.birthday.value = date
        else:
            self.birthday = Birthday(date)
        
    def days_to_birthday (self) -> int:
        """
        Повертає кількість днів до дня нарожддення
        """
        if self.birthday is None:
            raise ValueError('--❗ birthay is not set -- Try "set birthay" to set the date of birth')
        day, mouth, _ = self.birthday.value.split('/')
        now = datetime.now()
        birthday_this_year = datetime(day=int(day), month=int(mouth), year=int(now.year))
        return (birthday_this_year - now).days


    def delete_number(self, number: str) -> str:
        """
        Видаляємо новий телефона з контакту в телефонній книзі
        """
        is_deleted = False
        number = Phone(number)
        for phone in self.phones:
            if number == phone:
                self.phones.remove(phone)
                is_deleted = True
        if is_deleted:
            return '... Deleted ...'
        raise ValueError(NUMBER_NOT_FOUND)
    
    def __str__(self) ->str:
        """
        повертає в строковій формі інформацію про запис
        """
        name = self.name.value
        phones = SEPARATOR.join([phone.value for phone in self.phones])
        if self.birthday:
            birthday = self.birthday.value 
        else:
            birthday = '--'
        return '|{:^20}|{:^50}|{:^20}|'.format(name, phones, birthday)


class AdressBook(UserDict):
    """
    клас якмй відповідає за телефонну книгу
    """
    total_records = 0

    def add_record(self, record: Record) -> str:
        """ 
        Додаємо нову запис чи додоткові телефони до телефонної книги
        """
        result = '... Done ...'
        contact_name = record.name.value
        if contact_name not in self:
            #якщо в телефоній книзі немає контакн з іменем contact_name, то додаємо новий контакт
            self.data[contact_name] = record
            AdressBook.total_records += 1
        else:
            #якщо такий контакт вже є, то додаємо новий номер number_to_add до наявного контакку
            contact_name = record.name.value
            number_to_add, = record.phones
            result = self.data[contact_name].add_number(number_to_add)
        return result


    def del_record(self, name: str) -> str:
        """
        видаляємо контакт за імʼям за телефонної книги
        """
        try:
            self.pop(name)
        except KeyError:
            return (CONTACT_NOT_FOUND)
        else:
            print(f'... contact {name} deleted ...')


    def __len__(self):
        """ Повертаємо кількість записів в телефонній книзі"""
        return AdressBook.total_records


    def iterator(self, num, pages):
        
        list_of_keys = list(self)
        for i in range(pages):
            yield list_of_keys[i*num: i*num + num]




