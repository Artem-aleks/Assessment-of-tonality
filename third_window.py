from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit, QFileDialog, QListWidget, QSpacerItem, QSizePolicy,
    QLabel
)


class ThirdWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.parent_window = parent
        self.setWindowTitle("Инструкция")
        self.setGeometry(350, 200, 900, 600)

        main_layout = QVBoxLayout()

        title_label = QLabel("Инструкция по исользованию приложения")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        main_layout.addWidget(title_label)

        instruction_text = ("Инструкция")

        text_edit = QTextEdit()
        text_edit.setPlainText(instruction_text)
        text_edit.setReadOnly(True)
        main_layout.addWidget(text_edit)

        back_button = QPushButton("Назад")

        back_button.clicked.connect(self.back_to_main)
        main_layout.addWidget(back_button)

        self.setLayout(main_layout)

    def back_to_main(self):
        self.close()
        # print("Возврат в главное окно...")
        # if self.parent_window is not None:  # Проверяем наличие родителя
        #     self.parent_window.show()  # Показываем главное окно
        # else:
        #     print("Родительское окно не задано.")

