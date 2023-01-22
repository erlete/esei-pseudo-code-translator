"""Application execution script.

Authors:
    Paulo Sanchez (@erlete)
"""

import sys

from PyQt6.QtWidgets import QApplication

from src.gui.application import MainWindow

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
