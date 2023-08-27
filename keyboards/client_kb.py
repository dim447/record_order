from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, \
    InlineKeyboardButton

b1 = KeyboardButton('Вход')
b2 = KeyboardButton('Регистрация')
b3 = KeyboardButton('Запись на консультацию')
b6 = KeyboardButton('Выбрать время для консультации')
b7 = KeyboardButton('Выход')
b9 = KeyboardButton('Мои записи')
# b4 = KeyboardButton ('Экскурсии в Анапе')
# b5 = KeyboardButton ('Поделиться номером', request_contact=True)

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)#, one_time_keyboard=True)
kb_client.row(b1, b2).add(b7)
# kb_client_view_records = ReplyKeyboardMarkup(resize_keyboard=True)
# kb_client_view_records.row(b9, b3)
kb_order = ReplyKeyboardMarkup(resize_keyboard=True).row(b9, b3).add(b7)
kb_order1 = ReplyKeyboardMarkup(resize_keyboard=True).row(b3).add(b7)
kb_cancel = ReplyKeyboardMarkup(resize_keyboard=True).row(b9, b7)
kb_order_time = ReplyKeyboardMarkup(resize_keyboard=True).row(b6).add(b9, b7)

#
# time_keyb = InlineKeyboardMarkup(row_width=2,
#                                  inline_keyboard=[
#                                      [
#                                          InlineKeyboardButton(text='10-11', callback_data='time_10-11'),
#                                          InlineKeyboardButton(text='11-12', callback_data='time_11-12')
#                                      ],
#                                      [
#                                          InlineKeyboardButton(text='13-14', callback_data='time_13-14'),
#                                          InlineKeyboardButton(text='14-15', callback_data='time_14-15'),
#                                          InlineKeyboardButton(text='15-16', callback_data='time_15-16')
#                                      ]
#                                  ])
