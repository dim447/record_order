from data_base.sqlite_db import sql_add_client, sql_read_client

hi_text = '''
Добрый день!\nВот не ожидал тебя тут увидеть, бро \U0001F91D \n
Начнём: выбери -->
Итак, вот что я умею:\n<-- ------------------------ -->
- Записаться на консультацию  --> 1
- Добавить свои данные --> 2
- Посмотреть клиентов -- > 3
'''
data = []


def hi_client():
    print(hi_text)
    action_client = input(f'Что вы хотите: 1 / 2 / 3 ')
    if action_client == "1" or action_client == 1:
        record_consalt()
    elif action_client == "3" or action_client == 3:
        sql_read_client()
    else:
        input_data()


def input_data():
    name = input(f'Введите имя ')
    surname = input(f'Введите фамилию ')
    age = input(f'Введите возраст ')
    phone_number = input(f'Введите телефон ')
    email = input(f'Введите e-mail ')
    data = [name, surname, age, phone_number, email]
    sql_add_client(data)
    print(tuple(data))


def record_consalt():
    print('Выбери дату')


