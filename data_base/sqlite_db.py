import sqlite3 as sq
# from create_bot import bot, dp

base_connect = sq.connect('data_base/clients.db')
cur = base_connect.cursor()
name_clients = []


def sql_start():
    if base_connect:
        print('Data base connected Ok!')
    base_connect.execute(
        'CREATE TABLE IF NOT EXISTS clients '
        '(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, '
        'name TEXT NOT NULL, '
        'surname TEXT NOT NULL, '
        'age INTEGER, '
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
    # execute("UPDATE CATEGORY SET NAME=? WHERE ID=?", (name, category_id))
    cur.execute('UPDATE clients SET description = ? WHERE name = ?', (data, name))
    base_connect.commit()
    base_connect.close()


def sql_read_client():
    # ret = cur.execute('SELECT * FROM clients ORDER BY RANDOM() LIMIT 1').fetchone()
    ret = cur.execute('SELECT * FROM clients').fetchall()
    # # ret = cur.execute('SELECT * FROM table ORDER BY RANDOM() LIMIT 1')
    for _ in ret:
        print(_)
        name_clients.append(_[1])
    return name_clients


async def sql_delete_client(name):
    cur.execute('DELETE FROM clients WHERE name == ?', (name,))
    base_connect.commit()


def add_client_order(date, time, name):
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
    ret = cur.execute('SELECT * FROM shedule WHERE date = ?', (date,)).fetchone()
    column_names = [i[0] for i in cur.description]
    # for i in range(len(column_names)):
    print(f'Часы', column_names[1:])
    # for i in ret[1:]:
    #     print(i, end='  ')
    print(f'       ', ret[1:])
