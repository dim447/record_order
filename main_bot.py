import logging
from aiogram import executor
from create_bot import dp
from data_base import sqlite_db
from handlers import client_bot


async def on_startup(dp):
    # Включаем логирование, чтобы не пропустить важные сообщения
    logging.basicConfig(level=logging.INFO)
    # sqlite_db.sql_start()


##############################################################
if __name__ == '__main__':
    print('Анапский бот запущен!')
    executor.start_polling(dp, skip_updates=False, on_startup=on_startup)
##############################################################
