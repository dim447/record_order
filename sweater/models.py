# from main import db
#
#
# class Clients(db.Model):
#     """ Класс Клиент получает из базы данных информацию о клиенте   """
#
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(80), nullable=False)
#     surname = db.Column(db.String(80), nullable=False)
#     age = db.Column(db.Integer, nullable=False)
#     phone_number = db.Column(db.String(10), unique=True, nullable=False)
#     e_mail = db.Column(db.String(120), nullable=False)
#     description = db.Column(db.Text)
#
#     def __repr__(self):
#         return '<Clients %r>' % self.name
#
#
# class Sсhedule(db.Model):
#     """ Класс Расписание получает из базы данных информацию о свободном времени   """
#
#     date = db.Column(db.String(10), primary_key=True)
#     time10 = db.Column(db.String(80), nullable=False)
#     time11 = db.Column(db.String(80), nullable=False)
#     time13 = db.Column(db.String(80), nullable=False)
#     time14 = db.Column(db.String(80), nullable=False)
#     time15 = db.Column(db.String(80), nullable=False)
#
#     def __repr__(self):
#         return '<Schedule %r>' % self.date
#
#     def __str__(self):
#         return f"Расписание на  " \
#                f"дату: {self.date}. " \
#                f"10-11: {self.time10}. " \
#                f"11-12: {self.time11}. " \
#                f"13-14: {self.time13}. " \
#                f"14-15: {self.time14}. " \
#                f"15-16: {self.time15}. "
