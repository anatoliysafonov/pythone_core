from datetime import datetime

# список словників users. Вхідні дані
PERSONS = [{'name': 'Bill', 'birthday': datetime(year=1956, month=9, day=24)},
           {'name': 'Tom',  'birthday': datetime(year=2000, month=9, day=24)},
           {'name': 'Elle', 'birthday': datetime(year=1973, month=9, day=25)},
           {'name': 'Anna', 'birthday': datetime(year=1999, month=9, day=26)},
           {'name': 'Tonny', 'birthday': datetime(year=1944, month=9, day=24)},
           {'name': 'Fafa', 'birthday': datetime(year=2000, month=9, day=28)}
           ]


def get_birthdays_per_week(users: list) -> None:
    # сортуємо вхідний список по датам нарождення
    list_persons_sorted = sorted(PERSONS, key=lambda x: x['birthday'])
    data_out = {}  # вловник вихідних даних

    # знаходимо день привітання з врахуванням вихідних днів [Saturday, Sunday, Monday] -> Nonday
    def get_day_str(dt: datetime) -> str:

        WEEKEND = ['Saturday', 'Sunday']
        string = dt.strftime('%A')
        if string in WEEKEND:
            string = 'Monday'
        return string

    date_now = datetime.now()  # поточна дата

    for person in users:

        birthday_this_year = datetime(
            year=date_now.year, month=person['birthday'].month, day=person['birthday'].day)  # дата народження person в поточному році
        # умова дяля перевірки, чи person святкує день нарождення на протязі тижня
        if 0 <= (birthday_this_year - date_now).days < 7:
            # стороке значення дня нарождення Monday...Sunday. Використається як ключ словника
            str_day = get_day_str(birthday_this_year)
            if str_day in data_out.keys():
                # якщо такий день в словнику вже існує, то добавляємо person в цей день
                data_out[str_day] = ', '.join(
                    [data_out[str_day], person['name']])
            else:
                # якщо такого дня в словнику ще немає, то добаляємо його
                data_out[str_day] = person['name']

    for item in data_out.keys():  # виводимо результат
        print('{}: {}'.format(item, data_out[item]))


get_birthdays_per_week(PERSONS)
