import os
import json
from video_gui import VideoWindow
from workout import exercises_names
from save_new_set_window import SaveNewSetWindow
from add_user_window import AddUserWindow
from sync_data_window import SyncDataWindow
from stats import show_stats
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
    QPushButton,
    QLabel,
    QStyle,
    QHBoxLayout,
    QComboBox,
    QMessageBox,
)


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

        self.set_of_users_label = QLabel('Выберите пользователя')
        self.set_of_users = QComboBox()
        self.load_users()
        self.add_user_button = QPushButton('Добавить пользователя')
        self.add_user_button.clicked.connect(self.add_user)
        self.remove_user_button = QPushButton('Удалить пользователя')
        self.remove_user_button.clicked.connect(self.remove_user)

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

        self.set_of_exercises_label = QLabel('Выберите комплекс упражнений')
        self.set_of_exercises = QComboBox()
        self.load_sets()
        self.set_of_exercises.currentIndexChanged.connect(self.on_set_changed)

        self.save_set_button = QPushButton('Сохранить')
        self.save_set_button.clicked.connect(self.on_save_set_click)

        self.delete_set_button = QPushButton('Удалить')
        self.delete_set_button.clicked.connect(self.on_delete_set_click)

        self.stats_button = QPushButton('Показать статистику')
        self.stats_button.clicked.connect(self.on_show_stats_click)
        self.sync_button = QPushButton('Синхронизировать данные')
        self.sync_button.clicked.connect(self.sync_button_clicked)

        self.start_button = QPushButton('Начать')
        self.start_button.clicked.connect(self.open_video_window)

        self.users_layout = QHBoxLayout()
        self.users_layout.addWidget(self.set_of_users)
        self.users_layout.addWidget(self.add_user_button)
        self.users_layout.addWidget(self.remove_user_button)

        self.up_down_buttons_layout = QHBoxLayout()
        self.up_down_buttons_layout.addWidget(self.move_up_button)
        self.up_down_buttons_layout.addWidget(self.move_down_button)

        self.set_save_layout = QHBoxLayout()
        self.set_save_layout.addWidget(self.set_of_exercises)
        self.set_save_layout.addWidget(self.save_set_button)
        self.set_save_layout.addWidget(self.delete_set_button)

        self.stats_sync_layout = QHBoxLayout()
        self.stats_sync_layout.addWidget(self.stats_button)
        self.stats_sync_layout.addWidget(self.sync_button)

        self.layout.addWidget(self.set_of_users_label)
        self.layout.addLayout(self.users_layout)
        self.layout.addWidget(self.table)
        self.layout.addLayout(self.up_down_buttons_layout)
        self.layout.addWidget(self.set_of_exercises_label)
        self.layout.addLayout(self.set_save_layout)
        self.layout.addLayout(self.stats_sync_layout)
        self.layout.addWidget(self.start_button)

    def init_table(self):
        for exercise in exercises_names:
            row = self.table.rowCount()
            self.table.insertRow(row)

            exercise_cell = QTableWidgetItem(exercise)
            exercise_cell.setFlags(exercise_cell.flags() ^ Qt.ItemIsEditable)
            self.table.setItem(row, 0, exercise_cell)

            count_cell = QTableWidgetItem('0')
            self.table.setItem(row, 1, count_cell)

    def fill_table_with_zeros(self):
        for row in range(self.table.rowCount()):
            self.table.item(row, 1).setText('0')

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
            self.table.setItem(
                selected_row - 1, column, self.table.takeItem(selected_row + 1, column)
            )
        self.table.removeRow(selected_row + 1)
        self.table.selectRow(selected_row - 1)

    def move_down(self):
        selected_row = self.table.currentRow()
        if selected_row > self.table.rowCount() - 1:
            return

        self.table.insertRow(selected_row + 2)
        for column in range(self.table.columnCount()):
            self.table.setItem(selected_row + 2, column, self.table.takeItem(selected_row, column))
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
                self.display_warning('Введите положительное число')
        except ValueError:
            item.setText('0')
            self.display_warning('Введите положительное число')

    def load_users(self):
        self.set_of_users.clear()
        users = os.listdir('users')
        self.set_of_users.addItems(users)

    def add_user(self):
        self.setEnabled(False)
        self.add_user_window = AddUserWindow()
        self.add_user_window.close_signal.connect(lambda: self.setEnabled(True))
        self.add_user_window.close_signal.connect(self.load_users)
        self.add_user_window.show()

    def remove_user(self):
        selected_user = self.set_of_users.currentText()
        if selected_user == '':
            self.display_warning('Пользователей не найдено')
            return

        selected_user_directory = os.path.join('users', selected_user)
        if os.path.exists(selected_user_directory):
            os.rmdir(selected_user_directory)
        self.load_users()

    def load_sets(self):
        self.set_of_exercises.clear()

        sets = ['Новый']
        path = 'saved_sets.json'
        if not os.path.exists(path):
            self.set_of_exercises.addItems(sets)
            return

        with open(path, 'r') as json_file:
            json_data = json.load(json_file)
        sets.extend(json_data.keys())
        self.set_of_exercises.addItems(sets)

    def on_set_changed(self):
        selected_set = self.set_of_exercises.currentText()
        if selected_set == 'Новый':
            self.fill_table_with_zeros()
            return

        path = 'saved_sets.json'
        if not os.path.exists(path):
            return

        with open(path, 'r') as json_file:
            json_data = json.load(json_file)

        exercise_counts = json_data.get(selected_set)
        if exercise_counts is None:
            return

        for row in range(self.table.rowCount()):
            ex_name = self.table.item(row, 0).text()
            ex_count = exercise_counts.get(ex_name, 0)
            self.table.item(row, 1).setText(str(ex_count))

    def on_save_set_click(self):
        exercises = self.get_table_data()
        selected_set = self.set_of_exercises.currentText()

        if selected_set != 'Новый':
            path = 'saved_sets.json'
            with open(path, 'r') as json_file:
                sets = json.load(json_file)

            sets[selected_set] = exercises
            with open(path, 'w') as json_file:
                json.dump(sets, json_file, indent=4, ensure_ascii=False)
        else:
            self.setEnabled(False)
            self.save_new_set_window = SaveNewSetWindow(exercises)
            self.save_new_set_window.close_signal.connect(lambda: self.setEnabled(True))
            self.save_new_set_window.close_signal.connect(self.load_sets)
            self.save_new_set_window.show()

    def on_delete_set_click(self):
        selected_set = self.set_of_exercises.currentText()
        if selected_set == 'Новый':
            self.fill_table_with_zeros()
            return

        path = 'saved_sets.json'
        with open(path, 'r') as json_file:
            sets = json.load(json_file)
        sets.pop(selected_set, None)

        with open(path, 'w') as json_file:
            json.dump(sets, json_file, indent=4, ensure_ascii=False)
        self.load_sets()

    def sync_button_clicked(self):
        selected_user = self.set_of_users.currentText()
        if selected_user == '':
            self.display_warning('Пользователь не выбран')
            return

        self.sync_data_window = SyncDataWindow(selected_user)
        self.sync_data_window.show()

    def on_show_stats_click(self):
        path = 'data.csv'
        if not os.path.exists(path):
            self.display_warning('Файл со статистикой не найден')
        else:
            show_stats()

    def open_video_window(self):
        exercises = self.get_table_data()
        if any(value > 0 for value in exercises.values()):
            self.video_window = VideoWindow(exercises)
            self.video_window.close_signal.connect(lambda: self.setEnabled(True))
            self.video_window.show()
            self.setEnabled(False)
        else:
            self.display_warning('Не выбрано ни одно упражнение')

    def closeEvent(self, _):
        QApplication.closeAllWindows()

    def display_warning(self, text: str):
        QMessageBox.warning(self, 'Ошибка', text)
