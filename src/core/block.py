"""Structural module for code organization and rendering.

This module contains three generic classes, `InterpreterConfig`, `Expression`
and `Block`, that are used to represent the code in a more structured way.
Furthermore, there are multiple other derived classes that are used to
represent specific structures of the code (`IfStatement`, `ForLoop`...).

Authors:
    Paulo Sanchez (@erlete)
"""

from __future__ import annotations

from typing import Any

import regex as re

from ..config import EditorConfig, RegexConfig


class Expression:
    """Class for single statement translation.

    This class is used to translate a single line of code into a valid Python
    expression.

    Attributes:
        body (str): line of code.
        OPERATORS (dict[str, str]): dictionary of operator translations.
        IDENTIFIERS (dict[str, str]): dictionary of identifier translations.
        REPR_LIMIT (int): the character limit for the collapsed representation
            of the expression.
    """

    OPERATORS: dict[str, str] = {
        r"\/\/": '#',
        r'(.*[^<>!])=(.*)': r"\1 == \2",
        r"(.*?)\s*<-\s*(.*)": r"\1 = \2",
        r"(.*?)\s*<>\s*(.*)": r"\1 != \2",
        r"(.*?)\s*MOD\s*(.*)": r"\1 % \2",
        r"(.*?)\s*==\s*(.*)": r"\1 == \2",
        r"\b(\w+)\s*<\s*(\w+)\b": r"\1 < \2",
        r"\b(\w+)\s*>\s*(\w+)\b": r"\1 > \2",
        r"(.*?)\s*<=\s*(.*)": r"\1 <= \2",
        r"(.*?)\s*>=\s*(.*)": r"\1 >= \2",
        r"(.*?)\s*\+\s*(.*)": r"\1 + \2",
        r"(.*?)\s*-\s*(.*)": r"\1 - \2",
        r"(.*?)\s*\*\s*(.*)": r"\1 * \2",
        r"(.*?)\s*\/\s*(.*)": r"\1 / \2"
    }

    IDENTIFIERS: dict[str, str] = {
        r"ESCRIBIR\s*\((.*)\)": r"print(\1)",
        r"LEER\s*\((.*)\)": r"\1 = input()",
        r"DEVOLVER\s*(.*)": r"return \1",
        r"Entero": "int",
        r"Real": "float"
    }

    REPR_LIMIT: int = 15

    def __init__(self, code: str) -> None:
        """Initialize the expression.

        Args:
            code (str): body of the expression.
        """
        self.body = code.strip()

    @property
    def body(self) -> str:
        """Get the body attribute value.

        Returns:
            str: the body attribute value.
        """
        return self._body

    @body.setter
    def body(self, value: Any) -> None:
        """Set the body attribute value.

        Args:
            value (Any): the value of the body attribute.
        """
        self._body = str(value)
        self._translate()

    def _translate(self):
        """Translate the expression into a valid Python statement."""
        self._body = self._translate_identifiers(
            self._translate_operators(
                self._body
            )
        )

    def _translate_operators(self, code: str) -> str:
        """Translate operators in the expression.

        Args:
            code (str): body of the expression.

        Returns:
            str: body of the expression with translated operators.
        """
        for expression, replacement in self.OPERATORS.items():
            code = re.sub(
                expression,
                replacement,
                code,
                flags=RegexConfig.FLAGS
            )

        return code

    def _translate_identifiers(self, code: str) -> str:
        """Translate identifiers in the expression.

        Args:
            code (str): body of the expression.

        Returns:
            str: body of the expression with translated identifiers.
        """
        for expression, replacement in self.IDENTIFIERS.items():
            code = re.sub(
                expression,
                replacement,
                code,
                flags=RegexConfig.FLAGS
            )

        return code

    def __str__(self) -> str:
        """Return the expanded representation of the expression.

        Returns:
            str: expanded representation of the expression.
        """
        return self.body

    def __repr__(self) -> str:
        """Return the collapsed representation of the expression.

        Returns:
            str: collapsed representation of the expression.
        """
        if len(self.body) >= self.REPR_LIMIT:
            return f"Expression(\"{self.body[:self.REPR_LIMIT]}...\")"

        return f"Expression(\"{self.body}\")"


