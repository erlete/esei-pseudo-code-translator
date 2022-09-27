"""Main execution module for parsing functionality.

Author:
-------
 - Paulo Sanchez (@erlete)
"""


import sys

from PyQt6.QtWidgets import QApplication

from ui.application import MainWindow


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
