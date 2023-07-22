''' Добавить описание клиента '''
from data_base import sqlite_db
from data_base.sqlite_db import name_clients


def add_description():
    name = input("Введите имя клиента ")
    sqlite_db.sql_read_client()
    if name in name_clients:
        desc_client = input('Введите комментарии для клиента ')
        sqlite_db.add_client_description(desc_client, name)
    else:
        print(f'Такого имени клиента нет в базе!')
        add_description()


# add_description()
