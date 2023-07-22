import sqlite3 as sq
# from create_bot import bot, dp

base_connect = sq.connect('data_base/clients.db')
cur = base_connect.cursor()
name_clients = []


def sql_start():
    if base_connect:
        print('Data base connected Ok!')
    base_connect.execute(
        'CREATE TABLE IF NOT EXISTS clients (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, '
        'surname TEXT NOT NULL, age INTEGER, phone_number TEXT NOT NULL, e_mail TEXT, description TEXT)')
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


async def sql_delete_client(data):
    cur.execute('DELETE FROM clients WHERE name == ?', (data,))
    base_connect.commit()
