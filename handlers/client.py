from data_base import sqlite_db
from data_base.sqlite_db import add_client_order, sql_read_free_time, check_phone_number
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
    '''
    меню выбора у клиента, если он уже зарегистрирован, то может записаться на консультацию,
    если нет, то регистрирует свои данные
    :return:
    '''
    global name
    action_client = input(f'''<-- ------------------------ --> 
    - Вы уже зарегистрированы?
Начнём: выбери  -- Y/N ''')
    match action_client:
        case 'Y' | 'y':
            phone_number = input(f'Введите свой номер телефона --> ')
            name = check_phone_number(phone_number)
            if name:
                print(f"Добро пожаловать {name}! Можете записаться на консультацию.")
                record_consult()
            else:
                print(f"Вы не зарегистрированы в базе данных. Пройдите регистрацию.")
                input_data()
                record_consult()
        case 'N' | 'n':
            input_data()
            record_consult()
        case 'admin':
            admin_menu()


def input_data():
    '''
    Ввод данных клиента
    :return: имя клиента
    '''
    name = input(f'Введите имя ')
    surname = input(f'Введите фамилию ')
    age = input(f'Введите возраст ')
    phone_number = input(f'Введите телефон ')
    email = input(f'Введите e-mail ')
    data_of_client = (name, surname, age, phone_number, email,)
    sqlite_db.sql_add_client(data_of_client)
    return name


def record_consult():
    now = datetime.datetime.now()
    year = now.year
    month = now.month
    # print(f"Calendar of {month} {year} is:")
    print(calendar.month(year, month, 2, 1))
    check_data_format()  # Проверка формата даты
    time_consult(date_order)


def time_consult(date_order):
    '''
    Проверка на свободные часы на дату. Если да, то можно записаться
    :param date_order: дата записи
    :return:
    '''
    print(f'Свободные часы для консультации на дату: {date_order}')
    sql_read_free_time(date_order)
    time_order = input('\nВведи время  -- > ')
    # name = record_consult()
    match time_order:
        case '10':
            time_order = '10-11'
        case '11':
            time_order = '11-12'
        case '13':
            time_order = '13-14'
        case '14':
            time_order = '14-15'
        case '15':
            time_order = '15-16'

    add_client_order(date_order, time_order, name)
    print(f'Вы записались на {date_order} на {time_order}')


def check_data_format():
    '''
    Проверка формата даты.
    :return: дату
    '''
    global date_order
    try:
        date_order = input('\nВведи дату (ГГГГ-ММ-ДД) -- > ')
        datetime.date.fromisoformat(date_order)
        return date_order
        # time_consult(date_order)
    except ValueError:
        print(f'Вы ввели не правильную дату, попробуйте еще раз! \n')
        check_data_format()




