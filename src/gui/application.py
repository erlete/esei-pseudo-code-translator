"""Main GUI application container module.

This script contains all classes used to define the GUI application. This
includes the main window, the main layout, and the main widgets, as well as
secondary windows used to display information and receive input.

Authors:
    Paulo Sanchez (@erlete)
"""

import os
import sys
from io import StringIO
from ..core.code import Code

from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QCloseEvent, QDesktopServices, QIcon, QPixmap, QScreen
from PyQt6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout,
                             QInputDialog, QMainWindow, QPushButton,
                             QStackedLayout, QVBoxLayout, QWidget)

from ..core.scanner import Scanner
from .labels import Footer, Subtitle, TextBoxLabel, Title
from .text_boxes import CodeField


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller."""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class InputWindow(QMainWindow):
    """Code input, output and execution window.

    This window contains all the widgets used to receive code input, translate
    it and execute it. It also contains the widgets used to display the output
    after code execution.

    Attributes:
        LABELS (dict[str, str]): the labels used in the window.
        PLACEHOLDERS (dict[str, str]): the placeholders used in the window.
        layout_parent (QStackedLayout): the parent layout.
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

    LABELS: dict[str, str] = {
        "title": "Pseudo Code Translator · Input Window",
        "clear_button": "Clear fields",
        "exec_button": "Execute code",
        "code_input": "Code input",
        "code_output": "Translation",
        "exec_output": "Execution output",
        "exec_status": "Execution status"
    }

    PLACEHOLDERS: dict[str, str] = {
        "code_input": "Enter pseudo code here...",
        "code_output": "Translated code will be displayed here...",
        "exec_output": "Execution output will be displayed here...",
        "exec_status": "Execution status will be displayed here..."
    }

    def __init__(self, layout_parent) -> None:
        """Initialize a text input window instance.

        Args:
            layout_parent (QStackedLayout): the parent layout.
        """
        super().__init__()
        self.layout_parent = layout_parent

        self.setWindowIcon(QIcon(resource_path("icon.ico")))
        # Window title and central widget:
        self.setWindowTitle(self.LABELS["title"])
        self.central_widget = QWidget()

        # Set up fields, buttons, event handlers and layout:
        self.setup_fields()
        self.setup_buttons()
        self.setup_event_handlers()
        self.setup_layout()

        # Display settings:
        screen = QScreen.geometry(QApplication.primaryScreen())
        self.resize(int(screen.width() * .8), int(screen.height() * .8))

    def setup_fields(self) -> None:
        """Set up text fields with their corresponding labels."""
        self.code_input_label = TextBoxLabel(
            self.LABELS["code_input"]
        )
        self.code_input = CodeField(
            self.PLACEHOLDERS["code_input"],
            read_only=False
        )

        self.code_output_label = TextBoxLabel(
            self.LABELS["code_output"]
        )
        self.code_output = CodeField(
            self.PLACEHOLDERS["code_output"],
            read_only=False
        )

        self.exec_output_label = TextBoxLabel(
            self.LABELS["exec_output"]
        )
        self.exec_output = CodeField(
            self.PLACEHOLDERS["exec_output"],
            read_only=True
        )

        self.exec_status_label = TextBoxLabel(
            self.LABELS["exec_status"]
        )
        self.exec_status = CodeField(
            self.PLACEHOLDERS["exec_status"],
            read_only=True
        )

    def setup_buttons(self) -> None:
        """Set up control buttons."""
        self.clear_button = QPushButton(self.LABELS["clear_button"])
        self.execute_button = QPushButton(self.LABELS["exec_button"])

    def setup_event_handlers(self) -> None:
        """Set up event handlers."""
        self.code_input.text.textChanged.connect(  # type: ignore
            self.translate_input
        )

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

    def setup_layout(self) -> None:
        """Set up the window layout."""
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

    def translate_input(self) -> None:
        """Translate the input code into a valid Python code."""
        scanner = Scanner(self.code_input.text.toPlainText())
        scanner.scan()
        code = Code(scanner)
        self.code_output.text.setText(code.render())

    def execute_code(self) -> None:
        """Execute the code and display outputs."""
        tmp = sys.stdout
        sys.stdout = StringIO()  # Redirect standard output.

        code_input = self.code_output.text.toPlainText()
        code_status = "OK"

        def input():
            text, ok = QInputDialog.getText(
                self, "Input", "Introduce un valor:")
            if ok:
                if '.' in text:
                    try:
                        return float(text)
                    except ValueError:
                        return text
                else:
                    try:
                        return int(text)
                    except ValueError:
                        return text

        try:
            if code_input:
                exec(code_input, locals(), locals())
                code_output = f"{sys.stdout.getvalue().strip()}"
            else:
                code_output = "No executable code found."

        except Exception as exception:
            code_output = ''
            code_status = str(exception).capitalize()

        finally:
            self.exec_output.text.setText(code_output.strip())
            self.exec_status.text.setText(code_status.strip())
            if code_status != "OK":
                self.exec_status.text.setStyleSheet("color: red")
            else:
                self.exec_status.text.setStyleSheet("color: green")

            sys.stdout = tmp  # Restore standard output.

    def closeEvent(self, event: QCloseEvent) -> None:
        """Reset the layout when the window is closed."""
        self.layout_parent.reset_layout(event)
        event.accept()


