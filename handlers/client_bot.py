import datetime
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher.filters import Text
from create_bot import bot, dp
from data_base.sqlite_db import base_init, check_phone_number, base_close, sql_add_client, sql_read_free_time, \
    add_client_order
from keyboards.client_kb import kb_client, kb_order, kb_order_time, time_keyb
import re


class FSMReg(StatesGroup):
    name = State()
    surname = State()
    age = State()
    phone_number = State()
    e_mail = State()


class FSMAdmin(StatesGroup):
    surname = State()
    phone_number = State()


class FSMDate(StatesGroup):
    date_order = State()


client_session = ()
data_order_session = None

HI = '''
(f"Добрый день, _{message.from_user.username}_! "
f"\nНачнём: жми  /start", parse_mode="Markdown", reply_markup=kb_client)
'''
HELP = ''' Итак, вот что умеет бот:\n-------------------------- -->\n
- /start                - начало работы с ботом
- /help                 - информация о том, что делает бот
- кнопка "Вход"         - вход для зарегистрированных клиентов
- кнопка "Регистрация"  - регистрация клиента
После регистрации или входа вы можете получить доступ 
для записи на консультацию
'''


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer(f"Добрый день, _{message.from_user.username}_! \nНачнём: --->\n"
                         f"Чтобы узнать, как записаться на консультацию,\nжмите /help для информации",
                         parse_mode="Markdown")
    await message.delete()


@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await bot.send_message(message.from_user.id, HELP, reply_markup=kb_client)
    await message.delete()


@dp.message_handler(text='В начало')
async def help_command(message: types.Message):
    await message.answer(f'fghgh {message.from_user.id}, {HELP}', reply_markup=kb_client)
    await message.delete()


def validate_phone_number(phone_number):
    # Паттерн для проверки номера телефона в формате +7XXXXXXXXXX
    pattern = r'^\+7\d{10}$'
    if re.match(pattern, phone_number):
        return True
    else:
        return False


# Блок входа клиента
# Ловим фамилию и телефон для проверки клиента в базе
@dp.message_handler(text='Вход', state="*")
async def enter_start(message: types.Message, state: FSMContext):
    await message.answer("Введите фамилию или имя")
    await state.set_state(FSMAdmin.surname.state)
    await message.delete()


@dp.message_handler(state=FSMAdmin.surname)
async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['surname'] = message.text
    await FSMAdmin.next()
    await message.reply("Введите телефон в формате +7**********")


@dp.message_handler(state=FSMAdmin.phone_number)
async def load_phone(message: types.Message, state: FSMContext):
    global client_session
    if validate_phone_number(message.text):
        async with state.proxy() as data:
            data['phone_number'] = message.text
            try:
                """ Проверка клиента на присутствие в базе данных """
                base_connect, cur = base_init()
                name, id_client = check_phone_number(data['phone_number'])
                client_session = (id_client, name, data['phone_number'])
                print(client_session)
                base_close(base_connect)
                await state.finish()
                await message.answer(f'{name}, Вы вошли, запишитесь на консультацию.', reply_markup=kb_order)
            except:
                await message.answer(f"Вы не зарегистрированы в базе данных. Пройдите регистрацию.")
    else:
        await message.reply(
            f"Номер телефона невереного формата.\nПовторите ввод фамилии и номер телефона в формате +7**********")
    # return client_session


# ********** Блок регистрации клиента **************
@dp.message_handler(text='Регистрация', state="*")
async def reg_client(message: types.Message):
    """ Регистрация клиента  """
    await FSMReg.name.set()
    await message.answer("Введите имя")


# Ловим первый ответ
@dp.message_handler(content_types=['text'], state=FSMReg.name)
async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMReg.next()
    await message.reply("Введите фамилию")


# Ловим второй ответ
@dp.message_handler(state=FSMReg.surname)
async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['surname'] = message.text
    await FSMReg.next()
    await message.reply("Введите ваш возраст")


