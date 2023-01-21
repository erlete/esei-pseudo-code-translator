import os

import regex as re

from ..core.scanner import Scanner


def strip(string: str) -> str:
    lines = string.splitlines()
    return "\n".join([
        line.rstrip() for line in lines
        if not re.match(r"^\s*$", line, re.MULTILINE)
    ])


class TestIfStatement:

    SAMPLES_ROOT = "src/tests/samples/if_statement"
    SAMPLES = os.listdir(SAMPLES_ROOT)

    CHECKS_ROOT = "src/tests/validations/if_statement"
    CHECKS = os.listdir(CHECKS_ROOT)

    TESTS = {}
    for sample in SAMPLES:
        check = sample.replace(".txt", ".py")

        with open(f"{SAMPLES_ROOT}/{sample}", mode='r', encoding="utf-8") as f:
            sample_code = f.read()

        with open(f"{CHECKS_ROOT}/{check}", mode='r', encoding="utf-8") as f:
            check_code = f.read()

        TESTS[sample] = (sample_code, check_code)

    def test(self):
        for (sample_code, check_code) in self.TESTS.values():
            scanner = Scanner(sample_code)
            scanner.scan()
            print(scanner.render())
            expected = strip(check_code)
            actual = strip(scanner.render())

            assert expected == actual
