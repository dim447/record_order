class Client:
    '''Описание класса клиент'''

    def __init__(self, name, surname, age, phone_number, email):
        self.name = name
        self.surname = surname
        self.age = age
        self.phone_number = phone_number
        self.email = email

    def add_client(self, *args):
        pass

    def record_consult(self):
        print('Вы записались на консультацию')

    def __str__(self):
        return f'Имя: {self.name}\n' \
               f'Фамилия: {self.surname}\n' \
               f'Возраст: {self.age}\n' \
               f'Номер телефона: {self.phone_number}\n' \
               f'e-mail: {self.email}\n'


ivan = Client('Иван', 'Иванов', 12, '89009009000', 'client@gmail.com')
print(ivan)
ivan.record_consult()
