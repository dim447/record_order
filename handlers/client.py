from date_base.sqlite_db import sql_add_client

hi_text = '''
Добрый день!\nВот не ожидал тебя тут увидеть, бро \U0001F91D \n
Начнём: выбери -->
Итак, вот что я умею:\n<-- ------------------------ -->
- Записаться на консультацию  --> 1
- Добавить свои данные --> 2
'''
data = []


def hi_client():
    print(hi_text)
    action_client = input(f'Что вы хотите: 1 / 2 ')
    if action_client == 1:
        pass
    else:
        input_data()
        # sql_add_client(data)


def input_data():
    for i in range(3):
        data.append(input())
    print(tuple(data))
