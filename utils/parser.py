"""Container module for the pseudo code parser classes.

This script contains the main parser class and the interface that adds
its essential components.

Author:
-------
 - Paulo Sánchez (@erlete)
"""


import os
import re


class PseudoCodeParserBase:
    """Interface for the PseudoCodeParser class.

    This class ontains essential information about the syntax specification of
    the pseudo code language.
    """

    _SP = r"[ ]{0,}"

    _OPERATORS = {
        rf"{_SP}={_SP}": " == ",         # Equal to
        rf"{_SP}<{_SP}-{_SP}": " = ",    # Asignment.
        rf"{_SP}<{_SP}>{_SP}": " != ",   # Different from.
        rf"{_SP}mod{_SP}": " % ",        #  Modulus.
        rf"{_SP}\+{_SP}": " + ",         #  Addition.
        rf"{_SP}\*{_SP}": " * ",         #  Multiplication.
        rf"{_SP}\/{_SP}": " / ",         #  Division.
        rf"{_SP}\-{_SP}": " - ",         #  Subtraction.
        rf"{_SP}\<{_SP}": " < ",         #  Lower than.
        rf"{_SP}\>{_SP}": " > ",         #  Greater than.
        rf"{_SP}\<{_SP}={_SP}": " <= ",  #  Lower than or equal to.
        rf"{_SP}\>{_SP}={_SP}": " >= "   #  Greater than or equal to.
    }

    _STATEMENTS = {
        r"escribir\s+": "print"
    }

    _BEHAVIOR = {
        "range_end_inclusive": True,
        "range_step": 1
    }


class PseudoCodeParser(PseudoCodeParserBase):
    """Parser class for the pseudo code language.

    This class is responsible for parsing the pseudo code language and
    converting it into Python code.
    """

    @property
    def sample(self):
        return self._sample

    @sample.setter
    def sample(self, value: str):
        if not isinstance(value, str):
            raise TypeError("Sample must be a string")

        self._sample = value

    @property
    def parsed_code(self):
        return self._parsed_code

    def __init__(self, sample: str):
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

        for index, _ in enumerate(self._lines):
            for symbol in self._OPERATORS:
                self._lines[index] = self._lines[index].replace(
                    symbol, self._OPERATORS.get(symbol)
                )

    def _parse_for_statement(self, line: str):
        """Converts pseudo code "for loop" statements into Python ones.

        Parameters:
        -----------
         - line: str
            The line to be analyzed.

        Original pseudo code structure:
        -------------------------------
        DESDE <variable> <- <value> HASTA <variable/value> HACER
            ...
        FIN_DESDE

        Converted Python code structure:
        --------------------------------
        for i in range(n, m):
            ...

        Note:
        -----
        The m value might be increased by one depending on whether the
        `PseudoCodeParserBase._BEHAVIOR` map has the `range_end_inclusive`
        key set to `True` or `False`.
        """

        line = line.split(' ')
        range_end = int(line[4]) + self._BEHAVIOR.get("range_end_inclusive")

        return f"for {line[1]} in range({line[3]}, {range_end}):"

    def _parse_if_statement(self, line: str):
        """Converts pseudo code "if" statements into Python ones.

        Parameters:
        -----------
         - line: str
            The line to be analyzed.

        Original pseudo code structure:
        -------------------------------
        SI <variable/value> <operator> <variable/value> HACER
            ...
        FIN_SI

        Converted Python code structure:
        --------------------------------
        if <variable/value> <operator> <variable/value>:
            ...
        """

        line = line.split(' ')

        return f"if {line[1]} {line[2]} {line[3]} {line[4]} {line[5]}:"

    @staticmethod
    def count_tabs(line: str):
        """Counts the amount of spaces inserted at the beginning of a line.

        Parameters:
        -----------
         - line: str
            The line to be analyzed.
        """

        return len(line) - len(line.lstrip())

    def parse(self):
        """Main parser method.

        Converts pseudo code to Python code using `PseudoCodeParserBase`
        specification and outputs the result to a temporary file that is
        later executed.
        """

        self._parsed_code = ''

        for index, line in enumerate(self._lines):
            nline = ''

            if line.strip().startswith("desde"):
                nline = self._parse_for_statement(line)

            elif line.strip().startswith("si"):
                nline = self._parse_if_statement(line)

            else:
                nline = line

            self._parsed_code += f"{' ' * self._spacing.get(str(index))}{nline}\n"
