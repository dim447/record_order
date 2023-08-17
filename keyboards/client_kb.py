from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, \
    InlineKeyboardButton

b1 = KeyboardButton('Вход')
b2 = KeyboardButton('Регистрация')
b3 = KeyboardButton('Запись на консультацию')
b7 = KeyboardButton('В начало')
b6 = KeyboardButton('Выбрать время для консультации')
# b9 = KeyboardButton ('Фотографии Анапы')
# b4 = KeyboardButton ('Экскурсии в Анапе')
# b5 = KeyboardButton ('Поделиться номером', request_contact=True)

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)#, one_time_keyboard=True)
kb_client.row(b1, b2).add(b7)
kb_order = ReplyKeyboardMarkup(resize_keyboard=True).row(b3).add(b7)
kb_order_time = ReplyKeyboardMarkup(resize_keyboard=True).row(b6).add(b7)


time_keyb = InlineKeyboardMarkup(row_width=2,
                                 inline_keyboard=[
                                     [
                                         InlineKeyboardButton(text='10-11', callback_data='10-11'),
                                         InlineKeyboardButton(text='11-12', callback_data='11-12')
                                     ],
                                     [
                                         InlineKeyboardButton(text='13-14', callback_data='13-14'),
                                         InlineKeyboardButton(text='14-15', callback_data='14-15'),
                                         InlineKeyboardButton(text='15-16', callback_data='15-16')
                                     ]
                                 ])
