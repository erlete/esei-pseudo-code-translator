"""Container module for the `Scanner` class.

Authors:
    Paulo Sanchez (@erlete)
"""


import regex as re

from .block import TYPES, Block


class Scanner:
    """Code scanning and organization class.

    This class is responsible for scanning the code and finding the blocks
    that compose the program. It also sets the hierarchy of the blocks,
    collapses its contents and translates them.

    Attributes:
        code (str): the code to be scanned.
        lines (list[str]): the code trimmed and split into lines.
        blocks (list[Block]): the list of blocks found in the code.
        roots (list[Block]): the list of root blocks found in the code.
    """

    def __init__(self, code: str) -> None:
        """Initialize a scanner instance.

        Args:
            code (str): the code to be scanned.
        """
        self.code = code
        self.lines = [line.strip() for line in code.splitlines()]
        self.blocks: list[Block] = []
        self.roots: list[Block] = []

    def scan(self) -> None:
        """Scan the code and find structural blocks.

        This method is a public caller for the recursive `Scanner._scan`
        method, which is responsible for iterating over the code and each
        block type, identifying its header and footer and enclosing the body
        in between.
        """
        self.blocks = self._scan(start=0)
        self._organize()

    def _scan(self, start: int) -> list[Block]:
        """Scan the code and find structural blocks.

        This method iterates over each line of code and every defined block
        type, identifying the corresponding headers and footers with each line
        of code and classifying the blocks accordingly.

        Args:
            start (int): the index from which the search begins.

        Returns:
            list[Block]: the list of identified `Block` elements.

        Notes:
            This method should not be called directly, since it is designed for
            internal use and it might have undefined outputs if it is called
            manually.
        """
        blocks = []

        i = 0
        while i < len(self.lines[start:]):
            line = self.lines[start:][i]

            for block_type in TYPES:
                header, footer = block_type.HEADER, block_type.FOOTER

                if re.match(header, line, flags=block_type.FLAGS):
                    blocks.extend(self._scan(start + i + 1))

                    if blocks:
                        indices = {block.end: block for block in blocks}
                        i = indices[max(indices)].end - start

                if re.match(footer, line, flags=block_type.FLAGS):
                    blocks.append(
                        block_type(
                            self.lines[start - 1:start + i + 1],
                            start - 1,
                            start + i
                        )
                    )

                    return blocks

            i += 1

        return blocks

    def _organize(self) -> None:
        """Organize scanned blocks.

        This method calls several other methods that set up the block
        hierarchy, define the roots of the block tree, collapse nested blocks
        and translate their contents.
        """
        self._set_hierarchy()
        self._set_roots()
        self._collapse()
        self._translate()

    def _set_hierarchy(self) -> None:
        """Set the hierarchy of the blocks.

        This method sets the hierarchy of the blocks by setting the parent
        and children attributes of each block based on the containment of some
        blocks into others.
        """
        for block in self.blocks:
            remaining = [other for other in self.blocks if block in other]

            if remaining:
                distances = {
                    abs(other.start - block.start): other
                    for other in remaining
                }
                parent = distances[min(distances)]

                block.parent = parent
                parent.children.append(block)

    def _set_roots(self) -> None:
        """Set the root blocks.

        This method sets the root blocks by finding the blocks that have no
        parent.
        """
        self.roots = sorted(
            [block for block in self.blocks if block.is_root()]
        )

    def _collapse(self) -> None:
        """Collapse the contents of the blocks."""
        for root in sorted(self.roots):
            root.fold()

    def _translate(self) -> None:
        """Translate scanned blocks."""
        for block in sorted(self.blocks):
            block.translate()

    def render(self, collapsed: bool = False) -> str:
        """Render the tree block representation.

        Args:
            collapsed (bool, optional): whether to render the block tree
                collapsing the contents of each block or not. Defaults to
                False.

        Returns:
            str: the rendered and indented tree block representation.
        """
        if collapsed:
            return ''.join(root.tree() for root in self.roots).strip()

        return '\n'.join(
            '\n'.join(root.render())
            for root in self.roots
        ).strip()
