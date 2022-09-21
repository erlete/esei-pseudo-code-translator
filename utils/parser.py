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

    _TEMP_OUTPUT = "temp.py"

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
        self._sample = sample.lower()

        # Line spacing mapping:
        self._spacing = {
            str(index): self.count_tabs(line)
            for index, line in enumerate(self.sample.split('\n'))
        }

        self._lines = self._reduce_code()
        self._parse_symbols()

    def _reduce_code(self):
        """Returns a reduced list of each line of code.

        This method removes spacing from all lines of code and returns a list
        that might contain empty strings.

        Note:
        -----
        Empty strings must be returned in order to prevent `self._spacing` map
        from indexing lines incorrectly.
        """

        return [
            item.strip()
            for item in self._sample.split('\n')
        ]

    def _parse_symbols(self):
        """Converts pseudo code symbols Python ones.

        This method uses `PseudoCodeParserBase._SYMBOLS` map to replace each
        pseudo code expression with its Python equivalent.
        """

        for l_index, _ in enumerate(self._lines):
            for symbol in self._SYMBOLS:
                self._lines[l_index] = self._lines[l_index].replace(
                    symbol, self._SYMBOLS.get(symbol)
                )

    def _parse_for_statement(self, line):
        """Converts pseudo code "for loop" statements into Python ones."""

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

    def parse(self):
        output = open(f"./{self._TEMP_OUTPUT}", mode='w', encoding="utf-8")

        for index, line in enumerate(self._lines):
            nline = ''

            if line.strip().startswith("desde"):
                nline = self._parse_for_statement(line)

            elif line.strip().startswith("si"):
                nline = self._parse_if_statement(line)

            else:
                nline = line

            output.write(f"{' ' * self._spacing.get(str(index))}{nline}\n")

        output.close()

        os.system(f"python3 {self._TEMP_OUTPUT}")
        os.remove(f"./{self._TEMP_OUTPUT}")
