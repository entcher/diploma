import os
import re
from io import BytesIO
import zipfile
import requests
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox,
)


class SyncDataWindow(QWidget):
    def __init__(self, selected_user: str):
        super().__init__()

        self.selected_user = selected_user

        self.setWindowTitle('Синхронизация данных')
        self.setGeometry(100, 100, 500, 100)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.label = QLabel('Введите ключ или оставьте поле пустым, чтобы получить новый ключ')
        self.input = QLineEdit()

        self.download_button = QPushButton('Загрузить данные с сервера')
        self.download_button.clicked.connect(self.download_button_clicked)

        self.upload_button = QPushButton('Сохранить текущие данные на сервер')
        self.upload_button.clicked.connect(self.upload_button_clicked)

        self.update_button = QPushButton('Обновить существующие данные на сервере')
        self.update_button.clicked.connect(self.update_button_clicked)

        self.delete_button = QPushButton('Удалить данные с сервера')
        self.delete_button.clicked.connect(self.delete_button_clicked)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.input)
        self.layout.addWidget(self.download_button)
        self.layout.addWidget(self.upload_button)
        self.layout.addWidget(self.update_button)
        self.layout.addWidget(self.delete_button)

    def download_button_clicked(self):
        key = self.input.text()
        if key == '':
            QMessageBox.critical(None, 'Ошибка', 'Невозможно получить ваши данные без ключа')
            return

        url = 'http://localhost:3000'
        params = {'key': key}
        response = requests.get(url, params)
        if response.status_code == 200:
            path = os.path.join('users', self.selected_user)
            with zipfile.ZipFile(BytesIO(response.content)) as unzipper:
                unzipper.extractall(path)
            QMessageBox.information(None, 'Успешно', 'Ваши данные успешно обновлены')
            self.close()
        else:
            QMessageBox.critical(
                None, 'Ошибка', f'{response.text}\nКод ошибки: {response.status_code}'
            )

    def upload_button_clicked(self):
        key = self.input.text()
        if key == '':
            QMessageBox.critical(None, 'Ошибка', 'Невозможно получить ваши данные без ключа')
            return
        elif not validate_filename(key):
            QMessageBox.critical(None, 'Ошибка', 'Ключ должен состоять из цифр, букв и точек')
            return

        buffer = BytesIO()
        user_directory = os.path.join('users', self.selected_user)
        files_names = os.listdir(user_directory)
        with zipfile.ZipFile(buffer, 'w') as zipper:
            for file_name in files_names:
                file_path = os.path.join(user_directory, file_name)
                with open(file_path, 'r') as f:
                    file_content = f.read()
                    zipper.writestr(file_name, file_content)

        url = 'http://localhost:3000'
        params = {'key': key}
        response = requests.post(
            url, files={'file': ('file.zip', buffer.getvalue(), 'application/zip')}, params=params
        )

        if response.status_code == 200:
            QMessageBox.information(None, 'Успех', 'Фалы успешно сохранены')
        elif response.status_code == 404:
            QMessageBox.critical(None, 'Ошибка', 'Сохранений по данному ключу не найдено')
        else:
            QMessageBox.critical(
                None, 'Ошибка', f'{response.text}\nКод ошибки: {response.status_code}'
            )

    def update_button_clicked(self):
        key = self.input.text()
        if key == '':
            QMessageBox.critical(None, 'Ошибка', 'Невозможно обновить ваши данные без ключа')
            return

        buffer = BytesIO()
        user_directory = os.path.join('users', self.selected_user)
        files_names = os.listdir(user_directory)
        with zipfile.ZipFile(buffer, 'w') as zipper:
            for file_name in files_names:
                file_path = os.path.join(user_directory, file_name)
                with open(file_path, 'r') as f:
                    file_content = f.read()
                    zipper.writestr(file_name, file_content)

        url = 'http://localhost:3000'
        params = {'key': key}
        response = requests.put(
            url, files={'file': ('file.zip', buffer.getvalue(), 'application/zip')}, params=params
        )
        if response.status_code == 202:
            QMessageBox.information(None, 'Успех', 'Данные успешно обновлены')
        else:
            QMessageBox.critical(
                None, 'Ошибка', f'{response.text}\nКод ошибки: {response.status_code}'
            )

    def delete_button_clicked(self):
        key = self.input.text()
        if key == '':
            QMessageBox.critical(None, 'Ошибка', 'Невозможно удалить ваши данные без ключа')
            return

        url = 'http://localhost:3000'
        params = {'key': key}
        response = requests.delete(url, params=params)
        if response.status_code == 202:
            QMessageBox.information(None, 'Успех', 'Данные успешно удалены')
        else:
            QMessageBox.critical(
                None, 'Ошибка', f'{response.text}\nКод ошибки: {response.status_code}'
            )


def validate_filename(s: str):
    pattern = r'^[a-zA-Zа-яА-Я0-9.]+$'
    return bool(re.match(pattern, s))
