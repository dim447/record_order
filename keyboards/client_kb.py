from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

b1 = KeyboardButton('Вход')
b2 = KeyboardButton('Регистрация')
b3 = KeyboardButton('Запись на консультацию')
# b7 = KeyboardButton ('Курсы валют')
# b6 = KeyboardButton ('Стоимость топлива в Анапе')
# b9 = KeyboardButton ('Фотографии Анапы')
# b4 = KeyboardButton ('Экскурсии в Анапе')
# b5 = KeyboardButton ('Поделиться номером', request_contact=True)

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)#, one_time_keyboard=True)
kb_client.row(b1, b2)
kb_order = ReplyKeyboardMarkup(resize_keyboard=True).row(b3)
