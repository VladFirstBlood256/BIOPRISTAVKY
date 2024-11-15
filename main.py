import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QTextEdit, \
    QHBoxLayout, QStackedWidget, QMessageBox
from PyQt5.QtCore import Qt

# Базовый URL для взаимодействия с API
API_URL = "http://localhost:8000/api/users/"

# Функция для регистрации нового пользователя через API
def register_user(username, password, space1, space2, space3):
    data = {
        "username": username,
        "password": password,
        "space1": space1,
        "space2": space2,
        "space3": space3
    }
    # Отправляем POST запрос для регистрации пользователя
    response = requests.post(f"{API_URL}register/", json=data)

    if response.status_code == 201:  # 201 означает успешное создание
        return True
    else:
        return False

# Функция для получения данных пользователя через API
def get_user_data_by_username(username):
    response = requests.get(f"{API_URL}get_user_data/", params={"username": username})

    if response.status_code == 200:
        user_data = response.json()
        if user_data:
            print(user_data)
            return (
                user_data.get('username'),
                user_data.get('password'),
                user_data.get('space1'),
                user_data.get('space2'),
                user_data.get('space3')
            )
        else:
            return None
    else:
        return None

def is_ok(number):
    data = int(number)
    if data == 5:
        return "В норме"
    elif data < 5:
        return "Понижено"
    else:
        return "Повышено"

# Окно для регистрации и поиска пароля
class RegisterWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("DATA")
        self.setGeometry(300, 200, 400, 350)

        layout = QVBoxLayout()

        # Кнопка "Назад"
        back_button = QPushButton("Назад", self)
        back_button.clicked.connect(self.go_back)

        # Помещаем кнопку "Назад" в верхний правый угол с помощью QHBoxLayout
        back_layout = QHBoxLayout()
        back_layout.addWidget(back_button)
        back_layout.setAlignment(Qt.AlignRight)  # Выравнивание вправо
        layout.addLayout(back_layout)

        # Форма для ввода данных
        form_layout = QFormLayout()

        self.username_input = QLineEdit(self)
        self.password_input = QLineEdit(self)

        form_layout.addRow("Токен:", self.username_input)
        form_layout.addRow("IP:", self.password_input)

        layout.addLayout(form_layout)

        # Кнопка регистрации
        self.register_button = QPushButton("Зарегистрироваться", self)
        self.register_button.clicked.connect(self.register)

        layout.addWidget(self.register_button)

        # Кнопка для поиска пароля по логину
        self.search_button = QPushButton("Поиск IP", self)
        self.search_button.clicked.connect(self.search_password)

        layout.addWidget(self.search_button)

        # Поле для вывода пароля и других данных
        self.password_output = QTextEdit(self)
        self.password_output.setReadOnly(True)  # Только для чтения
        layout.addWidget(self.password_output)

        self.setLayout(layout)

    def register(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if username and password:
            # Регистрация пользователя в базе данных через API
            if register_user(username, password):
                self.show_message("Успех", "Пользователь зарегистрирован успешно!")
            else:
                self.show_message("Ошибка", "Пользователь с таким логином уже существует.")
        else:
            self.show_message("Ошибка", "Пожалуйста, заполните все поля.")

    def search_password(self):
        username = self.username_input.text()

        if username:
            # Поиск данных пользователя по логину через API
            user_data = get_user_data_by_username(username)
            if user_data:
                # Выводим все данные пользователя, включая пароли и space1, space2, space3
                user_info = f"IP: {user_data[1]}"
                self.password_output.setText(user_info)
            else:
                self.password_output.setText("Пользователь не найден.")
        else:
            self.password_output.setText("Пожалуйста, введите логин.")

    def show_message(self, title, text):
        QMessageBox.information(self, title, text)

    def go_back(self):
        # Возвращаемся в главное окно через родительский виджет (QStackedWidget)
        self.parent().setCurrentIndex(0)

# Окно входа
class LoginWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("DATA")
        self.setGeometry(300, 200, 400, 350)

        layout = QVBoxLayout()

        # Кнопка "Назад"
        back_button = QPushButton("Назад", self)
        back_button.clicked.connect(self.go_back)

        # Помещаем кнопку "Назад" в верхний правый угол с помощью QHBoxLayout
        back_layout = QHBoxLayout()
        back_layout.addWidget(back_button)
        back_layout.setAlignment(Qt.AlignRight)  # Выравнивание вправо
        layout.addLayout(back_layout)

        # Форма для ввода данных
        form_layout = QFormLayout()

        self.username_input = QLineEdit(self)

        # Кнопка для поиска пароля по логину
        self.search_button = QPushButton("Поиск", self)
        self.search_button.clicked.connect(self.search_password)

        layout.addWidget(self.search_button)

        # Поле для вывода пароля и других данных
        self.password_output = QTextEdit(self)
        self.password_output.setReadOnly(True)  # Только для чтения
        layout.addWidget(self.password_output)

        self.setLayout(layout)

    def search_password(self):
        username = self.username_input.text()


        if username:
            # Поиск данных пользователя по логину через API
            user_data = get_user_data_by_username(username)
            print(user_data[2])
            if user_data:
                # Выводим все данные пользователя, включая пароли и space1, space2, space3
                user_info = (f"IP: {user_data[1]}\n"
                             f"Space1: {user_data[2]}        {is_ok(user_data[2])}\n"
                             f"Space2: {user_data[3]}        {is_ok(user_data[3])}\n"
                             f"Space3: {user_data[4]}        {is_ok(user_data[4])}")

                self.password_output.setText(user_info)
            else:
                self.password_output.setText("Пользователь не найден.")
        else:
            self.password_output.setText("Пожалуйста, введите логин.")

    def show_message(self, title, text):
        QMessageBox.information(self, title, text)

    def go_back(self):
        # Возвращаемся в главное окно через родительский виджет (QStackedWidget)
        self.parent().setCurrentIndex(0)

# Главное окно
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Главное окно")
        self.setGeometry(300, 200, 400, 200)

        # Основной layout
        layout = QVBoxLayout()

        # Кнопка для открытия окна регистрации
        self.open_register_window_button = QPushButton("Регистрация пациента", self)
        self.open_register_window_button.clicked.connect(self.open_register_window)
        layout.addWidget(self.open_register_window_button)

        # Кнопка для выхода
        self.login_button = QPushButton("Войти", self)
        self.login_button.clicked.connect(self.close_and_open_login)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def open_register_window(self):
        # Переключаемся на окно регистрации
        self.parent().setCurrentIndex(1)

    def close_and_open_login(self):
        # Закрываем главное окно и открываем окно входа
        self.parent().setCurrentIndex(2)

# Основное приложение
class App(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Главное окно")
        self.setGeometry(300, 200, 400, 300)

        # Используем QStackedWidget для переключения между окнами
        self.stacked_widget = QStackedWidget(self)

        self.main_window = MainWindow()
        self.register_window = RegisterWindow(self)
        self.login_window = LoginWindow(self)

        self.stacked_widget.addWidget(self.main_window)
        self.stacked_widget.addWidget(self.register_window)
        self.stacked_widget.addWidget(self.login_window)

        layout = QVBoxLayout()
        layout.addWidget(self.stacked_widget)
        self.setLayout(layout)

    def show(self):
        self.stacked_widget.setCurrentIndex(0)  # Показываем главное окно при старте
        super().show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_app = App()  # Основное приложение, которое содержит QStackedWidget
    main_app.show()  # Показываем главное окно
    sys.exit(app.exec_())
