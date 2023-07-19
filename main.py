import logging
from data_base import sqlite_db
from handlers.client import hi_client


def on_startup():
    # Включаем логирование, чтобы не пропустить важные сообщения
    logging.basicConfig(level=logging.INFO)
    # sqlite_db.sql_start()
    hi_client()


##############################################################
if __name__ == '__main__':
    # print('Анапский бот запущен!')
    on_startup()

