from aiogram import types
from create_bot import bot, dp
import json
from handlers.excursions import get_one_excursion
from keyboards import inline_kb
from keyboards.client_kb import kb_client
from handlers.weather import get_weather
from handlers.fact import get_fact
from data_base import sqlite_db
import datetime

HI = '''
(f"Здарова, _{message.from_user.username}_! "
                             f"Какие люди! \nВот не ожидал тебя тут увидеть, бро \U0001F91D \nНачнём: жми  /start", parse_mode="Markdown", reply_markup=kb_client)
'''
HELP = ''' Итак, вот что я умею:\n-------------------------- -->\n
- /start                            - запуск бота
- Новости Анапы          - официальные новости Анапы.
- Интересный факт      - случаный факт об Анапе.
- Фотографии Анапы   - случаное фото Анапы.
- Экскурсии в Анапе   - одна из экскурсий Анапы.
- Погода в Анапе         - текущая погода в Анапе.
- Курсы валют              - курсы ЦБ (USD, EURO, CNY)

'''
# - курсы криптовалют (BTC, ETH), \n - Стоимость бензина в Анапе.
a = datetime.datetime.today().strftime("%d-%m-%Y")


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer(f"Привет, _{message.from_user.username}_! \nНачнём: --->\n"
                         f"Поздоровайся  с ботом - набери 'Привет' или 'Hi'\nили жми /help для информации",
                         parse_mode="Markdown")
    await message.delete()


@dp.message_handler(commands=['help'])
async def start_command(message: types.Message):
    await bot.send_message(message.from_user.id, HELP, reply_markup=kb_client)
    await message.delete()


@dp.message_handler(lambda message: 'Фотографии Анапы' in message.text)
async def photo_command(message: types.Message):
    await sqlite_db.sql_read(message)
    # await message.delete()


# @dp.message_handler(lambda message: 'Стоимость топлива в Анапе' in message.text)
# async def gas_price(message: types.Message):
#     for keys in news_keys:
#         await bot.send_message(message.from_user.id, f'\n\n"{data_azs[keys][0]}" \n{data_azs[keys][1]}')
#         i = 0
#         while i < len(data_azs[keys][2]):
#             await bot.send_message(message.from_user.id, f'{data_azs[keys][2][i]} : {data_azs[keys][2][i + 1]}')
#             i += 2
#     # await bot.send_message(message.from_user.id, "Стоимость")


@dp.message_handler(lambda message: 'Интересный факт' in message.text)
async def fact(message: types.Message):
    one_fact = get_fact()
    await bot.send_message(message.from_user.id, one_fact)
    # await message.delete()


@dp.message_handler(lambda message: 'Новости Анапы' in message.text)
async def news_func(message: types.Message):
    with open("handlers/news.json", "r") as read_file:
        data = json.load(read_file)
        news_keys = list(data.keys())
        i = 0
        for keys in news_keys:
            date_news = data[keys][0]
            titles_news = data[keys][1]
            news_news = data[keys][2]
            await bot.send_message(message.from_user.id, f"{date_news}: \n_{titles_news}_", parse_mode="Markdown")
            await bot.send_message(message.from_user.id, news_news)
            i += 1
    # await message.delete()


@dp.message_handler(lambda message: 'Погода в Анапе' in message.text)
async def weather(message: types.Message):
    all_data = get_weather('anapa')
    await bot.send_message(message.from_user.id, all_data)


@dp.message_handler(lambda message: 'Экскурсии в Анапе' in message.text)
async def excurs(message: types.Message):
    one_excurs = get_one_excursion()
    photo = one_excurs[4]
    await bot.send_message(message.from_user.id, f'_{one_excurs[0]}_\n-----------------\n{one_excurs[1]}\n-----------------\n{one_excurs[2]}\n_{one_excurs[3]}_ (Цены ориентировочные)', parse_mode="Markdown")
    # await bot.send_message(message.from_user.id, one_excurs[4])
    # photo = open(f'../img/{key_random}.jpg', 'rb')
    # photo = InputFile("files/test.png")
    #
    await bot.send_photo(chat_id=message.chat.id, photo=photo)

@dp.message_handler(lambda message: 'Курсы валют' in message.text)
async def curr(message: types.Message):
    with open("handlers/currency.json", "r") as read_file:
        data = json.load(read_file)
        usd_curs = data['USD']
        eur_curs = data['EUR']
        cny_curs = data['CNY']
    await message.answer(f'Курс Центробанка РФ на {a}')
    await message.answer(f'USD  : {usd_curs}')
    await message.answer(f'EURO : {eur_curs}')
    await message.answer(f'Юань : {cny_curs}')


# @dp.callback_query_handler(text='crypto')
# async def parce(callback: types.CallbackQuery):
#     curs_cr = get_currency_crypto('BTC')
#     await callback.message.answer(f'Курс Bitcoin на {a}: {curs_cr}')
#     curs_cr = get_currency_crypto('ETH')
#     await callback.message.answer(f'Курс Ethreum на {a}: {curs_cr}')
#     await callback.answer()


""" ********** Улавливаем текст с кнопки **************"""


@dp.message_handler(content_types=['text'])
async def echo_send(message: types.Message):
    if message.text == "Привет" or message.text == 'привет' or message.text == 'hi' or message.text == 'Hi' or message.text == 'HI':
        await message.answer(f"Здарова, _{message.from_user.username}_! "
                             f"Какие люди! \nВот не ожидал тебя тут увидеть, бро \U0001F91D \nНачнём: жми  /help",
                             parse_mode="Markdown")
    else:
        await message.answer(f"УПС \U0001F914, _{message.from_user.username}_! "
                             f"Такой команды нет, бро \U0001F91D \nНачнём: жми  /help",
                             parse_mode="Markdown", reply_markup=kb_client)
        await message.delete()
