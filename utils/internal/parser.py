"""Container module for the pseudo code parser classes.

This script contains the main parser class and the interface that adds
its essential components.

Author:
-------
 - Paulo Sánchez (@erlete)
"""


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
        rf"{_SP}mod{_SP}": " % ",        # Modulus.
        rf"{_SP}\+{_SP}": " + ",         # Addition.
        rf"{_SP}\*{_SP}": " * ",         # Multiplication.
        rf"{_SP}\/{_SP}": " / ",         # Division.
        rf"{_SP}\-{_SP}": " - ",         # Subtraction.
        rf"{_SP}\<{_SP}": " < ",         # Lower than.
        rf"{_SP}\>{_SP}": " > ",         # Greater than.
        rf"{_SP}\<{_SP}={_SP}": " <= ",  # Lower than or equal to.
        rf"{_SP}\>{_SP}={_SP}": " >= "   # Greater than or equal to.
    }

    _STATEMENTS = {
        r"escribir[ ]{0,}\(": "print("
    }

    _REDUNDANT = (
        r"[ ]{0,}fin_\w+",
    )

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
        self._remove_redundant_statements()
        self._parse_operators()
        self._parse_statements()

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

    def _remove_redundant_statements(self):
        """Removes redundant statements from the parsed code.

        This method removes redundant statements from the parsed code using
        the `PseudoCodeParserBase._REDUNDANT` collection.
        """

        for index, _ in enumerate(self._lines):
            for expression in self._REDUNDANT:
                self._lines[index] = re.sub(
                    expression,
                    '',
                    self._lines[index]
                )

    def _parse_operators(self):
        """Converts pseudo code symbols Python ones.

        This method uses `PseudoCodeParserBase._SYMBOLS` map to replace each
        pseudo code expression with its Python equivalent.
        """

        for index, _ in enumerate(self._lines):
            for expression, replacement in self._OPERATORS.items():
                self._lines[index] = re.sub(
                    expression,
                    replacement,
                    self._lines[index]
                )

    def _parse_statements(self):
        """Converts pseudo code statements into Python ones.

        This method uses `PseudoCodeParserBase._STATEMENTS` map to replace each
        pseudo code expression with its Python equivalent.
        """

        for index, _ in enumerate(self._lines):
            for expression, replacement in self._STATEMENTS.items():
                self._lines[index] = re.sub(
                    expression,
                    replacement,
                    self._lines[index]
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

        step = 1
        increment = self._BEHAVIOR.get("range_end_inclusive")
        line = line.split(' ')

        # Check for 6 elements and numeric start/end values:
        if len(line) >= 6 and (line[3] + line[5]).isnumeric():

            # Check for 8 elements containing keyword and numeric step value:
            if len(line) >= 8 and "paso" in line and line[7].isnumeric():
                step = int(line[7])

            end = int(line[5]) + increment

            return f"for {line[1]} in range({line[3]}, {end}, {step}):"

        return ' '.join(line)

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

        args = line.split(' ')

        if args[0] == "si_no":
            return "else:"

        if len(args) >= 6 and (f" {args[2]} " in self._OPERATORS.values()
                and f" {args[4]} " in self._OPERATORS.values()):
            return f"if {args[1]} {args[2]} {args[3]} {args[4]} {args[5]}:"

        elif len(args) >= 4 and f" {args[2]} " in self._OPERATORS.values():
            return f"if {args[1]} {args[2]} {args[3]}:"

        return line

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
