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

    def test_concatenation(self) -> None:
        a_parser = parser.CharParser('a')
        b_parser = parser.CharParser('b')

        ab_combo = combinator.Concatenation(a_parser, b_parser)
        print(ab_combo)
        ab_result_1 = ab_combo.parse('ab')
        ab_result_2 = ab_combo.parse('aa')

        for n, r in enumerate([ab_result_1, ab_result_2]):
            print(n, r)


if __name__ == '__main__':
    unittest.main()
