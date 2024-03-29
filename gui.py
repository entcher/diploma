from detector import show
from PyQt5.QtWidgets import QMainWindow, QPushButton, QFileDialog, QLabel, QVBoxLayout, QWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Определение положения тела человека")
        self.setGeometry(100, 100, 400, 100)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        self.button = QPushButton("Выбрать файл", self)
        layout.addWidget(self.button)
        self.button.clicked.connect(self.open_file_dialog)

        self.file_path_label = QLabel("Выберите файл!", self)
        layout.addWidget(self.file_path_label)

        self.done_button = QPushButton("Готово", self)
        self.done_button.clicked.connect(self.define_pose)
        layout.addWidget(self.done_button)

    def open_file_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Выбрать файл", "", "Media File (*.mp4, *.jpg)")
        if file_path:
            self.file_path_label.setText(file_path)

    def define_pose(self):
        if self.file_path_label.text() == 'Выберите файл!':
            return
        show(self.file_path_label)
