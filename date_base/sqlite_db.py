import sqlite3 as sq
# from create_bot import bot, dp


def sql_start():
    global base_connect, cur
    base_connect = sq.connect('data_base/clients.db')
    cur = base_connect.cursor()
    if base_connect:
        print('Data base connected Ok!')
    base_connect.execute(
        'CREATE TABLE IF NOT EXISTS clients (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, client_name TEXT NOT NULL, '
        'phone_number TEXT NOT NULL, e_mail TEXT, description TEXT)')
    base_connect.commit()


def sql_add_client(data):
    cur.execute('INSERT INTO clients (client_name, phone_number, e_mail, description) VALUES (?,?,?,?)', tuple(data))
    base_connect.commit()


def sql_read_client(message):
    ret = cur.execute('SELECT * FROM clients ORDER BY RANDOM() LIMIT 1').fetchone()
    # ret = cur.fetchone()
    # # ret = cur.execute('SELECT * FROM table ORDER BY RANDOM() LIMIT 1')
    for ret in cur.execute('SELECT * FROM pic').fetchall():
        print(ret)
    # await bot.send_photo(message.from_user.id, ret[1], f'{ret[2]}\n{ret[3]}')
    # base.close()


async def sql_delete_client(data):
    cur.execute('DELETE FROM clients WHERE client_name == ?', (data,))
    base_connect.commit()


