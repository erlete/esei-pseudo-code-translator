"""Container module for labels in the application.

This module contains the labels used in the application. These are the labels
that are used to display text.

Authors:
    Paulo Sanchez (@erlete)
"""

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QLabel


class Text(QLabel):
    """Standard text label.

    Attributes:
        _font (QFont): the font of the text.
    """

    def __init__(self, *args, **kwargs) -> None:
        """Initialize the text label.

        Args:
            *args: the arguments.
            **kwargs: the keyword arguments.
        """
        super().__init__(*args, **kwargs)

        self._font = QFont("Monaco", 14, QFont.Weight.Normal)

        self.setFont(self._font)
        self.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.setContentsMargins(11, 11, 11, 11)


class Header1(Text):
    """Header 1 text label.

    Attributes:
        _font (QFont): the font of the text.
    """

    def __init__(self, *args, **kwargs) -> None:
        """Initialize the text label.

        Args:
            *args: the arguments.
            **kwargs: the keyword arguments.
        """
        super().__init__(*args, **kwargs)

        self._font.setPointSize(20)
        self.setFont(self._font)
        self.setContentsMargins(20, 20, 20, 20)


class Header2(Text):
    """Header 2 text label.

    Attributes:
        _font (QFont): the font of the text.
    """

    def __init__(self, *args, **kwargs) -> None:
        """Initialize the text label.

        Args:
            *args: the arguments.
            **kwargs: the keyword arguments.
        """
        super().__init__(*args, **kwargs)

        self._font.setPointSize(18)
        self.setFont(self._font)
        self.setContentsMargins(18, 18, 18, 18)


class Header3(Text):
    """Header 3 text label.

    Attributes:
        _font (QFont): the font of the text.
    """

    def __init__(self, *args, **kwargs) -> None:
        """Initialize the text label.

        Args:
            *args: the arguments.
            **kwargs: the keyword arguments.
        """
        super().__init__(*args, **kwargs)

        self._font.setPointSize(16)
        self.setFont(self._font)
        self.setContentsMargins(16, 16, 16, 16)


class Title(Text):
    """Title text label.

    Attributes:
        _font (QFont): the font of the text.
    """

    def __init__(self, *args, **kwargs) -> None:
        """Initialize the text label.

        Args:
            *args: the arguments.
            **kwargs: the keyword arguments.
        """
        super().__init__(*args, **kwargs)

        self._font.setPointSize(30)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setFont(self._font)
        self.setContentsMargins(30, 30, 30, 30)


class Subtitle(Text):
    """Subtitle text label.

    Attributes:
        _font (QFont): the font of the text.
    """

    def __init__(self, *args, **kwargs) -> None:
        """Initialize the text label.

        Args:
            *args: the arguments.
            **kwargs: the keyword arguments.
        """
        super().__init__(*args, **kwargs)

        self._font.setPointSize(14)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setFont(self._font)
        self.setContentsMargins(14, 14, 14, 14)


class Footer(Text):
    """Footer text label.

    Attributes:
        _font (QFont): the font of the text.
    """

    def __init__(self, *args, **kwargs) -> None:
        """Initialize the text label.

        Args:
            *args: the arguments.
            **kwargs: the keyword arguments.
        """
        super().__init__(*args, **kwargs)

        self._font.setPointSize(8)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setContentsMargins(8, 8, 8, 8)


class TextBoxLabel(QLabel):
    """Text box element head label.

    Attributes:
        _font (QFont): the font of the text.
    """

    def __init__(self, *args, **kwargs) -> None:
        """Initialize the text label.

        Args:
            *args: the arguments.
            **kwargs: the keyword arguments.
        """
        super().__init__(*args, **kwargs)

        self._font = QFont("Arial", 14, QFont.Weight.Normal)
        self.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.setContentsMargins(5, 10, 0, 5)
