import sys, os

from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from utils.parser import PseudoCodeParser

import subprocess
from io import StringIO

class TextInputWindow(QMainWindow):

    HEADERS = {
        "title": "Pseudo Code Parser · Text Mode",
        "clear_button": "Clear input",
        "exec_button": "Execute code",
        "code_output": "Code execution output:\n\n"
    }

    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window

        self.setWindowTitle(self.HEADERS.get("title"))
        self.widget = QWidget()

        # Code input field:
        self.code_input = QTextEdit()
        self.code_input.textChanged.connect(self.parse_input)

        # Code output field:
        self.code_output = QTextEdit()

        # Control buttons:
        self.clear_button = QPushButton(self.HEADERS.get("clear_button"))
        self.clear_button.clicked.connect(self.code_input.clear)

        self.execute_button = QPushButton(self.HEADERS.get("exec_button"))
        self.execute_button.clicked.connect(self.execute_code)

        # Execution output field:
        self.exec_output = QLabel(self.HEADERS.get("code_output"))

        # Layout settings:
        self.input_area = QHBoxLayout()
        self.window_area = QVBoxLayout()

        self.input_area.addWidget(self.code_input)
        self.input_area.addWidget(self.code_output)

        self.window_area.addWidget(self.clear_button)
        self.window_area.addWidget(self.execute_button)
        self.window_area.addLayout(self.input_area)
        self.window_area.addWidget(self.exec_output)

        # Main widget settings:
        self.widget.setLayout(self.window_area)
        self.setCentralWidget(self.widget)

        # Screen resizing:
        screen = QScreen.geometry(QApplication.primaryScreen())
        self.resize(screen.width() * 0.8, screen.height() * .8)

    def parse_input(self):
        self.exec_output.setText(self.HEADERS.get("code_output"))
        parser = PseudoCodeParser(self.code_input.toPlainText())
        parser.parse()
        self.code_output.setText(parser.parsed_code)

    def execute_code(self):
        # Output retrieval and standard output redirection:
        tmp = sys.stdout
        sys.stdout = redirect = StringIO()
        code_string = self.code_output.toPlainText()

        try:
            # If there is code to execute:
            if code_string:
                exec(code_string)
                exec_string = f"{redirect.getvalue().strip()}"

            else:
                exec_string = "No executable code found."

        except Exception as exception:
            exec_string = f"Error: {exception}"

        finally:
            # Standard output restoration:
            sys.stdout = tmp

            # Label text update:
            self.exec_output.setText(
                self.HEADERS.get("code_output")
                + exec_string
            )

    def closeEvent(self, event):
        self.main_window.reset_layout(event)
        event.accept()

class InformationWindow(QMainWindow):

    HEADERS = {
        "title": "Pseudo Code Parser · Usage Information"
    }

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle(self.HEADERS.get("title"))

        screen = QScreen.geometry(QApplication.primaryScreen())
        self.resize(screen.width() * 0.8, screen.height() * .8)

    def closeEvent(self, event):
        self.main_window.reset_layout(event)
        event.accept()

class MainWindow(QMainWindow):

    HEADERS = {
        "title": "Pseudo Code Parser"
    }

    def __init__(self):
        super().__init__()

        self.setWindowTitle(self.HEADERS.get("title"))

        self.window_1 = InformationWindow(self)
        self.window_2 = TextInputWindow(self)

        header = QLabel("Title")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setFont(QFont("Monaco", 30))

        self.info_button = QPushButton("How to use the parser?")
        self.text_input_button = QPushButton("Text input")

        self.info_button.clicked.connect(self.set_info_screen)
        self.text_input_button.clicked.connect(self.set_text_input_screen)

        footer = QLabel("Footer")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer.setFont(QFont("Monaco", 30))

        # create main widget
        self.widget = QWidget()

        # create a stacked layout
        self.stacked_layout = QStackedLayout()
        self.stacked_layout.setCurrentIndex(0)

        # add the widgets to the stacked layout
        self.stacked_layout.addWidget(self.widget)
        self.stacked_layout.addWidget(self.window_1)
        self.stacked_layout.addWidget(self.window_2)

        self.padding = QHBoxLayout()

        self.window_area = QVBoxLayout()
        self.window_area.addWidget(header)
        self.window_area.addWidget(self.info_button)
        self.window_area.addWidget(self.text_input_button)
        self.window_area.addWidget(footer)
        #self.window_area.addLayout(self.stacked_layout)

        self.padding.addWidget(QWidget())
        self.padding.addLayout(self.window_area)
        self.padding.addWidget(QWidget())

        #self.widget.setLayout(self.window_area)
        self.widget.setLayout(self.padding)
        self.setCentralWidget(self.widget)

        # Screen resizing:
        screen = QScreen.geometry(QApplication.primaryScreen())
        self.resize(screen.width() * 0.4, screen.height() * .6)

    def set_info_screen(self):
        self.stacked_layout.setCurrentIndex(1)
        self.hide()

    def set_text_input_screen(self):
        self.stacked_layout.setCurrentIndex(2)
        self.hide()

    def reset_layout(self, event):
        if event:
            self.stacked_layout.setCurrentIndex(0)
            self.show()
