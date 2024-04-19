import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QComboBox

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Создание вертикального макета
        vbox = QVBoxLayout(self)

        # Создание горизонтального макета
        hbox = QHBoxLayout()

        # Создание и добавление QComboBox в горизонтальный макет
        combo_box = QComboBox()
        hbox.addWidget(combo_box)

        # Создание и добавление QPushButton в горизонтальный макет
        button = QPushButton('Нажми меня')
        hbox.addWidget(button)

        # Добавление горизонтального макета в вертикальный макет
        vbox.addLayout(hbox)

        self.setLayout(vbox)
        self.setWindowTitle('Пример размещения горизонтальных элементов')
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    sys.exit(app.exec_())
