from decorator import input_error
PHONEBOOK = {}


@input_error
def add(*args) -> str:
	"""
	Adds a new entry to the phonebook
	:param args:
	:return:
	"""

	if not args:
		raise IndexError(f"Enter the user's name and phone number")
	if len(args[0]) < 2:
		raise IndexError(f'You have not entered a phone number')
	user_name, number = args[0]
	if user_name in PHONEBOOK:
		raise KeyError(f'user {user_name} already exists in phonebook')
	PHONEBOOK[user_name] = number
	return 'added...'


@input_error
def change(*args) -> str:
	"""
	Changes the phone number of an existing entry in the phone book
	:param args:
	:return:
	"""

	if not args or len(args[0]) < 2:
		raise IndexError("The name and also the phone number are not correct")
	user_name, number = args[0]
	if user_name not in PHONEBOOK:
		raise KeyError(f'User {user_name} not exists')
	PHONEBOOK[user_name] = number
	return 'changed...'


@input_error
def name(*args) -> str:
	"""
	Searches for a record by phone number
	:param args:
	:return:
	"""
	if not args:
		raise IndexError('Enter a phone number to search')
	number = args[0][0]
	if number not in PHONEBOOK.values():
		raise ValueError(f'User with phone number {number} not  exists')
	for key, value in PHONEBOOK.items():
		if value == number:
			return f'{key} : {number}'


@input_error
def phone(*args) -> str:
	"""
	Searches for a record by name
	:param args:
	:return:
	"""
	if not args:
		raise IndexError('Enter a name  to search')
	user_name = args[0][0]
	if user_name not in PHONEBOOK:
		raise KeyError(f'User {user_name} non exists in phonebook')
	return f'{user_name} : {PHONEBOOK[user_name]}'


def hello() -> str:
	"""
	print some text
	:return:
	"""
	return 'How can I help you?'


def show_all() -> str:
	"""
	prints all entries in the phone book
	:return:
	"""
	string = ''
	if not PHONEBOOK:
		return 'PHONEBOOK is empty'

	for key, value in PHONEBOOK.items():
		string = ''.join([string, f'{key} : {value}', '\n'])
	return string[:-1]


def stop() -> str:
	"""
	exit script
	:return:
	"""
	return 'Good by!'


FUNCTIONS = {
	'add': add,
	'change ': change,
	'name': name,
	'phone': phone,
	'hello': hello,
	'show all': show_all,
	'close': stop,
	'exit': stop,
	'good by': stop
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
