''' Админская часть '''
from data_base import sqlite_db
from data_base.sqlite_db import name_clients, sql_read_free_time, sql_read_client, add_client_description



################# Проверка пароля ##############
def is_valid_password(password):
    # Правила проверки пароля
    # Минимальная длина пароля: 8 символов
    # Наличие как минимум одной буквы в верхнем регистре
    # Наличие как минимум одной буквы в нижнем регистре
    # Наличие как минимум одной цифры

    if len(password) < 8:
        return False

    has_uppercase = any(char.isupper() for char in password)
    has_lowercase = any(char.islower() for char in password)
    has_digit = any(char.isdigit() for char in password)

    return has_uppercase and has_lowercase and has_digit

# Пример использования функции
# password = input("Введите пароль: ")
# if is_valid_password(password):
#     print("Пароль действителен.")
# else:
#     print("Пароль недействителен. Проверьте правила.")

###############################


def admin_menu():
    action_admin = input(f'''<-- ------------------------ --> 
        - Добавить заметку о клиенте    --> 1
        - Посмотреть расписание на дату --> 2
        - Посмотреть клиентов           --> 3 
    Начнём: выбери  -- ''')
    match action_admin:
        case 1 | '1':
            add_description()
        case 2 | '2':
            view_free_time()
            admin_menu()
        case 3 | '3':
            sqlite_db.sql_read_client()
            admin_menu()


# Добавить описание клиента
def add_description():
    name = input("Введите имя клиента ")
    sql_read_client()
    if name in name_clients:
        desc_client = input('Введите комментарии для клиента ')
        add_client_description(desc_client, name)
    else:
        print(f'Такого имени клиента нет в базе!')
        add_description()


# Посмотреть свободное время на дату
def view_free_time():
    from handlers.client import check_data_format
    # date_order = input('\nВведи дату (ГГГГ-ММ-ДД) -- > ')
    check_data_format()
    sql_read_free_time(date_order)

