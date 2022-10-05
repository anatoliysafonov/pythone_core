from collections import UserDict

SEPARATOR = ', '


class Field:
    """
    class Field
    """

    def __init__(self, value: str) -> None:
        self.value = self.normalize_value(value)

    def normalize_value(self, value: str) -> str:
        return value


class Phone(Field):
    """
    class Phone
    """
    pass


class Record:

    def __init__(self, name: str, phones=[], emails=[]) -> None:
        if not name:
            raise ValueError("-- ❗ Must be contact's name ❗ --")
        self.name = Field(name)
        self.phones = phones
        self.emails = emails

    def _get_numbers(self) -> list:
        return self.phones

    def _get_emails(self):
        return self.emails

    def add_number(self, number) -> str:
        """
        добавляє новий номсер телефона якщо його немає в списку.
        """
        numbers = [item.value for item in self.phones]
        for current_number in number:
            if current_number not in numbers:
                self.phones.append(Phone(current_number))
            else:
                print(
                    f'-- ❗ Phone number {current_number} exists already ❗ --')

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
            raise ValueError('-- ❗ Number to change not exists ❗ --')
        return '✅ Changed...'

    def out_info(self) -> str:
        numbers = [item.value for item in self.phones]
        numbers = SEPARATOR.join(numbers)
        return f'{self.name.value} : {numbers}'

    def show_numbers(self):
        """
        виводить в термінал всі записи в телефонній книзі
        """
        return self.phones

    def delete_number(self, numbers: list) -> str:
        is_deleted = False
        for number in numbers:
            for phone in self.phones:
                if number == phone.value:
                    self.phones.remove(phone)
                    is_deleted = True
        if is_deleted:
            return '✅ Deleted...'
        raise ValueError('-- ❗ Numbers to delete not found in adressbook ❗ --')


class AdressBook(UserDict):
    total_records = 0

    def __init__(self) -> None:
        self.data = {}

    def add_record(self, name: str, numbers: list) -> str:
        number_unique = []
        for number in numbers:
            if number not in number_unique:
                number_unique.append(number)
        if name in self.data:
            self.data[name].add_number(number_unique)
        else:
            number_unique = [Phone(item) for item in number_unique]
            record = Record(name, phones=number_unique)
            self.data[name] = record
            AdressBook.total_records += 1
        return '✅ Done...'

    def del_record(self, name: str) -> str:
        try:
            self.data.pop(name)
        except KeyError:
            return (f"-- ❗ Can't delete {name}. Contact not found ❗ --")
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