class Block:
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

    HEADER: str | None = None  # type: ignore
    FOOTER: str | None = None  # type: ignore
    EXCLUDE_LINES: tuple[str] = tuple()  # type: ignore

    def __init__(self, lines: Any[str | Block], start: int, end: int) -> None:
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
        self._body = self.lines[1:-1]
        self._footer = self.lines[-1]

        self.parent: Block | None = None
        self.children: list[Block] = list()

        self.globals: list[str] = list()
        self.calls: list[Expression] = list()

    @staticmethod
    def indent(text: Any, indentation_level: int) -> str:
        """Indent text.

        Args:
            text (str): the text to indent.
            indentation_level (int): the indentation level.

        Returns:
            str: the indented text.
        """
        spacing = EditorConfig.SPACES_PER_TAB * EditorConfig.INDENTATION_CHAR
        return f"{spacing * indentation_level}{text}"

    def is_excluded(self, line: str) -> bool:
        """Determine whether a line should be excluded from the translation.

        Args:
            line (str): the line to be analyzed.

        Returns:
            bool: True if the line should be excluded, False otherwise.
        """
        for expression in self.EXCLUDE_LINES:
            if re.match(expression, line, flags=RegexConfig.FLAGS):
                return True

        return False

    def translate(self) -> None:
        """Translate block to Python code.

        The block is only translated when all three translations (header,
        footer and body) have a successful output (not None).
        """
        outputs = (
            self._translate_header(),
            self._translate_footer(),
            self._translate_body()
        )

        if all(output is not None for output in outputs):
            self._header = outputs[0]
            self._footer = outputs[1]
            self._body = outputs[2]

    def _translate_header(self) -> str | None:
        """Translate block header to Python code.

        This method acts as placeholder for the header translation. It is
        called by the `translate` method and has got a specific
        implementation in each child descendant of the `Block` class.

        Returns:
            str | None: the translated header or None, if the process was not
                successful.
        """
        pass

    def _translate_footer(self) -> str | None:
        """Translate block footer to Python code.

        This method acts as placeholder for the footer translation. It is
        called by the `translate` method after `_translate_header` and
        has got a specific implementation in each child descendant of the
        `Block` class.

        Returns:
            str | None: the translated footer or None, if the process was not
                successful.
        """
        pass

    def _translate_body(self) -> list[Expression | Block] | None:
        """Translate block body to Python code.

        This method translates the body of the block, ignoring lines excluded
        by regular expressions defined in `Block.EXCLUDED_LINES`. It is called
        by the `translate` method after `_translate_header` and
        `_translate_footer`. It might have a specific implementation in each
        child descendant of the `Block` class.

        Returns:
            list[Expression | Block] | None: the translated body as list of
                Expressions and Blocks or None, if the process was not
                successful.
        """
        lines: list[Expression | Block] = []

        for line in self.lines[1:-1]:
            if not isinstance(line, Block) and not self.is_excluded(line):
                lines.append(Expression(line))
            else:
                lines.append(line)

        return lines

    def collapse(self) -> None:
        """Collapse blocks that contain children blocks.

        This method is used to replace the children blocks' content in the body
        of the parent with a reference to the child. This way, blocks can be
        easily manipulated without line indices limitations.

        Note:
            This method should only be called on the root blocks in order to
            prevent redundant calls.
        """
        reduction = 0
        for child in sorted(self.children):
            start_i = child.start - self.start - reduction
            end_i = child.end - self.start + 1 - reduction

            self.lines[start_i:end_i] = [child]
            reduction += end_i - start_i - 1

        for child in sorted(self.children):
            child.collapse()

    def render(self, indentation_level: int = 0) -> list[str]:
        """Render the block as indented, expanded code.

        This method is responsible for expanding nested code blocks and
        indenting each line so that the output conforms with Python syntax
        rules. It might have a specific implementation in each child descendant
        of the `Block` class.

        Args:
            indentation_level (int): the indentation level of each line.

        Returns:
            list[str]: the indented, expanded lines of code.
        """
        lines: list[str] = [self.indent(self._header, indentation_level)]

        for line in self._body:  # type: ignore
            if isinstance(line, Block):
                sub_render = line.render(indentation_level + 1)
                lines.extend(sub_render)
            else:
                lines.append(self.indent(line, indentation_level + 1))

        lines.append(self.indent(self._footer, indentation_level))
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

    HEADER = r"^DESDE.*HACER$"
    FOOTER = r"^FIN_DESDE$"
    BREAKPOINTS: dict[str, str] = {}

    def _translate_header(self) -> str | None:
        """Translate block header to Python code.

        Returns:
            str | None: the translated header or None, if the process was not
                successful.
        """
        step = re.match(
            r"^DESDE\s+(.+?)\s+HASTA\s+(.+)\s+PASO\s+(.+)\s+HACER$",
            self._header,
            flags=RegexConfig.FLAGS
        )

        no_step = re.match(
            r"^DESDE\s+(.+?)\s+HASTA\s+([^PASO]+?)\s+HACER$",
            self._header,
            flags=RegexConfig.FLAGS
        )

        if step is None and no_step is None:
            return None

        head = (step if step is not None else no_step).groups()

        if "<-" in head[0]:
            iterator = Expression(head[0].split('<-')[0].strip())
            start = Expression(head[0].split('<-')[1].strip())
            end = Expression(head[1])
        else:
            iterator = Expression("_")
            start = Expression(head[0])
            end = Expression(head[1])

        if step is not None:
            step = Expression(head[2])
        else:
            step = Expression('1')

        return f"for {iterator} in range({start}, {end} + 1, {step}):"

    def _translate_footer(self) -> str | None:
        """Translate block footer to Python code.

        Returns:
            str | None: the translated footer or None, if the process was not
                successful.
        """
        return ''


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

    HEADER = r"^MIENTRAS.*HACER$"
    FOOTER = r"^FIN_MIENTRAS$"

    def _translate_header(self) -> str | None:
        """Translate block header to Python code.

        Returns:
            str | None: the translated header or None, if the process was not
                successful.
        """
        match = re.match(
            r"^MIENTRAS\s+(.+?)\s+HACER$",
            self._header,
            flags=RegexConfig.FLAGS
        )

        if match is None:
            return None

        condition = Expression(match.groups()[0])

        return f"while {condition}:"

    def _translate_footer(self) -> str | None:
        """Translate block footer to Python code.

        Returns:
            str | None: the translated footer or None, if the process was not
                successful.
        """
        return ''


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

    HEADER = r"^HACER$"
    FOOTER = r"^MIENTRAS.*[^HACER]$"

    def _translate_header(self) -> str | None:
        """Translate block header to Python code.

        Returns:
            str | None: the translated header or None, if the process was not
                successful.
        """
        return ''

    def _translate_footer(self) -> str | None:
        """Translate block footer to Python code.

        Returns:
            str | None: the translated footer or None, if the process was not
                successful.
        """
        header = re.match(
            r"^MIENTRAS\s+(.+?)$",
            self._footer,
            flags=RegexConfig.FLAGS
        )

        if header is None:
            return None

        self._temp = Expression(header.groups()[0])
        return ''

    def render(self, indentation_level: int = 0) -> list[str]:
        """Render the block as indented, expanded code.

        This method is responsible for expanding nested code blocks and
        indenting each line so that the output conforms with Python syntax
        rules.

        Args:
            indentation_level (int): the indentation level of each line.

        Returns:
            list[str]: the indented, expanded lines of code.
        """
        lines: list[str] = []
        for line in self._body:
            if isinstance(line, Block):
                sub_render = line.render(indentation_level)
                lines.extend(sub_render)
            else:
                lines.append(self.indent(line, indentation_level))

        lines.append(self.indent(f"while {self._temp}:", indentation_level))

        for line in self._body:
            if isinstance(line, Block):
                sub_render = line.render(indentation_level + 1)
                lines.extend(sub_render)
            else:
                lines.append(self.indent(line, indentation_level + 1))

        return lines


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

    HEADER = r"^SI[^_].*ENTONCES$"
    FOOTER = r"^FIN_SI$"

    def _translate_header(self) -> str | None:
        """Translate block header to Python code.

        Returns:
            str | None: the translated header or None, if the process was not
                successful.
        """
        header = re.match(
            r"^SI\s+(.+?)\s+ENTONCES$",
            self._header,
            flags=RegexConfig.FLAGS
        )

        if header is None:
            return None

        condition = Expression(header.groups()[0])
        return f"if {condition}:"

    def _translate_footer(self) -> str | None:
        """Translate block footer to Python code.

        Returns:
            str | None: the translated footer or None, if the process was not
                successful.
        """
        return ''

    def _translate_body(self) -> list[Expression | Block] | None:
        """Translate block body to Python code.

        Returns:
            list[Expression | Block] | None: the translated body as list of
                Expressions and Blocks or None, if the process was not
                successful.
        """
        lines: list[Expression | Block] = []

        for line in self.lines[1:-1]:
            if not isinstance(line, Block) and not self.is_excluded(line):
                if re.match(r"^SI_NO.*$", line, flags=RegexConfig.FLAGS):
                    lines.append(Expression("else:"))
                else:
                    lines.append(Expression(line))
            else:
                lines.append(line)

        return lines

    def render(self, indentation_level: int = 0) -> list[str]:
        """Render the block as indented, expanded code.

        This method is responsible for expanding nested code blocks and
        indenting each line so that the output conforms with Python syntax
        rules.

        Args:
            indentation_level (int): the indentation level of each line.

        Returns:
            list[str]: the indented, expanded lines of code.
        """
        lines: list[str] = [self.indent(self._header, indentation_level)]

        for line in self._body:  # type: ignore
            if isinstance(line, Block):
                sub_render = line.render(indentation_level + 1)
                lines.extend(sub_render)
            else:
                if line.body == "else:":
                    lines.append(self.indent(line, indentation_level))
                else:
                    lines.append(self.indent(line, indentation_level + 1))

        lines.append(self.indent(self._footer, indentation_level))
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

    HEADER = r"^CASO.*SEA$"
    FOOTER = r"^FIN_CASO$"
    EXCLUDE_LINES: tuple[str] = (r"^SI_NO$",)

    def _translate_header(self) -> str | None:
        """Translate block header to Python code.

        Returns:
            str | None: the translated header or None, if the process was not
                successful.
        """
        header = re.match(
            r"^CASO\s+(.+?)\s+SEA$",
            self._header,
            flags=RegexConfig.FLAGS
        )

        if header is None:
            return None

        case = Expression(header.groups()[0])
        return f"match {case}:"

    def _translate_footer(self) -> str | None:
        """Translate block footer to Python code.

        Returns:
            str | None: the translated footer or None, if the process was not
                successful.
        """
        return ''

    def _translate_body(self) -> list[Expression | Block] | None:
        """Translate block body to Python code.

        Returns:
            list[Expression | Block] | None: the translated body as list of
                Expressions and Blocks or None, if the process was not
                successful.
        """
        lines = []
        for line in self._body:
            if not isinstance(line, Block) and "SI_NO" not in line:
                if ':' not in line and line != '':
                    lines.append(Expression(f"case _: {line}"))
                else:
                    value, expression = [
                        item.strip() for item in line.split(':')
                    ]
                    lines.append(Expression(f"case {value}: {expression}"))

        return lines  # type: ignore


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

    HEADER = r"^.+FUNCION.+"
    FOOTER = r"^FIN_FUNCION$"

    @staticmethod
    def split_args(args: str) -> list[str]:
        """Split function arguments.

        Args:
            args (str): function arguments.

        Returns:
            list[str]: list of arguments.
        """
        return [arg.strip() for arg in args.split(',')]

    def translate_args(self, *args: str) -> tuple[list[Expression], list[str]]:
        """Translate function arguments.

        Args:
            arg (str): function arguments.

        Returns:
            str: translated arguments.
        """
        identifiers, references = [], []
        args = tuple([arg for arg in args if arg])

        for arg in args:
            components = re.match(
                r"^(.*?)\s+(.*?):\s+(.*?)$",
                arg,
                flags=RegexConfig.FLAGS
            )

            if components is not None:
                components = components.groups()

                structural_type = components[0]
                data_type = components[1]
                identifier = components[2]

                if structural_type == "E/S":
                    references.append(identifier)
                    identifiers.append(Expression(
                        f"{identifier}_: {data_type}"
                    ))
                else:
                    identifiers.append(Expression(
                        f"{identifier}: {data_type}"
                    ))

        self.globals.extend(references)
        return identifiers, references

    def filter_lines(self):
        """Filter redundant lines of code from the body."""
        start = None
        for i, line in enumerate(self.lines[1:-1]):
            if (
                not isinstance(line, Block)
                and start is None
                and re.match(r"^INICIO$", line, flags=RegexConfig.FLAGS)
            ):
                start = i + 1

        if start is None:
            return None

        self._header = self.lines[0]
        self.lines = [self._header] + self.lines[start + 1:]

    def _translate_header(self) -> str | None:
        """Translate block header to Python code.

        Returns:
            str | None: the translated header or None, if the process was not
                successful.
        """
        self.filter_lines()
        components = re.match(
            r"^(.*?)\s+FUNCION\s+(.*?)\s*\((.*)\)$",
            self._header,
            flags=RegexConfig.FLAGS
        )

        if components is not None:
            components = components.groups()

            return_type = Expression(components[0])
            identifier = components[1]
            arguments, references = self.translate_args(
                *self.split_args(components[2])
            )

            arguments_str = ", ".join(
                str(identifier) for identifier in arguments
            )

            if references:
                references_str = EditorConfig.SPACES_PER_TAB \
                    * EditorConfig.INDENTATION_CHAR
                references_str += f"global {', '.join(references)}"

                return f"def {identifier}({arguments_str}) -> {return_type}:" \
                    + f"\n{references_str}"

            return f"def {identifier}({arguments_str}) -> {return_type}:"

        return None

    def _translate_footer(self) -> str | None:
        """Translate block footer to Python code.

        Returns:
            str | None: the translated footer or None, if the process was not
                successful.
        """
        return ''

    def _translate_body(self) -> list[Expression | Block] | None:
        """Translate block body to Python code.

        Returns:
            list[Expression | Block] | None: the translated body as list of
                Expressions and Blocks or None, if the process was not
                successful.
        """
        lines: list[Expression | Block] = []

        for line in self.lines[1:-1]:
            if not isinstance(line, Block):
                lines.append(Expression(line))
            else:
                lines.append(line)

        return lines


