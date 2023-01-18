from PyQt6.QtWidgets import QScrollArea, QTextEdit


class CodeField(QScrollArea):
    @property
    def text(self):
        return self._text

    def __init__(self, placeholder_text, read_only):
        super().__init__()

        self.setWidgetResizable(True)

        self._text = QTextEdit()
        self._text.setReadOnly(read_only)
        self._text.setTabChangesFocus(False)
        self._text.setContentsMargins(0, 0, 0, 0)
        self._text.setPlaceholderText(placeholder_text)
        self._text.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
        self._text.keyPressEvent = self.keyPressEvent
        self._text.setTabStopDistance(
            8 * self._text.fontMetrics().horizontalAdvance(' ')
        )

        self.setWidget(self._text)

    def keyPressEvent(self, event):
        if event.key() == 16777217:
            self._text.insertPlainText(" " * 4)
        else:
            QTextEdit.keyPressEvent(self._text, event)
