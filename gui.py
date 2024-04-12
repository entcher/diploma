from detector import show_cam
from PyQt5.QtCore import Qt, QItemSelectionModel
from PyQt5.QtWidgets import (
    QMainWindow,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
    QPushButton,
    QStyle,
    QHBoxLayout,
    QMessageBox)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Выберите набор упражнений')
        self.setGeometry(100, 100, 450, 500)
        self.setFixedSize(450, 500)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setColumnWidth(0, 200)
        self.table.setColumnWidth(1, 200)
        self.table.setHorizontalHeaderLabels(['Упражнения', 'Повторения'])
        self.init_table()
        self.table.cellChanged.connect(self.check_count_cell_value)

        self.move_up_button = QPushButton()
        icon_arrow_up = self.style().standardIcon(QStyle.SP_TitleBarShadeButton)
        self.move_up_button.setIcon(icon_arrow_up)
        self.move_up_button.clicked.connect(self.move_up)

        self.move_down_button = QPushButton()
        icon_arrow_down = self.style().standardIcon(QStyle.SP_TitleBarUnshadeButton)
        self.move_down_button.setIcon(icon_arrow_down)
        self.move_down_button.clicked.connect(self.move_down)

        self.start_button = QPushButton('Начать')
        self.start_button.clicked.connect(self.start_workout)

        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.addWidget(self.move_up_button)
        self.buttons_layout.addWidget(self.move_down_button)

        self.layout.addWidget(self.table)
        self.layout.addLayout(self.buttons_layout)
        self.layout.addWidget(self.start_button)

    def init_table(self):
        exercises_names = ['Сгибания в локтях',
                           'Приседания', 'Наклоны', 'Отжимания']
        for exercise in exercises_names:
            row = self.table.rowCount()
            self.table.insertRow(row)

            exercise_cell = QTableWidgetItem(exercise)
            exercise_cell.setFlags(exercise_cell.flags() ^ Qt.ItemIsEditable)
            self.table.setItem(row, 0, exercise_cell)

            count_cell = QTableWidgetItem('0')
            self.table.setItem(row, 1, count_cell)

    def get_table_data(self) -> dict[str, int]:
        exercises = {}
        for row in range(self.table.rowCount()):
            ex_name = self.table.item(row, 0).text()
            ex_count = int(self.table.item(row, 1).text())
            if ex_count > 0:
                exercises[ex_name] = ex_count
        return exercises

    def move_up(self):
        selected_row = self.table.currentRow()
        if selected_row == 0:
            return

        self.table.insertRow(selected_row - 1)
        for column in range(self.table.columnCount()):
            self.table.setItem(selected_row - 1, column,
                               self.table.takeItem(selected_row + 1, column))
        self.table.removeRow(selected_row + 1)
        self.table.selectRow(selected_row - 1)

    def move_down(self):
        selected_row = self.table.currentRow()
        if selected_row > self.table.rowCount() - 1:
            return

        self.table.insertRow(selected_row + 2)
        for column in range(self.table.columnCount()):
            self.table.setItem(selected_row + 2, column,
                               self.table.takeItem(selected_row, column))
        self.table.removeRow(selected_row)
        self.table.selectRow(selected_row + 1)

    def check_count_cell_value(self, row, column):
        if column == 0:
            return

        item = self.table.item(row, column)
        if item is None:
            return

        try:
            value = int(item.text())
            if value < 0:
                item.setText('0')
                QMessageBox.information(
                    None, 'Ошибка', 'Введите положительное число')
        except ValueError:
            item.setText('0')
            QMessageBox.information(
                None, 'Ошибка', 'Введите положительное число')

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

    def start_workout(self):
        exercises = self.get_table_data()
        if any(value > 0 for value in exercises.values()):
            show_cam(exercises)
        else:
            QMessageBox.warning(
                None, 'Ошибка', 'Не выбрано ни одно упражнение')
