"""Main execution module for parsing functionality.

Author:
-------
 - Paulo Sanchez (@erlete)
"""


import sys

from PyQt6.QtWidgets import QApplication

from gui.application import MainWindow


if sys.argv[-1] == "debug":
    from utils.internal.parser import PseudoCodeParser

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
