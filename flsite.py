import sqlite3 as sq
import time

from flask import Flask, render_template, request, flash, jsonify, url_for, redirect, session
from data_base.sqlite_db import sql_add_client, base_init, check_phone_number, sql_read_free_time
from handlers.client import time_consult

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sdjlkwkwjer435kjhj234gv2349fdjh38'

# Временное хранилище данных клиентов (обычно заменяется базой данных)
clients = ()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/order', methods=['GET', 'POST'])
def order():
    flash(f"Добро пожаловать ! Можете записаться на консультацию.")
    if request.method == 'POST':
        # Получаем данные из формы
        date_order = request.form['date']
        # base_connect = base_init()
        # time_consult(date_order)
        # if date_order:
        #     flash(f"Вы выбрали {date_order}! Выберите время.")
        # base_connect.close()
        # print(date_order)
        return redirect(url_for('booking', date=date_order))
    return render_template('order.html')


@app.route('/enter', methods=['GET', 'POST'])
def input_client():
    if request.method == 'POST':
        # Получаем данные из формы
        name = request.form['name']
        phone = request.form['phone']

        # Проверяем есть ли клиент в базе
        base_connect = base_init()
        name = check_phone_number(phone)
        # if name:
        #     flash(f"Добро пожаловать {name}! Можете записаться на консультацию.")
        #     # record_consult()
        # else:
        #     flash(f"Вы не зарегистрированы в базе данных. Пройдите регистрацию.")
            # time.sleep(5)
            # return render_template('reg.html')
        # base_connect.close()
        return redirect(url_for('order', name=name))
    return render_template('enter.html')


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
        base_connect = base_init()
        sql_add_client(clients)
        # base_connect.close()
        # Отправляем клиенту сообщение об успешной регистрации (можно также перенаправить на другую страницу)
        return redirect(url_for('new'))

    # Если метод запроса GET, отображаем форму для регистрации
    return render_template('reg.html')


# @app.route('/new', methods=['GET', 'POST'])
# def new_index():
#     if request.method == 'POST':
#         date = request.form.get('date')
#
#         return redirect(url_for('booking', date=date))
#     return render_template('new.html')


@app.route('/booking/<date>')
def booking(date):
    base_connect = base_init()
    column_names, records = sql_read_free_time(date)
    return render_template('booking.html', column_names=column_names, records=records, date=date)


# @app.route('/booking')
# def booking():
#     date = request.args.get('date', None)
#     return render_template('booking.html', date=date)


if __name__ == '__main__':
    app.run(debug=True)
