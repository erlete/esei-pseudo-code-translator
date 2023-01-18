class InterpreterConfig:

    SPACES_PER_TAB = 4
    INDENTATION_CHAR = ' '


class Block(InterpreterConfig):

    def __init__(self, lines, start, end):
        self.lines = lines
        self.start = start
        self.end = end
        self.parent = None
        self.children = list()

    def compile(self):
        for child in sorted(self.children):
            offset = len(child.lines)
            for i in range(len(self.lines) - offset):
                if self.lines[i:i + offset] == child.lines:
                    self.lines[i:i + offset] = [child]
                    break

        for child in sorted(self.children):
            child.compile()

    def render(self, indentation_level=0, no_recursion=False):
        spacing = self.SPACES_PER_TAB * self.INDENTATION_CHAR
        outer_ind = indentation_level * spacing
        inner_ind = (indentation_level + 1) * spacing

        lines = [f"{outer_ind}{self.lines[0]}"]
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

    def is_root(self):
        return self.parent is None

    def tree(self, indentation_level=0):
        output = f"{indentation_level * '  '}{self!r}\n"
        for child in sorted(self.children):
            output += f"{(indentation_level + 1) * '  '}{child.tree(indentation_level + 1)}"

        return output

    def __repr__(self):
        return (
            f"Block({self.start}, {self.end})"
            #+ (f" -/-> {self.parent!r}" if self.parent else '')
        )

    def __str__(self):
        return self.__repr__()

    def __contains__(self, item):
        return self.start < item.start and item.end < self.end

    def __len__(self):
        return len(self.lines)

    def __eq__(self, other):
        if not isinstance(other, Block):
            return False

        return self.start == other.start and self.end == other.end

    def __ne__(self, other):
        if not isinstance(other, Block):
            return False

        return not self == other

    def __lt__(self, other):
        if not isinstance(other, Block):
            return False

        return self.start < other.start

    def __gt__(self, other):
        if not isinstance(other, Block):
            return False

        return self.start > other.start

    def __le__(self, other):
        if not isinstance(other, Block):
            return False

        return self.start <= other.start

    def __ge__(self, other):
        if not isinstance(other, Block):
            return False

        return self.start >= other.start

    def __hash__(self):
        return hash((self.start, self.end))
