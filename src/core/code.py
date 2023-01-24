from .scanner import Scanner


class Code:

    def __init__(self, scanner: Scanner):
        self.scanner = scanner
        self._set_top()
        self._set_bottom()

    def _set_top(self):
        self.top = []
        for block in self.scanner.blocks:
            self.top.extend(block.top)

    def _set_bottom(self):
        self.bottom = []
        for block in self.scanner.blocks:
            self.bottom.extend(block.bottom)

    def render(self) -> str:
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
