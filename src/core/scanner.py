"""Container module for the `Scanner` class.

Author:
    Paulo Sanchez (@erlete)
"""


import regex as re

from .block import Block, TYPES
from .logger import Logger


class Scanner:
    """Code scanning class.

    This class is responsible for scanning the code and finding the blocks
    that make up the program. It also sets the hierarchy of the blocks.

    Attributes:
        code (str): the code to be scanned.
        lines (list[str]): the code trimmed and split into lines.
        logger (Logger): the logger instance.
        blocks (list[Block]): the list of blocks found in the code.
        roots (list[Block]): the list of root blocks found in the code.
        BLOCK_TYPES (dict[str, tuple[str, str]]): the block types and their
            delimiters.
    """

    def __init__(self, code: str, log_level: int = 2) -> None:
        """Initialize a scanner instance.

        Args:
            code (str): the code to be scanned.
            log_level (int): the log level to be used.
        """
        self.code = code
        self.lines = [line.strip() for line in code.lower().splitlines()]
        self.logger = Logger(log_level)
        self.blocks: list[Block] = []
        self.roots: list[Block] = []

    def scan(self) -> None:
        """Scan the code and find the blocks.

        This method scans the code and finds the blocks that make up the
        program. It also sets the hierarchy of the blocks.
        """
        blocks = []
        for block_type in TYPES:
            i = 0
            di = i + 1  # Displayed index.

            self.logger.log(
                f"Searching for {block_type.__name__} blocks...",
                log_level=1
            )

            while i < len(self.lines):
                line = self.lines[i]

                self.logger.log(
                    f"{di:0>3} - Analyzing \"{line}\"",
                    log_level=0
                )

                if re.match(block_type.HEADER, line, block_type.FLAGS):
                    self.logger.log(
                        f"{di:0>3} - Found header. Recursing...",
                        log_level=1
                    )

                    blocks.extend(
                        self._find_blocks(
                            self.lines,
                            block_type,
                            i + 1
                        )
                    )

                    self.logger.log(
                        f"{di:0>3} - Returning to root...",
                        log_level=1
                    )

                i += 1

        self.blocks = list(set(blocks))
        self._set_hierarchy()

    def _find_blocks(self, lines: list[str],
                     block_type, start: int) -> list[Block]:
        """Identify blocks in the code.

        This method is a recursive function that finds the blocks in the code
        and returns them as a list.

        Args:
            lines (list[str]): the code trimmed and split into lines.
            block_type (Block): the block type to search for.
            start (int): the line to start searching from.
        """
        blocks = []
        header, footer = block_type.HEADER, block_type.FOOTER

        self.logger.log(
            f"Searching for \"{header}\" or \"{footer}\" from line {start}",
            log_level=0
        )

        i = 0
        while i < len(lines[start:]):
            di = i + 1  # Displayed index.
            line = lines[start:][i]

            self.logger.log(
                f"({start + di:0>3}) {di:0>3} - Analyzing \"{line}\"",
                log_level=0
            )

            if re.match(header, line, re.IGNORECASE | re.MULTILINE):
                self.logger.log(
                    f"({start + di:0>3}) {di:0>3} - Found header. "
                    + "Recursing...",
                    log_level=0
                )

                blocks.extend(
                    self._find_blocks(
                        lines,
                        block_type,
                        i + start + 1
                    )
                )

                if blocks:
                    i = max(blocks, key=lambda x: x.end).end - start
                    self.logger.log(f"Detected blocks {blocks}", log_level=1)
                else:
                    self.logger.log("No blocks detected", log_level=2)

            if re.match(footer, line, re.IGNORECASE | re.MULTILINE):
                self.logger.log(
                    f"({start + di:0>3}) {di:0>3} - Found footer. "
                    + "Returning to previous call...",
                    log_level=0
                )

                blocks.append(block_type(
                    lines[start - 1:start + i + 1],
                    start - 1,
                    start + i
                ))

                return blocks

            i += 1

        return blocks

    def _set_hierarchy(self) -> None:
        """Set the hierarchy of the blocks.

        This method sets the hierarchy of the blocks by setting the parent
        and children attributes of each block.
        """
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

    def _set_roots(self) -> None:
        """Set the root blocks.

        This method sets the root blocks by finding the blocks that have no
        parent.
        """
        self.roots = sorted(
            [block for block in self.blocks if block.is_root()])
        for root in sorted(self.roots):
            root.fold()

        for block in sorted(self.blocks):
            block.translate()

    def tree(self) -> str:
        """Return the unrendered, indented representation of the blocks.

        Returns:
            str: the tree unrendered, indented representation of the blocks.
        """
        output = ''
        for root in self.roots:
            output += root.tree()
        return output.strip()

    def render(self) -> str:
        """Return the rendered, indented representation of the blocks.

        Returns:
            str: the rendered, indented representation of the blocks.
        """
        output = ''
        for root in self.roots:
            output += '\n'.join(root.render()) + '\n'
        return output.strip()
