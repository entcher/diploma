import os
import json
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton


class SaveNewSetWindow(QWidget):
    close_signal = pyqtSignal()

    def __init__(self, exercises):
        super().__init__()

        self.setWindowTitle('Сохранение комплекса')
        self.setGeometry(100, 100, 500, 100)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.label = QLabel('Введите название комплекса')
        self.input = QLineEdit()

        self.save_button = QPushButton('Сохранить')
        self.save_button.clicked.connect(
            lambda: self.save_button_clicked(exercises))
        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(self.save_button, alignment=Qt.AlignRight)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.input)
        self.layout.addWidget(self.save_button)

    def save_button_clicked(self, exercises: dict[str, int]):
        path = 'saved_sets.json'
        name = self.input.text()

        json_data = {}
        if os.path.exists(path):
            with open(path, 'r') as json_file:
                json_data = json.load(json_file)
            json_data.pop(name, None)

        json_data[name] = exercises
        with open(path, 'w') as json_file:
            json.dump(json_data, json_file, indent=4, ensure_ascii=False)

        self.close()

    def closeEvent(self, _):
        self.close_signal.emit()
