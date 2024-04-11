from detector import show
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator, QFont
from PyQt5.QtWidgets import QPushButton, QLabel, QLineEdit, QFormLayout, QWidget, QComboBox, QMessageBox


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.choose_label = QLabel('Выберите набор упражнений', self)

        exercises_names = ['Сгибания в локтях', 'Приседания', 'Наклоны', 'Отжимания']
        self.exercises = self.init_exercises_gui(exercises_names)

        self.start_button = QPushButton('Начать тренировку', self)
        self.start_button.clicked.connect(
            lambda: self.start_workout(self.exercises))

        self.set_of_exercises_label = QLabel('Готовые комплексы упражнений')
        self.set_of_exercises = QComboBox()
        set_of_exercises_items = ['Свой', 'Утренний', 'Дневной', 'Ночной']
        self.set_of_exercises.addItems(set_of_exercises_items)
        self.set_of_exercises.currentIndexChanged.connect(self.on_set_changed)

        layout = QFormLayout()
        layout.addWidget(self.choose_label)
        for ex_label, ex_input in self.exercises.items():
            layout.addRow(ex_label, ex_input)
        layout.addWidget(self.start_button)
        layout.addWidget(self.set_of_exercises_label)
        layout.addWidget(self.set_of_exercises)

        self.setLayout(layout)
        self.setWindowTitle('Контроль упражнений')
        self.setGeometry(100, 100, 300, 100)

    def init_exercises_gui(self, names):
        exercises = {}
        for name in names:
            label = QLabel(name)
            input = QLineEdit()
            input.setValidator(QIntValidator(0, 2147483647))
            input.setAlignment(Qt.AlignmentFlag.AlignRight)
            input.setFont(QFont('Calibri', 20))
            input.setText('0')
            exercises[label] = input
        return exercises

    def start_workout(self, exercises):
        if all(value.text() == '0' for value in exercises.values()):
            QMessageBox.warning(None, 'Ошибка', 'Не выбрано ни одно упражнение')
            return
        show(exercises)

    def on_set_changed(self):
        selected_set = self.set_of_exercises.currentText()
        match selected_set:
            case 'Свой':
                self.set_exercises()
            case 'Утренний':
                self.set_exercises(squats=10, bends=10, pushups=5)
            case 'Дневной':
                self.set_exercises(squats=20, bends=10, pushups=10)
            case 'Ночной':
                self.set_exercises(squats=2, bends=10)

    def set_exercises(self, curls=0, squats=0, bends=0, pushups=0):
        for ex_label, ex_input in self.exercises.items():
            match ex_label.text():
                case 'Сгибания в локтях':
                    ex_input.setText(str(curls))
                case 'Приседания':
                    ex_input.setText(str(squats))
                case 'Наклоны':
                    ex_input.setText(str(bends))
                case 'Отжимания':
                    ex_input.setText(str(pushups))
