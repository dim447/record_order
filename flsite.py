import sqlite3 as sq
import time

from flask import Flask, render_template, request, flash
from data_base.sqlite_db import sql_add_client, base_init, check_phone_number
from handlers.client import time_consult

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sdjlkwkwjer435kjhj234gv2349fdjh38'

# Временное хранилище данных клиентов (обычно заменяется базой данных)
clients = ()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/order.html', methods=['GET', 'POST'])
def order():
    if request.method == 'POST':
        # Получаем данные из формы
        date_order = request.form['order_day']
        base_connect = base_init()
        time_consult(date_order)
        if date_order:
            flash(f"Вы выбрали {date_order}! Выберите время.")
        base_connect.close()
    return render_template('order.html')


@app.route('/input.html', methods=['GET', 'POST'])
def input_client():
    if request.method == 'POST':
        # Получаем данные из формы
        name = request.form['name']
        phone = request.form['phone']

        # Проверяем есть ли клиент в базе
        base_connect = base_init()
        name = check_phone_number(phone)
        if name:
            flash(f"Добро пожаловать {name}! Можете записаться на консультацию.")
            # record_consult()
        else:
            flash(f"Вы не зарегистрированы в базе данных. Пройдите регистрацию.")
            # time.sleep(5)
            # return render_template('reg.html')
        # base_connect.close()
    return render_template('input.html')


@app.route('/reg.html', methods=['GET', 'POST'])
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
        base_connect = base_init()
        sql_add_client(clients)
        base_connect.close()
        # Отправляем клиенту сообщение об успешной регистрации (можно также перенаправить на другую страницу)
        return f"Спасибо за регистрацию, {name}!"

    # Если метод запроса GET, отображаем форму для регистрации
    return render_template('reg.html')


if __name__ == '__main__':
    app.run(debug=True)
