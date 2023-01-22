"""Container module for text fields in the application.

This module contains the text fields used in the application. These are the
text fields that are used to receive input text and display output text.

Authors:
    Paulo Sanchez (@erlete)
"""

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QKeyEvent
from PyQt6.QtWidgets import QScrollArea, QTextEdit


class CodeField(QScrollArea):
    """A scrollable text field for code.

    Attributes:
        text (QTextEdit): the text field.
    """

    def __init__(self, placeholder_text: str, read_only: bool = True) -> None:
        """Initialize the code field.

        Args:
            placeholder_text (str): the placeholder text.
            read_only (bool): whether the field is read-only.
        """
        super().__init__()

        self.setWidgetResizable(True)

        self._text = QTextEdit()
        self._text.setReadOnly(read_only)
        self._text.setTabChangesFocus(False)
        self._text.setContentsMargins(0, 0, 0, 0)
        self._text.setPlaceholderText(placeholder_text)
        self._text.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
        self._text.keyPressEvent = self.key_press_event  # type: ignore
        self._text.setTabStopDistance(
            8 * self._text.fontMetrics().horizontalAdvance(' ')
        )

        self.setFont(QFont(
            "Monaco",
            11,
            QFont.Weight.Normal
        ))
        self.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.setContentsMargins(11, 11, 11, 11)

        self.setWidget(self._text)

    @property
    def text(self) -> QTextEdit:
        """Get the text field.

        Returns:
            QTextEdit: the text field.
        """
        return self._text

    def key_press_event(self, event: QKeyEvent) -> None:
        """Handle key press events.

        Args:
            event (QKeyEvent): the key press event.
        """
        if event.key() == 16777217:
            self._text.insertPlainText(" " * 4)
        else:
            QTextEdit.keyPressEvent(self._text, event)
