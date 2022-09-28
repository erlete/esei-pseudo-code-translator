from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QLabel


class Text(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.font = QFont("Monaco", 11, QFont.Weight.Normal)

        self.setFont(self.font)
        self.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.setContentsMargins(11, 11, 11, 11)


class Header1(Text):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.font.setPointSize(20)
        self.setFont(self.font)
        self.setContentsMargins(20, 20, 20, 20)


class Header2(Text):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.font.setPointSize(18)
        self.setFont(self.font)
        self.setContentsMargins(18, 18, 18, 18)


class Header3(Text):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.font.setPointSize(16)
        self.setFont(self.font)
        self.setContentsMargins(16, 16, 16, 16)


class Title(Text):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.font.setPointSize(30)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setFont(self.font)
        self.setContentsMargins(30, 30, 30, 30)


class Subtitle(Text):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.font.setPointSize(14)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setFont(self.font)
        self.setContentsMargins(14, 14, 14, 14)


class Footer(Text):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.font.setPointSize(8)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setContentsMargins(8, 8, 8, 8)
