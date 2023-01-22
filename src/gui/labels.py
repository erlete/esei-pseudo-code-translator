"""Container module for labels in the application.

This module contains the labels used in the application. The standard label is
represented by the `Text` class. Some extended labels are also provided, such as
`Header1` and `Header2`.

Authors:
    Paulo Sanchez (@erlete)
"""

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QLabel


class Text(QLabel):
    """Standard text label.

    This class represents the standard text format of the application. Extended
    text formats can be added by inheriting from this class.

    Attributes:
        font_name (str): the name of the font.
        font_size (int): the size of the font.
        font_weight (QFont.Weight): the weight of the font.
        text_alignment (Qt.AlignmentFlag): the alignment of the text.
        contents_margins (tuple): the margins of the text.
        WEIGHTS (dict): the weights of the font.
        ALIGNMENTS (dict): the alignments of the text.
    """

    WEIGHTS = {
        "normal": QFont.Weight.Normal,
        "bold": QFont.Weight.Bold,
        "light": QFont.Weight.Light,
        "thin": QFont.Weight.Thin,
        "black": QFont.Weight.Black,
        "demibold": QFont.Weight.DemiBold,
        "medium": QFont.Weight.Medium,
        "extrabold": QFont.Weight.ExtraBold,
        "extralight": QFont.Weight.ExtraLight
    }

    ALIGNMENTS = {
        "left": Qt.AlignmentFlag.AlignLeft,
        "right": Qt.AlignmentFlag.AlignRight,
        "center": Qt.AlignmentFlag.AlignCenter,
        "justify": Qt.AlignmentFlag.AlignJustify
    }

    def __init__(self, *args, **kwargs) -> None:
        """Initialize the text label.

        Args:
            *args: the arguments.
            **kwargs: the keyword arguments.
        """
        super().__init__(*args, **kwargs)

        self.font_name = "Menlo"
        self.font_size = 13
        self.font_weight = self.WEIGHTS["normal"]
        self.text_alignment = self.ALIGNMENTS["left"]
        self.contents_margins = (11, 11, 11, 11)

        self.setup()

    def setup(self) -> None:
        """Set up the text label."""
        self.setFont(QFont(
            self.font_name,
            self.font_size,
            self.font_weight
        ))
        self.setAlignment(self.text_alignment)
        self.setContentsMargins(*self.contents_margins)


class TextBoxLabel(Text):
    """Text box element head label.

    Attributes:
        font_name (str): the name of the font.
        font_size (int): the size of the font.
        font_weight (QFont.Weight): the weight of the font.
        text_alignment (Qt.AlignmentFlag): the alignment of the text.
        contents_margins (tuple): the margins of the text.
    """

    def __init__(self, *args, **kwargs) -> None:
        """Initialize the text label.

        Args:
            *args: the arguments.
            **kwargs: the keyword arguments.
        """
        super().__init__(*args, **kwargs)

        self.font_name = "Menlo"
        self.font_size = 12
        self.font_weight = self.WEIGHTS["bold"]
        self.text_alignment = self.ALIGNMENTS["center"]
        self.contents_margins = (5, 10, 0, 5)

        self.setup()


class Header1(Text):
    """Header 1 text label.

    Attributes:
        font_name (str): the name of the font.
        font_size (int): the size of the font.
        font_weight (QFont.Weight): the weight of the font.
        text_alignment (Qt.AlignmentFlag): the alignment of the text.
        contents_margins (tuple): the margins of the text.
    """

    def __init__(self, *args, **kwargs) -> None:
        """Initialize the text label.

        Args:
            *args: the arguments.
            **kwargs: the keyword arguments.
        """
        super().__init__(*args, **kwargs)

        self.font_name = "Menlo"
        self.font_size = 20
        self.font_weight = self.WEIGHTS["normal"]
        self.text_alignment = self.ALIGNMENTS["left"]
        self.contents_margins = (20, 20, 20, 20)

        self.setup()


