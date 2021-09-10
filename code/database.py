# Работаем с sqlite для максимальной переносимости программы
# self.database можно инициализировать любым сокетом sql базы данных
import sqlite3


class Database():
    # Класс sql запросов в кабзе данных

    def __init__(self, database_name):
        # При инициализации в качестве аргумента принимает имя файла с базой данных.
        # Создает саму базу и вызывает метод создания таблицы пользователей.

        self.database = sqlite3.connect(database_name)
        self.cursor = self.database.cursor()
        self.create_user_table()
        self.create_cv_table()

    def create_user_table(self):
        # Метод создания таблицы пользователей
        # Name, Surname, Email - референсные поля с данными пользователя
        # Username, Password - ключевые поля для авторизации

        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS usernames (Name text, Surname text, Email text, Username text, Password text)''')
        self.database.commit()

    def create_cv_table(self):
        # Метод создания таблицы с резюме

        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS cv (Username text, Name text, Bd text, City text, Email text, Phone text, Study text, Job text, Skill test, Other text)''')
        self.database.commit()

    def insert_row(self, name, surname, username, password, email):
        # Метод добавления новой записи в таблицу пользователей

        self.cursor.execute('''INSERT INTO usernames (Name,Surname,Username,Password,Email) values (?,?,?,?,?)''',
                            (name, surname, username, password, email))
        self.database.commit()

    def insert_cv(self, username, name, bd, city, email, phone, study, job, skill, other):
        # Метод добавления новой записи в таблицу резюме

        self.cursor.execute('''INSERT INTO cv (Username, Name, Bd, City, Email, Phone, Study, Job, Skill, Other) values (?,?,?,?,?,?,?,?,?,?)''',
                            (username, name, bd, city, email, phone, study, job, skill, other))
        self.database.commit()

    def retrieve_user(self, username):
        # Метод получения пользователя по его логину

        self.data = self.cursor.execute('''SELECT * FROM usernames WHERE Username = ?''', (username,))
        for row in self.data:
            return row

    def retrieve_cv(self, username):

        self.data = self.cursor.execute('''SELECT * FROM cv WHERE Username = ?''', (username,))
        for row in self.data:
            return row

    def delete_user(self, username):
        # Метод удаления пользователя по его логину

        self.cursor.execute('''DELETE FROM usernames WHERE Username = ?''', (username,))
        self.database.commit()

    def update_user(self, username, name=None, surname=None, password=None, email=None):
        # Метод изменения данных пользователя

        if name:
            self.cursor.execute('''UPDATE usernames SET Name = ?''', (name,))
            self.database.commit()
        if surname:
            self.cursor.execute('''UPDATE usernames SET Surname = ?''', (surname,))
            self.database.commit()
        if password:
            self.cursor.execute('''UPDATE usernames SET Password = ?''', (password,))
            self.database.commit()
        if email:
            self.cursor.execute('''UPDATE usernames SET Email = ?''', (email,))
            self.database.commit()

    def update_cv(self, username, name=None, bd=None, city=None, email=None, phone=None, study=None, job=None, skill=None, other=None):
        # Метод изменения резюме пользователя

        if name:
            self.cursor.execute('''UPDATE cv SET Name = ?''', (name,))
            self.database.commit()
        if bd:
            self.cursor.execute('''UPDATE cv SET Bd = ?''', (bd,))
            self.database.commit()
        if city:
            self.cursor.execute('''UPDATE cv SET City = ?''', (city,))
            self.database.commit()
        if email:
            self.cursor.execute('''UPDATE cv SET Email = ?''', (email,))
            self.database.commit()
        if phone:
            self.cursor.execute('''UPDATE cv SET Phone = ?''', (phone,))
            self.database.commit()
        if study:
            self.cursor.execute('''UPDATE cv SET Study = ?''', (study,))
            self.database.commit()
        if job:
            self.cursor.execute('''UPDATE cv SET Job = ?''', (job,))
            self.database.commit()
        if skill:
            self.cursor.execute('''UPDATE cv SET Skill = ?''', (skill,))
            self.database.commit()
        if other:
            self.cursor.execute('''UPDATE cv SET Other = ?''', (other,))
            self.database.commit()