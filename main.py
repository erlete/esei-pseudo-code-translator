"""Main execution module for parsing functionality.

Author:
-------
 - Paulo Sanchez (@erlete)
"""


from utils.parser import PseudoCodeParser


with open("sample.txt", "r") as sample:
    parser = PseudoCodeParser(sample.read())
    parser.parse()
