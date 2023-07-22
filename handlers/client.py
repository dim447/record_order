from data_base import sqlite_db
from handlers.admin import add_description

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
            record_consalt()
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


def record_consalt():
    print('Выбери дату')