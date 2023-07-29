import sqlite3 as sq
# from create_bot import bot, dp

name_clients = []


def base_init():
    global base_connect, cur
    base_connect = sq.connect('data_base/clients.db')
    cur = base_connect.cursor()
    return base_connect, cur


def sql_start():
    base_init()
    base_connect.execute(
        'CREATE TABLE IF NOT EXISTS clients '
        '(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, '
        'name TEXT NOT NULL, '
        'surname TEXT NOT NULL, '
        'surname TEXT NOT NULL, '
        'age INTEGER NOT NULL, '
        'phone_number TEXT NOT NULL, '
        'e_mail TEXT, '
        'description TEXT)')
    base_connect.execute('''
           CREATE TABLE IF NOT EXISTS shedule (
               date TEXT PRIMARY KEY,
               "10-11" TEXT,
               "11-12" TEXT,
               "13-14" TEXT,
               "14-15" TEXT,
               "15-16" TEXT
           )
       ''')
    base_connect.commit()


def sql_add_client(data):
    cur.execute('INSERT INTO clients (name, surname, age, phone_number, e_mail) VALUES (?,?,?,?,?)', tuple(data))
    base_connect.commit()
    # base_connect.close()
    print('Клиент добавлен...')


def add_client_description(data, name):
    '''
    Добавление комментария о клиенте
    :param data: сам комментарий
    :param name: имя клиента
    :return:
    '''
    cur.execute('UPDATE clients SET description = ? WHERE name = ?', (data, name))
    base_connect.commit()
    base_connect.close()


def sql_read_client():
    '''
    Чтение данных о всех клиентах в базе.
    :return: список всех клиентов
    '''
    ret = cur.execute('SELECT * FROM clients').fetchall()
    # # ret = cur.execute('SELECT * FROM table ORDER BY RANDOM() LIMIT 1')
    for _ in ret:
        print(_)
        name_clients.append(_[1])
    return name_clients


async def sql_delete_client(name):
    '''
    Удаление клиента.
    :param name: имя клиента, надо подумать, имена могут быть разные
    :return:
    '''
    cur.execute('DELETE FROM clients WHERE name == ?', (name,))
    base_connect.commit()


def add_client_order(date, time, name):
    '''
    Функция добавления записи на консультацию. Проверяет если даты нет, то добавляет строчку с датой.
    :param date:  дата
    :param time:  время в интервале
    :param name: имя клиента
    :return:
    '''
    record_exists = check_record_exists(date)
    if record_exists:
        pass
    else:
        cur.execute('INSERT INTO shedule (date) VALUES (?)', [date])
    match time:
        case '10-11':
            cur.execute('UPDATE shedule SET "10-11" = ? WHERE date = ?', (name, date))
        case '11-12':
            cur.execute('UPDATE shedule SET "11-12" = ? WHERE date = ?', (name, date))
        case '13-14':
            cur.execute('UPDATE shedule SET "13-14" = ? WHERE date = ?', (name, date))
        case '14-15':
            cur.execute('UPDATE shedule SET "14-15" = ? WHERE date = ?', (name, date))
        case '15-16':
            cur.execute('UPDATE shedule SET "15-16" = ? WHERE date = ?', (name, date))
    base_connect.commit()
    base_connect.close()


def sql_read_free_time(date):
    '''
    Проверяет по дате есть ли записи на эту дату.
    Выводит в виде таблицы часы записи и имена клиентов
    '''
    record_exists = check_record_exists(date)
    if record_exists:
        ret = cur.execute('SELECT * FROM shedule WHERE date = ?', (date,)).fetchone()
        column_names = [i[0] for i in cur.description]
        print(f'Часы', *column_names[1:], sep="  ")
        print(f'   ', *ret[1:], sep="    ")
    else:
        print(f"Запись на дату {date} не найдена.")


def check_record_exists(key_value):
    """
    Проверяет наличие записи в таблице по ключевому полю и его значению.
    :param key_value: Значение ключевого поля для поиска -- дата.
    :return: True, если запись с заданным ключевым значением существует, иначе False.
    """
    query = f"SELECT COUNT(*) FROM shedule WHERE date = ?;"
    cur.execute(query, (key_value,))
    count = cur.fetchone()[0]
    # cur.close()

    return count > 0


def check_phone_number(phone_number):
    '''
    Проверка по уникальному номеру телефона
    :param phone_number: номер телефона
    :return:
    '''
    # Выполняем запрос для проверки наличия записи с указанным телефонным номером
    cur.execute('SELECT * FROM clients WHERE phone_number = ?', (phone_number,))
    row = cur.fetchone()
    # Закрываем соединение
    # base_connect.close()
    # Если запрос вернул запись, значит телефонный номер найден в базе данных
    return row[1] if row else None
