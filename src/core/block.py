"""Structural module for code organization and rendering.

This module contains the `Block` class, which is used to represent a block of
code. Furthermore, it also contains the `InterpreterConfig` class, which is
used to configure the emulated Python interpreter.

Author:
    Paulo Sanchez (@erlete)
"""

from __future__ import annotations


class InterpreterConfig:
    """Base class for interpreter configuration.

    This class provides with some attributes that allow customization of the
    emulated Python interpreter. These attributes are used by the `Block` class
    to render the code.

    Attributes:
        SPACES_PER_TAB (int): number of spaces per tab.
        INDENTATION_CHAR (str): character used for indentation.
    """

    SPACES_PER_TAB: int = 4
    INDENTATION_CHAR: str = ' '


class Block(InterpreterConfig):
    """Structural class for code organization and rendering.

    This class is used to represent a block of code, isolate it in order to
    allow internal modifications and render it recursively (also rendering
    children blocks).

    Attributes:
        lines (list[str | Block]): list of lines of code (can contain nested
            blocks).
        start (int): index of the first line of the block in the original code.
        end (int): index of the last line of the block in the original code.
        parent (Block | None): parent block.
        children (list[Block]): list of child blocks.
    """

    def __init__(self, lines: list[str | Block], start: int, end: int) -> None:
        """Initialize a new block.

        Args:
            lines (list[str | Block]): list of lines of code (can contain
                nested blocks).
            start (int): index of the first line of the block in the original
                code.
            end (int): index of the last line of the block in the original
                code.
        """
        self.lines = lines
        self.start = start
        self.end = end
        self.parent: Block | None = None
        self.children: list[Block] = list()

    def fold(self) -> None:
        """Fold blocks that contain children blocks.

        This method is used to fold blocks that contain children blocks. This
        is done by replacing the lines of the parent block with the children
        blocks. This method is called recursively on the children blocks.

        Note:
            This method should only be called on the root blocks in order to
            prevent redundant calls.
        """
        for child in sorted(self.children):
            offset = len(child.lines)
            for i in range(len(self.lines) - offset):
                if self.lines[i:i + offset] == child.lines:
                    self.lines[i:i + offset] = [child]
                    break

        for child in sorted(self.children):
            child.fold()

    def render(self, indentation_level: int = 0,
               no_recursion: bool = False) -> list[str]:
        """Render the block.

        This method is used to render the block recursively. This is done by
        replacing the children blocks with their rendered versions. This method
        is called recursively on the children blocks.

        Args:
            indentation_level (int): indentation level of the block.
            no_recursion (bool): if True, the children blocks will not be
                rendered.

        Returns:
            list[str]: list of lines of code.
        """
        spacing = self.SPACES_PER_TAB * self.INDENTATION_CHAR
        outer_ind = indentation_level * spacing
        inner_ind = (indentation_level + 1) * spacing

        lines: list[str] = [f"{outer_ind}{self.lines[0]}"]
        for line in self.lines[1:-1]:
            if isinstance(line, Block):
                if no_recursion:
                    lines.append(f"{inner_ind}{line!r}")
                else:
                    sub_render = line.render(indentation_level + 1)
                    lines.extend(sub_render)
            else:
                lines.append(f"{inner_ind}{line}")

        lines.append(f"{outer_ind}{self.lines[-1]}")
        return lines

    def is_root(self) -> bool:
        """Determine if the block is a root block.

        Returns:
            bool: True if the block is a root block, False otherwise.
        """
        return self.parent is None

    def is_leaf(self) -> bool:
        """Determine if the block is a leaf block.

        Returns:
            bool: True if the block is a leaf block, False otherwise.
        """
        return len(self.children) == 0

    def tree(self, indentation_level: int = 0) -> str:
        """Render the block tree recursively.

        This method is used to render the block tree recursively. This is done
        by recursively calling the `tree` method on the children blocks. The
        output is a list of strings with the representation of the block,
        indented according to the indentation level (automatically incremented
        by 1 for each recursive call).

        Args:
            indentation_level (int): indentation level of the block.

        Returns:
            str: string representation of the block tree.
        """
        output = f"{indentation_level * '  '}{self!r}\n"
        for child in sorted(self.children):
            output += (
                (indentation_level + 1) * '  '
                + child.tree(indentation_level + 1)
            )

        return output

    def __repr__(self) -> str:
        """Return the string representation of the block.

        Returns:
            str: string representation of the block.
        """
        return (f"Block({self.start}, {self.end})")

    def __str__(self) -> str:
        """Return the string representation of the block.

        Returns:
            str: string representation of the block.
        """
        return self.__repr__()

    def __contains__(self, item) -> bool:
        """Determine if the block contains another block.

        Args:
            item (Block): block to check.

        Returns:
            bool: True if the block contains the other block, False otherwise.
        """
        return self.start < item.start and item.end < self.end

    def __len__(self) -> int:
        """Return the number of lines of code in the block.

        Returns:
            int: number of lines of code in the block.
        """
        return len(self.lines)

    def __eq__(self, other) -> bool:
        """Determine if the block is equal to another block.

        Args:
            other (Block): block to check.

        Returns:
            bool: True if the block is equal to the other block, False
                otherwise.
        """
        if not isinstance(other, Block):
            return False

        return self.start == other.start and self.end == other.end

    def __ne__(self, other) -> bool:
        """Determine if the block is not equal to another block.

        Args:
            other (Block): block to check.

        Returns:
            bool: True if the block is not equal to the other block, False
                otherwise.
        """
        if not isinstance(other, Block):
            return False

        return not self.__eq__(other)

    def __lt__(self, other) -> bool:
        """Determine if the block is less than another block.

        Args:
            other (Block): block to check.

        Returns:
            bool: True if the block is less than the other block, False
                otherwise.
        """
        if not isinstance(other, Block):
            return False

        return self.start < other.start

    def __gt__(self, other) -> bool:
        """Determine if the block is greater than another block.

        Args:
            other (Block): block to check.

        Returns:
            bool: True if the block is greater than the other block, False
                otherwise.
        """
        if not isinstance(other, Block):
            return False

        return self.start > other.start

    def __le__(self, other) -> bool:
        """Determine if the block is less than or equal to another block.

        Args:
            other (Block): block to check.

        Returns:
            bool: True if the block is less than or equal to the other block,
                False otherwise.
        """
        if not isinstance(other, Block):
            return False

        return self.start <= other.start

    def __ge__(self, other) -> bool:
        """Determine if the block is greater than or equal to another block.

        Args:
            other (Block): block to check.

        Returns:
            bool: True if the block is greater than or equal to the other
                block, False otherwise.
        """
        if not isinstance(other, Block):
            return False

        return self.start >= other.start

    def __hash__(self) -> int:
        """Return the hash of the block.

        The hash of the block is computed using the start and end line numbers.

        Returns:
            int: hash of the block.
        """
        return hash((self.start, self.end))
