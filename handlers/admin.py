''' Добавить описание клиента '''
from data_base.sqlite_db import add_client_description, sql_start


def add_description():
    name = input("Введите имя клиента ")
    desc_client = input('Введите комментарии для клиента ')
    # sql_start()
    add_client_description(desc_client, name)


# add_description()
