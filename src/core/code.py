"""Container module for the `Code` class.

Authors:
    Paulo Sanchez (@erlete)
"""


from .scanner import Scanner


class Code:
    """Code organization class.

    This class is responsible for organizing and rendering final code blocks.
    It is required due to the fact that some code blocks require header or
    footer statements, such as `global` declarations for variables or `main`
    function calls at the bottom of the script.

    Attributes:
        scanner (Scanner): the scanner object that identifies blocks.
        top (list[str]): global declarations at the top of the script.
        bottom (list[str]): function calls at the bottom of the script.
    """

    def __init__(self, scanner: Scanner):
        """Initialize code instance.

        Args:
            scanner (Scanner): tje scanner object that identifies blocks.
        """
        self.scanner = scanner
        self._set_top()
        self._set_bottom()

    def _set_top(self):
        """Set top statements."""
        self.top = []
        for block in self.scanner.blocks:
            self.top.extend(block.top)

    def _set_bottom(self):
        """Set bottom statements."""
        self.bottom = []
        for block in self.scanner.blocks:
            self.bottom.extend(block.bottom)

    def render(self) -> str:
        """Render the final organized code.

        Returns:
            str: the final organized code.
        """
        if self.top:
            header = f"global {', '.join(str(top) for top in self.top)}\n"
        else:
            header = ''

        if self.bottom:
            footer = '\n'.join(str(bottom) for bottom in self.bottom)
            footer = f"\n\n{footer}\n"
        else:
            footer = ''

        return f"{header}{self.scanner.render()}{footer}"
