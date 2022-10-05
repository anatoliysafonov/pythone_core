from collections import UserDict

SEPARATOR = ', '


class Field:
    """
    class Field.
    """
    pass


class Phone(Field):
    """
    class Phone
    """

    def __init__(self, value: str) -> None:
        self.value = value


class Name (Field):
    """
    class Name
    """

    def __init__(self, value) -> None:
        self.value = value


class Record:
    """
    class Record contains Name(Field), Phones(list), Email(list) 
    """

    def __init__(self, name: str, phones=[], emails=[]) -> None:
        if not name:
            raise ValueError("-- ❗ Must be contact's name --")
        self.name = Name(name)
        if phones:
            self.phones = [Phone(number) for number in phones]
        else:
            phones = []

    def _get_numbers(self) -> list:
        return self.phones

    def _get_emails(self):
        return self.emails

    def add_number(self, number) -> str:
        """
        добавляє новий номсер телефона якщо його немає в списку.
        """
        isexists = False
        numbers = [item.value for item in self.phones]
        for current_number in number:
            if current_number.value not in numbers:
                self.phones.append(current_number)
            else:
                print(
                    f'-- ❗ Phone number {current_number.value} exists already --')
                isexists = True
        return isexists

    def change_number(self, name: str, old_number: str, new_number: str) -> str:
        """
        міняє номер існуючого контакту з існуючим номером на новий номер
        """
        is_founded = False
        for current_phone in self._get_numbers():
            if current_phone.value == old_number:
                index = self.phones.index(current_phone)
                self.phones[index] = Phone(new_number)
                is_founded = True
        if not is_founded:
            raise ValueError('-- ❗ Number to change not exists --')
        return '✅ Changed...'

    def out_info(self) -> str:
        """
        Повертає інформацію про всі номера данного запису
        """
        numbers = [item.value for item in self.phones]
        numbers = SEPARATOR.join(numbers)
        return f'{self.name.value} : {numbers}'

    def show_numbers(self):
        """
        виводить в термінал всі записи в телефонній книзі
        """
        return [phone.value for phone in self.phones]

    def delete_number(self, numbers: list) -> str:
        is_deleted = False
        for number in numbers:
            for phone in self.phones:
                if number == phone.value:
                    self.phones.remove(phone)
                    is_deleted = True
        if is_deleted:
            return '✅ Deleted...'
        raise ValueError('-- ❗ Numbers to delete not found in adressbook --')


class AdressBook(UserDict):
    total_records = 0

    def add_record(self, record: Record) -> str:
        result = False
        if record.name.value not in self:
            self.data[record.name.value] = record
            AdressBook.total_records += 1
        else:
            result = self.data[record.name.value].add_number(record.phones)
        if not result:
            return '✅ Done...'
        return ''

    def del_record(self, name: str) -> str:
        try:
            self.pop(name)
        except KeyError:
            return (f"-- ❗ Can't delete {name}. Contact not found --")
        else:
            print(f'✅ contact {name} deleted...')

    def __len__(self):
        return AdressBook.total_records


MESSAGE_DATA = [['COMMAND', 'ARGUMENTS', 'ACTION'],
                ['add', '[name][phone(1)][phone(2)]...[phone(N)]',
                'create / add contact with phone numbers'],
                ['change', '[name][old_phone][new_phone]',
                "change replace contact's old phone number wuth new phone numbers"],
                ['delete', '[name][phone(1)][phone(2)]...[phone(N)]',
                "delete contact's phone number"],
                ['name', '[phone_number]', 'search contact by[phone_number]'],
                ['phone', '[name]', "search phone number by contact's[name]"],
                ['show all', '', 'display all contact in adressbook'],
                ['contact delete', '[name]',
                'delete contact with [name]from adressbook'],
                ['cls', '', 'clear console'],
                ['exit,close,good by', '', 'exit']]
