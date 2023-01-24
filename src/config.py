"""Configuration module.

This module contains all the configuration constants, methods and classes
required to properly configure the application.

Authors:
    Paulo Sanchez (@erlete)
"""


import regex as re


class RegexConfig:
    """Base class for regular expresion usage configuration.

    This class provides with some attributes that allow customization of the
    regular expression instructions used by the rest of the modules.

    Attributes:
        FLAGS (Any): collection of regex flags for pattern matching.
    """

    FLAGS = re.MULTILINE | re.IGNORECASE


class EditorConfig:
    """Base class for editor configuration.

    This class provides with some attributes that allow customization of the
    code editor emulated inside the application.

    Attributes:
        SPACES_PER_TAB (int): number of spaces per tab.
        INDENTATION_CHAR (str): character used for indentation.
    """

    SPACES_PER_TAB: int = 4
    INDENTATION_CHAR: str = ' '
