import sys
import re
import traceback
from io import StringIO

from PyQt6.QtGui import QPixmap, QScreen, QFont
from PyQt6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QMainWindow,
                             QPushButton, QScrollArea, QStackedLayout,
                             QTextEdit, QVBoxLayout, QWidget, QGridLayout, QScrollArea)
from utils.parser import PseudoCodeParser

from ui.labels import Title, Subtitle, Text, Footer
from ui.text_boxes import CodeField


class TextInputWindow(QMainWindow):

    HEADERS = {
        "title": "Pseudo Code Parser · Text Mode",
        "clear_button": "Clear input",
        "exec_button": "Execute code",
        "code_output": "Code execution output:",
        "exec_status": "Code execution status:"
    }

    def __init__(self, layout_parent):
        super().__init__()
        self.layout_parent = layout_parent

        # Window title and central widget:
        self.setWindowTitle(self.HEADERS.get("title"))
        self.central_widget = QWidget()

        # Code input and output fields:
        self.code_input = CodeField("Enter your code here...", False)
        self.code_output = CodeField("Parsed code will appear here...", False)

        self.code_input.text.textChanged.connect(self.parse_input)

        self.exec_output = Text(self.HEADERS.get("code_output"))
        self.exec_status = Text(self.HEADERS.get("exec_status"))

        self.scroll_1 = CodeField(
            "Code execution output will be displayed here...", True
        )
        self.scroll_2 = CodeField(
            "Code execution status will be displayed here...", True
        )

        # Control buttons:
        self.clear_button = QPushButton(self.HEADERS.get("clear_button"))
        self.clear_button.clicked.connect(self.code_input.text.clear)
        self.clear_button.clicked.connect(self.code_output.text.clear)
        self.clear_button.clicked.connect(self.scroll_1.text.clear)
        self.clear_button.clicked.connect(self.scroll_2.text.clear)

        self.execute_button = QPushButton(self.HEADERS.get("exec_button"))
        self.execute_button.clicked.connect(self.execute_code)

        # Execution output field:

        # TODO: move this to labels.py
        self.exec_output.setFont(QFont("Arial", 14, QFont.Weight.Normal))
        self.exec_status.setFont(QFont("Arial", 14, QFont.Weight.Normal))

        self.exec_output.setContentsMargins(5, 10, 0, 5)
        self.exec_status.setContentsMargins(5, 10, 0, 5)

        # Layout settings:
        self.control_area = QHBoxLayout()
        self.input_area = QHBoxLayout()
        self.output_area = QGridLayout()
        self.window_area = QVBoxLayout()

        self.control_area.addWidget(self.clear_button)
        self.control_area.addWidget(self.execute_button)

        self.input_area.addWidget(self.code_input)
        self.input_area.addWidget(self.code_output)

        self.output_area.addWidget(self.exec_output, 0, 0)
        self.output_area.addWidget(self.exec_status, 0, 1)

        self.output_area.setContentsMargins(0, 0, 0, 0)

        self.output_area.addWidget(self.scroll_1, 1, 0)
        self.output_area.addWidget(self.scroll_2, 1, 1)

        # reduce separation between sct_2 and exec_status
        self.output_area.setRowMinimumHeight(1, 0)
        self.output_area.setRowMinimumHeight(2, 0)
        self.output_area.setVerticalSpacing(10)
        self.output_area.setContentsMargins(0, 0, 0, 0)

        self.window_area.addLayout(self.control_area)
        self.window_area.addLayout(self.input_area)
        self.window_area.addLayout(self.output_area)

        # Main widget settings:
        self.central_widget.setLayout(self.window_area)
        self.setCentralWidget(self.central_widget)

        # Display settings:
        screen = QScreen.geometry(QApplication.primaryScreen())
        self.resize(int(screen.width() * .8), int(screen.height() * .8))

    def parse_input(self):
        # TODO: set label title in the constructor:
        self.exec_output.setText(self.HEADERS.get("code_output"))
        parser = PseudoCodeParser(self.code_input.text.toPlainText())
        parser.parse()
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