# Ловим третий ответ
@dp.message_handler(state=FSMReg.age)
async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['age'] = message.text
    await FSMReg.next()
    await message.reply("Введите номер телефона")


# Ловим четвертый ответ
@dp.message_handler(state=FSMReg.phone_number)
async def load_name(message: types.Message, state: FSMContext):
    if validate_phone_number(message.text):
        async with state.proxy() as data:
            data['phone_number'] = message.text
        await FSMReg.next()
        await message.reply("Введите электронную почту'")
    else:
        await message.reply(
            f"Номер телефона невереного формата.\nПовторите ввод фамилии и номер телефона в формате +7**********")


# Ловим пятый ответ
@dp.message_handler(state=FSMReg.e_mail)
async def load_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['e_mail'] = message.text
    # await sqlite_db.sql_add_command(state)
    client = (data['name'], data['surname'], data['age'], data['phone_number'], data['e_mail'])
    # print(client)
    try:
        base_connect, cur = base_init()
        sql_add_client(client)
        base_close(base_connect)
    except:
        return "Ошибка ввода данных"
    await state.finish()
    await message.answer(f'{data["name"]}, Вы успешно зарегистрировались, '
                         f'запишитесь на консультацию.', reply_markup=kb_order)


# ********** Конец Блока регистрации клиента **************


# ********** Запись на консультацию - запрос даты **************
@dp.message_handler(text='Запись на консультацию', state="*")
async def order_client(message: types.Message):
    """ Запись на консультацию  """
    await FSMDate.date_order.set()
    await message.answer("Введите дату")


@dp.message_handler(state=FSMDate.date_order)  # Вводим дату записи консультации
async def get_date_order(message: types.Message, state: FSMContext):
    global data_order_session
    try:
        datetime.date.fromisoformat(message.text)
        async with state.proxy() as data:
            data_order_session = message.text
        await state.finish()
        await message.answer(f"Посмотрите свободные часы на {data_order_session}", reply_markup=kb_order_time)
        try:
            base_connect, cur = base_init()
            column_names, records = sql_read_free_time(data_order_session)
            base_close(base_connect)
            column_names_str = ('10-11', '11-12', '13-14', '14-15', '15-16')
            for _ in range(len(column_names[1:]) + 1):
                if records[_]:
                    await message.answer(f'Время {column_names_str[_]} -- > Занято')
                else:
                    await message.answer(f'Время {column_names_str[_]} -- > Свободно')
        except:
            return "Ошибка при работе с базой"
        await message.reply(f"Выберите время для записи", reply_markup=kb_order_time)
    except ValueError:
        await message.reply(f'Вы ввели не правильную дату, попробуйте еще раз! \n')
    await message.delete()
    # return data_order


@dp.message_handler(text='Выбрать время для консультации')
async def new_search(message: types.Message):
    await message.answer(f'\nОтлично, {client_session[1]}, давайте выберем свободное время ...', reply_markup=time_keyb)
    await message.delete()


@dp.callback_query_handler(Text(startswith="time"))
async def callbacks_time(callback: types.CallbackQuery):
    action_time = callback.data.split("_")[1]
    print(action_time)
    base_connect, cur = base_init()
    add_client_order(data_order_session, action_time, client_session[0])
    base_close(base_connect)


""" ********** Улавливаем текст с кнопки **************"""

# @dp.message_handler(content_types=['text'])
# async def echo_send(message: types.Message):
#     if message.text == "Привет" or message.text == 'привет' or message.text == 'hi' or message.text == 'Hi' or message.text == 'HI':
#         await message.answer(f"Здарова, _{message.from_user.username}_! "
#                              f"Какие люди! \nВот не ожидал тебя тут увидеть, бро \U0001F91D \nНачнём: жми  /help",
#                              parse_mode="Markdown")
#     else:
#         await message.answer(f"УПС \U0001F914, _{message.from_user.username}_! "
#                              f"Такой команды нет, бро \U0001F91D \nНачнём: жми  /help",
#                              parse_mode="Markdown", reply_markup=kb_client)
#         await message.delete()
