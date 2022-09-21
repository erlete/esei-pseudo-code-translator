"""Container module for the pseudo code parser classes.

This script contains the main parser class and the interface that adds
its essential components.

Author:
-------
 - Paulo Sánchez (@erlete)
"""


import os


class PseudoCodeParserBase:
    """Interface for the PseudoCodeParser class.

    Contains constants used to relate pseudo code to the Python code, as well
    as getter and setter methods for the class.
    """

    _SYMBOLS = {
        '=': "==",
        "<-": '=',
        "mod": '%',
        "escribir ": "print",
        "escribir": "print",
        "fin_si": '',
        "fin_desde": ''
    }

    @property
    def sample(self):
        return self._sample

    @sample.setter
    def sample(self, value):
        if not isinstance(value, str):
            raise TypeError("Sample must be a string")

        self._sample = value


class PseudoCodeParser(PseudoCodeParserBase):
    def __init__(self, sample):
        self._sample = sample

        # Line spacing mapping:
        self._spacing = {
            str(line_index): self.count_tabs(line_index)
            for line_index in self.sample.split("\n")
        }

    def _parse_symbols(self):
        """Replaces pseudo code symbols with Python symbols.

        This method uses `PseudoCodeParserBase._SYMBOLS` map to replace each
        pseudo code expression with its Python equivalent.
        """

        line = line.strip()
        for symbol in self._SYMBOLS:
            line = line.replace(symbol, self._SYMBOLS[symbol])
        return line

    def _parse_for_statement(self, line):

        line = line.strip().split(' ')

        var = line[1]
        start = line[3]
        end = line[5]

        return f"for {var} in range({start}, {int(end) + 1}):"

    def _parse_if_statement(self, line):
        """Parse a line of the form "if i < 10:" and return a tuple of the form
        (i, 10)."""

        line = line.strip().split(' ')

        return f"if {line[1]} {line[2]} {line[3]} {line[4]} {line[5]}:"

    @staticmethod
    def count_tabs(line):
        """Counts the amount of spaces inserted at the beginning of a line.

        Parameters:
        -----------
         - line: str
            The line to be analyzed.
        """

        return len(line) - len(line.lstrip())

    def main(self):
        with open("./sample.txt", mode='r', encoding="utf-8") as file:
            data = file.read()

        data = data.split("\n")

        out = open("./out.py", mode='w', encoding="utf-8")

        # 1. Remove empty lines
        data = [line.lower() for line in data if line != ""]

        for index, line in enumerate(data):
            original = line
            nline = ''
            line = self._parse_symbols(line)
            if line.strip().startswith("desde"):
                nline = self._parse_for_statement(line)
            elif line.strip().startswith("si"):
                nline = self._parse_if_statement(line)
            else:
                nline = line

            out.write(f"{' ' * self.count_tabs(original)}{nline}\n")

        out.close()

        os.system("python3 out.py")
        os.remove("./out.py")
