"""Structural module for code organization and rendering.

This module contains the `Block` class, which is used to represent a block of
code. Furthermore, it also contains the `InterpreterConfig` class, which is
used to configure the emulated Python interpreter.

Author:
    Paulo Sanchez (@erlete)
"""

from __future__ import annotations

from typing import Any

import regex as re


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
        HEADER (str): regular expression to match the header of the for loop.
        FOOTER (str): regular expression to match the footer of the for loop.
        FLAGS (int): flags to use when matching the header and footer.
    """

    HEADER: str | None = None
    FOOTER: str | None = None
    FLAGS: int = re.IGNORECASE | re.MULTILINE

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
        self._header = self.lines[0]
        self._footer = self.lines[-1]
        self.parent: Block | None = None
        self.children: list[Block] = list()

        self._translate()

    def _translate(self):
        """Translate the block to Python code.

        This method represents the implementation of a custom translation
        method for each one of the classes that inherit from this class. This
        method is automatically called when the block is initialized.
        """
        pass

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
        lines: list[str] = [f"{outer_ind}{self._header}"]
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
        lines.append(f"{outer_ind}{self._footer}")
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
        return f"{self.__class__.__name__}({self.start}, {self.end})"

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


class ForLoop(Block):
    """For loop structural class.

    Attributes:
        start (int): start line number of the for loop.
        end (int): end line number of the for loop.
        lines (list): list of lines of code in the for loop.
        parent (Block): parent block of the for loop.
        children (list): list of children blocks of the for loop.
        HEADER (str): regular expression to match the header of the loop.
        FOOTER (str): regular expression to match the footer of the loop.
        FLAGS (int): flags to use when matching the header and footer.
    """

    HEADER = r"^desde\s+"
    FOOTER = r"^fin_desde$"


class WhileLoop(Block):
    """While loop structural class.

    Attributes:
        start (int): start line number of the for loop.
        end (int): end line number of the for loop.
        lines (list): list of lines of code in the for loop.
        parent (Block): parent block of the for loop.
        children (list): list of children blocks of the for loop.
        HEADER (str): regular expression to match the header of the loop.
        FOOTER (str): regular expression to match the footer of the loop.
        FLAGS (int): flags to use when matching the header and footer.
    """

    HEADER = r"^mientras\s+"
    FOOTER = r"^fin_mientras$"


class DoWhileLoop(Block):
    """Do-while loop structural class.

    Attributes:
        start (int): start line number of the for loop.
        end (int): end line number of the for loop.
        lines (list): list of lines of code in the for loop.
        parent (Block): parent block of the for loop.
        children (list): list of children blocks of the for loop.
        HEADER (str): regular expression to match the header of the loop.
        FOOTER (str): regular expression to match the footer of the loop.
        FLAGS (int): flags to use when matching the header and footer.
    """

    HEADER = r"^hacer$"
    FOOTER = r"^mientras\s+"


class IfStatement(Block):
    """If statement structural class.

    Attributes:
        start (int): start line number of the for loop.
        end (int): end line number of the for loop.
        lines (list): list of lines of code in the for loop.
        parent (Block): parent block of the for loop.
        children (list): list of children blocks of the for loop.
        HEADER (str): regular expression to match the header of the statement.
        FOOTER (str): regular expression to match the footer of the statement.
        FLAGS (int): flags to use when matching the header and footer.
    """

    HEADER = r"^si\s+"
    FOOTER = r"^fin_si$"

    def _translate(self):
        """Translate the block.

        This method is a specific implementation of the `Block._translate`
        method. Refer to the original documentation for further information.
        """
        self._translate_header()
        self._translate_footer()

    def _translate_header(self):
        """Translate the header of the block.

        This method translates the syntax of the header of the block and
        converts it to a equivalent Python statement.
        """
        self._header = re.sub(
            r"^si\s+(.*?)\s+entonces$",
            r"if \1:",
            self.lines[0],
            self.FLAGS
        )

    def _translate_footer(self):
        """Translate the footer of the block.

        This method translates the syntax of the footer of the block and
        converts it to a equivalent Python statement.
        """
        self._footer = re.sub(
            r"^fin_si$",
            '',
            self.lines[-1],
            self.FLAGS
        )

    def render(self, indentation_level: int = 0,
               no_recursion: bool = False) -> list[str]:
        """Render the block.

        This method is a specific implementation of the `Block.render` method.
        Refer to the original documentation for further information.

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

        lines: list[str] = [f"{outer_ind}{self._header}"]
        for line in self.lines[1:-1]:
            if isinstance(line, Block):
                if no_recursion:
                    lines.append(f"{inner_ind}{line!r}")
                else:
                    sub_render = line.render(indentation_level + 1)
                    lines.extend(sub_render)
            else:
                if re.match(r"^si_no", line, self.FLAGS):
                    lines.append(f"{outer_ind}else:")
                else:
                    lines.append(f"{inner_ind}{line}")

        lines.append(f"{outer_ind}{self._footer}")
        return lines


class MatchStatement(Block):
    """Match statement structural class.

    Attributes:
        start (int): start line number of the for loop.
        end (int): end line number of the for loop.
        lines (list): list of lines of code in the for loop.
        parent (Block): parent block of the for loop.
        children (list): list of children blocks of the for loop.
        HEADER (str): regular expression to match the header of the statement.
        FOOTER (str): regular expression to match the footer of the statement.
        FLAGS (int): flags to use when matching the header and footer.
    """

    HEADER = r"^caso\s+"
    FOOTER = r"^fin_caso$"


class Function(Block):
    """Function structural class.

    Attributes:
        start (int): start line number of the for loop.
        end (int): end line number of the for loop.
        lines (list): list of lines of code in the for loop.
        parent (Block): parent block of the for loop.
        children (list): list of children blocks of the for loop.
        HEADER (str): regular expression to match the header of the function.
        FOOTER (str): regular expression to match the footer of the function.
        FLAGS (int): flags to use when matching the header and footer.
    """

    HEADER = r"^.+funcion"
    FOOTER = r"^fin_funcion$"


class Procedure(Block):
    """Procedure structural class.

    Attributes:
        start (int): start line number of the for loop.
        end (int): end line number of the for loop.
        lines (list): list of lines of code in the for loop.
        parent (Block): parent block of the for loop.
        children (list): list of children blocks of the for loop.
        HEADER (str): regular expression to match the header of the function.
        FOOTER (str): regular expression to match the footer of the function.
        FLAGS (int): flags to use when matching the header and footer.
    """

    HEADER = r"^.+procedimiento"
    FOOTER = r"^fin_procedimiento$"


class Main(Function):
    """Main function structural class.

    Attributes:
        start (int): start line number of the for loop.
        end (int): end line number of the for loop.
        lines (list): list of lines of code in the for loop.
        parent (Block): parent block of the for loop.
        children (list): list of children blocks of the for loop.
        HEADER (str): regular expression to match the header of the function.
        FOOTER (str): regular expression to match the footer of the function.
        FLAGS (int): flags to use when matching the header and footer.
    """

    HEADER = r"^inicio$"
    FOOTER = r"^fin$"


TYPES: Any = (
    ForLoop, WhileLoop, DoWhileLoop, IfStatement, MatchStatement,
    Function, Procedure, Main
)
