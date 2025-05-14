from PyQt5 import QtWidgets, QtCore
import requests
from PyQt5.QtWidgets import QMessageBox


class LoginWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Вход")
        self.setFixedSize(300, 200)
        self.api_url = "http://127.0.0.1:8000/api"
        self.is_admin = False
        layout = QtWidgets.QVBoxLayout()

        self.username_input = QtWidgets.QLineEdit()
        self.username_input.setPlaceholderText("Логин")

        self.password_input = QtWidgets.QLineEdit()
        self.password_input.setPlaceholderText("Пароль")
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)

        self.login_button = QtWidgets.QPushButton("Войти")
        self.login_button.clicked.connect(self.handle_login)

        self.register_button = QtWidgets.QPushButton("Регистрация")
        self.register_button.clicked.connect(self.open_register_window)

        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        layout.addWidget(self.register_button)

        self.setLayout(layout)

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if not username or not password:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Заполните все поля!")
            return

        try:
            response = requests.get(f"{self.api_url}/client/?client_login={username}")
            if response.status_code == 200:
                data = response.json()
                if data["password"] == password:
                    self.is_admin = data.get("is_superuser", False)
                    QtWidgets.QMessageBox.information(self, "Успех", "Вход выполнен!")
                    self.accept()
                else:
                    QtWidgets.QMessageBox.warning(self, "Ошибка", "Неверный логин или пароль!")
            else:
                self.show_error(f"Ошибка: {response.status_code}")
        except Exception as e:
            self.show_error(f"Не удалось подключиться к серверу: {str(e)}")


    def open_register_window(self):
        self.register_window = RegisterWindow()
        self.register_window.exec_()

    def show_error(self, message):
        QMessageBox.critical(self, "Ошибка", message)


class RegisterWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Регистрация")
        self.setFixedSize(300, 250)

        layout = QtWidgets.QVBoxLayout()

        self.api_url = "http://127.0.0.1:8000/api"

        self.username_input = QtWidgets.QLineEdit()
        self.username_input.setPlaceholderText("Логин")

        self.fio_input = QtWidgets.QLineEdit()
        self.fio_input.setPlaceholderText("ФИО")

        self.password_input = QtWidgets.QLineEdit()
        self.password_input.setPlaceholderText("Пароль")
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)

        self.register_button = QtWidgets.QPushButton("Зарегистрироваться")
        self.register_button.clicked.connect(self.handle_register)

        layout.addWidget(self.username_input)
        layout.addWidget(self.fio_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.register_button)

        self.setLayout(layout)

    def handle_register(self):
        username = self.username_input.text()
        password = self.password_input.text()
        fio = self.fio_input.text()


        if not username or not password:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Логин и пароль обязательны!")
            return

        try:
            data_to_send = {
                "login": username,
                "password": password,
                "fio": fio
            }
            response = requests.post(
                f"{self.api_url}/client/",
                json = data_to_send
            )
            if response.status_code == 201:
                QtWidgets.QMessageBox.information(self, "Успех", "Пользователь зарегистрирован!")
                self.accept()
            else:
                self.show_error(f"Ошибка: {response.status_code}")
        except Exception as e:
            self.show_error(f"Ошибка: {str(e)}")

    def show_error(self, message):
        QMessageBox.critical(self, "Ошибка", message)