from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from handlers import client, admin


admin_keyb = InlineKeyboardMarkup(row_width=2,
                                  inline_keyboard=[
                                      [
                                          InlineKeyboardButton(text='Загрузить фото', callback_data='upload'),
                                          InlineKeyboardButton(text='Удалить фото', callback_data='delete')
                                      ],
                                      [
                                          InlineKeyboardButton(text='Загрузить факт -->', callback_data='get_fact')
                                      ]
                                  ])

