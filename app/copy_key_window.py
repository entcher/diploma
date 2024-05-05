from PyQt5.QtWidgets import QApplication, QPushButton, QMessageBox, QVBoxLayout, QWidget, QLabel


class CopyKeyWindow(QWidget):
    def __init__(self, key):
        super().__init__()

        self.key = key

        self.setWindowTitle('Copy Text Example')
        self.setGeometry(100, 100, 400, 200)

        key_label = QLabel(f'Ваш ключ доступа: {key}')

        copy_button = QPushButton('Нажмите, чтобы скопировать ключ')
        copy_button.clicked.connect(self.copy_button_clicked)

        layout = QVBoxLayout()
        layout.addWidget(key_label)
        layout.addWidget(copy_button)
        self.setLayout(layout)

    def copy_button_clicked(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.key)

        QMessageBox.information(self, 'Успешно', 'Текст успешно скопирован')