class MainWindow(QMainWindow):
    """Primary window of the application.

    Attributes:
        LABELS (dict): labels for the window.
        URL (str): URL for the application's GitHub page.
        input_window (InputWindow): input window.
        layout_parent (LayoutParent): layout parent.
        logo_image (QLabel): logo image.
        slogan (QLabel): slogan label.
        copyright_footer (QLabel): copyright label.
        info_button (QPushButton): info button.
        text_info_button (QLabel): text info button.
    """

    LABELS = {
        "title": "Pseudo Code Translator · v3.0"
    }

    URL = "https://github.com/erlete/pseudo-code-translator/wiki/Welcome!"

    def __init__(self):
        """Initialize the window."""
        super().__init__()

        self.setWindowIcon(QIcon(resource_path("icon.ico")))
        self.setWindowTitle(self.LABELS["title"])

        self.setup_fields()
        self.setup_buttons()
        self.setup_event_handlers()
        self.setup_layout()

        screen = QScreen.geometry(QApplication.primaryScreen())
        self.resize(int(screen.width() * .3), int(screen.height() * .5))
        self.setFixedSize(self.size())

    def setup_fields(self) -> None:
        """Set up the window fields."""
        self.input_window = InputWindow(self)

        self.logo_image = Title(self)
        self.logo_image.setPixmap(QPixmap(resource_path("logo_text.png")))
        self.logo_image.setScaledContents(False)

        self.slogan = Subtitle(
            "The ultimate solution for students struggling"
            + "\nto understand how pseudo code works"
        )

        self.copyright_footer = Footer(
            "© erlete, 2022 - 2023, All Rights Reserved"
        )

    def setup_buttons(self) -> None:
        """Set up control buttons."""
        self.info_button = QPushButton("Usage instructions")
        self.text_input_button = QPushButton("Translator")

    def setup_event_handlers(self) -> None:
        """Set up event handlers."""
        self.info_button.clicked.connect(  # type: ignore
            lambda: QDesktopServices.openUrl(QUrl(self.URL))
        )
        self.text_input_button.clicked.connect(  # type: ignore
            self.set_input_window
        )

    def setup_layout(self) -> None:
        """Set up the window layout."""
        self.widget = QWidget()

        self.stacked_layout = QStackedLayout()
        self.stacked_layout.setCurrentIndex(0)

        self.stacked_layout.addWidget(self.widget)
        self.stacked_layout.addWidget(self.input_window)

        self.padding = QHBoxLayout()

        self.window_area = QVBoxLayout()
        self.window_area.addWidget(self.logo_image)
        self.window_area.addWidget(self.slogan)
        self.window_area.addWidget(self.info_button)
        self.window_area.addWidget(self.text_input_button)
        self.window_area.addWidget(self.copyright_footer)

        self.window_area.setContentsMargins(30, 30, 30, 30)

        self.padding.addWidget(QWidget())
        self.padding.addLayout(self.window_area)
        self.padding.addWidget(QWidget())

        self.widget.setLayout(self.padding)
        self.setCentralWidget(self.widget)

    def set_input_window(self) -> None:
        """Set the code input screen."""
        self.stacked_layout.setCurrentIndex(1)
        self.hide()

    def reset_layout(self, event: QCloseEvent) -> None:
        """Get the previous window or close the application.

        Args:
            event: the close event.
        """
        if event:
            self.stacked_layout.setCurrentIndex(0)
            self.show()