class Header2(Text):
    """Header 2 text label.

    Attributes:
        font_name (str): the name of the font.
        font_size (int): the size of the font.
        font_weight (QFont.Weight): the weight of the font.
        text_alignment (Qt.AlignmentFlag): the alignment of the text.
        contents_margins (tuple): the margins of the text.
    """

    def __init__(self, *args, **kwargs) -> None:
        """Initialize the text label.

        Args:
            *args: the arguments.
            **kwargs: the keyword arguments.
        """
        super().__init__(*args, **kwargs)

        self.font_name = "Menlo"
        self.font_size = 18
        self.font_weight = self.WEIGHTS["normal"]
        self.text_alignment = self.ALIGNMENTS["left"]
        self.contents_margins = (18, 18, 18, 18)

        self.setup()


class Header3(Text):
    """Header 3 text label.

    Attributes:
        font_name (str): the name of the font.
        font_size (int): the size of the font.
        font_weight (QFont.Weight): the weight of the font.
        text_alignment (Qt.AlignmentFlag): the alignment of the text.
        contents_margins (tuple): the margins of the text.
    """

    def __init__(self, *args, **kwargs) -> None:
        """Initialize the text label.

        Args:
            *args: the arguments.
            **kwargs: the keyword arguments.
        """
        super().__init__(*args, **kwargs)

        self.font_name = "Menlo"
        self.font_size = 16
        self.font_weight = self.WEIGHTS["normal"]
        self.text_alignment = self.ALIGNMENTS["left"]
        self.contents_margins = (16, 16, 16, 16)

        self.setup()


class Title(Text):
    """Title text label.

    Attributes:
        font_name (str): the name of the font.
        font_size (int): the size of the font.
        font_weight (QFont.Weight): the weight of the font.
        text_alignment (Qt.AlignmentFlag): the alignment of the text.
        contents_margins (tuple): the margins of the text.
    """

    def __init__(self, *args, **kwargs) -> None:
        """Initialize the text label.

        Args:
            *args: the arguments.
            **kwargs: the keyword arguments.
        """
        super().__init__(*args, **kwargs)

        self.font_name = "Menlo"
        self.font_size = 30
        self.font_weight = self.WEIGHTS["normal"]
        self.text_alignment = self.ALIGNMENTS["center"]
        self.contents_margins = (30, 30, 30, 30)

        self.setup()


class Subtitle(Text):
    """Subtitle text label.

    Attributes:
        font_name (str): the name of the font.
        font_size (int): the size of the font.
        font_weight (QFont.Weight): the weight of the font.
        text_alignment (Qt.AlignmentFlag): the alignment of the text.
        contents_margins (tuple): the margins of the text.
    """

    def __init__(self, *args, **kwargs) -> None:
        """Initialize the text label.

        Args:
            *args: the arguments.
            **kwargs: the keyword arguments.
        """
        super().__init__(*args, **kwargs)

        self.font_name = "Menlo"
        self.font_size = 14
        self.font_weight = self.WEIGHTS["normal"]
        self.text_alignment = self.ALIGNMENTS["center"]
        self.contents_margins = (14, 14, 14, 14)

        self.setup()


class Footer(Text):
    """Footer text label.

    Attributes:
        font_name (str): the name of the font.
        font_size (int): the size of the font.
        font_weight (QFont.Weight): the weight of the font.
        text_alignment (Qt.AlignmentFlag): the alignment of the text.
        contents_margins (tuple): the margins of the text.
    """

    def __init__(self, *args, **kwargs) -> None:
        """Initialize the text label.

        Args:
            *args: the arguments.
            **kwargs: the keyword arguments.
        """
        super().__init__(*args, **kwargs)

        self.font_name = "Menlo"
        self.font_size = 8
        self.font_weight = self.WEIGHTS["normal"]
        self.text_alignment = self.ALIGNMENTS["center"]
        self.contents_margins = (8, 8, 8, 8)

        self.setup()
