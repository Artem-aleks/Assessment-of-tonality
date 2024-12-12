import sqlite3
import re
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit, QFileDialog, QListWidget,
    QSpacerItem, QSizePolicy, QLabel, QGridLayout
)
from PyQt6.QtCore import Qt
from summary_window import SummaryWindow


class SecondWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Настройка базы данных
        self.db_connection = sqlite3.connect('texts_analysis.db')
        self.create_texts_table()

        self.default_file_path = 'leksem.txt'
        self.speech_dictionary = [
            'сказал', 'заявил', 'высказался', 'объявил', 'подчеркнул',
            'отметил', 'упомянул', 'прокомментировал', 'говорил'
        ]
        self.author_dictionary = [
            'Джо Байден', 'Байден', 'Трамп', 'Эрдоган', 'Клинтон',
            'Обама', 'Зеленский', 'Лукашенко'
        ]
        self.statement_dictionary = {
            'агрессия': -3,
            'сотрудничество': 3,
            'взаимопомощь': 2,
            'поддержка': 3,
            'санкции': -1,
            'война': -3,
            'предсказуемые отношения': 1,
            'борьба вместе': 2,
            'ключевые партнеры': 3,
            'лидер великой страны': 3,
            'самый близкий друг': 3,
            'дестабилизировать': -2,
            'опасная война': -3,
            'газовые станции': -3,
            'враг': -3,
            'не американский друг': -3,
            'под риском': -1,
            'коррупция': -3,
            'наше сотрудничество': 3,
            'поражение Кремля': -3,
            'победа Кремля': 3,
            'победа Путина': 3,
            'поражение Путина': -3,
            'изоляция России': -3,
            'другая России': 3
        }

        self.setWindowTitle("Программа Loyalue")
        self.setGeometry(350, 200, 900, 600)

        main_layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        button_layout = QVBoxLayout()

        self.select_file_button = QPushButton("Выбрать файл", self)
        self.exit_button = QPushButton("Выход", self)
        self.evaluate_texts_button = QPushButton("Оценка текстов", self)
        self.summary_table_button = QPushButton("Сводная таблица", self)

        self.setup_button_styles()

        button_layout.addWidget(self.select_file_button)
        button_layout.addWidget(self.exit_button)
        button_layout.addSpacing(10)
        button_layout.addWidget(self.evaluate_texts_button)
        button_layout.addWidget(self.summary_table_button)

        self.scale_label = QLabel("Шкала Тональности")
        self.scale_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.scale_layout = QGridLayout()
        tones = [-3, -2, -1, 0, 1, 2, 3]
        colors = [
            QColor(255, 0, 0),
            QColor(255, 102, 102),
            QColor(255, 153, 153),
            QColor(200, 200, 200),

            QColor(153, 255, 153),
            QColor(102, 255, 102),
            QColor(0, 255, 0)
        ]

        for i, tone in enumerate(tones):
            tone_label = QLabel(str(tone))
            tone_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            tone_label.setStyleSheet(f"background-color: {colors[i].name()}; border: 1px solid black;")
            self.scale_layout.addWidget(tone_label, 0, i)

        self.info_list = QListWidget()

        button_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        left_layout.addLayout(button_layout)
        left_layout.addLayout(self.scale_layout)
        left_layout.addWidget(self.info_list)

        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)

        main_layout.addLayout(left_layout)
        main_layout.addWidget(self.text_edit)

        self.setLayout(main_layout)

        self.exit_button.clicked.connect(self.close)
        self.select_file_button.clicked.connect(self.load_info)
        self.evaluate_texts_button.clicked.connect(self.analyze_texts)
        self.summary_table_button.clicked.connect(self.open_summary_window)  # Подключаем кнопку "Сводная таблица"

        self.load_default_file()

    def create_texts_table(self):
        """Создает таблицу для хранения данных о текстах и анализа."""
        try:
            cursor = self.db_connection.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS text_analysis (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    file_name TEXT NOT NULL,
                    author TEXT NOT NULL,
                    statement TEXT NOT NULL,
                    weight INTEGER NOT NULL
                )
            ''')
            self.db_connection.commit()
        except sqlite3.Error as e:
            print(f"Ошибка при создании таблицы: {e}")

    def setup_button_styles(self):
        for button in [self.select_file_button, self.exit_button,
                       self.evaluate_texts_button, self.summary_table_button]:
            button.setFixedSize(150, 30)
            button.setStyleSheet(
                "QPushButton {"
                "   background-color: lightgray;"
                "   color: black;"
                "   border: 1px solid gray;"
                "   border-radius: 5px;"
                "   padding: 5px;"
                "}"
                "QPushButton:hover {"
                "   background-color: darkgray;"
                "   color: white;"
                "}"
            )

    def load_info(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Выбрать текстовый файл",
            "",
            "Text Files (*.txt);;All Files (*)"
        )

        if file_name:
            try:
                with open(file_name, 'r', encoding='utf-8') as file:
                    content = file.read()
                    self.text_edit.setPlainText(content)
            except Exception as e:
                self.text_edit.setPlainText(f"Ошибка при загрузке файла: {e}")

    def load_default_file(self):
        """Загружает текст из файла по умолчанию при инициализации окна."""
        try:
            with open(self.default_file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                self.info_list.clear()
                for line in content.splitlines():
                    self.info_list.addItem(line)
        except Exception as e:
            self.text_edit.setPlainText(f"Ошибка при загрузке файла: {e}")

    def analyze_texts(self):
        text = self.text_edit.toPlainText()

        print("Текст для анализа:", text)  # Debugging output
        print("Словарь речей:", self.speech_dictionary)  # Проверка словаря речей

        results = []
        for speech in self.speech_dictionary:
            if not speech:  # Проверка на пустую строку
                print("Слово речи пустое, пропускаем.")
                continue

            print(f"Обработка речи: '{speech}'")  # Debugging output

            # Обновлённое регулярное выражение для захвата всей фразы с ключевым словом
            pattern = r'(?P<text>.*?\b' + re.escape(speech) + r'\b.*?[.?!])'

            try:
                matches = list(re.finditer(pattern, text))
            except re.error as e:
                print(f"Ошибка регулярного выражения для '{speech}': {e}")
                continue

            print(f"Совпадений для '{speech}': {len(matches)}")

            if not matches:
                print(f"Совпадений для '{speech}' не найдено.")
                continue

            for match in matches:
                matched_text = match.group('text')
                print("Найдено совпадение:", matched_text)  # Debugging output

                # Найти автора в тексте
                author = self.find_author(matched_text)
                if author:
                    print("Автор найден:", author)  # Debugging output
                    statement_data = self.extract_statement(matched_text)

                    if statement_data:
                        print("Данные о высказывании:", statement_data)  # Debugging output
                        results.append({
                            'file_name': self.default_file_path,
                            'author': author,
                            'statement': statement_data['statement'],

                            'weight': statement_data['weight']
                        })
                        self.save_to_database(self.default_file_path, author, statement_data['statement'],
                                              statement_data['weight'])
                    else:
                        print("Не удалось извлечь данные о высказывании.")  # Debugging output
                else:
                    print("Автор не найден.")  # Debugging output

                self.text_edit.append("\nАнализ результатов:")
                if results:
                    for result in results:
                        self.text_edit.append(
                            f"Файл: {result['file_name']}, Автор: {result['author']}, Высказывание: {result['statement']} (Вес: {result['weight']})")
                else:
                    self.text_edit.append("Нет результатов для отображения.")

    def save_to_database(self, file_name, author, statement, weight):
        cursor = self.db_connection.cursor()
        cursor.execute('''
                        INSERT INTO text_analysis (file_name, author, statement, weight)
                        VALUES (?, ?, ?, ?)
                    ''', (file_name, author, statement, weight))
        self.db_connection.commit()

    def find_author(self, text):
        # Проверка авторов в тексте
        for author in self.author_dictionary:
            if author in text:
                return author
        return None

    def extract_statement(self, matched_text):
        # Предполагая, что высказывание будет между кавычками
        start_quote = matched_text.find('“')
        end_quote = matched_text.find('”')

        # Если кавычек нет, можно использовать обычные
        if start_quote == -1 or end_quote == -1:
            start_quote = matched_text.find('"')
            end_quote = matched_text.rfind('"')

        if start_quote != -1 and end_quote != -1 and end_quote > start_quote:
            statement = matched_text[start_quote + 1:end_quote]
            return {
                'statement': statement.strip(),
                'weight': 1  # или какое-то другое значение веса
            }
        else:
            print("Не удалось найти кавычки в тексте:", matched_text)  # Дополнительная отладочная информация
            return None

    def open_summary_window(self):
        print("Попытка открыть сводную таблицу...")
        summary_window = SummaryWindow()
        summary_window.show()  # Используйте show(), чтобы окно работало как отдельное

    # Здесь можно добавить код запуска приложения PyQt.
    if __name__ == "__main__":  # исправлено здесь
        app = QApplication(sys.argv)
        window = SecondWindow()
        window.show()
        sys.exit(app.exec())

