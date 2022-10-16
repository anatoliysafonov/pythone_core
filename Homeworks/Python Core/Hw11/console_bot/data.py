from collections import UserDict
from datetime import datetime
from os import system as _system
import warnings
import re


def start_message():
    _system('clear')
    print(warnings.LOGO)
    print(warnings.START_MESSAGE)


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
        MAX_LENGTH = 10
        if new_value[0].isdigit() or len(new_value) > MAX_LENGTH:
            raise ValueError(warnings.INVALID_DATA)
        self._value = new_value


class Birthday(Field):


    @Field.value.setter
    def value (self, new_value) -> None:
        try:
            datetime.strptime(new_value, '%d/%m/%Y')
        except ValueError:
            raise ValueError(warnings.INVALID_DATA)
        self._value = new_value



class Record:
    """ class Record  """
    def __init__(self, name: str, phone:str, birthday:str = None) -> None:
        self.name = Name(name)
        self.phones = [Phone(phone)]
        self._birthday = None
        if birthday:
            self.birthday = birthday

    @property
    def birthday(self)->str:
        """Повертаємо дату народження i якщо її немає, то повертаємо None """
        if self._birthday: 
            return self._birthday
        else: 
            return None 
        

    @birthday.setter
    def birthday(self, date:str) -> None:
        """встановлюємо дату народження i якщо дата ще не встановлена, то ми добавляємо її в даний запис якщо дата є, то ми її міняємо """
        date = Birthday(date)
        if date:
            self._birthday = date
        else:
            self._birthday = None
        return warnings.DONE

    


    def __add__(self, phone) -> str:
        """ добавляє новий номсер телефона якщо його немає в списку """
        if phone in self.phones: raise ValueError(warnings.NUMBER_EXISTS)
        self.phones.append(phone)
        return warnings.DONE

    def __sub__(self,phone):
        if phone not in self.phones: raise ValueError(warnings.CONTANT_NOT_FOUND)
        self.phones.remove(phone)

    def change(self, name: str, old: str, new: str) -> str:
        """ міняє номер існуючого контакту з існуючим номером на новий номер """
        old = Phone(old)
        new = Phone(new)
        self - old
        self + new
        return warnings.DONE
        

    def days(self) -> int:
        """ Повертає кількість днів до дня нарожддення """
        if self.birthday is None: raise ValueError(warnings.BIRTHDAY_NOT_SET)
        day, mouth, _ = self.birthday.value.split('/')
        now = datetime.now()
        this_year = datetime(day=int(day), month=int(mouth), year=int(now.year))
        return (this_year - now).days

    def delete(self, phone: str) -> str:
        """ Видаляємо новий телефона з контакту в телефонній книзі """
        phone = Phone(phone)
        self - phone
        return '...Done...'
    
    def __str__(self) ->str:
        """
        повертає в строковій формі інформацію про запис
        """
        name = self.name.value
        phones = warnings.SEPARATOR.join([phone.value for phone in self.phones])
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

    def __add__(self, record: Record) -> str:
        """ Додаємо нову запис чи додоткові телефони до телефонної книги """
        user = record.name.value
        if user not in self:
            self.data[user] = record
            AdressBook.total_records += 1
        else:
            phone, = record.phones
            result = self.data[user].phones.append(phone)
        return warnings.DONE


    def __sub__(self, name: str) -> str:
        """
        видаляємо контакт за імʼям за телефонної книги
        """
        try:
            self.pop(name)
        except KeyError:
            return (warnings.CONTACT_NOT_FOUND)
        else:
            return warnings.CONTACT_DELETED


    def __len__(self):
        """ Повертаємо кількість записів в телефонній книзі"""
        return AdressBook.total_records


    def iterator(self, num, pages):
        
        list_of_keys = list(self)
        for i in range(pages):
            yield list_of_keys[i*num: i*num + num]



