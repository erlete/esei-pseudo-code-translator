import re
import sys
import traceback
from io import StringIO

from PyQt6.QtGui import QPixmap, QScreen
from PyQt6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout,
                             QMainWindow, QPushButton, QScrollArea,
                             QStackedLayout, QTextEdit, QVBoxLayout, QWidget)
from utils.interface.labels import Footer, Subtitle, TextBoxLabel, Title
from utils.interface.text_boxes import CodeField
from utils.internal.parser import PseudoCodeParser


class TextInputWindow(QMainWindow):

    HEADERS = {
        "title": "Pseudo Code Parser · Text Mode",

        "clear_button": "Clear input",
        "exec_button": "Execute code",

        "code_input_label": "Code input:",
        "code_input_placeholder": "Enter your code here...",
        "code_output_label": "Code parsing output:",
        "code_output_placeholder": "Parsed code will be displayed here...",
        "exec_output_label": "Code execution output:",
        "exec_output_placeholder": "Code execution output will be displayed here...",
        "exec_status_label": "Code execution status:",
        "exec_status_placeholder": "Code execution status will be displayed here..."
    }

    def __init__(self, layout_parent):
        super().__init__()
        self.layout_parent = layout_parent

        # Window title and central widget:
        self.setWindowTitle(self.HEADERS.get("title"))
        self.central_widget = QWidget()

        # Input/output fields' labels:
        self.code_input_label = TextBoxLabel(
            self.HEADERS.get("code_input_label"))
        self.code_output_label = TextBoxLabel(
            self.HEADERS.get("code_output_label"))
        self.exec_output_label = TextBoxLabel(
            self.HEADERS.get("exec_output_label"))
        self.exec_status_label = TextBoxLabel(
            self.HEADERS.get("exec_status_label"))

        # Input/output fields' text boxes:
        self.code_input = CodeField(
            self.HEADERS.get("code_input_placeholder"), False)
        self.code_output = CodeField(
            self.HEADERS.get("code_output_placeholder"), False)
        self.exec_output = CodeField(
            self.HEADERS.get("exec_output_placeholder"), True)
        self.exec_status = CodeField(
            self.HEADERS.get("exec_status_placeholder"), True)

        # Input/output fields' events:
        self.code_input.text.textChanged.connect(self.parse_input)

        # Control buttons:
        self.clear_button = QPushButton(self.HEADERS.get("clear_button"))
        self.execute_button = QPushButton(self.HEADERS.get("exec_button"))

        # Control buttons' events:
        self.clear_button.clicked.connect(self.code_input.text.clear)
        self.clear_button.clicked.connect(self.code_output.text.clear)
        self.clear_button.clicked.connect(self.exec_output.text.clear)
        self.clear_button.clicked.connect(self.exec_status.text.clear)
        self.execute_button.clicked.connect(self.execute_code)

        # Layouts:
        layout = QGridLayout()
        layout.setRowMinimumHeight(2, 0)
        layout.setVerticalSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)

        # Control area (top):
        layout.addWidget(self.clear_button, 0, 0)
        layout.addWidget(self.execute_button, 0, 1)

        # Input/output area (middle):
        layout.addWidget(self.code_input_label, 1, 0)
        layout.addWidget(self.code_output_label, 1, 1)
        layout.addWidget(self.code_input, 2, 0)
        layout.addWidget(self.code_output, 2, 1)

        # Output area (bottom):
        layout.addWidget(self.exec_output_label, 3, 0)
        layout.addWidget(self.exec_status_label, 3, 1)
        layout.addWidget(self.exec_output, 4, 0)
        layout.addWidget(self.exec_status, 4, 1)

        # Central widget settings:
        self.central_widget.setLayout(layout)
        self.setCentralWidget(self.central_widget)

        # Display settings:
        screen = QScreen.geometry(QApplication.primaryScreen())
        self.resize(int(screen.width() * .8), int(screen.height() * .8))

    def parse_input(self):
        (parser := PseudoCodeParser(
            self.code_input.text.toPlainText()
        )).parse()

        self.code_output.text.setText(parser.parsed_code)

    def execute_code(self):
        # Output retrieval and standard output redirection:
        tmp = sys.stdout
        sys.stdout = redirect = StringIO()
        code_string = self.code_output.text.toPlainText()
        error_string = "OK"

        try:
            # If there is code to execute:
            if code_string:
                exec(code_string)
                exec_string = f"{redirect.getvalue().strip()}"

            else:
                exec_string = "No executable code found."

        except Exception as exception:

            exec_string = ''
            error_string = f"{Exception.__name__}:\n    {exception}\n\n" \
                + re.sub(
                    r"(\s*)File(.*)(\s*)exec\(code_string\)", '',
                    traceback.format_exc()
                ).replace("  ", "    ")

        finally:
            # Standard output restoration:
            sys.stdout = tmp

            # Code execution output update:
            self.scroll_1.text.setText(exec_string)

            # Code execution status output update:
            self.scroll_2.text.setText(error_string)

    def closeEvent(self, event):
        self.layout_parent.reset_layout(event)
        event.accept()


