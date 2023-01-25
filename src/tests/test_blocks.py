import os

import regex as re

from ..core.code import Code
from ..core.scanner import Scanner


def strip(string: str) -> str:
    lines = string.splitlines()
    return "\n".join([
        line.rstrip() for line in lines
        if not re.match(r"^\s*$", line, flags=re.MULTILINE | re.IGNORECASE)
    ])


CLASS_NAMES = {
    "TestIfStatement": "if_statement",
    "TestMatchStatement": "match_statement",
    "TestForLoop": "for_loop",
    "TestWhileLoop": "while_loop",
    "TestDoWhileLoop": "do_while_loop",
    "TestFunction": "function",
    "TestMainFunction": "main_function",
    "TestProcedure": "procedure"
}


class BaseTest:

    @classmethod
    def setup_tests(cls):
        name = CLASS_NAMES[cls.__name__]

        cls.ROOTS = {
            "samples": f"src/tests/samples/{name}",
            "validations": f"src/tests/validations/{name}"
        }

        cls.SAMPLES = os.listdir(cls.ROOTS["samples"])

    @classmethod
    def block_test(cls):
        cls.setup_tests()

        for sample_name in cls.SAMPLES:

            sample_file = f"{cls.ROOTS['samples']}/{sample_name}"
            validation_file = (
                f"{cls.ROOTS['validations']}/"
                + f"{sample_name.replace('.txt', '.py')}"
            )

            with open(sample_file, mode='r', encoding="utf-8") as f:
                sample = f.read()

            with open(validation_file, mode='r', encoding="utf-8") as f:
                validation = f.read()

            scanner = Scanner(sample)
            scanner.scan()
            code = Code(scanner)

            assert strip(code.render()) == strip(validation)


class TestIfStatement(BaseTest):

    def test(self):
        self.block_test()


class TestMatchStatement(BaseTest):

    def test(self):
        self.block_test()


class TestForLoop(BaseTest):

    def test(self):
        self.block_test()


class TestWhileLoop(BaseTest):

    def test(self):
        self.block_test()


class TestDoWhileLoop(BaseTest):

    def test(self):
        self.block_test()


class TestFunction(BaseTest):

    def test(self):
        self.block_test()


class TestMainFunction(BaseTest):

    def test(self):
        self.block_test()


class TestProcedure(BaseTest):

    def test(self):
        self.block_test()
