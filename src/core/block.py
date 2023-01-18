from __future__ import annotations


class InterpreterConfig:

    SPACES_PER_TAB: int = 4
    INDENTATION_CHAR: str = ' '


class Block(InterpreterConfig):

    def __init__(self, lines: list[str | Block], start: int, end: int) -> None:
        self.lines = lines
        self.start = start
        self.end = end
        self.parent: Block | None = None
        self.children: list[Block] = list()

    def fold(self) -> None:
        for child in sorted(self.children):
            offset = len(child.lines)
            for i in range(len(self.lines) - offset):
                if self.lines[i:i + offset] == child.lines:
                    self.lines[i:i + offset] = [child]
                    break

        for child in sorted(self.children):
            child.fold()

    def render(self, indentation_level: int = 0,
               no_recursion: bool = False) -> list[str | Block]:

        spacing = self.SPACES_PER_TAB * self.INDENTATION_CHAR
        outer_ind = indentation_level * spacing
        inner_ind = (indentation_level + 1) * spacing

        lines: list[str | Block] = [f"{outer_ind}{self.lines[0]}"]
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
        return self.parent is None

    def tree(self, indentation_level: int = 0) -> str:
        output = f"{indentation_level * '  '}{self!r}\n"
        for child in sorted(self.children):
            output += (
                (indentation_level + 1) * '  '
                + child.tree(indentation_level + 1)
            )

        return output

    def __repr__(self) -> str:
        return (f"Block({self.start}, {self.end})")

    def __str__(self) -> str:
        return self.__repr__()

    def __contains__(self, item) -> bool:
        return self.start < item.start and item.end < self.end

    def __len__(self) -> int:
        return len(self.lines)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Block):
            return False

        return self.start == other.start and self.end == other.end

    def __ne__(self, other) -> bool:
        if not isinstance(other, Block):
            return False

        return not self.__eq__(other)

    def __lt__(self, other) -> bool:
        if not isinstance(other, Block):
            return False

        return self.start < other.start

    def __gt__(self, other) -> bool:
        if not isinstance(other, Block):
            return False

        return self.start > other.start

    def __le__(self, other) -> bool:
        if not isinstance(other, Block):
            return False

        return self.start <= other.start

    def __ge__(self, other) -> bool:
        if not isinstance(other, Block):
            return False

        return self.start >= other.start

    def __hash__(self) -> int:
        return hash((self.start, self.end))
