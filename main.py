"""Main execution module for parsing functionality.

Author:
-------
 - Paulo Sanchez (@erlete)
"""

import sys

from PyQt6.QtWidgets import QApplication

from src.core.scanner import Scanner
from src.gui.application import MainWindow

if sys.argv[-1] == "debug":
    sample = (f := open("samples/sample_2.txt", "r")).read()
    scanner = Scanner(sample)
    scanner.scan()

    print(scanner.render())

    f.close()
else:
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()
