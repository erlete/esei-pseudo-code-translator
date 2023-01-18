"""Main execution module for parsing functionality.

Author:
-------
 - Paulo Sanchez (@erlete)
"""

import sys

from PyQt6.QtWidgets import QApplication

from src.core.parser import PseudoCodeParser
from src.gui.application import MainWindow

if sys.argv[-1] == "debug":
    sample = (f := open("samples/sample_2.txt", "r")).read()
    parser = PseudoCodeParser(sample)
    parser.parse()

    print(parser.parsed_code)

    f.close()
else:
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()
