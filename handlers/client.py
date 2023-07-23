from data_base import sqlite_db
from data_base.sqlite_db import add_client_order, sql_read_free_time
from handlers.admin import add_description
import calendar
import datetime


hi_text = '''
Добрый день!\nВот не ожидал тебя тут увидеть, бро \U0001F91D \n'''


def hi_client():
    print(hi_text)
    action_client_1()


def action_client_1():
    action_client = input(f'''<-- ------------------------ --> 
    - Записаться на консультацию    --> 1
    - Добавить свои данные          --> 2
    - Посмотреть клиентов           --> 3 
Начнём: выбери  -- ''')
    match action_client:
        case 1 | '1':
            record_consult()
        case 2 | '2':
            input_data()
            action_client_1()
        case 3 | '3':
            sqlite_db.sql_read_client()
            action_client_1()
        case 'admin':
            add_description()


def input_data():
    name = input(f'Введите имя ')
    surname = input(f'Введите фамилию ')
    age = input(f'Введите возраст ')
    phone_number = input(f'Введите телефон ')
    email = input(f'Введите e-mail ')
    data_of_client = [name, surname, age, phone_number, email]
    sqlite_db.sql_add_client(data_of_client)


def record_consult():
    now = datetime.datetime.now()
    current_date = datetime.date.today()
    print(f' Сегодня: {current_date}')
    # datetime.date.fromisoformat('2020-10-09')
    year = now.year
    month = now.month
    # print(f"Calendar of {month} {year} is:")
    print(calendar.month(year, month, 2, 1))
    date_order = input('\nВведи дату -- > ')
    sql_read_free_time(date_order)
    # add_client_order(date_order, '11-12', "Дим")

