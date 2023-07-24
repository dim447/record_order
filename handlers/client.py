from data_base import sqlite_db
from data_base.sqlite_db import add_client_order, sql_read_free_time
from handlers.admin import admin_menu
import calendar
import datetime


hi_text = '''
Добрый день!
Это программа записи на консультацию к психологу.
Чтобы записаться на приём добавьте ваши данные.
'''


def hi_client():
    print(hi_text)
    action_client_1()


def action_client_1():
    action_client = input(f'''<-- ------------------------ --> 
    - Записаться на консультацию    --> 1
Начнём: выбери  -- ''')
    match action_client:
        case 1 | '1':
            # input_data()
            record_consult()
        case 'admin':
            admin_menu()


def input_data():
    name = input(f'Введите имя ')
    surname = input(f'Введите фамилию ')
    age = input(f'Введите возраст ')
    phone_number = input(f'Введите телефон ')
    email = input(f'Введите e-mail ')
    data_of_client = (name, surname, age, phone_number, email,)
    sqlite_db.sql_add_client(data_of_client)


def record_consult():
    now = datetime.datetime.now()
    # current_date = datetime.date.today()
    # print(f' Сегодня: {current_date}')
    # datetime.date.fromisoformat('2020-10-09')
    year = now.year
    month = now.month
    # print(f"Calendar of {month} {year} is:")
    print(calendar.month(year, month, 2, 1))
    date_order = input('\nВведи дату -- > ')
    print(f'Свободные часы для консультации на дату: {date_order}')
    sql_read_free_time(date_order)
    time_order = input('\nВведи время  -- > ')
    match time_order:
        case '10' | '11':
            time_order = '10-11'
        case '11' | '12':
            time_order = '11-12'
        case '13' | '14':
            time_order = '13-14'
        case '14' | '15':
            time_order = '14-15'
        case '15' | '16':
            time_order = '15-16'

    add_client_order(date_order, time_order, "Том")
    print(f'Вы записались на {date_order} на {time_order}')
