''' Админская часть '''
from data_base import sqlite_db
from data_base.sqlite_db import name_clients, sql_read_free_time, sql_read_client, add_client_description



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
    date = input(f'Введите дату: ')
    sql_read_free_time(date)

# add_description()
