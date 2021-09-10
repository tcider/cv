# pip install pysqlite3
# pip install tk
# pip install fpdf


# Модуль реугялрных выражения для проверки маски почты
import re

# Модуль оконных функций
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

# Модуль экспорта в pdf
from fpdf import FPDF

# Модуль БД
from database import Database

# Глобальные константы
DB_NAME = "user.db"
VALIDATE_EMAIL = 1
VALIDATE_PASSWORD = 0


class App(tk.Tk):
    # Главный класс оконного модуля Tkinter

    def __init__(self):
        # Инициализиурем класс и отображаем окно логина

        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(LoginFrame)

    def switch_frame(self, frame_class):
        # Смена окна, при переключение с Логина на Регистрацию и обратно

        self.new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = self.new_frame
        self._frame.pack()


class LoginFrame(tk.Frame):
    # Окно логина/входа

    def __init__(self, master):
        # При инициализации окна расчитываем его размер и положение

        super().__init__(master)

        master.title("Вход")

        w = 220
        h = 120
        ws = master.winfo_screenwidth()
        hs = master.winfo_screenheight()
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        master.geometry('%dx%d+%d+%d' % (w, h, x, y))

        # Метки окна

        self.label_username = tk.Label(self, text="Логин")
        self.label_password = tk.Label(self, text="Пароль")

        # Поля ввода

        self.entry_username = tk.Entry(self)
        self.entry_password = tk.Entry(self, show="*")

        # Размещение меток и полей ввода в окне

        self.label_username.grid(row=0)
        self.label_password.grid(row=1)
        self.entry_username.grid(row=0, column=1)
        self.entry_password.grid(row=1, column=1)

        # Кнопка Входа

        self.logbtn = tk.Button(self, text="Войти", command=self.login_btn_clicked)
        self.logbtn.grid(row=3, column=0, sticky="ew")

        # Кнопка Регистрации пользователя

        self.create_new_user_button = tk.Button(self, text="Зарегистрироваться", command=lambda: master.switch_frame(SignUpFrame))
        self.create_new_user_button.grid(row=3, column=1, sticky="e")

        self.pack(expand=1)

    def login_btn_clicked(self):
        # Метод запускающийся при нажатии на кнопку

        # Получаем данные из полей ввода

        self.username = self.entry_username.get()
        self.password = self.entry_password.get()

        if len(self.username) == 0 and len(self.password) == 0:
            # Ошибка если не введены поля логина и пароля

            messagebox.showerror("Вход", "Введите логин и пароль")
        elif len(self.username) == 0:
            # Не введен логин

            messagebox.showerror("Вход", "Введите логин")
        elif len(self.password) == 0:
            # Не введен пароль

            messagebox.showerror("Вход", "Введите пароль")
        else:
            # Подключение к базе
            self.database = Database(DB_NAME)

            # Если база пустая - создаем таблицу
            self.database.create_user_table()

            # Получения записи о пользователе из базы
            self.check = self.database.retrieve_user(self.username)

            if self.check is None:
                # Ошибка - пользователь не найден

                messagebox.showerror("Ошибка входа", "Пользователя не существует")
            else:
                if self.username == self.check[3] and self.password == self.check[4]:
                    # Если авторизауия прошла успешно

                    #messagebox.showinfo("Login info", "Добро пожаловать " + self.check[0])
                    self.master.destroy()
                    root = tk.Tk()
                    MainFrame(root, self.check)
                    root.mainloop()

                else:
                    # Если пользователя не существует

                    messagebox.showerror("Ошибка входа", "Наверная пара логин - пароль")


