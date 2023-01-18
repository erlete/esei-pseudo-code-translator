from .logger import Logger
from .block import Block


class Scanner:

    BLOCK_TYPES = {
        "for": ("desde ", "fin_desde"),
        "while": ("mientras ", "fin_mientras"),
        "if": ("si ", "fin_si"),
        "match": ("caso ", "fin_caso")
    }

    def __init__(self, code: str, log_level=2):
        self.code = code
        self.lines = [line.strip() for line in code.lower().splitlines()]
        self.logger = Logger(log_level)
        self.blocks = []
        self.roots = []

    def scan(self):
        blocks = []
        for block_type in self.BLOCK_TYPES:
            header, footer = self.BLOCK_TYPES[block_type]

            i = 0
            while i < len(self.lines):
                line = self.lines[i]
                self.logger.log(f"{i:0>3} - Analyzing line: \"{line}\"", 0)

                if header in line:
                    self.logger.log(
                        f"{i:0>3} - Found open statement. Recursing...", 0
                    )
                    blocks.extend(self._find_blocks(
                        self.lines, header, footer, i + 1))
                    self.logger.log(f"{i:0>3} - Returning to root...", 0)

                i += 1

        self.blocks = list(set(blocks))
        self._set_hierarchy()

    def _find_blocks(self, lines, header, footer, start):
        blocks = []
        self.logger.log(
            f"Searching for \"{header}\" or \"{footer}\" from line {start}",
            0
        )

        i = 0
        while i < len(lines[start:]):
            line = lines[start:][i]

            self.logger.log(
                f"({start + i:0>3}) {i:0>3} - Analyzing line: \"{line}\"",
                0
            )

            if header in line:
                self.logger.log(
                    f"({start + i:0>3}) {i:0>3} - Found open statement. "
                    + "Recursing...",
                    0
                )

                blocks.extend(self._find_blocks(lines, header,
                                                footer, i + start + 1))
                i = max(blocks, key=lambda x: x.end).end - start

            if footer in line:
                self.logger.log(
                    f"({start + i:0>3}) {i:0>3} - Found close statement. "
                    + "Returning to previous call...",
                    0
                )

                blocks.append(
                    Block(lines[start - 1:start + i + 1], start - 1, start + i))

                return blocks

            i += 1

        return blocks

    def _set_hierarchy(self):
        for block in self.blocks:
            remaining = [other for other in self.blocks if block in other]

            if remaining:
                parent = min(
                    remaining,
                    key=lambda x: abs(x.start - block.start)
                )
                block.parent = parent
                parent.children.append(block)

        self._set_roots()

    def _set_roots(self):
        self.roots = sorted(
            [block for block in self.blocks if block.is_root()])
        for root in sorted(self.roots):
            root.fold()

    def tree(self):
        output = ''
        for root in self.roots:
            output += root.tree()
        return output.strip()

    def render(self):
        output = ''
        for root in self.roots:
            output += '\n'.join(root.render()) + '\n'
        return output.strip()
