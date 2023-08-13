from flask import render_template, request, flash, url_for, redirect

from sweater import app, db
from sweater.models import Clients, Sсhedule

from data_base.sqlite_db import base_init, check_phone_number, base_close, sql_read_free_time


@app.route('/')
def index():
    """ Главная страница проекта   """
    return render_template('index.html')


@app.route('/enter', methods=['GET', 'POST'])
def enter():
    """ Функция входа зарегистрированного клиента   """
    if request.method == 'POST':
        # Получаем данные из формы
        name1 = request.form['name']
        phone = request.form['phone']

        # Проверяем есть ли клиент в базе
        try:
            # name = db.session.get(Clients, name1)
            # print(name1, name)
            base_connect, cur = base_init()
            name, id_client = check_phone_number(phone)
            base_close(base_connect)
        except:
            flash(f"Вы не зарегистрированы в базе данных. Пройдите регистрацию.")
            return render_template('reg.html')
            # return "Ошибка ввода данных"
        if name:
            if name == "admin":
                return redirect(url_for('admin'))
            else:
                return redirect(url_for('order', name=name, id=id_client))
        else:
            flash(f"Вы не зарегистрированы в базе данных. Пройдите регистрацию.")
            return render_template('reg.html')

    return render_template('enter.html')


@app.route('/reg', methods=['GET', 'POST'])
def registration():
    """ Регистрация клиента  """
    if request.method == 'POST':
        # Получаем данные из формы
        name = request.form['name']
        surname = request.form['surname']
        age = request.form['age']
        phone = request.form['phone']
        email = request.form['email']

        client = Clients(name=name, surname=surname, age=age, phone_number=phone, e_mail=email)
        # Добавляем клиента в базу данных
        try:
            db.session.add(client)
            db.session.commit()
            return redirect(url_for('enter'))
        except:
            return "Ошибка ввода данных"

    # Если метод запроса GET, отображаем форму для регистрации
    return render_template('reg.html')


@app.route('/order/<int:id>', methods=['GET', 'POST'])
def order(id):
    """ Проверка свободных слотов на дату   """
    # print(id)
    if request.method == 'POST':
        # Получаем данные из формы
        date_order = request.form['date']
        try:
            record_exists = db.session.query(db.exists().where(Sсhedule.date == date_order)).scalar()
        except:
            return "Ошибка ввода данных"
        if record_exists:
            return redirect(url_for('booking', date=date_order, id=id))
        else:
            schedule = Sсhedule(date=date_order, time10="", time11="", time13="", time14="", time15="")
            # Добавляем дату  расписание в базу данных
            try:
                db.session.add(schedule)
                db.session.commit()
                return redirect(url_for('booking', date=date_order, id=id))
            except:
                return "Ошибка ввода данных"
            # return "На дату нет записей"
    return render_template('order.html')


@app.route('/booking/<int:id>/<date>', methods=['GET', 'POST'])
def booking(id, date):
    """ Вывод свободных слотов    """
    # print(id)
    if request.method == 'POST':
        # Получаем данные из формы
        time_order = request.form['time_order']
        # client = Clients.query.get(id)
        # print(client.name, time_order)
        return redirect(url_for('success', date=date, time=time_order, id=id))
    else:
        try:
            base_connect, cur = base_init()
            column_names, records = sql_read_free_time(date)
            base_close(base_connect)
            # return redirect(url_for('index'))
            return render_template('booking.html', column_names=column_names, records=records, date=date)
        except:
            return "Ошибка при работе с базой"


@app.route('/success/<int:id>/<date>=<time>')
def success(id, date, time):
    """ Страница подтверждения записи   """
    print(id, date, time)

    try:
        client = db.session.get(Clients, id)
        schedule = db.session.get(Sсhedule, date)
        match time:
            case '10-11':
                schedule.time10 = id
            case '11-12':
                schedule.time11 = id
            case '13-14':
                schedule.time13 = id
            case '14-15':
                schedule.time14 = id
            case '15-16':
                schedule.time15 = id
        db.session.commit()
    except:
        return "Ошибка при работе с базой"

    return render_template('success.html', date=date, time=time, client=client)


@app.route('/admin')
def admin():
    """ Главная страница админа   """
    return render_template('admin.html')


@app.route('/order_admin', methods=['GET', 'POST'])
def order_admin():
    """ Вывод расписания на дату (для консультанта-админа)   """
    if request.method == 'POST':
        # Получаем данные из формы
        date_order = request.form['date']
        try:
            record_exists = db.session.query(db.exists().where(Sсhedule.date == date_order)).scalar()
        except:
            return "Ошибка ввода данных"
        # try:
        #     base_connect, cur = base_init()
        #     record_exists = check_date_exists(date_order)
        #     base_close(base_connect)
        # except:
        #     return "Ошибка ввода данных"
        if record_exists:
            return redirect(url_for('book', date=date_order))
        else:
            return "На дату нет записей"
    return render_template('order_admin.html')


@app.route('/book/<date>', methods=['GET', 'POST'])
def book(date):
    """ Расписание на дату   """
    client_list_name, client_list_surname = [], []
    schedule = db.session.get(Sсhedule, date)
    # print(schedule)
    id_list = [schedule.time10, schedule.time11, schedule.time13, schedule.time14, schedule.time15]
    # print(id_list)
    for i in id_list:
        if i != '':
            client_list_name.append(db.session.get(Clients, i).name)
        else:
            client_list_name.append("Null")
    # print(client_list_name)
    for i in id_list:
        if i != '':
            client_list_surname.append(db.session.get(Clients, i).surname)
        else:
            client_list_surname.append("Null")

    if request.method == 'POST':
        # Получаем данные из формы
        # schedule.date = request.form['date']
        schedule.time10 = request.form['time10']
        schedule.time11 = request.form['time11']
        schedule.time13 = request.form['time13']
        schedule.time14 = request.form['time14']
        schedule.time15 = request.form['time15']

        # Добавляем клиента в базу данных
        try:
            db.session.commit()
            return redirect('/order_admin')
        except:
            return "Ошибка ввода данных"
    else:
        # Если метод запроса GET, отображаем форму для регистрации
        return render_template('book.html', schedule=schedule, client_list_name=client_list_name,
                               client_list_surname=client_list_surname, date=date)


@app.route('/clients')
def clients():
    """ Вывод всех клиентов (для админа)   """
    client_s = Clients.query.order_by(Clients.id).all()
    return render_template('clients.html', clients=client_s)


@app.route('/clients/<int:id>')
def client_detail(id):
    """ Детальная информация по клиенту  """
    client = Clients.query.get(id)
    return render_template('client_detail.html', client=client)


@app.route('/clients/<int:id>/del')
def client_del(id):
    """ Удаление клиента  """
    client = Clients.query.get_or_404(id)
    try:
        db.session.delete(client)
        db.session.commit()
        return redirect(url_for('clients'))
    except:
        return "При удалении клиента произошла Ошибка"


@app.route('/clients/<int:id>/update', methods=['GET', 'POST'])
def client_update(id):
    """ Добавление заметки по клиенту   """
    client = Clients.query.get(id)
    if request.method == 'POST':
        # Получаем данные из формы
        client.name = request.form['name']
        client.surname = request.form['surname']
        client.age = request.form['age']
        client.phone_number = request.form['phone']
        client.e_mail = request.form['email']
        client.description = request.form['description']

        # Добавляем заметку о клиенте в базу данных
        try:
            db.session.commit()
            return redirect('/clients')
        except:
            return "Ошибка ввода данных"
    else:
        # Если метод запроса GET, отображаем форму для регистрации
        return render_template('client_update.html', client=client)