class SignUpFrame(tk.Frame):
    # Форма регистрации

    def __init__(self, master):
        # Инициализация формы и вычисления ее размеров
        super().__init__(master)

        master.title("Регистрация")

        w = 220
        h = 190
        ws = master.winfo_screenwidth()
        hs = master.winfo_screenheight()
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        master.geometry('%dx%d+%d+%d' % (w, h, x, y))

        # Метки

        self.information_label = tk.Label(self, text="Все поля обязательны!")
        self.name_label = tk.Label(self, text="Имя")
        self.surname_label = tk.Label(self, text="Фамилия")
        self.email_label = tk.Label(self, text="Email")
        self.username_label = tk.Label(self, text="Логин")
        self.password_label = tk.Label(self, text="Пароль")

        # Поля

        self.name_entry = tk.Entry(self)
        self.surname_entry = tk.Entry(self)
        self.email_entry = tk.Entry(self)
        self.username_entry = tk.Entry(self)
        self.password_entry = tk.Entry(self, show="*")

        # Верстка

        self.information_label.grid(row=0, column=1, sticky="w")

        self.name_label.grid(row=1, column=0, sticky="w")
        self.name_entry.grid(row=1, column=1)

        self.surname_label.grid(row=2, column=0, sticky="w")
        self.surname_entry.grid(row=2, column=1)

        self.email_label.grid(row=3, column=0, sticky="w")
        self.email_entry.grid(row=3, column=1)

        self.username_label.grid(row=4, column=0, sticky="w")
        self.username_entry.grid(row=4, column=1)

        self.password_label.grid(row=5, column=0, sticky="w")
        self.password_entry.grid(row=5, column=1)

        # Кнопки

        self.return_button = tk.Button(self, text="Отмена", command=lambda: master.switch_frame(LoginFrame))
        self.return_button.grid(row=7, column=0, sticky="w")

        self.submit_button = tk.Button(self, text="Регистрация", command=self.createUser)
        self.submit_button.grid(row=7, column=1, sticky="e")

        self.pack(expand=1)


    def createUser(self):
        # Вставка пользователя в базу

        # Получем данные из формы регистрации

        self.name_entry_content = self.name_entry.get()
        self.surname_entry_content = self.surname_entry.get()
        self.username_entry_content = self.username_entry.get()
        self.password_entry_content = self.password_entry.get()
        self.email_entry_content = self.email_entry.get()

        if self.validate_data(self.name_entry_content, self.surname_entry_content,
                              self.username_entry_content, self.password_entry_content,
                              self.email_entry_content):
            # Валидируем введенные данные

            # Создаем таблицу если база пуста
            self.database.create_user_table()

            self.database.insert_row(self.name_entry_content, self.surname_entry_content, self.username_entry_content,
                                     self.password_entry_content, self.email_entry_content)
            messagebox.showinfo("Регистрация", "Пользователь зарегистрирован")
            self.master.switch_frame(LoginFrame)

    def validate_data(self,
                      name, surname,
                      username, password,
                      email):
        # Метод валидирующий данные

        if self.validate_name(name) and self.validate_surname(surname) and self.validate_email(
                email) and self.validate_username(username) and self.validate_password(password):
            return True

    def validate_name(self, name):
        # Валидация имени

        if len(name) == 0:
            messagebox.showerror("Регистрация", "Введите Имя")
        else:
            return True

    def validate_surname(self, surname):
        # Валидация фамилии

        if len(surname) == 0:
            messagebox.showerror("Регистрация", "Введите фамилию")
        else:
            return True

    def validate_password(self, password):
        # Валидация пароля по 2-м уровням

        # Проверка на размер
        if len(password) == 0:
            messagebox.showerror("Регистрация", "Введите пароль")

        # Если включена константа VALIDATE_PASSWORD пароль валидируется на сложность
        elif VALIDATE_PASSWORD:
            if len(password) < 8:
                messagebox.showerror("Регистрация", "Пароль должен быть более чем 8 символов")
            elif not re.search(r"[A-Z]", password):
                messagebox.showerror("Регистрация", "Пароль должен содержать заглавные буквы")
            elif not re.search(r"[!@#]", password):
                messagebox.showerror("Регистрация", "Пароль должен содержать символ кроме букв")
            else:
                return True
        else:
            return True

    def validate_username(self, username):
        # Валидация пользователя

        if len(username) == 0:
            messagebox.showerror("Регистрация", "Пожалуйста введите имя пользователя")
        else:
            self.database = Database(DB_NAME)
            if self.database.retrieve_user(username) == None:
                return True
            else:
                messagebox.showerror("Регистрация", "Такой пользователь уже существует")
                return False

    def validate_email(self, email):
        # Валидация адреса электронной почты

        if len(email) == 0:
            # Проверка на пустоту поля

            messagebox.showerror("Регистрация", "Укажите адрес электронной почты")
        elif not VALIDATE_EMAIL:
            return True
        else:
            if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
                # Проверка по маске электронного ящика

                return True
            else:
                messagebox.showerror("Регистрация", "Почтовый адрес не верен")
                return False


