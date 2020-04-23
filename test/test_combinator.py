"""
TEST_COMBINATOR
Tests of combinator objects

Stefan Wong 2020
"""

import unittest
# unit(s) under test
from parsercom import combinator
from parsercom import parser


class TestCombinator(unittest.TestCase):
    def setUp(self) -> None:
        self.inp_string_1 = "boondoggle"

    def test_alternation(self) -> None:
        boo_parser = parser.StringParser('boo')
        boondoggle_parser = parser.StringParser('boondoggle')

        alt_combo = combinator.Alternation(
            boo_parser,
            boondoggle_parser
        )

        alt_result = alt_combo.parse(self.inp_string_1)

        print(alt_combo)
        print(alt_result)


class TestConcatenation(unittest.TestCase):
    def setUp(self) -> None:
        self.inp_strings = ('ab', 'aa', 'aaa', 'aba')

    def test_concatenation(self) -> None:
        a_parser = parser.CharParser('a')
        b_parser = parser.CharParser('b')
        # expected results
        ab_combo = combinator.Concatenation(a_parser, b_parser)

        results = []
        for inp in self.inp_strings:
            results.append(ab_combo.parse(inp))

        for n, r in enumerate(results):
            print(n, r)


class TestKleeneStar(unittest.TestCase):
    def setUp(self) -> None:
        self.inp_strings = ('a', 'aa', 'aaa', 'aaaa', 'aaabcdefg')

    def test_kleene_star(self) -> None:
        p = parser.CharParser('a')
        ks = combinator.KleeneStar(p)

        results = []
        for inp in self.inp_strings:
            results.append(ks.parse(inp))

        for n, r in enumerate(results):
            print(n, r)


if __name__ == '__main__':
    unittest.main()
