"""Container module for the `Code` class.

Authors:
    Paulo Sanchez (@erlete)
"""


from .scanner import Scanner
from .block import Main


class Code:
    """Code organization class.

    This class is responsible for correctly assigning global declarations to
    the main function, as well as defining function calls at the bottom of the
    program.

    Attributes:
        scanner (Scanner): the scanner object that identifies blocks.
        globals (list[str]): global declarations at the top of the script.
        calls (list[str]): function calls at the bottom of the script.
    """

    def __init__(self, scanner: Scanner):
        """Initialize code instance.

        Args:
            scanner (Scanner): tje scanner object that identifies blocks.
        """
        self.scanner = scanner
        self._set_globals()
        self._set_calls()

    def _set_globals(self):
        """Set global statements."""
        self.globals = []
        for block in self.scanner.blocks:
            self.globals.extend(block.globals)

    def _set_calls(self):
        """Set call statements."""
        self.calls = []
        for block in self.scanner.blocks:
            self.calls.extend(block.calls)

    def render(self) -> str:
        """Render the final organized code.

        Returns:
            str: the final organized code.
        """
        if self.calls:
            footer = '\n'.join(str(bottom) for bottom in self.calls)
            footer = f"\n\n{footer}\n"
        else:
            footer = ''

        main_index = None
        for i, block in enumerate(self.scanner.blocks):
            if isinstance(block, Main):
                main_index = i
                break

        if main_index is not None and self.globals:
            self.scanner.blocks[main_index]._body = [
                f"global {', '.join(glob for glob in self.globals)}"
            ] + self.scanner.blocks[main_index]._body

        return f"{self.scanner.render()}{footer}"