class InformationWindow(QMainWindow):

    HEADERS = {
        "title": "Pseudo Code Parser · Usage Information"
    }

    def __init__(self, layout_parent):
        super().__init__()
        self.layout_parent = layout_parent

        self.setWindowTitle(self.HEADERS.get("title"))

        widget = QWidget()
        layout = QVBoxLayout()

        # Information text:
        header_1 = Title("Pseudo Code Parser")
        paragraph_1 = Subtitle("""The parser is a simple tool that allows you to write pseudo code and execute
it in a Python environment. The program will parse the code and convert it
into Python code so that it can be executed.""")

        header_2 = Title("Usage")
        paragraph_2 = Subtitle("""The parser is divided into two modes: text mode and image mode.

In text mode, you can write pseudo code in the text area on the left and
execute it using the button that says "Execute code", located on top of the
window. You can also clear the input using the button that says "Clear input".
The output of the code execution will be displayed on the bottom side of the
window.

Furthermore, you might notice that the text area on the right displays updated
Python code as you write pseudo code. This is the parsed code, which is the
code that will be executed when you press the "Execute code" button. If, by
any change, the execution returns an error code due to a parsing feature that
is not yet implemented, you can directly edit the code in the right text area,
fix the issue and execute it.

Image mode is yet to be implemented. Stay tuned!""")

        layout.addWidget(header_1)
        layout.addWidget(paragraph_1)
        layout.addWidget(header_2)
        layout.addWidget(paragraph_2)

        padding = QHBoxLayout()

        padding.addWidget(QWidget())
        padding.addLayout(layout)
        padding.addWidget(QWidget())

        widget.setLayout(padding)

        self.setCentralWidget(QScrollArea())
        self.centralWidget().setWidgetResizable(False)
        self.centralWidget().setWidget(widget)

        screen = QScreen.geometry(QApplication.primaryScreen())
        self.resize(int(screen.width() * .6), int(screen.height() * .8))

    def closeEvent(self, event):
        self.layout_parent.reset_layout(event)
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

        header_1 = Title(self)
        header_1.setPixmap(QPixmap("media/logo_text_1.png"))
        header_1.setScaledContents(True)

        header_2 = Subtitle(
            "The ultimate solution for students"
            + "\nstruggling to understand how"
            + "\npseudo code works"
        )

        self.info_button = QPushButton("How to use the parser?")
        self.text_input_button = QPushButton("Text input")

        self.info_button.clicked.connect(self.set_info_screen)
        self.text_input_button.clicked.connect(self.set_text_input_screen)

        footer = Footer(
            "For more information about my work, please visit"
            + "\nhttps://github.com/erlete"
            + "\n\nHope you like it! :)"
            + "\n\n© erlete, 2022, All Rights Reserved"
        )

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
        self.window_area.addWidget(header_1)
        self.window_area.addWidget(header_2)
        self.window_area.addWidget(self.info_button)
        self.window_area.addWidget(self.text_input_button)
        self.window_area.addWidget(footer)

        MARGINS = (30, 30, 30, 30)
        self.window_area.setContentsMargins(*MARGINS)

        self.padding.addWidget(QWidget())
        self.padding.addLayout(self.window_area)
        self.padding.addWidget(QWidget())

        # self.widget.setLayout(self.window_area)
        self.widget.setLayout(self.padding)
        self.setCentralWidget(self.widget)

        # Screen resizing:
        screen = QScreen.geometry(QApplication.primaryScreen())
        self.resize(int(screen.width() * .4), int(screen.height() * .6))
        # prevent resizing
        self.setFixedSize(self.size())

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
