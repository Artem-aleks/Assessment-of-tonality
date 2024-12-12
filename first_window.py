import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from second_window import SecondWindow
from third_window import ThirdWindow

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Устанавливаем заголовок окна и его размеры
        self.setWindowTitle("Программа Loyalue")
        self.setGeometry(550, 150, 500, 700)

        # Загрузка изображения
        self.image_label = QLabel(self)
        pixmap = QPixmap(
            "/Users/artemaleksanov/Уник/Assessment of tonality/Png_main.jpg")  # Укажите путь к вашей картинке
        scaled_pixmap = pixmap.scaled(500, 500, Qt.AspectRatioMode.KeepAspectRatio)
        self.image_label.setPixmap(scaled_pixmap)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Центрируем изображение

        # Создаем кнопки
        self.start_button = QPushButton("Запустить программу", self)
        self.manual = QPushButton("Информация о программе", self)
        self.exit_button = QPushButton("Выйти", self)

        # Улучшаем стиль кнопок
        self.start_button.setStyleSheet(
            "QPushButton {"
            "   background-color: lightgreen;"
            "   color: black;"
            "   border: 2px solid green;"
            "   border-radius: 10px;"
            "   padding: 10px;"
            "}"
            "QPushButton:hover {"
            "   background-color: green;"
            "   color: white;"
            "}"
        )

        self.manual.setStyleSheet(
            "QPushButton {"
            "   background-color: lightblue;"
            "   color: black;"
            "   border: 2px solid blue;"
            "   border-radius: 10px;"
            "   padding: 10px;"
            "}"
            "QPushButton:hover {"
            "   background-color: blue;"
            "   color: white;"
            "}"
        )

        self.exit_button.setStyleSheet(
            "QPushButton {"
            "   background-color: lightcoral;"
            "   color: black;"
            "   border: 2px solid red;"
            "   border-radius: 10px;"
            "   padding: 10px;"
            "}"
            "QPushButton:hover {"
            "   background-color: red;"
            "   color: white;"
            "}"
        )

        # Подключаем кнопки к действиям
        self.start_button.clicked.connect(self.start_program)
        self.manual.clicked.connect(self.open_manual)
        self.exit_button.clicked.connect(self.close)

        # Создаем вертикальный layout и добавляем метку и кнопки
        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addWidget(self.start_button)
        layout.addWidget(self.manual)
        layout.addWidget(self.exit_button)

        # Устанавливаем layout для главного окна
        self.setLayout(layout)

    def start_program(self):
        self.close()
        self.second_window = SecondWindow()
        self.second_window.show()

    def open_manual(self):
        print("Открытие окна с инструкцией...")
        self.manual_window = ThirdWindow()
        self.manual_window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
