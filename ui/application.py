import sys, os

from PyQt6.QtWidgets import *
from utils.parser import PseudoCodeParser

import subprocess
from io import StringIO

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Parser")

        # Main widget:
        widget = QWidget()

        # Multi-line input field:
        self.input_field = QTextEdit()
        self.input_field.textChanged.connect(self.parse_input)

        # Output field:
        self.output_field = QTextEdit()

        self.clear_btn = QPushButton("Clear text")
        self.clear_btn.clicked.connect(self.input_field.clear)

        self.run_btn = QPushButton("Execute code")
        self.run_btn.clicked.connect(self.execute_code)

        self.output_label = QLabel("Output:")

        # Layout settings:
        self.outer_layout = QVBoxLayout()
        self.inner_layout = QHBoxLayout()

        self.inner_layout.addWidget(self.input_field)
        self.inner_layout.addWidget(self.output_field)

        self.outer_layout.addWidget(self.clear_btn)
        self.outer_layout.addWidget(self.run_btn)

        self.outer_layout.addLayout(self.inner_layout)
        self.outer_layout.addWidget(self.output_label)

        # Main widget settings:
        widget.setLayout(self.outer_layout)
        self.setCentralWidget(widget)

        self.resize(800, 600)

    def parse_input(self):
        self.output_label.setText("Output:")
        parser = PseudoCodeParser(self.input_field.toPlainText())
        parser.parse()
        self.output_field.setText(parser.parsed_code)

    def execute_code(self):

        tmp = sys.stdout
        sys.stdout = redirect = StringIO()

        try:
            if self.output_field.toPlainText():
                exec(self.output_field.toPlainText())
                self.output_label.setText("Output:\n\n" + redirect.getvalue().strip())
            else:
                self.output_label.setText("Output:\n\nNo code to execute.")
        except Exception as e:
            self.output_label.setText("Output:\n\n" + str(e) + f"\n{redirect.getvalue()}")
        finally:
            sys.stdout = tmp
