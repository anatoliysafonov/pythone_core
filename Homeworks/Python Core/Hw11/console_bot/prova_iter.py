class Phone:
    def __init__(self, value):
        self.value = value
    
    def __eq__(self, other):
        if type(other) == type(self):
            if other.value == self.value:
                return True
        return False

class Record:
    def __init__(self, name, phone):
        self.name = name
        self.phones = [Phone(phone)]
        self.current = 0

    def __add__(self, phone):
        self.phones.append(Phone(phone))


    def __str__(self):
        return ', '.join([phone.value for phone in self.phones])

    def __iter__(self):
        return self

    def __next__(self):
        if self.current >= len(self.phones):
            raise StopIteration
        result = self.phones[self.current]
        self.current += 1
        return result

    def check(self, phone):
        phone = Phone(phone)
        for ph in self:
            if phone == ph:
                self.count = 0
                return 'Found'
        self.count = 0
        return 'Not found'



record = Record ('Vasia','0737700977')
record + '0675533044'
record + '0936598765'
phone  =  '0675533044'

print(record.check(phone))
# Found
