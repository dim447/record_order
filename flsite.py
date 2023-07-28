import sqlite3 as sq
from flask import Flask, render_template, request
from data_base.sqlite_db import sql_add_client, sql_start

app = Flask(__name__)

# Временное хранилище данных клиентов (обычно заменяется базой данных)
clients = []


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/reg', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        # Получаем данные из формы
        name = request.form['name']
        surname = request.form['surname']
        age = request.form['age']
        phone = request.form['phone']
        email = request.form['email']

        # Добавляем клиента в базу данных
        clients = (name, surname, int(age), phone, email,)
        base_connect = sq.connect('data_base/clients.db')
        cur = base_connect.cursor()
        cur.execute('INSERT INTO clients (name, surname, age, phone_number, e_mail) VALUES (?,?,?,?,?)', tuple(clients))
        base_connect.commit()
        base_connect.close()
        # Отправляем клиенту сообщение об успешной регистрации (можно также перенаправить на другую страницу)
        return f"Спасибо за регистрацию, {name}!"

    # Если метод запроса GET, отображаем форму для регистрации
    return render_template('reg.html')


if __name__ == '__main__':
    app.run(debug=True)
