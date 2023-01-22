from ..core.block import Expression
from itertools import combinations_with_replacement as comb


class TestExpression:

    SYMBOLS = {
        "add": "+",
        "as": "<-",
        "div": "/",
        "eq": "=",
        "ge": ">=",
        "gt": ">",
        "le": "<=",
        "lt": "<",
        "mod": "mod",
        "mul": "*",
        "ne": "<>",
        "sub": "-"
    }

    OPERATORS = {
        "-": "-",
        "*": "*",
        "/": "/",
        "+": "+",
        "<-": "=",
        "<": "<",
        "<=": "<=",
        "<>": "!=",
        "=": "==",
        ">": ">",
        ">=": ">=",
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

    @classmethod
    def expression_test(cls):
        operator = cls.__name__.replace("Test", "").lower()
        for term_a, term_b in cls.TERMS:
            for spacing_a, spacing_b in cls.SPACING:
                cls.check_operator(
                    cls.SYMBOLS[operator],
                    cls.OPERATORS[cls.SYMBOLS[operator]],
                    term_a,
                    term_b,
                    spacing_a,
                    spacing_b
                )

    @classmethod
    def check_operator(cls, operator, replacement, term_a,
                       term_b, spacing_a, spacing_b):
        text = f"{term_a}{spacing_a}{operator}{spacing_b}{term_b}"
        expected = f"{term_a} {replacement} {term_b}"
        expression = Expression(text)
        assert expression.body == expected


class TestAdd(TestExpression):

    def test(self):
        self.expression_test()


class TestAs(TestExpression):

    def test(self):
        self.expression_test()


class TestDiv(TestExpression):

    def test(self):
        self.expression_test()


class TestEq(TestExpression):

    def test(self):
        self.expression_test()


class TestNe(TestExpression):

    def test(self):
        self.expression_test()


class TestLt(TestExpression):

    def test(self):
        self.expression_test()


class TestLe(TestExpression):

    def test(self):
        self.expression_test()


class TestGt(TestExpression):

    def test(self):
        self.expression_test()


class TestGe(TestExpression):

    def test(self):
        self.expression_test()


class TestMul(TestExpression):

    def test(self):
        self.expression_test()


class TestSub(TestExpression):

    def test(self):
        self.expression_test()


class TestMod(TestExpression):

    def test(self):
        self.expression_test()
