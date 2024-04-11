import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
    QPushButton,
    QStyle,
    QHBoxLayout,
    QMessageBox)


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Выберите набор упражнений')
        self.setGeometry(100, 100, 600, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(['Упражнения', 'Повторения'])
        self.init_table_data()
        self.table.cellChanged.connect(self.check_count_cell_value)

        self.moveUpButton = QPushButton()
        icon_arrow_up = self.style().standardIcon(QStyle.SP_TitleBarShadeButton)
        self.moveUpButton.setIcon(icon_arrow_up)
        self.moveUpButton.clicked.connect(self.move_up)

        self.moveDownButton = QPushButton()
        icon_arrow_down = self.style().standardIcon(QStyle.SP_TitleBarUnshadeButton)
        self.moveDownButton.setIcon(icon_arrow_down)
        self.moveDownButton.clicked.connect(self.move_down)

        self.startButton = QPushButton('Начать')

        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.addWidget(self.moveUpButton)
        self.buttons_layout.addWidget(self.moveDownButton)

        self.layout.addWidget(self.table)
        self.layout.addLayout(self.buttons_layout)
        self.layout.addWidget(self.startButton)

    def init_table_data(self):
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

    def move_up(self):
        currentRow = self.table.currentRow()
        if currentRow == 0:
            return

        self.table.insertRow(currentRow - 1)
        for column in range(self.table.columnCount()):
            self.table.setItem(currentRow - 1, column,
                               self.table.takeItem(currentRow + 1, column))
        self.table.removeRow(currentRow + 1)

    def move_down(self):
        currentRow = self.table.currentRow()
        if currentRow > self.table.rowCount() - 1:
            return

        self.table.insertRow(currentRow + 2)
        for column in range(self.table.columnCount()):
            self.table.setItem(currentRow + 2, column,
                               self.table.takeItem(currentRow, column))
        self.table.removeRow(currentRow)

    def check_count_cell_value(self, row, column):
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
