import os
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox,
)


class AddUserWindow(QWidget):
    close_signal = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.setWindowTitle('Добавление нового пользователя')
        self.setGeometry(100, 100, 500, 100)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.label = QLabel('Введите имя пользователя')
        self.input = QLineEdit()

        self.save_button = QPushButton('Сохранить')
        self.save_button.clicked.connect(self.save_button_clicked)
        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.save_button, alignment=Qt.AlignRight)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.input)
        self.layout.addWidget(self.save_button)

    def save_button_clicked(self):
        username = self.input.text()
        users = os.listdir('users')
        if username in users:
            QMessageBox.warning(None, 'Ошибка', 'Пользователь уже существует\nВведите другое имя')
            return

        try:
            os.mkdir(f'users/{username}')
            QMessageBox.information(None, 'Успешно', 'Пользователь успешно добавлен')
            self.close()
        except:
            QMessageBox.warning(None, 'Ошибка', 'Выберите другое имя пользователя')

    def closeEvent(self, _):
        self.close_signal.emit()
