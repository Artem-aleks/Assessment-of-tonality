import sqlite3
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox


class SummaryWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Сводная таблица")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(3)
        self.table_widget.setHorizontalHeaderLabels(['Автор', 'Высказывание', 'Вес'])

        layout.addWidget(self.table_widget)

        # Кнопка для закрытия
        close_button = QPushButton("Закрыть")
        close_button.clicked.connect(self.close)

        layout.addWidget(close_button)
        self.setLayout(layout)

        self.load_data()

    def load_data(self):
        """Загружает данные из базы данных и отображает их в таблице."""
        try:
            connection = sqlite3.connect('texts_analysis.db')
            cursor = connection.cursor()

            cursor.execute("SELECT author, statement, weight FROM text_analysis")
            records = cursor.fetchall()

            self.table_widget.setRowCount(len(records))

            for row_idx, row_data in enumerate(records):
                for column_idx, data in enumerate(row_data):
                    self.table_widget.setItem(row_idx, column_idx, QTableWidgetItem(str(data)))

        except sqlite3.Error as e:
            QMessageBox.critical(self, "Ошибка базы данных", str(e))

        finally:
            if connection:
                connection.close()
