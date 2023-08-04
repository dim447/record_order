from flask import Flask, render_template, request, flash, jsonify, url_for, redirect, session
from flask_sqlalchemy import SQLAlchemy
from data_base.sqlite_db import sql_add_client, base_init, check_phone_number, sql_read_free_time

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/idim/PycharmProjects/record_order/data_base/clients.db'
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = 'sdjlkwkwjer435kjhj234gv2349fdjh38'


class Clients(db.Model):
    """ Класс Клиент получает из базы данных информацию о клиенте   """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    surname = db.Column(db.String(80), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    phone_number = db.Column(db.String(10), unique=True, nullable=False)
    e_mail = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)

    def __repr__(self):
        return '<Clients %r>' % self.name


class Sсhedule(db.Model):
    """ Класс Расписание получает из базы данных информацию о свободном времени   """

    date = db.Column(db.String(10), primary_key=True)
    time10 = db.Column(db.String(80), nullable=False)
    time11 = db.Column(db.String(80), nullable=False)
    time13 = db.Column(db.String(80), nullable=False)
    time14 = db.Column(db.String(80), nullable=False)
    time15 = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return '<Schedule %r>' % self.date

    def __str__(self):
        return f"Расписание на . " \
               f"Дата: {self.date}. " \
               f"10-11: {self.time10}. " \
               f"11-12: {self.time11}. " \
               f"13-14: {self.time13}. " \
               f"14-15: {self.time14}. " \
               f"15-16: {self.time15}. "


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
        base_connect = base_init()
        name = check_phone_number(phone)
        if name:
            if name == "admin":
                return redirect(url_for('admin'))
            else:
                return redirect(url_for('order', name=name))
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


@app.route('/order', methods=['GET', 'POST'])
def order():
    """ Проверка свободных слотов на дату   """
    if request.method == 'POST':
        # Получаем данные из формы
        date_order = request.form['date']
        return redirect(url_for('booking', date=date_order))
    return render_template('order.html')


@app.route('/order_admin', methods=['GET', 'POST'])
def order_admin():
    """ Принт расписания на дату (для консультанта-админа)   """
    if request.method == 'POST':
        # Получаем данные из формы
        date_order = request.form['date']
        return redirect(url_for('book', date=date_order))
    return render_template('order_admin.html')


@app.route('/admin')
def admin():
    """ Главная страница админа   """
    return render_template('admin.html')


@app.route('/booking/<date>')
def booking(date):
    """ Вывод свободных слотов    """
    base_connect = base_init()
    column_names, records = sql_read_free_time(date)
    # return redirect(url_for('index'))
    return render_template('booking.html', column_names=column_names, records=records, date=date)


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

        # Добавляем клиента в базу данных
        try:
            db.session.commit()
            return redirect('/clients')
        except:
            return "Ошибка ввода данных"
    else:
        # Если метод запроса GET, отображаем форму для регистрации
        return render_template('client_update.html', client=client)


@app.route('/book/<date>', methods=['GET', 'POST'])
def book(date):
    """ Расписание на дату   """
    schedule = db.session.get(Sсhedule, date)
    # schedule = Sсhedule.query.get(date)
    # print(schedule)
    if request.method == 'POST':
        # Получаем данные из формы
        schedule.date = request.form['date']
        schedule.time10 = request.form['time10']
        schedule.time11 = request.form['time11']
        schedule.time13 = request.form['time13']
        schedule.time14 = request.form['time14']
        schedule.time15 = request.form['time15']

        # Добавляем клиента в базу данных
        try:
            # db.session.commit()
            return redirect('/order')
        except:
            return "Ошибка ввода данных"
    else:
        # Если метод запроса GET, отображаем форму для регистрации
        return render_template('book.html', schedule=schedule, date=date)


if __name__ == '__main__':
    app.run(debug=True)
