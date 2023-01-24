"""Configuration module.

This module contains all the configuration constants, methods and classes
required to properly configure the application.

Authors:
    Paulo Sanchez (@erlete)
"""


class InterpreterConfig:
    """Base class for interpreter configuration.

    This class provides with some attributes that allow customization of the
    emulated Python interpreter. These attributes are used by the `Block` class
    to render the code.

    Attributes:
        SPACES_PER_TAB (int): number of spaces per tab.
        INDENTATION_CHAR (str): character used for indentation.
    """

    SPACES_PER_TAB: int = 4
    INDENTATION_CHAR: str = ' '
