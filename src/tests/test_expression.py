from ..core.block import Expression
from itertools import combinations_with_replacement as comb

class TestExpression:

    OPERATORS = {
        "=": "==",
        "<-": "=",
        "<>": "!=",
        "<": "<",
        ">": ">",
        "<=": "<=",
        ">=": ">=",
        "+": "+",
        "-": "-",
        "*": "*",
        "/": "/",
        "mod": "%"
    }

    TERMS = (
        ('1', '1'),
        ('a', 'a'),
        ('a1', 'a1'),
        ('a_1', 'a_1'),
        ('A', 'A'),
        ('A1', 'A1'),
        ('A_1', 'A_1'),
        ('a1b2c3', 'a1b2c3'),
        ('a_1_b_2_c_3', 'a_1_b_2_c_3')
    )

    SPACING_OPTIONS = (" ", "", "  ")
    SPACING = list(comb(SPACING_OPTIONS, 2))
    SPACING = list(set(
        SPACING + [(b, a) for a, b in SPACING]
    ))

    PAD = 35

    def test(self):
        for operator, replacement in self.OPERATORS.items():
            for term_a, term_b in self.TERMS:
                for spacing_a, spacing_b in self.SPACING:
                    self._check_operator(
                        operator, replacement, term_a, term_b, spacing_a, spacing_b)

    def _check_operator(self, operator, replacement, term_a, term_b, spacing_a, spacing_b):
        text = f"{term_a}{spacing_a}{operator}{spacing_b}{term_b}"
        expected = f"{term_a} {replacement} {term_b}"
        expression = Expression(text)
        assert expression.body == expected