class MainFrame(tk.Frame):
# Главное окно программы

    def __init__(self, master, userinfo):
        # При инициализации окна расчитываем его размер и положение

        super().__init__(master)

        master.title("Резюме")

        self.login = userinfo[3]
        self.database = Database(DB_NAME)

        w = 680
        h = 680
        ws = master.winfo_screenwidth()
        hs = master.winfo_screenheight()
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        master.geometry('%dx%d+%d+%d' % (w, h, x, y))

        # Метки окна

        self.label_username = tk.Label(self, text="ФИО")
        self.label_userbd = tk.Label(self, text="Дата рождения")
        self.label_usercity = tk.Label(self, text="Город")
        self.label_usermail = tk.Label(self, text="email")
        self.label_userphone = tk.Label(self, text="Телефон")
        self.label_userstudy = tk.Label(self, text="Образование")
        self.label_userjob = tk.Label(self, text="Опыт работы")
        self.label_userskill = tk.Label(self, text="Навыки/Умения")
        self.label_userother = tk.Label(self, text="Дополнительно")

        # Поля ввода

        self.entry_username = tk.Entry(self, width=93)
        self.entry_userbd = tk.Entry(self, width=93)
        self.entry_usercity = tk.Entry(self, width=93)
        self.entry_usermail = tk.Entry(self, width=93)
        self.entry_userphone = tk.Entry(self, width=93)
        self.entry_userstudy = tk.Text(self, width=70, height=8)
        self.entry_userjob = tk.Text(self, width=70, height=8)
        self.entry_userskill = tk.Text(self, width=70, height=8)
        self.entry_userother = tk.Text(self, width=70, height=8)

        # Заполняем значения полей данными которые есть

        self.cv = self.database.retrieve_cv(self.login)

        if self.cv is None:
            # Если резюме ще нет то заполянем даннеы из таблицы Логинов

            self.entry_username.insert(0, userinfo[1] + " " + userinfo[0])
            self.entry_usermail.insert(0, userinfo[2])
            # Флаг инидцирует, что резюме пользователя в БД еще нет
            self.flag = 0
        else:
            self.entry_username.insert(0, self.cv[1])
            self.entry_userbd.insert(0, self.cv[2])
            self.entry_usercity.insert(0, self.cv[3])
            self.entry_usermail.insert(0, self.cv[4])
            self.entry_userphone.insert(0, self.cv[5])
            self.entry_userstudy.insert("1.0", self.cv[6])
            self.entry_userjob.insert("1.0", self.cv[7])
            self.entry_userskill.insert("1.0", self.cv[8])
            self.entry_userother.insert("1.0", self.cv[9])
            # Флаг инидцирует, что резюме пользователя уже есть в БД
            self.flag = 1


        # Размещение меток и полей ввода в окне

        self.label_username.grid(row=0, column=0, sticky="w")
        self.label_userbd.grid(row=1, column=0, sticky="w")
        self.label_usercity.grid(row=2, column=0, sticky="w")
        self.label_usermail.grid(row=3, column=0, sticky="w")
        self.label_userphone.grid(row=4, column=0, sticky="w")
        self.label_userstudy.grid(row=5, column=0, sticky="w")
        self.label_userjob.grid(row=6, column=0, sticky="w")
        self.label_userskill.grid(row=7, column=0, sticky="w")
        self.label_userother.grid(row=8, column=0, sticky="w")


        self.entry_username.grid(row=0, column=1)
        self.entry_userbd.grid(row=1, column=1)
        self.entry_usercity.grid(row=2, column=1)
        self.entry_usermail.grid(row=3, column=1)
        self.entry_userphone.grid(row=4, column=1)
        self.entry_userstudy.grid(row=5, column=1)
        self.entry_userjob.grid(row=6, column=1)
        self.entry_userskill.grid(row=7, column=1)
        self.entry_userother.grid(row=8, column=1)

        # Кнопка Сохранить

        self.savebtn = tk.Button(self, text="Сохранить", command=self.save_btn_clicked)
        self.savebtn.grid(row=9, column=0, sticky="ew")

        # Кнопка Выгрузить

        self.expbtn = tk.Button(self, text="Выгрузить в pdf", command=self.export_btn_clicked)
        self.expbtn.grid(row=9, column=1, sticky="ew")

        self.pack(expand=1)


    def save_btn_clicked(self):
        # Метод запускающийся при нажатии на кнопку Сохранить

        self.username = self.entry_username.get()
        self.userbd = self.entry_userbd.get()
        self.usercity = self.entry_usercity.get()
        self.usermail = self.entry_usermail.get()
        self.userphone = self.entry_userphone.get()
        self.userstudy = self.entry_userstudy.get("1.0", 'end')
        self.userjob = self.entry_userjob.get("1.0", 'end')
        self.userskill = self.entry_userskill.get("1.0", 'end')
        self.userother = self.entry_userother.get("1.0", 'end')

        if self.flag:
            self.database.update_cv(self.login, self.username, self.userbd, self.usercity, self.usermail,
                                    self.userphone, self.userstudy, self.userjob, self.userskill, self.userother)
            messagebox.showinfo("Резюме обновлено", "Резюме обновлено")
        else:
            self.database.insert_cv(self.login, self.username, self.userbd, self.usercity, self.usermail, self.userphone, self.userstudy, self.userjob, self.userskill, self.userother)
            messagebox.showinfo("Резюме сохранено", "Резюме сохранено")


    def export_btn_clicked(self):
        # Метод запускающийся при нажатии на кнопку Выгрузить

        self.username = self.entry_username.get()
        self.userbd = self.entry_userbd.get()
        self.usercity = self.entry_usercity.get()
        self.usermail = self.entry_usermail.get()
        self.userphone = self.entry_userphone.get()
        self.userstudy = self.entry_userstudy.get("1.0", 'end')
        self.userjob = self.entry_userjob.get("1.0", 'end')
        self.userskill = self.entry_userskill.get("1.0", 'end')
        self.userother = self.entry_userother.get("1.0", 'end')

        pdf = FPDF(orientation='P', unit='mm', format='A4')
        # Add a DejaVu Unicode font (uses UTF-8)
        pdf.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
        pdf.add_page()
        pdf.set_font('DejaVu', '', 16)
        pdf.cell(200, 10, txt="РЕЗЮМЕ", ln=1, align="C")
        pdf.set_font('DejaVu', '', 12)
        pdf.cell(200, 10,
                 txt=f"Имя: {self.username}",
                 ln=1, align="L")
        pdf.cell(200, 10,
                 txt=f"Дата рождения: {self.userbd}",
                 ln=1, align="L")
        pdf.cell(200, 10,
                 txt=f"Город: {self.usercity}",
                 ln=1, align="L")
        pdf.cell(200, 10,
                 txt=f"Email: {self.usermail}",
                 ln=1, align="L")
        pdf.cell(200, 10,
                 txt=f"Телефон: {self.userphone}",
                 ln=1, align="L")
        pdf.set_font('DejaVu', '', 16)
        pdf.cell(200, 10, txt="Образование", ln=1, align="C")
        pdf.set_font('DejaVu', '', 12)
        for elem in self.userstudy.split("\n"):
            pdf.cell(200, 10, txt=f"{elem}", ln=1, align="L")
        pdf.set_font('DejaVu', '', 16)
        pdf.cell(200, 10, txt="Опыт работы", ln=1, align="C")
        pdf.set_font('DejaVu', '', 12)
        for elem in self.userjob.split("\n"):
            pdf.cell(200, 10, txt=f"{elem}", ln=1, align="L")
        pdf.set_font('DejaVu', '', 16)
        pdf.cell(200, 10, txt="Навыки/Умения", ln=1, align="C")
        pdf.set_font('DejaVu', '', 12)
        for elem in self.userskill.split("\n"):
            pdf.cell(200, 10, txt=f"{elem}", ln=1, align="L")
        pdf.set_font('DejaVu', '', 16)
        pdf.cell(200, 10, txt="Дополнительно", ln=1, align="C")
        pdf.set_font('DejaVu', '', 12)
        for elem in self.userother.split("\n"):
            pdf.cell(200, 10, txt=f"{elem}", ln=1, align="L")

        pdf.output("cv.pdf")
        messagebox.showinfo("Резюме экспортировано в cv.pdf", "Резюме экспортировано в cv.pdf")


def main():
    login = App()
    login.mainloop()


if __name__ == "__main__":
    main()