class Procedure(Function):
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

    HEADER = r"^PROCEDIMIENTO.*$"
    FOOTER = r"^FIN_PROCEDIMIENTO$"

    def _translate_header(self) -> str | None:
        """Translate block header to Python code.

        Returns:
            str | None: the translated header or None, if the process was not
                successful.
        """
        self.filter_lines()
        components = re.match(
            r"^PROCEDIMIENTO\s+(.*?)\s*\((.*)\)$",
            self._header,
            flags=RegexConfig.FLAGS
        )

        if components is not None:
            components = components.groups()

            identifier = components[0]
            arguments, references = self.translate_args(
                *self.split_args(components[1])
            )

            arguments_str = ", ".join(
                str(identifier) for identifier in arguments
            )

            if references:
                references_str = EditorConfig.SPACES_PER_TAB \
                    * EditorConfig.INDENTATION_CHAR
                references_str += f"global {', '.join(references)}"

                return f"def {identifier}({arguments_str}):" \
                    + f"\n{references_str}"

            return f"def {identifier}({arguments_str}):"

        return None


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

    HEADER = r"^ALGORITMO.*?$"
    FOOTER = r"^FIN$"

    def _translate_header(self) -> str | None:
        """Translate block header to Python code.

        Returns:
            str | None: the translated header or None, if the process was not
                successful.
        """
        self.filter_lines()
        return "def main():"

    def _translate_footer(self) -> str | None:
        """Translate block footer to Python code.

        Returns:
            str | None: the translated footer or None, if the process was not
                successful.
        """
        self.calls.append(Expression("main()"))
        return ''


TYPES: Any = (
    ForLoop, WhileLoop, DoWhileLoop, IfStatement, MatchStatement,
    Function, Procedure, Main
)
