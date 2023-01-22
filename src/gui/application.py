"""Main GUI application container module.

This script contains all classes used to define the GUI application. This
includes the main window, the main layout, and the main widgets, as well as
secondary windows used to display information and receive input.

Authors:
    Paulo Sanchez (@erlete)
"""


import re
import sys
import traceback
from io import StringIO
from typing import Any

from PyQt6.QtGui import QCloseEvent, QPixmap, QScreen
from PyQt6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout,
                             QMainWindow, QPushButton, QScrollArea,
                             QStackedLayout, QVBoxLayout, QWidget)

from ..core.scanner import Scanner
from .labels import Footer, Subtitle, TextBoxLabel, Title
from .text_boxes import CodeField


class TextInputWindow(QMainWindow):
    """Code input, output and execution window.

    This window contains all the widgets used to receive code input, translate
    it and execute it. It also contains the widgets used to display the output
    of the code execution.

    Attributes:
        layout_parent (QStackedLayout): the parent layout.
        HEADERS (dict): the window headers.
        central_widget (QWidget): the central widget.
        code_input_label (TextBoxLabel): the code input label.
        code_output_label (TextBoxLabel): the code output label.
        exec_output_label (TextBoxLabel): the execution output label.
        exec_status_label (TextBoxLabel): the execution status label.
        code_input (CodeField): the code input field.
        code_output (CodeField): the code output field.
        exec_output (CodeField): the execution output field.
        exec_status (CodeField): the execution status field.
        clear_button (QPushButton): the clear button.
        exec_button (QPushButton): the execute button.
    """

    HEADERS: dict[str, str] = {
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

    def __init__(self, layout_parent) -> None:
        """Initialize a text input window instance.

        Args:
            layout_parent (QStackedLayout): the parent layout.
        """
        super().__init__()
        self.layout_parent = layout_parent

        # Window title and central widget:
        self.setWindowTitle(self.HEADERS["title"])
        self.central_widget = QWidget()

        # Input/output fields' labels:
        self.code_input_label = TextBoxLabel(
            self.HEADERS["code_input_label"]
        )
        self.code_output_label = TextBoxLabel(
            self.HEADERS["code_output_label"]
        )
        self.exec_output_label = TextBoxLabel(
            self.HEADERS["exec_output_label"]
        )
        self.exec_status_label = TextBoxLabel(
            self.HEADERS["exec_status_label"]
        )

        # Input/output fields' text boxes:
        self.code_input = CodeField(
            self.HEADERS["code_input_placeholder"],
            False
        )
        self.code_output = CodeField(
            self.HEADERS["code_output_placeholder"],
            False
        )
        self.exec_output = CodeField(
            self.HEADERS["exec_output_placeholder"],
            True
        )
        self.exec_status = CodeField(
            self.HEADERS["exec_status_placeholder"],
            True
        )

        # Input/output fields' events:
        self.code_input.text.textChanged.connect(  # type: ignore
            self.translate_input
        )

        # Control buttons:
        self.clear_button = QPushButton(self.HEADERS["clear_button"])
        self.execute_button = QPushButton(self.HEADERS["exec_button"])

        # Control buttons' events:
        self.clear_button.clicked.connect(  # type: ignore
            self.code_input.text.clear
        )
        self.clear_button.clicked.connect(  # type: ignore
            self.code_output.text.clear
        )
        self.clear_button.clicked.connect(  # type: ignore
            self.exec_output.text.clear
        )
        self.clear_button.clicked.connect(  # type: ignore
            self.exec_status.text.clear
        )
        self.execute_button.clicked.connect(  # type: ignore
            self.execute_code
        )

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

    def translate_input(self) -> None:
        """Translate the input code into a valid Python code."""
        scanner = Scanner(self.code_input.text.toPlainText(), 2)
        scanner.scan()

        # Strip the code and add a single newline at the end:
        self.code_output.text.setText(scanner.render().strip() + '\n')

    def execute_code(self) -> None:
        """Execute the code and display outputs."""
        # Standard output redirection:
        tmp = sys.stdout
        sys.stdout = redirect = StringIO()

        # Input retrieval:
        code_input = self.code_output.text.toPlainText()
        code_status = "OK"

        # Code execution:
        try:
            if code_input:  # If there is code to execute.
                exec(code_input)
                code_output = f"{redirect.getvalue().strip()}"
            else:
                code_output = "No executable code found."

        # Exception + traceback display:
        except Exception as exception:
            code_output = ''

            filtered_traceback = re.sub(
                r"(\s*)File(.*)(\s*)exec\(code_string\)", '',
                traceback.format_exc()
            ).replace("  ", "    ")

            code_status = f"{Exception.__name__}:\n    {exception}\n\n" \
                + f"{filtered_traceback}"

        # Output fields' update:
        finally:
            self.exec_output.text.setText(code_output.strip())
            self.exec_status.text.setText(code_status.strip())

            sys.stdout = tmp  # Restores standard output.

    def closeEvent(self, event: Any) -> None:
        """Reset the layout when the window is closed."""
        self.layout_parent.reset_layout(event)
        event.accept()


class InformationWindow(QMainWindow):
    """Usage information window.

    Attributes:
        layout_parent: The parent layout.
    """

    HEADERS: dict[str, str] = {
        "title": "Pseudo Code Parser · Usage Information"
    }

    def __init__(self, layout_parent) -> None:
        """Initialize the window.

        Args:
            layout_parent: The parent layout.
        """
        super().__init__()
        self.layout_parent = layout_parent

        self.setWindowTitle(self.HEADERS["title"])

        widget = QWidget()
        layout = QVBoxLayout()

        #  Information text:
        header_1 = Title("Pseudo Code Parser")
        paragraph_1 = Subtitle(
            "The parser is a simple tool that allows you to write pseudo code"
            + " and execute it in a Python environment. The program will parse"
            + " the code and convert it into Python code so that it can be "
            + "executed."
        )

        header_2 = Title("Usage")
        paragraph_2 = Subtitle("""
The parser is divided into two modes: text mode and image mode.

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
        self.centralWidget().setWidgetResizable(False)  # type: ignore
        self.centralWidget().setWidget(widget)  # type: ignore

        screen = QScreen.geometry(QApplication.primaryScreen())
        self.resize(int(screen.width() * .6), int(screen.height() * .8))

    def closeEvent(self, event: QCloseEvent) -> None:
        """Reset the layout when the window is closed."""
        self.layout_parent.reset_layout(event)
        event.accept()


class MainWindow(QMainWindow):
    """Primary window of the application.

    Attributes:
        window_1: The information window.
        window_2: The text input window.
        info_button: The button that opens the information window.
        text_input_button: The button that opens the text input window.
    """

    HEADERS = {
        "title": "Pseudo Code Parser"
    }

    def __init__(self):
        """Initialize the window."""
        super().__init__()

        self.setWindowTitle(self.HEADERS["title"])

        self.window_1 = InformationWindow(self)
        self.window_2 = TextInputWindow(self)

        header_1 = Title(self)
        header_1.setPixmap(QPixmap("./media/logo_text.png"))
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

    def set_info_screen(self) -> None:
        """Set the information screen."""
        self.stacked_layout.setCurrentIndex(1)
        self.hide()

    def set_text_input_screen(self) -> None:
        """Set the text input screen."""
        self.stacked_layout.setCurrentIndex(2)
        self.hide()

    def reset_layout(self, event: QCloseEvent) -> None:
        """Get the previous window or close the application.

        Args:
            event: The close event.
        """
        if event:
            self.stacked_layout.setCurrentIndex(0)
            self.show()
